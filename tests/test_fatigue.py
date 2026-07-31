from vitalx.service import did_sleep_eight_hours_last_night
from vitalx.vitalx import VitalXSleep


def test_fatigue(monkeypatch):
    sleep = VitalXSleep(
        7,
        48,
        True
    )
    captured = {}
    def fake_execute_query(sql: str, params: dict[str, Any]):
    result = did_sleep_eight_hours_last_night()
    assert 