import os
import glob
import pandas as pd
from src.vitalx.dbutils import get_engine
from src.vitalx.exceptions import CsvImportError
from src.vitalx.utils import EXPORTS_FOLDER
from vitalx.logger import get_logger


logger = get_logger(__name__)


TABLE_PREFIX_MAPPING = {
    "vitalx_walk": "vitalx_walk",
    "vitalx_sleep": "vitalx_sleep",
    "vitalx_weather": "vitalx_weather",
    "vitalx_streak": "vitalx_streak",
}

def import_spreadsheets_to_database() -> None:
    """Reads the latest daily CSV exports and replaces database tables with them."""
    try:
        if not os.path.exists(EXPORTS_FOLDER):
            logger.warning("Exports folder not found at %s. No CSVs to import.", EXPORTS_FOLDER)
            return
        engine = get_engine()
        for table_name, prefix in TABLE_PREFIX_MAPPING.items():
            search_pattern = os.path.join(EXPORTS_FOLDER, f"{prefix}_*.csv")
            matching_files = glob.glob(search_pattern)
            if matching_files:
                latest_file = max(matching_files, key=os.path.getmtime)
                logger.info("Found latest backup file for %s: %s", table_name, latest_file)
                df = pd.read_csv(latest_file)
                if df.empty:
                    logger.warning("CSV file %s is empty. Skipping table %s.", latest_file, table_name)
                    continue
                with engine.begin() as conn:
                    df.to_sql(table_name, conn, if_exists="replace", index=False)
                logger.info("Successfully imported %d rows into table: %s", len(df), table_name)
            else:
                logger.warning("No CSV backup files found matching prefix: %s", prefix)  
    except Exception as e:
        logger.error("Failed to import CSV backups into database: %s", e, exc_info=True)
        raise CsvImportError(f"Failed to import from CSV due to: {e}")


def main() -> None:
    import_spreadsheets_to_database()


if __name__ == "__main__":
    main()