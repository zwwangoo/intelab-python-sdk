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
    from logging.handlers import TimedRotatingFileHandler as MultiProcessSafeHandler


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
        "%(isotime)s %(hostname)s %(process)s %(service_name)s\n"
        "%(levelname)s %(name)s:%(filename)s:%(lineno)d\n"
        "Message: %(message)s\n"
    )

    RFC5424_TIME_FORMAT = None

    def __init__(self, service_name):
        LogFormatter.__init__(
            self, service_name,
            fmt=self.RFC5424_LOG_FORMAT,
            datefmt=self.RFC5424_TIME_FORMAT)


def log_init(name, debug=None, log_path=None):
    """
    setup root logger
    debug: log message with level DEBUG or higher,
           add stdout handler to print log to screen
    """
    rfc5424_formatter = RFC5424LogFormatter(name)
    log.handlers = []

    if (debug is None and log_path is None) or debug:
        stdout_handler = logging.StreamHandler(sys.stdout)
        stdout_handler.setFormatter(rfc5424_formatter)
        log.addHandler(stdout_handler)

        log.setLevel(logging.DEBUG)
    else:
        log.setLevel(logging.INFO)
        if not debug and log_path is None:
            log.warning('log_path should not be null')

    if log_path:

        log_file = "{}/{}.info.log".format(log_path, name)
        file_log_handler = MultiProcessSafeHandler(log_file, when="MIDNIGHT")
        file_log_handler.setFormatter(rfc5424_formatter)
        log.addHandler(file_log_handler)

        log_file = "{}/{}.error.log".format(log_path, name)
        file_log_handler_err = MultiProcessSafeHandler(
            log_file, when="MIDNIGHT")
        file_log_handler_err.setFormatter(rfc5424_formatter)
        file_log_handler_err.setLevel(logging.ERROR)
        log.addHandler(file_log_handler_err)

    return log
