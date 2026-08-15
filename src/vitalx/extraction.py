import os
import pandas as pd
from src.vitalx.dbutils import load_sql_as_text, fetch_result
from src.vitalx.exceptions import CsvExportError
from src.vitalx.utils import EXPORTS_FOLDER, ANALYTICS_DBO
from vitalx.logger import get_logger


logger = get_logger(__name__)


TABLE_SQL_MAPPING = {
    "vitalx_walk.csv": (ANALYTICS_DBO, "get_all_vitalx_walk_data.sql"),
    "vitalx_sleep.csv": (ANALYTICS_DBO, "get_all_vitalx_sleep_data.sql"),
    "vitalx_weather.csv": (ANALYTICS_DBO, "get_all_weather_data.sql"),
    "vitalx_streak.csv": (ANALYTICS_DBO, "get_all_vitalx_walk_streak_data.sql"),
}


def export_tables_to_spreadsheets() -> None:
    try:
        for excel_filename, (folder_path, file_name) in TABLE_SQL_MAPPING.items():
            logger.info("Reading SQL file: %s/%s", folder_path, file_name)
            query_str = load_sql_as_text(folder_path, file_name)
            rows = fetch_result(query_str)
            df = pd.DataFrame(rows)
            output_path = os.path.join(EXPORTS_FOLDER, excel_filename)
            df.to_csv(output_path, index=False)
            logger.info("Successfully exported %d rows to %s", len(df), output_path)
    except Exception as e:
        logger.error("Failed to export database tables: %s", e, exc_info=True)
        raise CsvExportError(f"Failed to export to csv due to {e}")


def main() -> None:
    export_tables_to_spreadsheets()


if __name__ == "__main__":
    main()
