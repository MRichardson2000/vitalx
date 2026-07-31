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


######################################################################
# Insert Operations
######################################################################


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


######################################################################
# Analytics
######################################################################


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


######################################################################
# Walk History
######################################################################


def get_walk_history(query: str = "select * from vitalx_walk") -> list[dict[str, Any]]:
    try:
        walk_history = fetch_result(query)
        logger.debug("Successfully retrieved walk history")
        return walk_history
    except Exception as e:
        logger.error("Failed to get walk history: %s", e, exc_info=True)
        raise DatabaseError(f"Failed to get walk history due to: {e}")


def get_last_walk_date() -> date | None:
    try:
        rows = fetch_result(
            "select todays_date from vitalx_walk order by todays_date desc limit 1"
        )
        if not rows:
            return None
        logger.debug("Successfully retrieved last walk date")
        raw = rows[0]["todays_date"]
        if isinstance(raw, datetime):
            return raw.date()
        return datetime.fromisoformat(str(raw)).date()
    except Exception as e:
        logger.error("Failed to get last walk date: %s", e, exc_info=True)
        raise DatabaseError(f"Failed to get last walk date due to: {e}")


def did_walk_today() -> bool:
    today = datetime.now().date()
    try:
        rows = fetch_result(
            "select todays_date from vitalx_walk where todays_date::date = :today",
            {"today": today},
        )
        logger.debug("successfully confirmed that user walked today")
        return len(rows) > 0
    except Exception as e:
        logger.error("Failed to confirm if user walked today: %s", e, exc_info=True)
        raise DatabaseError(f"Failed to confirm if user walked today due to: {e}")


######################################################################
# Streak System
######################################################################


def get_latest_streak_entry() -> tuple[int, date] | None:
    try:
        rows = fetch_result(
            "select * from vitalx_walk_streak order by todays_date desc limit 1"
        )
        logger.debug("Successfully retrieved latest streak")
        if not rows:
            return None
        raw_date = rows[0]["todays_date"]
        if isinstance(raw_date, datetime):
            d = raw_date.date()
        else:
            d = datetime.fromisoformat(str(raw_date)).date()
        return rows[0]["streak"], d
    except Exception as e:
        logger.error("Failed to get latest streak due to: %s", e, exc_info=True)
        raise DatabaseError(f"Failed to get latest streak")


def streak_row_exists_for_today() -> bool:
    today = datetime.now().date()
    try:
        rows = fetch_result(
            "select todays_date from vitalx_walk_streak where todays_date::date = :today",
            {"today": today},
        )
        logger.debug("Successfully retrieved row from the database that matches today")
        return len(rows) > 0
    except Exception as e:
        logger.error(
            "Failed to confirm if streak row exists for today due to: %s",
            e,
            exc_info=True,
        )
        raise DatabaseError(f"Failed to confirm if streak row exists for today")


def update_streak() -> None:
    today = datetime.now().date()
    yesterday = today - timedelta(days=1)
    last_walk_date = get_last_walk_date()
    latest_streak_entry = get_latest_streak_entry()
    if last_walk_date != today:
        return
    if streak_row_exists_for_today():
        return
    if latest_streak_entry is None:
        new_streak = 1
    else:
        latest_streak_value, latest_streak_date = latest_streak_entry
        if latest_streak_date == yesterday:
            new_streak = latest_streak_value + 1
        else:
            new_streak = 1
    try:
        execute_query(
            "insert into vitalx_walk_streak (streak, todays_date) values (:streak, :todays_date)",
            {"streak": new_streak, "todays_date": datetime.now()},
        )
        logger.info("Streak updated: %d", new_streak)
    except Exception as e:
        logger.error("Failed to update streak due: %s", e, exc_info=True)
        raise DatabaseError(f"Failed to update streak due to: {e}")


def get_latest_streak() -> int:
    entry = get_latest_streak_entry()
    if entry is None:
        return 1
    streak_value, _ = entry
    return streak_value


def validate_streak(steps_walked: int, required_steps: int = 7000) -> bool:
    """Current minimum requirement for steps is 7k. This checks for this."""
    return steps_walked >= required_steps


######################################################################
# Sleep History
######################################################################


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


def did_sleep_eight_hours_last_night(
    query: str = "select hours_slept, todays_date from vitalx_sleep order by todays_date desc limit 1",
    hours: str = "hours_slept",
) -> bool | None:
    try:
        rows = fetch_result(query)
        if not rows:
            return None
        logger.debug(
            "Sucessfully retrieved hours slept and todays date for latest sleep entry"
        )
        return rows[0][hours] >= 8
    except Exception as e:
        logger.error("Failed to retrieve hours slept: %s", e, exc_info=True)
        raise DatabaseError(f"Failed to get last walk date due to: {e}")


def main() -> None:
    print(did_sleep_eight_hours_last_night())


if __name__ == "__main__":
    main()
