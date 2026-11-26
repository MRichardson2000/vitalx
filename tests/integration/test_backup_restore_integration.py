"""Integration tests for backup and restore functionality.

These tests verify that the CSV export/import and PG backup systems work
together correctly.

What to test:
- export_tables_to_spreadsheets creates CSVs, then import_spreadsheets_to_database reads them back
- Data integrity: exported then imported data matches the original
- perform_daily_pg_backup creates a valid .sql.gz file
- cleanup_old_csvs and cleanup_old_pg_backups remove old files correctly
- Full backup → restore flow works end-to-end

Suggested approach: Use tmp_path for file operations, mock the database
layer where needed.
"""

import os
import gzip
from datetime import datetime, timedelta
from vitalx.extraction import export_tables_to_spreadsheets, cleanup_old_csvs
from vitalx.csv_backup import import_spreadsheets_to_database
from vitalx.pg_backup import perform_daily_pg_backup, cleanup_old_pg_backups
from vitalx.exceptions import CsvExportError, CsvImportError, DatabaseError


def test_export_then_import_round_trip(monkeypatch, tmp_path):
    """
    Export tables to CSV, then import them back - data should be preserved.
    Hint: monkeypatch EXPORTS_FOLDER to tmp_path, mock fetch_result to
    return known data, call export_tables_to_spreadsheets, then call
    import_spreadsheets_to_database and verify the data matches.
    """
    pass


def test_export_creates_expected_number_of_csvs(monkeypatch, tmp_path):
    """
    export_tables_to_spreadsheets should create exactly 4 CSV files
    (one per table).
    Hint: count the CSV files in EXPORTS_FOLDER after exporting.
    """
    pass


def test_pg_backup_creates_valid_gz_file(monkeypatch, tmp_path):
    """
    perform_daily_pg_backup should create a .sql.gz file that can be
    decompressed and read.
    Hint: monkeypatch BACKUP_DIR to tmp_path, mock all I/O, then try
    to gzip.decompress the created file.
    """
    pass


def test_cleanup_old_csvs_removes_files_older_than_seven_days(tmp_path, monkeypatch):
    """
    CSV files older than 7 days should be deleted by cleanup_old_csvs.
    Hint: create CSV files with mtime 8+ days ago, call cleanup_old_csvs,
    verify they're gone.
    """
    pass


def test_cleanup_old_pg_backups_removes_files_older_than_seven_days(
    tmp_path, monkeypatch
):
    """
    .sql.gz backup files older than 7 days should be deleted.
    Hint: similar to test_cleanup_old_csvs but for pg backups.
    """
    pass


def test_export_raises_on_database_failure(monkeypatch, tmp_path):
    """
    If fetch_result raises during export, CsvExportError should be raised.
    Hint: mock fetch_result to raise an exception.
    """
    pass


def test_import_raises_on_missing_folder(monkeypatch):
    """
    If EXPORTS_FOLDER doesn't exist, import_spreadsheets_to_database
    should raise FileNotFoundError.
    """
    pass
