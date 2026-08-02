from vitalx.service import get_sleep_history
from datetime import datetime, date


def test_get_walk_history(monkeypatch):
    def fake_fetch_result(query):
        return [
            {
                "hours_slept": 8,
                "minutes_slept": 32,
                "good_sleep": True,
                "todays_date": datetime.now().date(),
            }
        ]

    monkeypatch.setattr("vitalx.service.fetch_result", fake_fetch_result)
    result = get_sleep_history()
    assert isinstance(result, list)
    assert result[0]["hours_slept"] == 8
    assert isinstance(result[0]["hours_slept"], int)
    assert result[0]["minutes_slept"] == 32
    assert isinstance(result[0]["minutes_slept"], int)
    assert result[0]["good_sleep"] == True
    assert isinstance(result[0]["good_sleep"], bool)
    assert result[0]["todays_date"] == datetime.now().date()
    assert isinstance(result[0]["todays_date"], date)
