from vitalx.service import get_walk_history
from datetime import datetime


def test_get_walk_history(monkeypatch):
    def fake_fetch_result(query):
        return [
            {
                "steps_walked": 6100,
                "calories_burnt": 304,
                "walk_location": "test_location",
                "todays_date": datetime.now(),
            }
        ]

    monkeypatch.setattr("vitalx.service.fetch_result", fake_fetch_result)
    result = get_walk_history()
    assert isinstance(result, list)
    assert result[0]["steps_walked"] == 6100
    assert isinstance(result[0]["steps_walked"], int)
    assert result[0]["calories_burnt"] == 304
    assert isinstance(result[0]["calories_burnt"], int)
    assert result[0]["walk_location"] == "test_location"
    assert isinstance(result[0]["walk_location"], str)
    assert isinstance(result[0]["todays_date"], datetime)
