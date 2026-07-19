from .dbutils import execute_query, load_sql_as_text, fetch_result
from .vitalx import VitalXWalk, VitalXSleep
from typing import Any
from datetime import datetime, timedelta
from src.vitalx.utils import ANALYTICS_DBO


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


def get_total_steps() -> int:
    sql = load_sql_as_text(ANALYTICS_DBO, "get_total_step_count.sql")
    rows = fetch_result(sql)
    return int(rows[0]["total_steps"] or 0)


def get_total_sleep_time() -> tuple[int, int]:
    sql = load_sql_as_text(ANALYTICS_DBO, "get_total_sleep_time.sql")
    rows = fetch_result(sql)
    total_hours = int(rows[0]["total_hours"])
    total_minutes = int(rows[0]["total_minutes"])
    total_hours += total_minutes // 60
    total_minutes = total_minutes % 60
    return total_hours, total_minutes


def get_walk_history() -> list[dict[str, Any]]:
    sql = "select * from vitalx_walk"
    return fetch_result(sql)


def did_walk_today() -> bool:
    for walk in get_walk_history():
        todays_date = walk.get("todays_date")
        todays_date = datetime.fromisoformat(str(todays_date))
        if todays_date.date() == datetime.now().date():
            return True
    return False


def get_last_walk_date() -> datetime:
    all_walk_data: list[dict[str, Any]] = []
    all_dates: list[datetime] = []
    walk_data = get_walk_history()
    for walk in walk_data:
        all_walk_data.append(walk)
    for x in all_walk_data:
        for k, v in x.items():
            if k == "todays_date":
                all_dates.append(v.date())
    return max(all_dates)


def get_current_streak() -> int:
    current_streak: list[int] = []
    yesterday = datetime.now().date() - timedelta(days=1)
    sql = fetch_result("select * from vitalx_walk_streak")
    for x in sql:
        if x["todays_date"].date() == yesterday:
            current_streak.append(x["streak"])
    return current_streak[0]


def calculate_new_streak() -> int:
    current_streak = get_current_streak()
    current_streak += 1
    return current_streak


def save_new_streak() -> None:
    sql = "insert into vitalx_walk_streak (streak, todays_date) values (:streak, :todays_date)"
    params: dict[str, Any] = {
        "streak": calculate_new_streak(),
        "todays_date": datetime.now(),
    }
    try:
        execute_query(sql, params)
    except Exception as e:
        raise RuntimeError(f"Failed to insert new streak due to: {e}")


def get_latest_streak() -> int:
    sql = "select streak from vitalx_walk_streak order by todays_date desc limit 1"
    rows = fetch_result(sql)
    if not rows:
        return 1
    return rows[0]["streak"]


def update_streak_call_point() -> None:
    if did_walk_today() == True:
        if get_last_walk_date() == datetime.now().date() - timedelta(days=1):
            save_new_streak()
    else:
        sql = "insert into vitalx_walk_streak (streak, todays_date) values (:streak, :todays_date)"
        params: dict[str, Any] = {"streak": 1, "todays_date": datetime.now()}
        try:
            execute_query(sql, params)
        except Exception as e:
            raise ValueError(f"Failed to insert new streak due to: {e}")


# Legacy code from when I was wrestling with this before I did the above
# def check_if_walked_today() -> bool:
#     walk_data = fetch_result("select * from vitalx_walk")
#     for walk in walk_data:
#         todays_date = walk.get("todays_date")
#         todays_date = datetime.fromisoformat(str(todays_date))
#         if todays_date.date() == datetime.now().date():
#             return True
#     return False


# def insert_streak(latest_streak: int, first: bool = False) -> None:
#     streak: list[int] = []
#     sql = "insert into vitalx_walk_streak (streak) values (:streak)"
#     if first == True:
#         streak.append(1)
#     else:
#         streak.append(latest_streak)
#     params: dict[str, Any] = {"streak": streak[0]}
#     try:
#         execute_query(sql, params)
#     except Exception as e:
#         raise RuntimeError(f"Failed to insert streak due to: {e}")

# def update_streak() -> int:
#     streak_data = fetch_result("select * from vitalx_walk_streak")
#     all_streaks: list[int] = []
#     current_streak_number: list[int] = []
#     for x in streak_data:
#         for k, v in x.items():
#             if k == "streak":
#                 all_streaks.append(v)
#     print(all_streaks)
# if len(all_streaks) == 0:
#     all_streaks.append(1)
# return all_streaks[0]
# streak_achieved = check_walk_streak()
# if streak_achieved == True:
# else:
#     streak = 0
# return streak


def main() -> None:
    print(get_latest_streak())


if __name__ == "__main__":
    main()
