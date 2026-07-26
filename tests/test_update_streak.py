from datetime import datetime, timedelta
from typing import Any
from vitalx.service import reset_streak, update_streak_call_point, validate_streak

# specific date and 5 days before for the test
FIVE_DAYS_BEFORE_TODAY = datetime(2026, 7, 21)
YESTERDAY = FIVE_DAYS_BEFORE_TODAY - timedelta(days=1)


def test_update_streak_call_point(monkeypatch) -> None:  # type: ignore
    # An in memory list acting as a mock database logger
    captured_queries: list[dict[str, Any]] = []

    # This makes sure the real database is never called. It intercepts the sql string and params then appends them to the list
    def fake_execute_query(sql: str, params: dict[str, Any]):
        captured_queries.append({"sql": sql, "params": params})

    # Real execute query is swapped out for the fake one during the test. Then the original function is restored
    monkeypatch.setattr("vitalx.service.execute_query", fake_execute_query)  # type: ignore

    fake_history: list[dict[str, Any]] = [
        {
            "steps_walked": 6900,
            "calories_burnt": 310,
            "walk_location": "test_location",
            "todays_date": datetime.combine(YESTERDAY, datetime.min.time()),
        }
    ]

    # Below validates step count is met
    last_walk_steps = fake_history[0]["steps_walked"]
    is_valid_walk = validate_streak(last_walk_steps)

    # When update streak call point calls reset streak fn, This wrapper runs.
    # It executes the actual reset streak function from the service layer but injects 2 lambdas to override the values
    # Because reset streak calls execute query under the hood it triggers the fake execute query and writes the sql and params to the captured queries list
    def mock_reset_streak():
        reset_streak(todays_date=lambda: FIVE_DAYS_BEFORE_TODAY, streak=1)

    # We pass in our fake values instead of calling the real ones.
    # walked_today_fn = lambda _: False receives walk history as an argument represented by _ because it's unused inside the lambda. It forces False
    # last_walk_date_fn = lambda _: YESTERDAY forces the system to believe the last walk was yesterday so the if-condition passes
    # todays_date_fn overrides datetime.now() with the specific date
    # save_new_streak_fn is a dummy function returning None since saving a new streak should not occur here
    # reset_streak_fn executes mock_reset_streak() which resets the streak back to 1
    # Due to these inputs, streak call point evaluates to not walked today and last walk date is yesterday which causes it to invoke reset_streak_fn
    update_streak_call_point(
        walk_history_fn=lambda: fake_history,
        # not walked today
        walked_today_fn=lambda _: False,
        # Walked yesterday
        last_walk_date_fn=lambda _: YESTERDAY,
        todays_date_fn=lambda: FIVE_DAYS_BEFORE_TODAY,
        save_new_streak_fn=lambda: None,
        reset_streak_fn=lambda: mock_reset_streak(),
    )

    assert is_valid_walk is False
    assert len(captured_queries) == 1
    assert "insert into vitalx_walk_streak" in captured_queries[0]["sql"]
    assert captured_queries[0]["params"]["streak"] == 1
    assert captured_queries[0]["params"]["todays_date"] == FIVE_DAYS_BEFORE_TODAY
