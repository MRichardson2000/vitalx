import os
import gzip
import glob
from datetime import datetime, date
from src.vitalx.dbutils import load_sql_as_text, fetch_result
from src.vitalx.utils import ANALYTICS_DBO
from vitalx.logger import get_logger
from src.vitalx.exceptions import DatabaseError

###########################################################################
# This is good enough for now, This will eventually be deleted as it
# will be automated on a raspberry pi inside pg inside a docker container
# I'm risk accepting that I don't fully understand what's happening below
# but it works so for now it will do.
###########################################################################

logger = get_logger(__name__)


BACKUP_DIR = "/app/backups"
EXPORT_QUERIES = [
    "get_all_vitalx_walk_data.sql",
    "get_all_vitalx_sleep_data.sql",
    "get_all_weather_data.sql",
    "get_all_vitalx_walk_streak_data.sql",
]


def format_sql_value(v: object) -> str:
    """Escapes single quotes and formats data types safely for sql insert statements."""
    if v is None:
        return "NULL"
    if isinstance(v, bool):
        return "TRUE" if v else "FALSE"
    if isinstance(v, (int, float)):
        return str(v)
    if isinstance(v, (datetime, date)):
        return f"'{v.isoformat()}'"
    escaped_str = str(v).replace("'", "''")
    return f"'{escaped_str}'"


def perform_daily_pg_backup() -> None:
    '''Daily pg backups with 7 day retention'''
    os.makedirs(BACKUP_DIR, exist_ok=True)
    today_str = datetime.now().strftime("%Y-%m-%d")
    backup_path = os.path.join(BACKUP_DIR, f"vitalx_backup_{today_str}.sql.gz")
    logger.info("Starting daily database backup to %s...", backup_path)
    try:
        with gzip.open(backup_path, "wt", encoding="utf-8") as gz_file:
            gz_file.write(f"-- VitalX Database Dump: {today_str}\n\n")
            for sql_file in EXPORT_QUERIES:
                query_str = load_sql_as_text(ANALYTICS_DBO, sql_file)
                rows = fetch_result(query_str)
                if sql_file == "get_all_vitalx_walk_streak_data.sql":
                    table_name = "vitalx_streak"
                else:
                    table_name = sql_file.replace("get_all_", "").replace(
                        "_data.sql", ""
                    )
                gz_file.write(f"-- Table: {table_name}\n")
                for row in rows:
                    if not row:
                        continue
                    keys = ", ".join(row.keys())
                    values = ", ".join(format_sql_value(v) for v in row.values())
                    gz_file.write(
                        f"INSERT INTO {table_name} ({keys}) VALUES ({values});\n"
                    )
                gz_file.write("\n")
        if not os.path.exists(backup_path) or os.path.getsize(backup_path) < 50:
            raise RuntimeError("Backup verification failed: File missing or empty.")
        logger.info(
            "Daily backup generated successfully (%d bytes).",
            os.path.getsize(backup_path),
        )
        cleanup_old_pg_backups()
    except Exception as e:
        logger.error("Database backup failed: %s", e, exc_info=True)
        if os.path.exists(backup_path):
            os.remove(backup_path)
        raise DatabaseError(f"Database backup failed due to: {e}")


def cleanup_old_pg_backups(retention_days: int = 7) -> None:
    """Purges compressed backup files older than N days."""
    now = datetime.now().timestamp()
    retention_sec = retention_days * 86400
    for file_path in glob.glob(os.path.join(BACKUP_DIR, "*.sql.gz")):
        if (now - os.path.getmtime(file_path)) > retention_sec:
            try:
                os.remove(file_path)
                logger.info("Deleted old database backup: %s", file_path)
            except Exception as e:
                logger.warning("Could not delete backup %s: %s", file_path, e)


def main() -> None:
    perform_daily_pg_backup()


if __name__ == "__main__":
    main()
