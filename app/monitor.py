import os
import sys
import logging
from watchdog.observers import Observer
from handler import EventHandler

if __name__ == "__main__":

    logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

    hiResPath = os.getenv('HIRES_DIR') #'/data/hiRes'
    dstPath = os.getenv('MP3_DIR') #'/data/mp3'
    if hiResPath is None or dstPath is None:
        logging.error('Missing either HIRES_DIR or MP3_DIR environment variable')
        sys.exit(1)

    event_handler = EventHandler(hiResPath, dstPath)
    observer = Observer()
    observer.schedule(event_handler, hiResPath, recursive=True)
    observer.start()

    observer.join()