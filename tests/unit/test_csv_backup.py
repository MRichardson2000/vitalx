"""Unit tests for vitalx.csv_backup (CSV import/restore functionality).

What to test:
- import_spreadsheets_to_database reads the latest CSV for each table
- import_spreadsheets_to_database drops the 'id' column if present
- import_spreadsheets_to_database inserts data using df.to_sql with if_exists="append"
- import_spreadsheets_to_database raises FileNotFoundError when exports folder doesn't exist
- import_spreadsheets_to_database raises ValueError when a CSV is empty
- import_spreadsheets_to_database raises CsvImportError when import fails
- TABLE_PREFIX_MAPPING maps the correct table names to CSV prefixes
- Only the latest file (by mtime) is imported when multiple CSVs exist for a table

Suggested mocks:
- Mock os.path.exists, glob.glob, os.path.getmtime
- Mock pandas.read_csv to return a DataFrame
- Mock the SQLAlchemy engine's begin() context manager
- Use tmp_path for EXPORTS_FOLDER
"""

import os
from vitalx.dbutils import fetch_result, load_sql_as_text
from vitalx import csv_backup
from vitalx.csv_backup import (
    import_spreadsheets_to_database,
    TABLE_PREFIX_MAPPING,
)
from vitalx.utils import ANALYTICS_DBO, EXPORTS_FOLDER
from vitalx.exceptions import CsvImportError
from typing import Any


def test_import_reads_latest_csv(monkeypatch, tmp_path):
    """
    import_spreadsheets_to_database should import the most recently modified CSV
    for each table.
    Hint: create multiple CSVs per table with different mtimes and verify
    only the latest is read.
    """
    csv_1 = tmp_path / "walk_b.csv"
    csv_1.write_text("steps\n10\n")
    os.utime(csv_1, (100, 100))
    csv_2 = tmp_path / "walk_a.csv"
    csv_2.write_text("steps\n20\n")
    os.utime(csv_2, (200, 200))
    monkeypatch.settattr(csv_backup, "EXPORTS_FOLDER", str(tmp_path))


def test_import_drops_id_column(monkeypatch, tmp_path):
    """
    If a CSV has an 'id' column, it should be dropped before inserting.
    Hint: mock pandas.read_csv to return a DataFrame with an 'id' column,
    then verify df.drop was called with columns=["id"].
    """
    pass


def test_import_uses_append_mode(monkeypatch, tmp_path):
    """
    Data should be inserted with if_exists="append" (not "replace" or "fail").
    Hint: mock df.to_sql and assert it was called with if_exists="append".
    """
    pass


def test_import_raises_file_not_found_when_folder_missing(monkeypatch):
    """
    When EXPORTS_FOLDER doesn't exist, import_spreadsheets_to_database
    should raise FileNotFoundError.
    Hint: monkeypatch os.path.exists to return False.
    """
    pass


def test_import_raises_value_error_when_csv_empty(monkeypatch, tmp_path):
    """
    When a CSV's DataFrame is empty, import should raise ValueError.
    Hint: mock pandas.read_csv to return an empty DataFrame.
    """
    pass


def test_import_raises_csv_import_error_on_failure(monkeypatch, tmp_path):
    """
    When the database insert fails, import_spreadsheets_to_database
    should raise CsvImportError.
    Hint: mock df.to_sql to raise an exception.
    """
    pass
