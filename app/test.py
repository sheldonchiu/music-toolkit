import os
srcFile = '/data/music/hiRes/The First Take/1..flac'
srcPath = '/data/music/hiRes'
dstPath = '/data/music/mp3'

fileName, fileFormat = os.path.splitext(os.path.basename(srcFile))
folder = os.path.relpath(srcFile, srcPath)
pathComponent = os.path.normpath(folder).split(os.sep)

outpath = os.path.join(dstPath,*pathComponent[:-1])
fullPath = f"{os.path.join(outpath, fileName)}.mp3"
print(fullPath)