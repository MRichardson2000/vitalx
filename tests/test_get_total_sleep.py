from vitalx.service import get_total_sleep_time


def test_get_total_sleep_time(monkeypatch):
    def fake_fetch_result(query):
        return [{"total_hours": 7, "total_minutes": 39}]

    monkeypatch.setattr("vitalx.service.fetch_result", fake_fetch_result)
    result = get_total_sleep_time()
    assert isinstance(result, tuple)
    assert result == (7, 39)
