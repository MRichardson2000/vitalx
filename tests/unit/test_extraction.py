"""Unit tests for vitalx.extraction (CSV export functionality).

What to test:
- export_tables_to_spreadsheets exports all four tables to CSV files
- Each CSV file is named correctly (<table>_<date>.csv)
- CSV files contain the expected data (correct columns and rows)
- cleanup_old_csvs deletes files older than retention_days
- cleanup_old_csvs keeps files newer than retention_days
- export_tables_to_spreadsheets calls cleanup_old_csvs after exporting
- export_tables_to_spreadsheets raises CsvExportError when a CSV is empty/missing
- TABLE_SQL_MAPPING maps the correct table names to SQL files

Suggested mocks:
- Mock vitalx.extraction.fetch_result to return sample rows
- Mock vitalx.extraction.load_sql_as_text to return dummy SQL
- Use tmp_path for EXPORTS_FOLDER to avoid writing real files
- Monkeypatch os.path.exists / os.path.getsize / os.remove for file operations
"""

import os
from datetime import datetime
from vitalx.extraction import (
    export_tables_to_spreadsheets,
    cleanup_old_csvs,
    TABLE_SQL_MAPPING,
)
from vitalx.exceptions import CsvExportError


def test_table_sql_mapping_has_four_tables():
    """
    TABLE_SQL_MAPPING should contain entries for vitalx_walk, vitalx_sleep,
    weather, and vitalx_streak.
    Hint: assert len(TABLE_SQL_MAPPING) == 4 and check keys.
    """
    pass


def test_export_tables_creates_csv_for_each_table(monkeypatch, tmp_path):
    """
    export_tables_to_spreadsheets should create one CSV per table in EXPORTS_FOLDER.
    Hint: monkeypatch EXPORTS_FOLDER to tmp_path, mock fetch_result and
    load_sql_as_text, then check that 4 CSV files were created.
    """
    pass


def test_export_csv_filename_format(monkeypatch, tmp_path):
    """
    CSV files should be named <table>_<YYYY-MM-DD>.csv.
    Hint: check the filenames of created CSVs match this pattern.
    """
    pass


def test_export_csv_contains_expected_data(monkeypatch, tmp_path):
    """
    The contents of each CSV should match the data returned by fetch_result.
    Hint: mock fetch_result to return known rows, then read the CSV back
    and compare with pandas or csv module.
    """
    pass


def test_export_raises_csv_export_error_when_csv_empty(monkeypatch, tmp_path):
    """
    If an exported CSV is empty (0 bytes), export_tables_to_spreadsheets
    should raise CsvExportError.
    Hint: mock to_csv to create an empty file, or mock os.path.getsize to return 0.
    """
    pass


def test_cleanup_old_csvs_deletes_old_files(tmp_path, monkeypatch):
    """
    cleanup_old_csvs should delete CSV files older than retention_days.
    Hint: create old CSV files (set mtime in the past) and recent files,
    then call cleanup_old_csvs and verify old ones are gone.
    """
    pass


def test_cleanup_old_csvs_keeps_recent_files(tmp_path, monkeypatch):
    """
    cleanup_old_csvs should NOT delete files newer than retention_days.
    """
    pass


def test_cleanup_old_csvs_default_retention_is_seven_days():
    """
    The default retention_days parameter should be 7.
    Hint: check the function signature default.
    """
    pass


def test_export_calls_cleanup_after_exporting(monkeypatch, tmp_path):
    """
    export_tables_to_spreadsheets should call cleanup_old_csvs after exporting all tables.
    Hint: mock cleanup_old_csvs and assert it was called.
    """
    pass
