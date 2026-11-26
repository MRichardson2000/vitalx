"""Unit tests for vitalx.vitalx dataclasses (VitalXWalk, VitalXSleep, Weather).

What to test:
- Default values are applied correctly (todays_date defaults to now, id defaults to None)
- All fields can be set via constructor
- Field types are correct (int, float, str, bool, datetime)
- Dataclass equality works as expected
- Creating instances with missing required fields raises TypeError

Suggested mocks: None needed - these are pure dataclasses.
"""

from datetime import datetime
from vitalx.vitalx import VitalXWalk, VitalXSleep, Weather


def test_vitalx_walk_default_todays_date_is_now():
    """
    When todays_date is not provided, it should default to the current datetime.
    Hint: create a VitalXWalk without todays_date and assert it's close to now.
    """
    pass


def test_vitalx_walk_all_fields_set_correctly():
    """
    All fields should be set exactly as passed to the constructor.
    Hint: use tests.fixtures.sample_data.SAMPLE_WALK or construct your own.
    """
    pass


def test_vitalx_walk_walk_location_defaults_to_none():
    """
    walk_location is Optional[str] and should default to None when not provided.
    """
    pass


def test_vitalx_sleep_default_todays_date_is_now():
    """
    When todays_date is not provided, it should default to the current datetime.
    """
    pass


def test_vitalx_sleep_all_fields_set_correctly():
    """
    All fields should be set exactly as passed to the constructor.
    Hint: good_sleep is a bool, hours/minutes are ints.
    """
    pass


def test_weather_all_fields_set_correctly():
    """
    All Weather fields should be set correctly including the optional id field.
    Hint: Weather has no default for todays_date - it's required.
    """
    pass


def test_weather_id_defaults_to_none():
    """
    Weather.id is Optional[int] and should default to None when not provided.
    """
    pass


def test_dataclasses_are_immutable_by_default():
    """
    Dataclasses are mutable by default unless frozen=True. Test that you CAN
    modify fields after creation (documenting current behaviour).
    """
    pass


def test_vitalx_walk_equality():
    """
    Two dataclass instances with the same field values should be equal.
    """
    pass


def test_vitalx_walk_inequality():
    """
    Two dataclass instances with different field values should not be equal.
    """
    pass
