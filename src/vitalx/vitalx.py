from datetime import datetime
from dataclasses import dataclass, field


@dataclass
class VitalXWalk:
    steps_walked: int
    calories_burnt: int
    miles_walked: float
    walk_location: str | None = None
    todays_date: datetime = field(default_factory=datetime.now)


@dataclass
class VitalXSleep:
    hours_slept: int
    minutes_slept: int
    good_sleep: bool
    todays_date: datetime = field(default_factory=datetime.now)


@dataclass
class Weather:
    temperature_2m_min: int
    temperature_2m_max: int
    sunrise: datetime
    sunset: datetime
    daylight_duration: int
    snowfall_sum: int
    rain_sum: int
    todays_date: datetime
    id: int | None = None
