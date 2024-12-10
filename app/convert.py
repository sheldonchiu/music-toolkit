
#%%
import os
from glob import glob
import multiprocessing
import argparse

from pydub import AudioSegment
import mutagen
from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

#%%
tags = ['album', 'composer', 'title', 'artist', 'albumartist', 'tracknumber']
wav_tags = {'album': 'TALB', 'composer': 'TCOM', 'title': 'TIT2', 'artist': 'TOPE', 'tracknumber': 'TRCK'}
bitrate_list = ['96k', '128k', '192k', '256k', '320k']

#%%
        
def copy_tag(src, dst, tag_key):
    try:
        dst[tag_key] = src[tag_key]
    except KeyError:
        logger.exception(f"Failed to copy tag {tag_key} for {src}")
        return -1
    return 0

def copy_tags(src, dst):
    for tag in tags:
        copy_tag(src, dst, tag)
    dst.save()
    
def copy_tags_wav(src, dst):
    for key, value in wav_tags.items():
        try:
            dst[key] = str(src.tags.get(value))
        except:
            logger.exception(f"Failed to copy tag {key} for {src}")
            print("wav copy tag failed")
    dst.save()
       
def copy_pic(src, dst):
    try:
        for pic in src.pictures:
            dst.tags.add(APIC(mime=pic.mime,type=pic.type,desc=pic.desc,data=pic.data))
    except:
        logger.exception(f"Failed to copy picture for {src}")
    dst.save()
    
def copy_pic_wav(src, dst):
    try:
        for pic in src.tags.getall('APIC'):
            dst.tags.add(pic)
    except:
        logger.exception(f"Failed to copy picture for {src}")
    dst.save()
    
    
def convert(srcPath, dstPath, srcFile, bitrate='320k', min=False, flatten=False):
    try:
        fileName, fileFormat = os.path.splitext(os.path.basename(srcFile))
        fileFormat = fileFormat.replace('.', '')
        folder = os.path.relpath(srcFile, srcPath)
        pathComponent = os.path.normpath(folder).split(os.sep)

        outpath = dstPath if flatten else os.path.join(dstPath,*pathComponent[:-1]) 
        
        outputFilePath = f"{os.path.join(outpath, fileName)}.mp3"
        if os.path.exists(outputFilePath):
            logger.info(f"[SKIP] {srcFile} already exists")
            return 0
        os.makedirs(outpath, exist_ok = True)
        org = AudioSegment.from_file(srcFile, fileFormat)
        org.export(outputFilePath, format="mp3", bitrate=bitrate)
    except:
        logger.exception(f"Failed to convert {srcFile}")
        return -1
    
    if not min:
        src = mutagen.File(srcFile)
        if 'wav' in srcFile:
            copy_tags_wav(src, EasyID3(outputFilePath))
            copy_pic_wav(src, MP3(outputFilePath, ID3=ID3))
        else:
            copy_tags(src,EasyID3(outputFilePath))
            copy_pic(src, MP3(outputFilePath, ID3=ID3))
    logger.info(f"Finish converting {srcFile}")

def convertAll(hiResPath, mp3Path, bitrate, min, flatten):
    files = glob(hiResPath +'/**', recursive=True)
    pool = multiprocessing.Pool(processes=multiprocessing.cpu_count()/2)
    
    for hiRes in files:
        if os.path.isfile(hiRes) == False:
            continue
        pool.starmap(convert, [(hiResPath, mp3Path, hiRes, bitrate, min, flatten),])
        
    pool.close()
    pool.join()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Convert hiRes to mp3')
    parser.add_argument('--src_dir', type=str, required=False, default='/data/hiRes', help='Path to source directory')
    parser.add_argument('--dst_dir', type=str, required=False, default='/data/mp3', help='Path to destination directory')
    parser.add_argument('--bitrate', type=str, required=False, default='320k', help='mp3 bitrate')
    parser.add_argument('--min', action='store_true', help='minimal mode')
    parser.add_argument('--flatten', action='store_true', help='copy to flat directory structure')
    args = parser.parse_args()
    convertAll(hiResPath=args.src_dir, mp3Path=args.dst_dir, bitrate=args.bitrate, min=args.min, flatten=args.flatten)

