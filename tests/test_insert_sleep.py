from vitalx.service import insert_sleep
from vitalx.vitalx import VitalXSleep


def test_insert_sleep(monkeypatch):  # type: ignore
    sleep = VitalXSleep(8, 0, False)
    captured = {}
    def fake_execute_query(sql: str, params: dict[str, object]):
        captured["sql"] = sql
        captured["params"] = params
    monkeypatch.setattr("vitalx.service.execute_query", fake_execute_query)  # type: ignore
    insert_sleep(sleep)
    assert "insert into vitalx_sleep" in captured["sql"]
    assert captured["params"]["hours_slept"] == 8
    assert captured["params"]["minutes_slept"] == 0
    assert captured["params"]["good_sleep"] == False
