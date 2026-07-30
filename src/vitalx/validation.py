from vitalx.vitalx import VitalXWalk, VitalXSleep
from vitalx.exceptions import ValidationError


def validate_walk(walk: VitalXWalk) -> None:
    if walk.steps_walked <= 0:
        raise ValidationError(
            f"Steps walked must be greater than 0 but you entered: {walk.steps_walked}"
        )
    if walk.calories_burnt <= 0:
        raise ValidationError(
            f"Calories burnt must be greater than 0 but you entered: {walk.calories_burnt}"
        )
    if not walk.walk_location or not walk.walk_location.strip():
        raise ValidationError("Walk location cannot be blank")


def validate_sleep(sleep: VitalXSleep) -> None:
    if sleep.hours_slept is None:
        raise ValidationError("Hours slept cannot be blank")

    if sleep.minutes_slept is None:
        raise ValidationError("Minutes slept cannot be blank")
