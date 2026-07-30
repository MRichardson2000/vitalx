from .dbutils import execute_query, load_sql_as_text, fetch_result
from vitalx.vitalx import VitalXWalk, VitalXSleep
from vitalx.validation import validate_walk, validate_sleep
from vitalx.exceptions import DatabaseError, EmptyDictionaryError, EmptyListError
from typing import Any
from pathlib import Path
from datetime import datetime, timedelta, date
from vitalx.utils import ANALYTICS_DBO
from vitalx.logger import get_logger


logger = get_logger(__name__)


def insert_walk(walk: VitalXWalk) -> None:
    validate_walk(walk)
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
        logger.debug("Walk inserted into the database successfully")
    except Exception as e:
        logger.error("Failed to insert walk into the database: %s", e, exc_info=True)
        raise DatabaseError(f"Failed to insert walk due to: {e}")


def insert_sleep(sleep: VitalXSleep) -> None:
    validate_sleep(sleep)
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
        logger.debug("Sleep inserted into the database successfully")
    except Exception as e:
        logger.error("Failed to insert sleep into the database: %s", e, exc_info=True)
        raise DatabaseError(f"Failed to insert sleep due to: {e}")


def get_total_steps(
    file_path: Path = ANALYTICS_DBO,
    file_name: str = "get_total_step_count.sql",
    return_value: str = "total_steps",
) -> int | None:
    sql = load_sql_as_text(file_path, file_name)
    try:
        rows = fetch_result(sql)
        logger.debug("Successfully retrieved total steps")
        return int(rows[0][return_value])
    except Exception as e:
        logger.error("Failed to retrieve total steps: %s", e, exc_info=True)
        raise DatabaseError(f"Failed to retrieve total steps due to: {e}")


def get_total_sleep_time(
    file_path: Path = ANALYTICS_DBO,
    file_name: str = "get_total_sleep_time.sql",
    hours_value: str = "total_hours",
    minutes_value: str = "total_minutes",
) -> tuple[int, int]:
    sql = load_sql_as_text(file_path, file_name)
    try:
        rows = fetch_result(sql)
        total_hours = int(rows[0][hours_value])
        total_minutes = int(rows[0][minutes_value])
        total_hours += total_minutes // 60
        total_minutes = total_minutes % 60
        logger.debug("Successfully retrieved total sleep time")
        return total_hours, total_minutes
    except Exception as e:
        logger.error("Failed to get total sleep time: %s", e, exc_info=True)
        raise DatabaseError(f"Failed to get total sleep time due to: {e}")


def get_walk_history(query: str = "select * from vitalx_walk") -> list[dict[str, Any]]:
    try:
        walk_history = fetch_result(query)
        logger.debug("Successfully retrieved walk history")
        return walk_history
    except Exception as e:
        logger.error("Failed to get walk history: %s", e, exc_info=True)
        raise DatabaseError(f"Failed to get walk history due to: {e}")


def did_walk_today(walk_history: list[dict[str, Any]]) -> bool:
    for walk in walk_history:
        raw_date = walk.get("todays_date")
        if not raw_date:
            continue
        if isinstance(raw_date, datetime):
            walk_date = raw_date.date()
        elif isinstance(raw_date, str):
            walk_date = datetime.fromisoformat(raw_date).date()
        else:
            walk_date = raw_date
        if walk_date == datetime.now().date():
            logger.info("User did walk today")
            return True
    return False


def get_last_walk_date(walk_history: list[dict[str, Any]]) -> date:
    all_dates: list[date] = []
    if not walk_history:
        logger.error("Walk History dictionary is empty", exc_info=True)
        raise EmptyDictionaryError("Walk history is empty")
    for walk in walk_history:
        raw_date = walk.get("todays_date")
        if isinstance(raw_date, datetime):
            all_dates.append(raw_date.date())
        elif isinstance(raw_date, date):
            all_dates.append(raw_date)
        elif isinstance(raw_date, str):
            all_dates.append(datetime.fromisoformat(raw_date).date())
    if not all_dates:
        logger.error("The all dates list in the get last walk date function is empty")
        raise EmptyListError("No Valid dates in all dates list")
    return max(all_dates)


