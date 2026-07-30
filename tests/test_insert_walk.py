from vitalx.service import insert_walk
from vitalx.vitalx import VitalXWalk
from datetime import datetime


def test_insert_walk(monkeypatch):
    walk = VitalXWalk(
        steps_walked=7100,
        calories_burnt=300,
        walk_location="test_location",
        todays_date=datetime.now(),
    )
    captured = {}

    def fake_execute_query(sql: str, params: dict[str, object]):
        captured["sql"] = sql
        captured["params"] = params

    monkeypatch.setattr("vitalx.service.execute_query", fake_execute_query)
    insert_walk(walk)
    assert "insert into vitalx_walk" in captured["sql"]
    assert isinstance(captured["params"]["steps_walked"], int)
    assert isinstance(captured["params"]["calories_burnt"], int)
    assert isinstance(captured["params"]["walk_location"], str)
    assert captured["params"]["steps_walked"] == 7100
    assert captured["params"]["calories_burnt"] == 300
    assert captured["params"]["walk_location"] == "test_location"
