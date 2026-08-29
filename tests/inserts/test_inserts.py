from vitalx.service import insert_walk, insert_sleep, insert_weather, update_streak
from vitalx.vitalx import VitalXWalk, VitalXSleep, Weather
from datetime import datetime, timedelta
import pytest


@pytest.fixture
def fake_execute_query(monkeypatch):
    captured = {}

    def fake_execute_query(sql: str, params: dict[str, object]):
        captured["sql"] = sql
        captured["params"] = params

    monkeypatch.setattr(
        "vitalx.service.execute_query",
        fake_execute_query,
    )
    return captured


def test_insert_walk(fake_execute_query):
    walk = VitalXWalk(
        steps_walked=7100,
        calories_burnt=300,
        miles_walked=4.6,
        walk_location="test_location",
        todays_date=datetime.now(),
    )
    insert_walk(walk)
    assert "insert into vitalx_walk" in fake_execute_query["sql"]
    assert fake_execute_query["params"]["steps_walked"] == 7100
    assert fake_execute_query["params"]["calories_burnt"] == 300
    assert fake_execute_query["params"]["walk_location"] == "test_location"


def test_insert_sleep(fake_execute_query):
    sleep = VitalXSleep(8, 0, False)
    insert_sleep(sleep)
    assert "insert into vitalx_sleep" in fake_execute_query["sql"]
    assert fake_execute_query["params"]["hours_slept"] == 8
    assert fake_execute_query["params"]["minutes_slept"] == 0
    assert fake_execute_query["params"]["good_sleep"] == False


def test_insert_weather(fake_execute_query):
    weather = Weather(
        10,
        17,
        datetime(2026, 8, 28, 4, 57, 0),
        datetime(2026, 8, 28, 19, 34, 0),
        13,
        0,
        4,
        datetime.now()
    )
    insert_weather(weather)
    assert "insert into weather" in fake_execute_query["sql"]
    assert fake_execute_query["params"]


def test_update_streak_increments(monkeypatch, fake_execute_query):
    today = datetime.now().date()
    yesterday = today - timedelta(days=1)
    monkeypatch.setattr("vitalx.service.get_last_walk_date", lambda: today)
    monkeypatch.setattr("vitalx.service.streak_row_exists_for_today", lambda: False)
    monkeypatch.setattr("vitalx.service.get_latest_streak_entry", lambda: (5, yesterday))
    update_streak()
    assert fake_execute_query["params"]["streak"] == 6


def test_update_streak_resets(monkeypatch, fake_execute_query):
    today = datetime.now().date()
    two_days_ago = today - timedelta(days=2)
    monkeypatch.setattr("vitalx.service.get_last_walk_date", lambda: today)
    monkeypatch.setattr("vitalx.service.streak_row_exists_for_today", lambda: False)
    monkeypatch.setattr("vitalx.service.get_latest_streak_entry", lambda: (5, two_days_ago))
    update_streak()
    assert fake_execute_query["params"]["streak"] == 1