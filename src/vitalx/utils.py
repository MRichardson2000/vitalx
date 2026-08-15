from pathlib import Path

DBO = (Path(__file__).parent.parent.parent / "dbo").resolve()
CREATES_DBO = DBO / "creates"
ANALYTICS_DBO = DBO / "analytics"
PROJECT_ROOT = (Path(__file__).parent.parent.parent).resolve()
LOG_DIR = PROJECT_ROOT / "logs"
LOG_FILE = LOG_DIR / "vitalx.log"
EXPORTS_FOLDER = PROJECT_ROOT / "exports"
