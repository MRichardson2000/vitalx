"""Integration tests for the VitalX database layer.

These tests verify that dbutils functions work correctly with SQL files
and the database connection. They test the layer that sits between the
service layer and the actual PostgreSQL database.

What to test:
- load_sql_as_text reads each SQL file in dbo/creates and dbo/analytics
- execute_query can run a CREATE TABLE statement
- fetch_result can run a SELECT statement and return rows
- get_engine creates a working connection from .env variables
- create_schemas creates all four tables in the database
- Round-trip: insert a row, then fetch it back

Suggested approach: These tests need a real test database. You can either:
- Use Docker to spin up a test Postgres container
- Use a SQLite in-memory database as a stand-in (if SQL is compatible)
- Mark these with @pytest.mark.integration and run separately
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
from vitalx.utils import CREATES_DBO, ANALYTICS_DBO


@pytest.mark.integration
def test_load_each_create_sql_file():
    """
    Each .sql file in dbo/creates should be readable as text.
    Files: create_vitalx_walk_table.sql, create_vitalx_sleep_table.sql,
    create_vitalx_walk_streak_table.sql, create_weather_table.sql
    Hint: iterate over the files in CREATES_DBO and call load_sql_as_text on each.
    """
    pass


@pytest.mark.integration
def test_load_each_analytics_sql_file():
    """
    Each .sql file in dbo/analytics should be readable as text.
    Hint: iterate over the files in ANALYTICS_DBO and call load_sql_as_text on each.
    """
    pass


@pytest.mark.integration
def test_get_engine_creates_connection():
    """
    get_engine should return an engine that can actually connect.
    Hint: call get_engine(), then engine.connect() and execute a simple
    query like "SELECT 1".
    """
    pass


@pytest.mark.integration
def test_create_schemas_creates_all_tables():
    """
    create_schemas should create all four tables in the database.
    Hint: call create_schemas(), then query information_schema.tables to
    verify all four tables exist.
    """
    pass


@pytest.mark.integration
def test_execute_and_fetch_round_trip():
    """
    Insert a row via execute_query, then fetch it back via fetch_result.
    This tests that the database layer can persist and retrieve data.
    Hint: insert into vitalx_walk, then select from vitalx_walk, compare.
    """
    pass


@pytest.mark.integration
def test_fetch_result_returns_dict_rows():
    """
    fetch_result should return a list of dicts, not tuples or Row objects.
    Hint: execute a SELECT query, check type(result[0]) is dict.
    """
    pass
