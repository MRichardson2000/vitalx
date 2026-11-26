"""Unit tests for vitalx.logger (logging setup).

What to test:
- get_logger returns a logging.Logger instance
- setup_logging configures the root logger with console and file handlers
- setup_logging creates the log directory if it doesn't exist
- setup_logging uses a RotatingFileHandler with backupCount=3
- Log messages are emitted at the correct level
- Calling setup_logging multiple times doesn't duplicate handlers

Suggested mocks:
- Monkeypatch vitalx.logger.LOG_DIR to a temporary path
- Use caplog fixture to capture log output
- Mock logging.handlers.RotatingFileHandler to avoid writing real files
"""

import logging
from vitalx.logger import get_logger, setup_logging


def test_get_logger_returns_logger():
    """
    get_logger(__name__) should return a logging.Logger instance.
    Hint: assert isinstance(result, logging.Logger).
    """
    pass


def test_get_logger_name_matches_input():
    """
    The logger's name attribute should match the name passed to get_logger.
    Hint: logger.name == "test_module" or similar.
    """
    pass


def test_setup_logging_configures_root_logger():
    """
    setup_logging() should configure the root logger with handlers.
    Hint: after calling setup_logging, check logging.getLogger().handlers
    is not empty.
    """
    pass


def test_setup_logging_creates_log_directory(tmp_path, monkeypatch):
    """
    setup_logging should create LOG_DIR if it doesn't exist.
    Hint: monkeypatch vitalx.logger.LOG_DIR to a non-existent path under tmp_path,
    call setup_logging, then assert the directory exists.
    """
    pass


def test_setup_logging_adds_file_and_console_handlers():
    """
    After setup_logging, the root logger should have both a StreamHandler
    (console) and a RotatingFileHandler (file).
    Hint: check the types of handlers on the root logger.
    """
    pass


def test_setup_logging_does_not_duplicate_handlers():
    """
    Calling setup_logging twice should not add duplicate handlers.
    Hint: call setup_logging() twice and check handler count stays the same.
    """
    pass


def test_log_message_emitted_at_info_level(caplog):
    """
    A logger should emit messages at INFO level and they should be capturable.
    Hint: use get_logger, call logger.info(), then check caplog.records.
    """
    pass
