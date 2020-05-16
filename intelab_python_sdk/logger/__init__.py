# encoding=utf-8
import datetime
import logging
import os
import re
import socket
import sys
import time
import platform

if platform.system() != 'Windows':
    from .timerotaingfilehandler import MultiProcessSafeHandler
else:
    from logging.handlers import TimedRotatingFileHandler as MultiProcessSafeHandler  # noqa


here = os.path.abspath(os.path.dirname(__file__))

log = logging.getLogger()


def tz_fix():
    # calculate TZ offset for isotime
    tz = re.compile(r'([+-]\d{2})(\d{2})$').match(time.strftime('%z'))
    if time.timezone and tz:
        opsym = '+' if time.timezone > 0 else '-'

        offset_hrs, offset_min = tz.groups()
        _tz_offset = "{0}{1}:{2}".format(opsym, offset_hrs, offset_min)
    else:
        # time.timezone == 0 => we're in UTC
        _tz_offset = "Z"
    return _tz_offset


class LogFormatter(logging.Formatter):
    """
    log formatter to add isotime, hostname
    """

    def __init__(self, service_name, *args, **kwargs):
        self._service_name = service_name
        self._tz_offset = tz_fix()

        # get hostname and save for later
        try:
            # force short-name
            self._hostname = socket.gethostname().split(".")[0]
        except Exception:
            self._hostname = "-"

        super(LogFormatter, self).__init__(*args, **kwargs)

    def format(self, record):
        """
        Add special content to record dict
        """
        record.hostname = self._hostname
        record.isotime = datetime.datetime.fromtimestamp(
            record.created).isoformat() + self._tz_offset
        record.service_name = self._service_name

        return logging.Formatter.format(self, record)


class RFC5424LogFormatter(LogFormatter):
    """
    formatter for rfc5424 messaging
    """

    RFC5424_LOG_FORMAT = (
        "%(isotime)s | %(hostname)s | %(process)-6s | %(service_name)s | "
        "%(levelname)-8s | %(name)s:%(filename)s:%(lineno)d | "
        "%(message)s"
    )

    RFC5424_TIME_FORMAT = None

    def __init__(self, service_name):
        LogFormatter.__init__(
            self, service_name,
            fmt=self.RFC5424_LOG_FORMAT,
            datefmt=self.RFC5424_TIME_FORMAT)


def log_init(name, debug=None, log_path=None, when='MIDNIGHT', **kwargs):
    """初始化配置logging

    :param debug: log message with level DEBUG or higher,
      add stdout handler to print log to screen
    :param log_path: log files path
    :return: log

    Usage::

        >>> from intelab_python_sdk.logger import log_init
        >>> # 初始化配置
        >>> log = log_init('test', debug=True, log_path='./logs')
        >>> log.info('info')
        2019-12-16T17:46:41.930061-+08:00 | wen-work-pc | 25689 | test | INFO    | root:<ipython-input-5-6a92ee17c096>:1 | info
        >>> log.debug('debug')
        2019-12-16T17:47:31.113047-+08:00 | wen-work-pc | 25689 | test | DEBUG   | root:<ipython-input-6-03b5a4252de9>:1 | debug
        >>> log.error('error')
        2019-12-16T17:48:02.338739-+08:00 | wen-work-pc | 25689 | test | ERROR   | root:<ipython-input-7-5bfd94e0c8ba>:1 | error
    """
    rfc5424_formatter = RFC5424LogFormatter(name)
    log.handlers = []

    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setFormatter(rfc5424_formatter)
    log.addHandler(stdout_handler)

    if (debug is None and log_path is None) or debug:
        log.setLevel(logging.DEBUG)
    else:
        log.setLevel(logging.INFO)
        if not debug and log_path is None:
            log.warning('log_path should not be null')

    if log_path:

        log_file = "{}/{}.info.log".format(log_path, name)
        file_log_handler = MultiProcessSafeHandler(
            log_file, when=when, **kwargs)
        file_log_handler.setFormatter(rfc5424_formatter)
        log.addHandler(file_log_handler)

        log_file = "{}/{}.error.log".format(log_path, name)
        file_log_handler_err = MultiProcessSafeHandler(
            log_file, when=when, **kwargs)
        file_log_handler_err.setFormatter(rfc5424_formatter)
        file_log_handler_err.setLevel(logging.ERROR)
        log.addHandler(file_log_handler_err)

    return log
