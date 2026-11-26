"""Shared pytest configuration and fixtures for all VitalX tests.

Fixtures defined here are available to all tests under tests/ (unit,
integration, and e2e) because conftest.py fixtures apply to their own
directory and all subdirectories.
"""

import logging
import pytest
from datetime import datetime
from unittest.mock import MagicMock

from vitalx.vitalx import VitalXWalk, VitalXSleep, Weather
from tests.fixtures.sample_data import (
    SAMPLE_WALK,
    SAMPLE_SLEEP,
    SAMPLE_WEATHER,
    SAMPLE_WALK_ROWS,
    SAMPLE_SLEEP_ROWS,
    SAMPLE_STREAK_ROWS,
)


@pytest.fixture(autouse=True)
def configure_test_logging(caplog):
    """
    Capture logs natively during tests so prod log files stay clean.

    This is autouse=True so it applies to every test automatically.
    """
    caplog.set_level(logging.DEBUG)


@pytest.fixture
def sample_walk() -> VitalXWalk:
    """Return a valid VitalXWalk instance."""
    return SAMPLE_WALK


@pytest.fixture
def sample_sleep() -> VitalXSleep:
    """Return a valid VitalXSleep instance."""
    return SAMPLE_SLEEP


@pytest.fixture
def sample_weather() -> Weather:
    """Return a valid Weather instance."""
    return SAMPLE_WEATHER


@pytest.fixture
def mock_fetch_result(monkeypatch):
    """
    Mock vitalx.service.fetch_result.

    Returns a MockState object with a `return_value` attribute you can set
    to control what the mocked function returns.

    Example:
        def test_something(mock_fetch_result):
            mock_fetch_result.return_value = [{"total_steps": 100}]
            result = get_total_steps()
            assert result == 100
    """

    class MockState:
        return_value = []

    def fake_fetch_result(query, params=None):
        return MockState.return_value

    monkeypatch.setattr("vitalx.service.fetch_result", fake_fetch_result)
    return MockState


@pytest.fixture
def mock_execute_query(monkeypatch):
    """
    Mock vitalx.service.execute_query.

    Returns a dict that captures the last SQL and params passed to it.

    Example:
        def test_something(mock_execute_query):
            insert_walk(sample_walk)
            assert "insert into" in mock_execute_query["sql"]
            assert mock_execute_query["params"]["steps_walked"] == 7500
    """
    captured = {}

    def fake_execute_query(sql, params=None):
        captured["sql"] = sql
        captured["params"] = params or {}

    monkeypatch.setattr("vitalx.service.execute_query", fake_execute_query)
    return captured


@pytest.fixture
def failing_execute_query(monkeypatch):
    """Mock execute_query to raise an exception (for error-path testing)."""

    def fake_execute_query(sql, params=None):
        raise Exception("Database connection lost")

    monkeypatch.setattr("vitalx.service.execute_query", fake_execute_query)


@pytest.fixture
def failing_fetch_result(monkeypatch):
    """Mock fetch_result to raise an exception (for error-path testing)."""

    def fake_fetch_result(query, params=None):
        raise Exception("Database connection lost")

    monkeypatch.setattr("vitalx.service.fetch_result", fake_fetch_result)
