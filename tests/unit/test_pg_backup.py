"""Unit tests for vitalx.pg_backup (PostgreSQL backup functionality).

What to test:
- format_sql_value handles None, bool, int, float, datetime, date, and str
- format_sql_value escapes single quotes in strings
- perform_daily_pg_backup creates a .sql.gz backup file
- perform_daily_pg_backup includes all four tables in the backup
- perform_daily_pg_backup raises DatabaseError when backup fails
- perform_daily_pg_backup verifies the backup file is not empty/too small
- cleanup_old_pg_backups deletes backups older than retention_days
- cleanup_old_pg_backups keeps recent backups
- BACKUP_DIR constant is "/app/backups"
- EXPORT_QUERIES lists the correct four SQL files

Suggested mocks:
- Monkeypatch BACKUP_DIR to tmp_path
- Mock fetch_result to return sample rows
- Mock load_sql_as_text to return dummy SQL
- Mock gzip.open to avoid writing real compressed files
- Mock os.path.getsize / os.remove for file verification and cleanup
"""

import os
from datetime import datetime, date
from vitalx.pg_backup import (
    format_sql_value,
    perform_daily_pg_backup,
    cleanup_old_pg_backups,
    BACKUP_DIR,
    EXPORT_QUERIES,
)
from vitalx.exceptions import DatabaseError


def test_format_sql_value_none_returns_null():
    """
    format_sql_value(None) should return the string "NULL".
    """
    pass


def test_format_sql_value_bool_returns_true_false():
    """
    format_sql_value(True) should return "TRUE", format_sql_value(False) should return "FALSE".
    """
    pass


def test_format_sql_value_int_returns_string():
    """
    format_sql_value(42) should return "42".
    """
    pass


def test_format_sql_value_float_returns_string():
    """
    format_sql_value(3.14) should return "3.14".
    """
    pass


def test_format_sql_value_datetime_returns_isoformat():
    """
    format_sql_value with a datetime should return a quoted ISO format string.
    """
    pass


def test_format_sql_value_date_returns_isoformat():
    """
    format_sql_value with a date should return a quoted ISO format string.
    """
    pass


def test_format_sql_value_escapes_single_quotes():
    """
    format_sql_value("O'Brien") should return "O''Brien" (single quotes doubled).
    """
    pass


def test_export_queries_has_four_files():
    """
    EXPORT_QUERIES should list exactly 4 SQL files.
    Hint: assert len(EXPORT_QUERIES) == 4.
    """
    pass


def test_perform_daily_pg_backup_creates_backup_file(monkeypatch, tmp_path):
    """
    perform_daily_pg_backup should create a backup file at BACKUP_DIR/<date>.sql.gz.
    Hint: monkeypatch BACKUP_DIR to tmp_path, mock all I/O, then check the file exists.
    """
    pass


def test_perform_daily_pg_backup_includes_all_tables(monkeypatch, tmp_path):
    """
    The backup should contain sections for all four tables (walk, sleep, weather, streak).
    Hint: mock the gzip file write calls and check all table names appear.
    """
    pass


def test_perform_daily_pg_backup_raises_when_backup_too_small(monkeypatch, tmp_path):
    """
    If the backup file is less than 50 bytes, perform_daily_pg_backup
    should raise DatabaseError (backup verification failed).
    Hint: mock os.path.getsize to return a small value.
    """
    pass


def test_cleanup_old_pg_backups_deletes_old_files(tmp_path, monkeypatch):
    """
    cleanup_old_pg_backups should delete .sql.gz files older than retention_days.
    Hint: create old backup files and recent files, call cleanup, verify old ones removed.
    """
    pass


def test_cleanup_old_pg_backups_default_retention_is_seven_days():
    """
    The default retention_days should be 7.
    """
    pass
