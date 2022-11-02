from pathlib import Path
import logging.config
from logging import Logger, getLogger
from ._logging_utils import ColoredFormatter, filter_log_record


class FailedToLoadLoggingConfigException(Exception):
    pass


def get_logger(
    file_name: str = None,
    logger_name: str = "miskibin",
    lvl: int = 20,
    format: str = "%(message)s (%(filename)s:%(lineno)d)",
    datefmt: str = "%H:%M:%S",
    disable_existing_loggers: bool = False,
) -> Logger:
    """Get logger with colored logs and filter for ipynb cells.
    Args:
        `file_name`: file that logs will be saved to. If None, logs will not saved to file.
        `lvl`: logging level. Default is 10 (DEBUG).
        `formatter`: logging formatter.
        `datefmt`: date format for logging formatter.
        `disable_existing_loggers`: if True, disable existing loggers.
    """

    if disable_existing_loggers:
        logging.config.dictConfig(
            {
                "version": 1,
                "disable_existing_loggers": True,
            }
        )

    logger = getLogger(logger_name)
    if logger.handlers:
        logger.handlers.clear()
    logger.addFilter(filter_log_record)
    logger.setLevel(lvl)
    logger.addHandler(logging.StreamHandler())
    logger.handlers[0].setFormatter(ColoredFormatter(format, datefmt))
    if file_name:
        if Path(file_name).suffix != ".log":
            file_name += ".log"
        logger.addHandler(logging.FileHandler(file_name))
        file_formatter = logging.Formatter(format, datefmt)
        logger.handlers[1].setFormatter(file_formatter)
    return logger