def get_current_streak(
    query: str = "select * from vitalx_walk_streak",
    todays_date_value: str = "todays_date",
    streak_value: str = "streak",
) -> int:
    yesterday = datetime.now().date() - timedelta(days=1)
    try:
        sql = fetch_result(query)
        logger.debug("Successfully retrieved all walk streak data")
        for x in sql:
            raw_date = x[todays_date_value]
            if isinstance(raw_date, datetime):
                val_date = raw_date.date()
            elif isinstance(raw_date, str):
                val_date = datetime.fromisoformat(raw_date).date()
            else:
                val_date = raw_date
            if val_date == yesterday:
                return int(x[streak_value])
        return 1
    except Exception as e:
        logger.error("Failed to retrieve walk streak data: %s", e, exc_info=True)
        raise DatabaseError(f"Failed to retrieve walk streak data due to: {e}")


def calculate_new_streak(
    get_current_streak: int,
) -> int:
    return get_current_streak + 1


def validate_streak(steps_walked: int, required_steps: int = 7000) -> bool:
    return steps_walked >= required_steps


def reset_streak(
    query: str = "insert into vitalx_walk_streak (streak, todays_date) values (:streak, :todays_date)",
    todays_date: datetime | None = None,
    streak: int = 1,
) -> None:
    if todays_date is None:
        todays_date = datetime.now()
    params: dict[str, Any] = {"streak": streak, "todays_date": todays_date}
    try:
        execute_query(query, params)
        logger.debug("Streak reset successfully")
    except Exception as e:
        logger.error("Failed to reset streak due to: %s", e, exc_info=True)
        raise DatabaseError(f"Failed to insert new streak due to: {e}")


def save_new_streak(
    calculate_streak: int,
    query: str = "insert into vitalx_walk_streak (streak, todays_date) values (:streak, :todays_date)",
    todays_date: datetime | None = None,
) -> None:
    if todays_date is None:
        todays_date = datetime.now()
    params: dict[str, Any] = {"streak": calculate_streak, "todays_date": todays_date}
    try:
        execute_query(query, params)
        logger.debug("Updated Streak has been entered into the database successfully")
    except Exception as e:
        logger.error(
            "Failed to save updated streak in the database: %s", e, exc_info=True
        )
        raise DatabaseError(f"Failed to insert new streak due to: {e}")


def get_latest_streak(
    query: str = "select streak from vitalx_walk_streak order by todays_date desc limit 1",
) -> int:
    try:
        rows = fetch_result(query)
        logger.debug("Successfully retrieved latest streak")
        if not rows:
            return 1
        return rows[0]["streak"]
    except Exception as e:
        logger.error("Failed to get latest streak: %s", e, exc_info=True)
        raise DatabaseError(f"Failed to retrieve latest streak due to: {e}")


def update_streak_call_point(walked_today: bool = True) -> None:
    walk_history = get_walk_history()
    if not walk_history:
        save_new_streak(1)
        return
    last_walk_date = get_last_walk_date(walk_history)
    yesterday = datetime.now().date() - timedelta(days=1)
    if walked_today == True:
        if last_walk_date == yesterday:
            current_streak = get_current_streak()
            new_streak = calculate_new_streak(current_streak)
            save_new_streak(new_streak)
    else:
        reset_streak()


def get_sleep_history(
    query: str = "select * from vitalx_sleep",
) -> list[dict[str, Any]]:
    try:
        sleep_history = fetch_result(query)
        logger.debug("Successfully retrieved sleep history")
        return sleep_history
    except Exception as e:
        logger.error("Failed to retreive sleep history: %s", e, exc_info=True)
        raise DatabaseError(f"Failed to retrieve sleep history due to: {e}")


def main() -> None:
    print(get_last_walk_date(get_walk_history()))


if __name__ == "__main__":
    main()
