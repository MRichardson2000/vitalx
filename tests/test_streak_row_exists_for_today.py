from vitalx.service import streak_row_exists_for_today
from datetime import datetime


def test_streak_row_exists_for_today(monkeypatch):
    def fake_fetch_result(query, params):
        return [{"todays_date": datetime.now().date()}]

    monkeypatch.setattr("vitalx.service.fetch_result", fake_fetch_result)
    result = streak_row_exists_for_today()
    assert isinstance(result, bool)
