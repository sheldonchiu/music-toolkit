
#%%
import os
import traceback
from glob import glob
import shutil
import argparse

from pydub import AudioSegment
import mutagen
from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC

#%%
tags = ['album', 'composer', 'title', 'artist', 'albumartist', 'tracknumber']
wav_tags = {'album': 'TALB', 'composer': 'TCOM', 'title': 'TIT2', 'artist': 'TOPE', 'tracknumber': 'TRCK'}

#%%

def copy_mp3(srcPath, dstPath, srcFile):
    # fileName = os.path.basename(srcFile)
    folder = os.path.relpath(srcFile, srcPath)
    pathComponent = os.path.normpath(folder).split(os.sep)
    outpath = os.path.join(dstPath,*pathComponent[:-1])
    #fullPath = os.path.join(outpath, fileName)
    os.makedirs(outpath, exist_ok = True)
    shutil.copy(srcFile, outpath)
        
def copy_tag(src, dst, tag_key):
    try:
        dst[tag_key] = src[tag_key]
    except KeyError:
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
            traceback.print_exc()
            print("wav copy tag failed")
    dst.save()
       
def copy_pic(src, dst):
    try:
        for pic in src.pictures:
            dst.tags.add(APIC(mime=pic.mime,type=pic.type,desc=pic.desc,data=pic.data))
    except:
        traceback.print_exc()
        print("copy picture encounter error")
    dst.save()
    
def copy_pic_wav(src, dst):
    try:
        for pic in src.tags.getall('APIC'):
            dst.tags.add(pic)
    except:
        traceback.print_exc()
        print("copy picture encounter error (wav)")
    dst.save()
    
def _convert(srcPath, dstPath, srcFile):
    try:
        fileName, fileFormat = os.path.splitext(os.path.basename(srcFile))
        fileFormat = fileFormat.replace('.', '')
        folder = os.path.relpath(srcFile, srcPath)
        pathComponent = os.path.normpath(folder).split(os.sep)

        outpath = os.path.join(dstPath,*pathComponent[:-1])
        fullPath = f"{os.path.join(outpath, fileName)}.mp3"
        if os.path.exists(fullPath):
            print(f"[SKIP] {srcFile} already exists")
            return -1
        os.makedirs(outpath, exist_ok = True)
        org = AudioSegment.from_file(srcFile, fileFormat)
        org.export(fullPath, format="mp3", bitrate="320k")
        return fullPath
    except:
        print(f"[FAILED] {srcFile}")
        traceback.print_exc()
        return -1
    
def convert(srcPath, dstPath, srcFile):
    if 'mp3' in srcFile:
        copy_mp3(srcPath, dstPath, srcFile)
        print(f"[SUCCESS] Finish copying {srcFile}")
        return 
    outputFilePath = _convert(srcPath, dstPath, srcFile)
    if outputFilePath == -1:
        return 
    src = mutagen.File(srcFile)
    if 'wav' in srcFile:
        copy_tags_wav(src, EasyID3(outputFilePath))
        copy_pic_wav(src, MP3(outputFilePath, ID3=ID3))
    else:
        copy_tags(src,EasyID3(outputFilePath))
        copy_pic(src, MP3(outputFilePath, ID3=ID3))
    print(f"Finish converting {srcFile}")

def convertAll(hiResPath, mp3Path):
    files = glob(hiResPath +'/**', recursive=True)
    for hiRes in files:
        if os.path.isfile(hiRes) == False:
            continue
        convert(hiResPath, mp3Path, hiRes)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Convert hiRes to mp3')
    parser.add_argument('--src_dir', type=str, required=False, default='/data/hiRes', help='Path to source directory')
    parser.add_argument('--dst_dir', type=str, required=False, default='/data/mp3', help='Path to destination directory')
    args = parser.parse_args()
    convertAll(hiResPath=args.src_dir, mp3Path=args.dst_dir)

