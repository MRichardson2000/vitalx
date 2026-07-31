from vitalx.service import get_total_steps


def test_get_total_steps_int(monkeypatch):
    def fake_fetch_result(query):
        return [{"total_steps": 4875}]

    monkeypatch.setattr("vitalx.service.fetch_result", fake_fetch_result)
    result = get_total_steps()
    assert isinstance(result, int)
    assert result == 4875
    assert result is not None
