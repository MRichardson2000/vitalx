from datetime import datetime
import pytest
from vitalx.service import (
    validate_streak,
    streak_row_exists_for_today,
    did_walk_today,
    did_sleep_eight_hours_last_night,
)


@pytest.fixture
def mock_fetch(monkeypatch):
    class MockState:
        return_value = []

    def fake_fetch_result(query):
        return MockState.return_value

    monkeypatch.setattr("vitalx.service.fetch_result", fake_fetch_result)
    return MockState


def test_validate_streak(mock_fetch):
    walk = [
        {
            "steps_walked": 5800,
            "calories_burnt": 300,
            "miles_walked": 5.1,
            "walk_location": "test_location",
        }
    ]
    mock_fetch.return_value = walk
    steps = walk[0]["steps_walked"]
    validation = validate_streak(steps)
    assert validation is False


def test_streak_row_exists_for_today(mock_fetch):
    mock_fetch.return_value = [{"todays_date": datetime.now().date()}]
    assert streak_row_exists_for_today()


def test_did_walk_today(mock_fetch):
    mock_fetch.return_value = [{"walked_today": True}]
    result = did_walk_today()
    assert result == True


def test_did_sleep_eight_hours_last_night(mock_fetch):
    sleep = [
        {
            "hours_slept": 8,
            "minutes_slept": 10,
            "good_sleep": True,
            "todays_date": datetime.now().date(),
        }
    ]
    mock_fetch.return_value = sleep
    result = did_sleep_eight_hours_last_night()
    assert result


def test_didnt_sleep_eight_hours_last_night(mock_fetch):
    sleep = [
        {
            "hours_slept": 7,
            "minutes_slept": 10,
            "good_sleep": True,
            "todays_date": datetime.now().date(),
        }
    ]
    mock_fetch.return_value = sleep
    result = did_sleep_eight_hours_last_night()
    assert not result


def test_fatigue_true(mock_fetch):
    mock_fetch.return_value = [{"hours_slept": 8}]
    result = did_sleep_eight_hours_last_night()
    assert result


def test_fatigue_false(mock_fetch):
    mock_fetch.return_value = [{"hours_slept": 7}]
    result = did_sleep_eight_hours_last_night()
    assert not result
