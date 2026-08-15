import os
import gzip
import glob
from datetime import datetime, date
from src.vitalx.dbutils import load_sql_as_text, fetch_result
from src.vitalx.utils import ANALYTICS_DBO
from vitalx.logger import get_logger, setup_logging
from src.vitalx.exceptions import DatabaseError

setup_logging()
logger = get_logger(__name__)


BACKUP_DIR = os.path.expanduser("~/Documents/VitalX/backups")
EXPORT_QUERIES = [
    "get_all_vitalx_walk_data.sql",
    "get_all_vitalx_sleep_data.sql",
    "get_all_weather_data.sql",
    "get_all_vitalx_walk_streak_data.sql",
]


def format_sql_value(v: object) -> str:
    """Escapes single quotes and formats data types safely for SQL INSERT statements."""
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


def perform_weekly_pg_backup(retention_weeks: int = 4) -> None:
    """Creates a compressed SQL dump using existing dbutils helpers."""
    os.makedirs(BACKUP_DIR, exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    backup_path = os.path.join(BACKUP_DIR, f"vitalx_backup_{timestamp}.sql.gz")
    logger.info("Starting database backup to %s...", backup_path)
    try:
        with gzip.open(backup_path, "wt", encoding="utf-8") as gz_file:
            gz_file.write(f"-- VitalX Database Dump: {timestamp}\n\n")
            for sql_file in EXPORT_QUERIES:
                query_str = load_sql_as_text(ANALYTICS_DBO, sql_file)
                rows = fetch_result(query_str)
                table_name = sql_file.replace("get_all_", "").replace("_data.sql", "")
                gz_file.write(f"-- Table: {table_name}\n")
                for row in rows:
                    if not row:
                        continue
                    keys = ", ".join(row.keys())
                    values = ", ".join(format_sql_value(v) for v in row.values())
                    gz_file.write(f"INSERT INTO {table_name} ({keys}) VALUES ({values});\n")
                gz_file.write("\n")
        if not os.path.exists(backup_path) or os.path.getsize(backup_path) < 50:
            raise RuntimeError("Backup verification failed: File missing or empty.")
        logger.info(
            "Backup generated successfully (%d bytes).", os.path.getsize(backup_path)
        )
        cleanup_old_pg_backups(retention_weeks)
    except Exception as e:
        logger.error("Database backup failed: %s", e, exc_info=True)
        if os.path.exists(backup_path):
            os.remove(backup_path)
        raise DatabaseError(f"Database backup failed due to: {e}")


def cleanup_old_pg_backups(retention_weeks: int) -> None:
    """Purges compressed backup files older than N weeks."""
    now = datetime.now().timestamp()
    retention_sec = retention_weeks * 7 * 86400
    for file_path in glob.glob(os.path.join(BACKUP_DIR, "*.sql.gz")):
        if (now - os.path.getmtime(file_path)) > retention_sec:
            try:
                os.remove(file_path)
                logger.info("Deleted old database backup: %s", file_path)
            except Exception as e:
                logger.warning("Could not delete backup %s: %s", file_path, e)


def main() -> None:
    perform_weekly_pg_backup()


if __name__ == "__main__":
    main()