from vitalx.service import get_latest_streak_entry
from datetime import datetime


def test_get_latest_streak_entry(monkeypatch):
    def fake_fetch_result(query):
        return [{"streak": 3, "todays_date": datetime.now().date()}]

    monkeypatch.setattr("vitalx.service.fetch_result", fake_fetch_result)
    result = get_latest_streak_entry()
    assert isinstance(result, tuple)
    assert result == (3, datetime.now().date())
