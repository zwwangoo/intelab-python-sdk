import os
import time
import codecs
import platform
import fcntl
from logging.handlers import TimedRotatingFileHandler


class Lock(object):

    def __init__(self, filename):
        self.filename = filename
        self.path = filename.rsplit('/', 1)[0]
        if not os.path.exists(self.path):
            os.makedirs(self.path)
        self.handle = open(self.filename, 'w')

    def acquire(self):
        fcntl.lockf(self.handle, fcntl.LOCK_EX)

    def release(self):
        fcntl.lockf(self.handle, fcntl.LOCK_UN)

    def __del__(self):
        try:
            self.handle.close()
        except Exception:
            pass


class MultiProcessSafeHandler(TimedRotatingFileHandler):
    def __init__(self, filename, when='h', interval=1,
                 backup_count=0, encoding=None, utc=False):
        TimedRotatingFileHandler.__init__(
            self, filename, when, interval, backup_count, encoding, True, utc)
        self.current_file_name = self.get_new_file_name()
        self.lock_file = Lock(self.baseFilename + '.lock')

    def shouldRollover(self, record):
        if self.current_file_name != self.get_new_file_name():
            return True
        return False

    def doRollover(self):
        if self.stream:
            self.stream.close()
            self.stream = None
        self.current_file_name = self.get_new_file_name()
        if self.backupCount > 0:
            for s in self.getFilesToDelete():
                os.remove(s)

    def get_new_file_name(self):
        return self.baseFilename + "." + time.strftime(self.suffix,
                                                       time.localtime())

    def _open(self):
        if self.encoding is None:
            stream = open(self.current_file_name, self.mode)
        else:
            stream = codecs.open(self.current_file_name,
                                 self.mode, self.encoding)
        return stream

    def acquire(self):
        self.lock_file.acquire()

    def release(self):
        self.lock_file.release()
