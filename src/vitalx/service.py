from vitalx.dbutils import execute_query, load_sql_as_text, fetch_result
from vitalx.vitalx import VitalXWalk, VitalXSleep, Weather
from vitalx.validation import validate_walk, validate_sleep
from vitalx.exceptions import DatabaseError
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
                miles_walked,
                walk_location,
                todays_date
            )
            values (:steps_walked, :calories_burnt, :miles_walked, :walk_location, :todays_date)
          """
    params: dict[str, Any] = {
        "steps_walked": walk.steps_walked,
        "calories_burnt": walk.calories_burnt,
        "miles_walked": walk.miles_walked,
        "walk_location": walk.walk_location,
        "todays_date": walk.todays_date,
    }
    try:
        execute_query(sql, params)
        logger.info("Walk inserted into the database successfully")
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
        logger.info("Sleep inserted into the database successfully")
    except Exception as e:
        logger.error("Failed to insert sleep into the database: %s", e, exc_info=True)
        raise DatabaseError(f"Failed to insert sleep due to: {e}")


def insert_weather(weather: Weather) -> None:
    sql = """
            insert into weather (
                todays_date,
                temperature_2m_min,
                temperature_2m_max,
                sunrise,
                sunset,
                daylight_duration,
                snowfall_sum,
                rain_sum
            )
            values (
                :todays_date, 
                :temperature_2m_min, 
                :temperature_2m_max, 
                :sunrise, 
                :sunset, 
                :daylight_duration, 
                :snowfall_sum, 
                :rain_sum
            )
            on conflict (todays_date) do nothing;
          """
    params: dict[str, Any] = {
        "todays_date": weather.todays_date,
        "temperature_2m_min": weather.temperature_2m_min,
        "temperature_2m_max": weather.temperature_2m_max,
        "sunrise": weather.sunrise,
        "sunset": weather.sunset,
        "daylight_duration": weather.daylight_duration,
        "snowfall_sum": weather.snowfall_sum,
        "rain_sum": weather.rain_sum,
    }
    try:
        execute_query(sql, params)
        logger.info("Weather inserted into the database successfully")
    except Exception as e:
        logger.error("Failed to insert Weather into the database: %s", e, exc_info=True)
        raise DatabaseError(f"Failed to insert weather due to: {e}")


######################################################################
# Analytics
######################################################################


def get_total_steps(
    file_path: Path = ANALYTICS_DBO, file_name: str = "get_total_step_count.sql"
) -> int:
    sql = load_sql_as_text(file_path, file_name)
    try:
        rows = fetch_result(sql)
        logger.debug("Successfully retrieved total steps")
        return rows[0]["total_steps"]
    except Exception as e:
        logger.error("Failed to retrieve total steps: %s", e, exc_info=True)
        raise DatabaseError(f"Failed to retrieve total steps due to: {e}")


def get_total_sleep_time(
    file_path: Path = ANALYTICS_DBO, file_name: str = "get_total_sleep_time.sql"
) -> tuple[int, int]:
    sql = load_sql_as_text(file_path, file_name)
    try:
        rows = fetch_result(sql)
        total_hours = rows[0]["total_hours"]
        total_minutes = rows[0]["total_minutes"]
        total_hours += total_minutes // 60
        total_minutes = total_minutes % 60
        logger.debug("Successfully retrieved total sleep time")
        return total_hours, total_minutes
    except Exception as e:
        logger.error("Failed to get total sleep time: %s", e, exc_info=True)
        raise DatabaseError(f"Failed to get total sleep time due to: {e}")


def get_total_days_walked(
    file_path: Path = ANALYTICS_DBO, file_name: str = "get_total_days_walked.sql"
) -> int:
    sql = load_sql_as_text(file_path, file_name)
    try:
        rows = fetch_result(sql)
        logger.debug("Successfully returned total days walked")
        return rows[0]["total_days_walked"]
    except Exception as e:
        logger.error("Failed to get total days walked: %s", e, exc_info=True)
        raise DatabaseError(f"Failed to get total days walked due to: {e}")


def get_total_calories_burnt(
    file_path: Path = ANALYTICS_DBO, file_name: str = "get_total_calories_burnt.sql"
) -> int:
    sql = load_sql_as_text(file_path, file_name)
    try:
        rows = fetch_result(sql)
        logger.debug("Successfully returned total calories burnt")
        return rows[0]["total_calories_burnt"]
    except Exception as e:
        logger.error("Failed to get total calories burnt: %s", e, exc_info=True)
        raise DatabaseError(f"Failed to get total calories burnt due to: {e}")


def get_total_miles_walked(
    file_path: Path = ANALYTICS_DBO, file_name: str = "get_total_miles_walked.sql"
) -> str:
    sql = load_sql_as_text(file_path, file_name)
    try:
        rows = fetch_result(sql)
        logger.debug("Successfully returned total miles walked")
        return str(round(rows[0]["total_miles_walked"], 1))
    except Exception as e:
        logger.error("Failed to get total miles walked: %s", e, exc_info=True)
        raise DatabaseError(f"Failed to get total miles walked due to: {e}")


def get_favourite_walk_location(
    file_path: Path = ANALYTICS_DBO, file_name: str = "get_favourite_walk_location.sql"
) -> str:
    sql = load_sql_as_text(file_path, file_name)
    try:
        rows = fetch_result(sql)
        logger.debug("Successfully retrieved favourite walk location")
        return rows[0]["walk_location"]
    except Exception as e:
        logger.error("Failed to get favourite walk location: %s", e, exc_info=True)
        raise DatabaseError(f"Failed to get favourite walk location due to: {e}")


def get_total_days_slept(
    file_path: Path = ANALYTICS_DBO, file_name: str = "get_total_days_slept.sql"
) -> int:
    sql = load_sql_as_text(file_path, file_name)
    try:
        rows = fetch_result(sql)
        logger.debug("Successfully returned total days slept")
        return rows[0]["total_days_slept"]
    except Exception as e:
        logger.error("Failed to get total days slept: %s", e, exc_info=True)
        raise DatabaseError(f"Failed to get total days slept due to: {e}")


######################################################################
# Walk History
######################################################################


def get_walk_history(
    file_path: Path = ANALYTICS_DBO, file_name: str = "get_all_vitalx_walk_data.sql"
) -> list[dict[str, Any]]:
    sql = load_sql_as_text(file_path, file_name)
    try:
        walk_history = fetch_result(sql)
        logger.debug("Successfully retrieved walk history")
        return walk_history
    except Exception as e:
        logger.error("Failed to get walk history: %s", e, exc_info=True)
        raise DatabaseError(f"Failed to get walk history due to: {e}")


def get_last_walk_date(
    file_path: Path = ANALYTICS_DBO, file_name: str = "get_last_walk_date.sql"
) -> date:
    sql = load_sql_as_text(file_path, file_name)
    try:
        rows = fetch_result(sql)
        logger.debug("Successfully retrieved last walk date")
        raw_date = rows[0]["todays_date"]
        if isinstance(raw_date, datetime):
            return raw_date.date()
        return datetime.fromisoformat(str(raw_date)).date()
    except Exception as e:
        logger.error("Failed to get last walk date: %s", e, exc_info=True)
        raise DatabaseError(f"Failed to get last walk date due to: {e}")


def did_walk_today(
    file_path: Path = ANALYTICS_DBO, file_name: str = "get_walk_day_is_today.sql"
) -> bool:
    sql = load_sql_as_text(file_path, file_name)
    try:
        rows = fetch_result(sql)
        logger.debug("successfully confirmed that user walked today")
        return len(rows) > 0
    except Exception as e:
        logger.error("Failed to confirm if user walked today: %s", e, exc_info=True)
        raise DatabaseError(f"Failed to confirm if user walked today due to: {e}")


def did_log_walk_today(
    file_path: Path = ANALYTICS_DBO, file_name: str = "get_daily_walk_status.sql"
) -> bool:
    sql = load_sql_as_text(file_path, file_name)
    try:
        rows = fetch_result(sql)
        logger.debug("Successfully checked daily walk status")
        return len(rows) > 0
    except Exception as e:
        logger.error("Failed to check daily walk status: %s", e, exc_info=True)
        raise DatabaseError(f"Failed to check daily walk status due to: {e}")


######################################################################
# Streak System
######################################################################


def get_latest_streak_entry(
    file_path: Path = ANALYTICS_DBO, file_name: str = "get_latest_streak.sql"
) -> tuple[int, date]:
    sql = load_sql_as_text(file_path, file_name)
    try:
        rows = fetch_result(sql)
        logger.debug("Successfully retrieved latest streak")
        raw_date = rows[0]["todays_date"]
        if isinstance(raw_date, datetime):
            d = raw_date.date()
        else:
            d = datetime.fromisoformat(str(raw_date)).date()
        return rows[0]["streak"], d
    except Exception as e:
        logger.error("Failed to get latest streak due to: %s", e, exc_info=True)
        raise DatabaseError(f"Failed to get latest streak due to: {e}")


def streak_row_exists_for_today(
    file_path: Path = ANALYTICS_DBO, file_name: str = "get_streak_exists_today.sql"
) -> bool:
    sql = load_sql_as_text(file_path, file_name)
    try:
        rows = fetch_result(sql)
        logger.debug("Successfully retrieved row from the database that matches today")
        return len(rows) > 0
    except Exception as e:
        logger.error(
            "Failed to confirm if streak row exists for today due to: %s",
            e,
            exc_info=True,
        )
        raise DatabaseError(
            f"Failed to confirm if streak row exists for today due to: {e}"
        )


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
            "insert into vitalx_streak (streak, todays_date) values (:streak, :todays_date)",
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
    return entry[0]


def validate_streak(steps_walked: int, required_steps: int = 6000) -> bool:
    """Current minimum requirement for steps is 6k."""
    return steps_walked >= required_steps


######################################################################
# Sleep History
######################################################################


def get_sleep_history(
    file_path: Path = ANALYTICS_DBO, file_name: str = "get_all_vitalx_sleep_data.sql"
) -> list[dict[str, Any]]:
    sql = load_sql_as_text(file_path, file_name)
    try:
        sleep_history = fetch_result(sql)
        logger.debug("Successfully retrieved sleep history")
        return sleep_history
    except Exception as e:
        logger.error("Failed to retreive sleep history: %s", e, exc_info=True)
        raise DatabaseError(f"Failed to retrieve sleep history due to: {e}")


def did_sleep_eight_hours_last_night(
    file_path: Path = ANALYTICS_DBO, file_name: str = "get_hours_slept_per_date.sql"
) -> bool:
    sql = load_sql_as_text(file_path, file_name)
    try:
        rows = fetch_result(sql)
        logger.debug(
            "Sucessfully retrieved hours slept and todays date for latest sleep entry"
        )
        return rows[0]["hours_slept"] >= 8
    except Exception as e:
        logger.error("Failed to retrieve hours slept: %s", e, exc_info=True)
        raise DatabaseError(f"Failed to get last walk date due to: {e}")


def did_log_sleep_today(
    file_path: Path = ANALYTICS_DBO, file_name: str = "get_daily_sleep_status.sql"
) -> bool:
    sql = load_sql_as_text(file_path, file_name)
    try:
        rows = fetch_result(sql)
        logger.debug(
            "Successfully retrieved data from database to check if sleep entry has been recorded in the database today"
        )
        return len(rows) > 0
    except Exception as e:
        logger.error("Failed to check daily sleep status: %s", e, exc_info=True)
        raise DatabaseError(f"Failed to check daily sleep status due to: {e}")


def main() -> None:
    print(did_log_sleep_today())


if __name__ == "__main__":
    main()
