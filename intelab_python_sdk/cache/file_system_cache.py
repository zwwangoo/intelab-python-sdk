import os
import pickle
from datetime import datetime


class FileSystemCache(object):

    def __init__(self, cache_dir):
        self.base_dir = cache_dir
        if not os.path.exists(self.base_dir):
            os.mkdir(self.base_dir)

    def _get_filename(self, key):
        return os.path.join(self.base_dir, key)

    def get(self, key):
        filename = self._get_filename(key)
        try:
            with open(filename, 'rb') as f:
                value = pickle.load(f)
        except (IOError, OSError, pickle.PickleError):
            value = None
        return value

    def set(self, key, value):
        filename = self._get_filename(key)
        with open(filename, 'wb') as f:
            pickle.dump(value, f, pickle.HIGHEST_PROTOCOL)


if __name__ == '__main__':
    cache = FileSystemCache('.cache')
    cache.set('12', datetime.now())
    print(cache.get('12'))
