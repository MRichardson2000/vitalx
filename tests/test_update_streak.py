from vitalx.service import update_streak_call_point, save_new_streak
from datetime import datetime, timedelta
from typing import Any


FIVE_DAYS_BEFORE_TODAY = datetime(2026, 7, 21)
YESTERDAY = FIVE_DAYS_BEFORE_TODAY - timedelta(days=1)


def test_update_streak_call_point(monkeypatch) -> None:  # type: ignore
    captured_queries: list[dict[str, Any]] = []

    def fake_execute_query(sql: str, params: dict[str, Any]):
        captured_queries.append({"sql": sql, "params": params})

    monkeypatch.setattr("vitalx.service.execute_query", fake_execute_query)  # type: ignore
    fake_history: list[dict[str, Any]] = [
        {
            "steps_walked": 6900,
            "calories_burnt": 310,
            "walk_location": "test_location",
            "todays_date": datetime.combine(YESTERDAY, datetime.min.time()),
        }
    ]

    def mock_save_new_streak():
        save_new_streak(
            todays_date=lambda: FIVE_DAYS_BEFORE_TODAY, calculate_streak_fn=lambda: 3
        )

    update_streak_call_point(
        walk_history_fn=lambda: fake_history,
        # not walked today
        walked_today_fn=lambda _: False,
        # Walked yesterday
        last_walk_date_fn=lambda _: YESTERDAY,
        todays_date_fn=lambda: FIVE_DAYS_BEFORE_TODAY,
        save_new_streak_fn=lambda: mock_save_new_streak(),
        reset_streak_fn=lambda: None,
    )
    assert len(captured_queries) == 1
    assert "insert into vitalx_walk_streak" in captured_queries[0]["sql"]
    assert captured_queries[0]["params"]["streak"] == 3
    assert captured_queries[0]["params"]["todays_date"] == FIVE_DAYS_BEFORE_TODAY
