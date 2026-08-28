from dotenv import load_dotenv
from pathlib import Path
import os
import sqlalchemy as sa
from typing import Any
from .utils import CREATES_DBO, ANALYTICS_DBO
from vitalx.logger import get_logger
from vitalx.exceptions import DatabaseError, ReadSqlAsTextError


logger = get_logger(__name__)
load_dotenv()


def get_engine() -> sa.Engine:
    """Forms the URL from details in the .env file and then creates the engine. Check the readme for the .env file format"""
    url = (
        f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
        f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
    )
    return sa.create_engine(url, echo=False, future=True)


def fetch_result(
    query: str, params: dict[str, Any] | None = None
) -> list[dict[str, Any]]:
    """
    Fetches a result from the database
    Returns a list[dict[str, Any]]
    Raises:
        DatabaseError if it fails to fetch the results
    """
    engine = get_engine()
    try:
        with engine.begin() as conn:
            result = conn.execute(sa.text(query), params or {})
            logger.debug("Successfully fetched results from the database")
            return [dict(r) for r in result.mappings()]
    except Exception as e:
        logger.error("Failed to fetch results from the database: %s", e, exc_info=True)
        raise DatabaseError(f"Failed to fetch results due to: {e}")


def execute_query(query: str, params: dict[str, Any] | None = None) -> None:
    """
    Executes a query against the database.
    Returns None, used for create, insert, update and delete operations.
    Use fetch result if you need to return a value from the database
    Raises:
        DatabaseError - For Database operations that fail
    """
    engine = get_engine()
    try:
        with engine.begin() as conn:
            conn.execute(sa.text(query), params or {})
            logger.debug("Successfully executed query against the database")
    except Exception as e:
        logger.error("Failed to execute query: %s", e, exc_info=True)
        raise DatabaseError(f"Failed to execute query due to: {e}")


def load_sql_as_text(path: Path, file_name: str) -> str:
    """
    All of my SQL query's are in my dbo folder. This function is for reading the query's in as text.
    Example use:
        sql = load_sql_as_text(ANALYTICS_DBO, "get_all_vitalx_walk_data.sql")
        print(fetch_result(sql))
    It auto defines the full path by joining the path and name together
    Then it opens the file in read mode and returns the contents as a str
    """
    try:
        full_path = str(path) + "/" + file_name
        with open(full_path, "r") as f:
            logger.debug("Successfully returned the sql query as text")
            return f.read()
    except Exception as e:
        logger.error("Failed to read the .sql file as text: %s", e, exc_info=True)
        raise ReadSqlAsTextError(f"Failed to read the .sql file as text due to: {e}")
            

def create_schemas() -> None:
    walk = load_sql_as_text(CREATES_DBO, "create_vitalx_walk_table.sql")
    sleep = load_sql_as_text(CREATES_DBO, "create_vitalx_sleep_table.sql")
    walk_streak = load_sql_as_text(CREATES_DBO, "create_vitalx_walk_streak_table.sql")
    weather = load_sql_as_text(CREATES_DBO, "create_weather_table.sql")
    print("# --- Creating Walk Table --- #")
    execute_query(walk)
    print("# --- Creating Sleep Table --- #")
    execute_query(sleep)
    print("# --- Creating Walk Streak Table --- #")
    execute_query(walk_streak)
    print("# --- Creating Weather Table --- #")
    execute_query(weather)


def view_sql_as_text() -> None:
    sql = load_sql_as_text(ANALYTICS_DBO, "get_all_vitalx_walk_data.sql")
    print(fetch_result(sql))


def main() -> None:
    create_schemas()
    # view_sql_as_text()


if __name__ == "__main__":
    main()
