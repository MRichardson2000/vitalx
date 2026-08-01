from vitalx.service import did_walk_today


def test_did_walk_today(monkeypatch):
    def fake_fetch_result(query, params):
        return [{"walked_today": True}]

    monkeypatch.setattr("vitalx.service.fetch_result", fake_fetch_result)
    result = did_walk_today()
    assert result is True
