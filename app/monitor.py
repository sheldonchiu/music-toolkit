import logging
from watchdog.observers import Observer
from handler import EventHandler

if __name__ == "__main__":
    hiResPath = '/data/hiRes'
    dstPath = '/data/mp3'
    logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')
    event_handler = EventHandler(hiResPath, dstPath)
    observer = Observer()
    observer.schedule(event_handler, hiResPath, recursive=True)
    observer.start()

    observer.join()