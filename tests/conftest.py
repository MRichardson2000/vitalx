import pytest
import logging


@pytest.fixture(autouse=True)
def configure_test_logging(caplog):  # type: ignore
    """
    I didn't want tests to clutter up my log file so I set up this
    function to capture the logs natively. This will prevent
    my prod log files from being bloated
    """
    caplog.set_level(logging.DEBUG)  # type: ignore
