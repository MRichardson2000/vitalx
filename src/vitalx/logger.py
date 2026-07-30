import logging
from logging.handlers import RotatingFileHandler
from vitalx.utils import LOG_FILE, LOG_DIR


def setup_logging(default_level: int = logging.INFO) -> None:
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    log_format = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(name)s:%(lineno)d - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    root_logger = logging.getLogger()
    root_logger.setLevel(default_level)
    if root_logger.hasHandlers():
        root_logger.handlers.clear()
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(log_format)
    console_handler.setLevel(default_level)
    root_logger.addHandler(console_handler)
    file_handler = RotatingFileHandler(
        LOG_FILE, maxBytes=5 * 1024 * 1024, backupCount=3, encoding="utf-8"
    )
    file_handler.setFormatter(log_format)
    file_handler.setLevel(default_level)
    root_logger.addHandler(file_handler)


def get_logger(name: str) -> logging.Logger:
    """Helper function to ensure each log file has a valid name that clearly states which module emitted the log event."""
    return logging.getLogger(name)
