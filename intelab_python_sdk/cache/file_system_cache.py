import os
import pickle


class FileSystemCache(object):
    """ 文件缓存

    :param chche_dir: 缓存文件目录

    Usage::

        >>> from intelab_python_sdk.cache import FileSystemCache
        >>> from datetime import datetime
        >>> cache = FileSystemCache('.cache')
        >>> cache.set('12', datetime.now())
        >>> cache.get('12')
        datetime.datetime(2019, 12, 19, 12, 16, 1, 511077)
        >>> list(cache.keys())
        ['12']
        >>> cache.delete('12')

    """

    def __init__(self, cache_dir):
        self.base_dir = cache_dir
        if not os.path.exists(self.base_dir):
            os.makedirs(self.base_dir)

    def _get_filename(self, key):
        return os.path.join(self.base_dir, key)

    def get(self, key, default=None):
        filename = self._get_filename(key)
        try:
            with open(filename, 'rb') as f:
                value = pickle.load(f)
        except (IOError, OSError, EOFError, pickle.PickleError):
            value = None
        if value is None and default is not None:
            value = default

        return value

    def set(self, key, value):
        filename = self._get_filename(key)
        with open(filename, 'wb') as f:
            pickle.dump(value, f, pickle.HIGHEST_PROTOCOL)

    def delete(self, key):
        filename = self._get_filename(key)
        if os.path.isfile(filename):
            os.remove(filename)

    def keys(self):
        keys = []
        for root, dirs, files in os.walk(self.base_dir, topdown=False):
            for file in files:
                keys.append(os.path.split(file)[-1])

        return iter(keys)
