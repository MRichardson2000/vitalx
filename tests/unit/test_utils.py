"""Unit tests for vitalx.utils (path and configuration constants).

What to test:
- DBO points to the dbo directory
- CREATES_DBO points to dbo/creates
- ANALYTICS_DBO points to dbo/analytics
- PROJECT_ROOT is the project root directory
- LOG_DIR points to the logs directory
- LOG_FILE points to logs/vitalx.log
- EXPORTS_FOLDER points to the exports directory
- All paths are absolute (resolved)
- All paths use Path objects

Suggested mocks: None needed - these are path constants computed at import time.
You can assert on the path structure without mocking.
"""

from pathlib import Path
from vitalx.utils import (
    DBO,
    CREATES_DBO,
    ANALYTICS_DBO,
    PROJECT_ROOT,
    LOG_DIR,
    LOG_FILE,
    EXPORTS_FOLDER,
)


def test_dbo_is_path_to_dbo_directory():
    """
    DBO should be a Path pointing to the dbo directory.
    Hint: assert DBO.name == "dbo" and DBO.is_absolute().
    """
    pass


def test_creates_dbo_is_path_to_creates():
    """
    CREATES_DBO should point to dbo/creates.
    Hint: assert CREATES_DBO.name == "creates" and "dbo" in str(CREATES_DBO).
    """
    pass


def test_analytics_dbo_is_path_to_analytics():
    """
    ANALYTICS_DBO should point to dbo/analytics.
    Hint: assert ANALYTICS_DBO.name == "analytics".
    """
    pass


def test_project_root_is_absolute():
    """
    PROJECT_ROOT should be an absolute Path.
    Hint: assert PROJECT_ROOT.is_absolute().
    """
    pass


def test_log_dir_is_under_project_root():
    """
    LOG_DIR should be PROJECT_ROOT / "logs".
    Hint: assert LOG_DIR == PROJECT_ROOT / "logs".
    """
    pass


def test_log_file_is_vitalx_log():
    """
    LOG_FILE should be LOG_DIR / "vitalx.log".
    Hint: assert LOG_FILE.name == "vitalx.log".
    """
    pass


def test_exports_folder_is_under_project_root():
    """
    EXPORTS_FOLDER should be PROJECT_ROOT / "exports".
    Hint: assert EXPORTS_FOLDER.name == "exports".
    """
    pass


def test_all_paths_are_path_objects():
    """
    All constants in utils should be pathlib.Path instances.
    Hint: assert isinstance(DBO, Path) etc. for each constant.
    """
    pass
