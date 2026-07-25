import logging
from logging.handlers import RotatingFileHandler
from vitalx.utils import LOG_FILE, LOG_DIR


def setup_logging(default_level: int = logging.INFO) -> None:
    # making sure the dir exists
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    # Formatting the logs into a human readable format
    log_format = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(name)s:%(lineno)d - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    # setting up the root logger - retrieves the top level root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(default_level)
    if root_logger.hasHandlers():
        # Removes any default handlers attached by web frameworks: "Dash" in this case. - It prevents dupe logs
        root_logger.handlers.clear()
    # Directs log messages to standard output(sys.stderr) - terminal screen so you can see live operations while the app is running locally.
    console_handler = logging.StreamHandler()
    # Applies the format rules and severity filter we set up previously
    console_handler.setFormatter(log_format)
    console_handler.setLevel(default_level)
    # Attaches the console destination to the root logging
    root_logger.addHandler(console_handler)
    # RotatingFileHandler directs log messages to a phsyical file on the storage drive
    # Once the VitalX log file reaches 5mb it automatically rolls over
    # backup count keeps 3 historical backups, when the 4th file is created, the oldest backup is cleared immediately
    file_handler = RotatingFileHandler(
        LOG_FILE, maxBytes=5 * 1024 * 1024, backupCount=3, encoding="utf-8"
    )
    file_handler.setFormatter(log_format)
    file_handler.setLevel(default_level)
    # addHandler attaches the file output destination to the root logger
    root_logger.addHandler(file_handler)


def get_logger(name: str) -> logging.Logger:
    """Helper function to ensure each log file has a valid name that clearly states which module emitted the log event."""
    return logging.getLogger(name)
