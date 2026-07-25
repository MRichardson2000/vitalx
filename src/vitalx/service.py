from .dbutils import execute_query, load_sql_as_text, fetch_result
from vitalx.vitalx import VitalXWalk, VitalXSleep  # type: ignore
from typing import Any, Callable
from pathlib import Path
from datetime import datetime, timedelta
from vitalx.utils import ANALYTICS_DBO  # type: ignore


def insert_walk(walk: VitalXWalk) -> None:
    sql = """
            insert into vitalx_walk (
                steps_walked,
                calories_burnt,
                walk_location,
                todays_date
            )
            values (:steps_walked, :calories_burnt, :walk_location, :todays_date)
          """
    params: dict[str, Any] = {
        "steps_walked": walk.steps_walked,
        "calories_burnt": walk.calories_burnt,
        "walk_location": walk.walk_location,
        "todays_date": walk.todays_date,
    }
    try:
        execute_query(sql, params)
    except Exception as e:
        raise RuntimeError(f"Failed to insert walk due to: {e}")


def insert_sleep(sleep: VitalXSleep) -> None:
    sql = """
            insert into vitalx_sleep (
                hours_slept, 
                minutes_slept,
                good_sleep,
                todays_date
            )
            values (:hours_slept, :minutes_slept, :good_sleep, :todays_date)
          """
    params: dict[str, Any] = {
        "hours_slept": sleep.hours_slept,
        "minutes_slept": sleep.minutes_slept,
        "good_sleep": sleep.good_sleep,
        "todays_date": sleep.todays_date,
    }
    try:
        execute_query(sql, params)
    except Exception as e:
        raise RuntimeError(f"Failed to insert sleep due to: {e}")


def get_total_steps(
    file_path: Path = ANALYTICS_DBO,
    file_name: str = "get_total_step_count.sql",
    return_value: str = "total_steps",
) -> int:
    sql = load_sql_as_text(file_path, file_name)
    rows = fetch_result(sql)
    return int(rows[0][return_value] or 0)


def get_total_sleep_time(
    file_path: Path = ANALYTICS_DBO,
    file_name: str = "get_total_sleep_time.sql",
    hours_value: str = "total_hours",
    minutes_value: str = "total_minutes",
) -> tuple[int, int]:
    sql = load_sql_as_text(file_path, file_name)
    rows = fetch_result(sql)
    total_hours = int(rows[0][hours_value])
    total_minutes = int(rows[0][minutes_value])
    total_hours += total_minutes // 60
    total_minutes = total_minutes % 60
    return total_hours, total_minutes


def get_walk_history(query: str = "select * from vitalx_walk") -> list[dict[str, Any]]:
    return fetch_result(query)


def did_walk_today(walk_history: list[dict[str, Any]]) -> bool:
    for walk in walk_history:
        todays_date = walk.get("todays_date")
        todays_date = datetime.fromisoformat(str(todays_date))
        if todays_date.date() == datetime.now().date():
            return True
    return False


def get_last_walk_date(walk_history: list[dict[str, Any]]) -> datetime:
    all_walk_data: list[dict[str, Any]] = []
    all_dates: list[datetime] = []
    walk_data = walk_history
    for walk in walk_data:
        all_walk_data.append(walk)
    for x in all_walk_data:
        for k, v in x.items():
            if k == "todays_date":
                all_dates.append(v.date())
    return max(all_dates)


def get_current_streak(
    query: str = "select * from vitalx_walk_streak",
    todays_date_value: str = "todays_date",
    streak_value: str = "streak",
) -> int:
    current_streak: list[int] = []
    yesterday = datetime.now().date() - timedelta(days=1)
    sql = fetch_result(query)
    for x in sql:
        if x[todays_date_value].date() == yesterday:
            current_streak.append(x[streak_value])
    return current_streak[0]


def calculate_new_streak(
    get_current_streak_fn: Callable[[], int] = get_current_streak,
) -> int:
    return get_current_streak_fn() + 1


def validate_streak(steps_walked: int, required_steps: int = 7000) -> bool:
    return steps_walked >= required_steps


def reset_streak(
    query: str = "insert into vitalx_walk_streak (streak, todays_date) values (:streak, :todays_date)",
    streak: int = 1,
    todays_date: Callable[[], datetime] = datetime.now,
) -> None:
    params: dict[str, Any] = {"streak": streak, "todays_date": todays_date()}
    try:
        execute_query(query, params)
    except Exception as e:
        raise RuntimeError(f"Failed to insert new streak due to: {e}")


def save_new_streak(
    query: str = "insert into vitalx_walk_streak (streak, todays_date) values (:streak, :todays_date)",
    todays_date: Callable[[], datetime] = datetime.now,
    calculate_streak_fn: Callable[[], int] = calculate_new_streak,
) -> None:
    streak = calculate_streak_fn()
    params: dict[str, Any] = {"streak": streak, "todays_date": todays_date()}
    try:
        execute_query(query, params)
    except Exception as e:
        raise RuntimeError(f"Failed to insert new streak due to: {e}")


def get_latest_streak(
    query: str = "select streak from vitalx_walk_streak order by todays_date desc limit 1",
    input_value: str = "streak",
) -> int:
    rows = fetch_result(query)
    if not rows:
        return 1
    return rows[0][input_value]


def update_streak_call_point(
    walk_history_fn: Callable[[], list[dict[str, Any]]] = get_walk_history,
    walked_today_fn: Callable[[list[dict[str, Any]]], bool] = did_walk_today,
    last_walk_date_fn: Callable[[list[dict[str, Any]]], datetime] = get_last_walk_date,
    save_new_streak_fn: Callable[[], None] = lambda: save_new_streak(),
    reset_streak_fn: Callable[[], None] = lambda: reset_streak(),
    todays_date_fn: Callable[[], datetime] = datetime.now,
) -> None:
    walk_history = walk_history_fn()
    walked_today = walked_today_fn(walk_history)
    last_walk_date = last_walk_date_fn(walk_history)
    today = todays_date_fn().date()
    yesterday = today - timedelta(days=1)
    if not walked_today and last_walk_date == yesterday:
        reset_streak_fn()
    save_new_streak_fn()


def main() -> None:
    print(get_latest_streak())


if __name__ == "__main__":
    main()
