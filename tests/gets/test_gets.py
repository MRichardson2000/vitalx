from vitalx.service import (
    get_total_steps,
    get_total_sleep_time,
    get_walk_history,
    get_last_walk_date,
    get_latest_streak_entry,
    get_total_days_walked,
    get_total_calories_burnt,
    get_total_miles_walked,
    get_favourite_walk_location,
    get_total_days_slept,
    get_latest_streak,
    get_sleep_history
)
from datetime import datetime
import pytest


@pytest.fixture
def mock_fetch(monkeypatch):
    class MockState:
        return_value = []

    def fake_fetch_result(query):
        return MockState.return_value

    monkeypatch.setattr("vitalx.service.fetch_result", fake_fetch_result)
    return MockState


def test_get_total_steps(mock_fetch):
    mock_fetch.return_value = [{"total_steps": 4875}]
    result = get_total_steps()
    assert result == 4875


def test_get_total_sleep(mock_fetch):
    mock_fetch.return_value = [{"total_hours": 7, "total_minutes": 39}]
    result = get_total_sleep_time()
    assert result == (7, 39)


def test_get_total_days_walked(mock_fetch):
    mock_fetch.return_value = [{"total_days_walked": 43}]
    result = get_total_days_walked()
    assert result == 43


def test_get_total_calories_burnt(mock_fetch):
    mock_fetch.return_value = [{"total_calories_burnt": 327}]
    result = get_total_calories_burnt()
    assert result == 327


def test_get_total_miles_walked(mock_fetch):
    mock_fetch.return_value = [{"total_miles_walked": 6.1}]
    result = get_total_miles_walked()
    assert result == "6.1"


def test_get_favourite_walk_location(mock_fetch):
    mock_fetch.return_value = [{"walk_location": "test"}]
    result = get_favourite_walk_location()
    assert result == "test"


def test_get_total_days_slept(mock_fetch):
    mock_fetch.return_value = [{"total_days_slept": 42}]
    result = get_total_days_slept()
    assert result == 42


def test_get_walk_history(mock_fetch):
    mock_fetch.return_value = [
        {
            "steps_walked": 6100,
            "calories_burnt": 304,
            "walk_location": "test_location",
            "todays_date": datetime.now(),
        }
    ]
    result = get_walk_history()
    assert result[0]["steps_walked"] == 6100
    assert result[0]["calories_burnt"] == 304
    assert result[0]["walk_location"] == "test_location"


def test_get_last_walk_date(mock_fetch):
    mock_fetch.return_value = [{"todays_date": datetime.now().date()}]
    result = get_last_walk_date()
    assert result == datetime.now().date()


def test_get_sleep_history(mock_fetch):
    mock_fetch.return_value  = [
        {
            "hours_slept": 8,
            "minutes_slept": 32,
            "good_sleep": True,
            "todays_date": datetime.now().date(),
        }
    ]
    result = get_sleep_history()
    assert isinstance(result, list)
    assert len(result) > 0


def test_get_latest_streak_entry(mock_fetch):
    mock_fetch.return_value = [{"streak": 23, "todays_date": datetime.now().date()}]
    result = get_latest_streak_entry()
    assert result == (23, datetime.now().date())


def test_get_latest_streak(mock_fetch):
    mock_fetch.return_value = [{"streak": 23, "todays_date": datetime.now().date()}]
    result = get_latest_streak()
    assert result == 23