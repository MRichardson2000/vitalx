from vitalx.vitalx import VitalXWalk, VitalXSleep
from vitalx.exceptions import ValidationError


def validate_walk(walk: VitalXWalk) -> None:
    """
    Validation rules:
    This is to make sure there's no null entries for clean data in the database and csv backups
    """
    if walk.steps_walked <= 0:
        raise ValidationError(
            f"Steps walked must be greater than 0 but you entered: {walk.steps_walked}"
        )
    if walk.calories_burnt <= 0:
        raise ValidationError(
            f"Calories burnt must be greater than 0 but you entered: {walk.calories_burnt}"
        )
    if walk.miles_walked <= 0.0:
        raise ValidationError(
            f"Miles walked must be greated than 0.0 but you entered: {walk.miles_walked}"
        )
    if not walk.walk_location or not walk.walk_location.strip():
        raise ValidationError("Walk location cannot be blank")


def validate_sleep(sleep: VitalXSleep) -> None:
    """
    Validation Rules
    This is mainly making sure that the value isn't 0 by mistake.
    """
    if sleep.hours_slept is None:
        raise ValidationError("Hours slept cannot be blank")

    if sleep.minutes_slept is None:
        raise ValidationError("Minutes slept cannot be blank")
