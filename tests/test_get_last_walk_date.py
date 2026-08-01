from vitalx.service import get_last_walk_date
from datetime import datetime, date


def test_get_last_walk_date(monkeypatch):
    def fake_fetch_result(query):
        return [{"todays_date": datetime.now().date()}]

    monkeypatch.setattr("vitalx.service.fetch_result", fake_fetch_result)
    result = get_last_walk_date()
    assert result == datetime.now().date()
    assert isinstance(result, date)
