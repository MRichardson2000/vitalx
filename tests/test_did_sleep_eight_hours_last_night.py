from vitalx.service import did_sleep_eight_hours_last_night
from datetime import datetime


# change to 7 hours and it fails as expected
def test_did_sleep_eight_hours_last_night(monkeypatch):
    def fake_fetch_result(query):
        return [
            {
                "hours_slept": 8,
                "minutes_slept": 10,
                "good_sleep": True,
                "todays_date": datetime.now().date(),
            }
        ]

    monkeypatch.setattr("vitalx.service.fetch_result", fake_fetch_result)
    result = did_sleep_eight_hours_last_night()
    assert result


def test_didnt_sleep_eight_hours_last_night(monkeypatch):
    def fake_fetch_result(query):
        return [
            {
                "hours_slept": 7,
                "minutes_slept": 10,
                "good_sleep": True,
                "todays_date": datetime.now().date(),
            }
        ]

    monkeypatch.setattr("vitalx.service.fetch_result", fake_fetch_result)
    result = did_sleep_eight_hours_last_night()
    assert not result