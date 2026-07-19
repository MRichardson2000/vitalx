from datetime import datetime


class VitalXWalk:
    def __init__(
        self,
        steps_walked: int,
        calories_burnt: int,
        walk_location: str | None = None,
        todays_date: datetime = datetime.now(),
    ) -> None:
        self.steps_walked = steps_walked
        self.calories_burnt = calories_burnt
        self.walk_location = walk_location
        self.todays_date = todays_date


class VitalXSleep:
    def __init__(
        self,
        hours_slept: int,
        minutes_slept: int,
        good_sleep: bool,
        todays_date: datetime = datetime.now(),
    ) -> None:
        self.hours_slept = hours_slept
        self.minutes_slept = minutes_slept
        self.good_sleep = good_sleep
        self.todays_date = todays_date
