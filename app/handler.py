import logging
from watchdog.events import FileSystemEventHandler
from convert import convert

class EventHandler(FileSystemEventHandler):

    def __init__(self, srcPath, dstPath, logger=None):
        super(EventHandler, self).__init__()
        self.logger = logger or logging.root
        self.srcPath = srcPath
        self.dstPath = dstPath

    def on_moved(self, event):
        super(EventHandler, self).on_moved(event)

        if event.is_directory:
            return
        self.logger.info("Moved: from %s to %s", event.src_path,
                         event.dest_path)

    def on_created(self, event):
        super(EventHandler, self).on_created(event)

        if event.is_directory:
            return
        self.logger.info("Created: %s", event.src_path)

    def on_deleted(self, event):
        super(EventHandler, self).on_deleted(event)

        if event.is_directory:
            return
        self.logger.info("Deleted: %s", event.src_path)

    def on_modified(self, event):
        super(EventHandler, self).on_modified(event)

        if event.is_directory or '.part' in event.src_path:
            return
        self.logger.info("Modified: %s", event.src_path)
        self.logger.info("start conversion")
        result = convert(self.srcPath, self.dstPath, event.src_path)
        if result == 0:
            self.logger.info('finish conversion')
        elif result == -1:
            self.logger.info("Error converting file")
