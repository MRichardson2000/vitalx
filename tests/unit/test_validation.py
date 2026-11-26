"""Unit tests for vitalx.validation (validate_walk, validate_sleep).

What to test:
- validate_walk raises ValidationError when steps_walked <= 0
- validate_walk raises ValidationError when calories_burnt <= 0
- validate_walk raises ValidationError when miles_walked <= 0.0
- validate_walk raises ValidationError when walk_location is blank/whitespace/None
- validate_walk passes (returns None) for valid walk data
- validate_sleep raises ValidationError when hours_slept is None
- validate_sleep raises ValidationError when minutes_slept is None
- validate_sleep passes (returns None) for valid sleep data

Suggested mocks: None needed - validation functions are pure.
Use pytest.raises(ValidationError) to test error cases.
"""

from datetime import datetime
import pytest
from vitalx.validation import validate_walk, validate_sleep
from vitalx.vitalx import VitalXWalk, VitalXSleep
from vitalx.exceptions import ValidationError


def test_validate_walk_positive_values_passes(sample_walk):
    """
    A walk with all positive values and a non-blank location should not raise.
    Hint: use the sample_walk fixture.
    """
    pass


def test_validate_walk_zero_steps_raises():
    """
    steps_walked = 0 should raise ValidationError.
    Hint: construct VitalXWalk(steps_walked=0, ...) and assert pytest.raises.
    """
    pass


def test_validate_walk_negative_steps_raises():
    """
    steps_walked < 0 should raise ValidationError.
    """
    pass


def test_validate_walk_zero_calories_raises():
    """
    calories_burnt = 0 should raise ValidationError.
    """
    pass


def test_validate_walk_zero_miles_raises():
    """
    miles_walked = 0.0 should raise ValidationError.
    """
    pass


def test_validate_walk_blank_location_raises():
    """
    walk_location = "" or "   " should raise ValidationError.
    Test both empty string and whitespace-only string.
    """
    pass


def test_validate_walk_none_location_raises():
    """
    walk_location = None should raise ValidationError.
    """
    pass


def test_validate_sleep_valid_passes(sample_sleep):
    """
    A sleep record with non-None hours and minutes should not raise.
    Hint: use the sample_sleep fixture.
    """
    pass


def test_validate_sleep_none_hours_raises():
    """
    hours_slept = None should raise ValidationError.
    """
    pass


def test_validate_sleep_none_minutes_raises():
    """
    minutes_slept = None should raise ValidationError.
    """
    pass


def test_validate_sleep_zero_hours_passes():
    """
    hours_slept = 0 should NOT raise (validation only checks for None, not zero).
    This documents current behaviour - zero hours is allowed by validation.
    """
    pass
