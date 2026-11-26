"""Unit tests for vitalx.dbutils (database utilities).

What to test:
- get_engine creates a SQLAlchemy engine from .env variables
- fetch_result returns a list of dicts from query results
- fetch_result raises DatabaseError when the query fails
- execute_query executes a query without returning results
- execute_query raises DatabaseError when execution fails
- load_sql_as_text reads a .sql file and returns its contents as a string
- load_sql_as_text raises ReadSqlAsTextError when the file is missing
- create_schemas executes all four CREATE TABLE SQL files

Suggested mocks:
- Monkeypatch vitalx.dbutils.get_engine to return a mock engine
- Monkeypatch vitalx.dbutils.execute_query / fetch_result for higher-level tests
- Use tmp_path fixture to create temporary .sql files for load_sql_as_text tests
"""

import pytest
from pathlib import Path
from vitalx.dbutils import (
    get_engine,
    fetch_result,
    execute_query,
    load_sql_as_text,
    create_schemas,
)
from vitalx.exceptions import DatabaseError, ReadSqlAsTextError


def test_get_engine_returns_engine(monkeypatch):
    """
    get_engine should return a SQLAlchemy Engine instance.
    Hint: you may need to monkeypatch os.getenv or set environment variables.
    Check that the returned object has a .connect() or .begin() method.
    """
    pass


def test_fetch_result_returns_list_of_dicts(monkeypatch):
    """
    fetch_result should return a list[dict[str, Any]].
    Hint: mock the engine's begin() context manager and execute() to return
    rows that can be converted via result.mappings().
    """
    pass


def test_fetch_result_raises_database_error_on_failure(monkeypatch):
    """
    When the database query fails, fetch_result should raise DatabaseError.
    Hint: mock execute() to raise an Exception and assert pytest.raises.
    """
    pass


def test_execute_query_executes_without_return(monkeypatch):
    """
    execute_query should run the query and return None.
    Hint: mock the connection and verify execute() was called with the query.
    """
    pass


def test_execute_query_raises_database_error_on_failure(monkeypatch):
    """
    When execution fails, execute_query should raise DatabaseError.
    """
    pass


def test_load_sql_as_text_returns_file_contents(tmp_path):
    """
    load_sql_as_text should read a .sql file and return its contents as a string.
    Hint: create a temporary .sql file with tmp_path, call load_sql_as_text,
    and assert the returned string matches the file contents.
    """
    pass


def test_load_sql_as_text_raises_on_missing_file():
    """
    When the .sql file does not exist, load_sql_as_text should raise ReadSqlAsTextError.
    Hint: pass a path to a non-existent file.
    """
    pass


def test_create_schemas_executes_all_tables(monkeypatch):
    """
    create_schemas should load and execute all four CREATE TABLE SQL files.
    Hint: mock load_sql_as_text and execute_query, then verify execute_query
    was called 4 times (once per table).
    """
    pass
