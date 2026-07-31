from vitalx.service import did_sleep_eight_hours_last_night
from vitalx.vitalx import VitalXSleep


def test_fatigue_true(monkeypatch):
    def fake_fetch_result(query):
        return [{"hours_slept": 8}]

    monkeypatch.setattr("vitalx.service.fetch_result", fake_fetch_result)
    assert did_sleep_eight_hours_last_night() is True


def test_fatigue_false(monkeypatch):
    def fake_fetch_result(query):
        return [{"hours_slept": 7}]

    monkeypatch.setattr("vitalx.service.fetch_result", fake_fetch_result)
    assert did_sleep_eight_hours_last_night() is False


def test_fatigue_none(monkeypatch):
    def fake_fetch_result(query):
        return []

    monkeypatch.setattr("vitalx.service.fetch_result", fake_fetch_result)
    assert did_sleep_eight_hours_last_night() is None
