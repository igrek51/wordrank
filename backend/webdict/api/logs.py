import logging
import sys
from typing import Optional

LOG_FORMAT = '\033[2m[%(asctime)s]\033[0m %(levelname)s %(message)s'
LOG_DATE_FORMAT = '%Y-%m-%d %H:%M:%S'


def configure_logs(verbosity: int = 0, log_level: Optional[str] = None):
    if log_level is None:
        if verbosity > 0:
            level = logging.DEBUG
        else:
            level = logging.INFO
    else:
        level = _get_logging_level(log_level)

    logger = logging.getLogger('webdict')
    handler = logging.StreamHandler(stream=sys.stdout)
    handler.setLevel(level)
    formatter = logging.Formatter(fmt=LOG_FORMAT, datefmt=LOG_DATE_FORMAT)
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    for handler in logger.handlers:
        handler.setFormatter(ColoredFormatter(handler.formatter))

    logger.propagate = False
    logger.setLevel(level)


def get_logger() -> logging.Logger:
    return logging.getLogger('webdict')


def _get_logging_level(str_level: str) -> int:
    return {
        'debug': logging.DEBUG,
        'info': logging.INFO,
        'warn': logging.WARNING,
        'warning': logging.WARNING,
        'error': logging.ERROR,
        'crit': logging.CRITICAL,
        'off': logging.NOTSET,
    }[str_level.lower()]


class ColoredFormatter(logging.Formatter):
    def __init__(self, plain_formatter):
        logging.Formatter.__init__(self)
        self.plain_formatter = plain_formatter

    log_level_templates = {
        'CRITICAL': '\033[1;31m{}\033[0m',
        'ERROR': '\033[1;31m{}\033[0m',
        'WARNING': '\033[0;33m{}\033[0m',
        'INFO': '\033[0;34m{}\033[0m',
        'DEBUG': '\033[0;32m{}\033[0m',
    }

    def format(self, record: logging.LogRecord):
        if record.levelname in self.log_level_templates:
            record.levelname = self.log_level_templates[record.levelname].format(record.levelname)
        return self.plain_formatter.format(record)
