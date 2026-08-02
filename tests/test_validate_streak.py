from vitalx.service import validate_streak
from vitalx.vitalx import VitalXWalk


def test_validate_streak():
    walk = VitalXWalk(
        6800,
        300,
        "test_location",
    )
    steps = walk.steps_walked
    validation = validate_streak(steps_walked=steps)
    assert validation is False
    steps = walk.steps_walked = 7100
    validation = validate_streak(steps_walked=steps)
    assert validation is True
