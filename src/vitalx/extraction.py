import os
import glob
from datetime import datetime
import pandas as pd
from src.vitalx.dbutils import load_sql_as_text, fetch_result
from src.vitalx.exceptions import CsvExportError
from src.vitalx.utils import EXPORTS_FOLDER, ANALYTICS_DBO
from vitalx.logger import get_logger, setup_logging


logger = get_logger(__name__)


TABLE_SQL_MAPPING = {
    "vitalx_walk": (ANALYTICS_DBO, "get_all_vitalx_walk_data.sql"),
    "vitalx_sleep": (ANALYTICS_DBO, "get_all_vitalx_sleep_data.sql"),
    "weather": (ANALYTICS_DBO, "get_all_weather_data.sql"),
    "vitalx_streak": (ANALYTICS_DBO, "get_all_vitalx_walk_streak_data.sql"),
}

def export_tables_to_spreadsheets(max_retention_days: int = 7) -> None:
    """Exports database tables to timestamped CSV's and removes old CSV exports."""
    try:
        os.makedirs(EXPORTS_FOLDER, exist_ok=True)
        today_str = datetime.now().strftime("%Y-%m-%d")
        for prefix, (folder_path, file_name) in TABLE_SQL_MAPPING.items():
            logger.info("Reading SQL file: %s/%s", folder_path, file_name)
            query_str = load_sql_as_text(folder_path, file_name)
            rows = fetch_result(query_str)
            df = pd.DataFrame(rows)
            filename = f"{prefix}_{today_str}.csv"
            output_path = os.path.join(EXPORTS_FOLDER, filename)
            df.to_csv(output_path, index=False)
            if not os.path.exists(output_path) or os.path.getsize(output_path) == 0:
                raise CsvExportError(f"Verification failed: {filename} is missing or empty.")
            logger.info("Successfully exported %d rows to %s", len(df), output_path)
        cleanup_old_csvs(max_retention_days)
    except Exception as e:
        logger.error("Failed to export database tables: %s", e, exc_info=True)
        raise CsvExportError(f"Failed to export to CSV due to: {e}")


def cleanup_old_csvs(retention_days: int) -> None:
    """Deletes CSV files older than the specified retention period."""
    now = datetime.now().timestamp()
    retention_sec = retention_days * 86400
    csv_files = glob.glob(os.path.join(EXPORTS_FOLDER, "*.csv"))
    for file_path in csv_files:
        file_age = now - os.path.getmtime(file_path)
        if file_age > retention_sec:
            try:
                os.remove(file_path)
                logger.info("Deleted old CSV backup: %s", file_path)
            except Exception as e:
                logger.warning("Could not delete file %s: %s", file_path, e)


def main() -> None:
    export_tables_to_spreadsheets()


if __name__ == "__main__":
    main()