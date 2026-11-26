"""Sample test data for VitalX tests.

Import these in your test files to keep test data consistent across the suite.
"""

from datetime import datetime, date
from vitalx.vitalx import VitalXWalk, VitalXSleep, Weather


# --- Valid sample domain objects ---

SAMPLE_WALK = VitalXWalk(
    steps_walked=7500,
    calories_burnt=350,
    miles_walked=4.2,
    walk_location="Central Park",
    todays_date=datetime(2026, 11, 20, 18, 0, 0),
)

SAMPLE_WALK_LOW_STEPS = VitalXWalk(
    steps_walked=100,
    calories_burnt=10,
    miles_walked=0.1,
    walk_location="Back Garden",
    todays_date=datetime(2026, 11, 20, 18, 0, 0),
)

SAMPLE_SLEEP = VitalXSleep(
    hours_slept=8,
    minutes_slept=0,
    good_sleep=True,
    todays_date=datetime(2026, 11, 20, 7, 0, 0),
)

SAMPLE_SLEEP_BAD = VitalXSleep(
    hours_slept=5,
    minutes_slept=30,
    good_sleep=False,
    todays_date=datetime(2026, 11, 20, 7, 0, 0),
)

SAMPLE_WEATHER = Weather(
    temperature_2m_min=10,
    temperature_2m_max=17,
    sunrise=datetime(2026, 11, 20, 4, 57, 0),
    sunset=datetime(2026, 11, 20, 19, 34, 0),
    daylight_duration=13,
    snowfall_sum=0,
    rain_sum=4,
    todays_date=datetime(2026, 11, 20),
)


# --- Sample database rows (as returned by fetch_result) ---

SAMPLE_WALK_ROWS = [
    {
        "steps_walked": 7500,
        "calories_burnt": 350,
        "miles_walked": 4.2,
        "walk_location": "Central Park",
        "todays_date": datetime(2026, 11, 20, 18, 0, 0),
    },
    {
        "steps_walked": 6200,
        "calories_burnt": 290,
        "miles_walked": 3.8,
        "walk_location": "High Street",
        "todays_date": datetime(2026, 11, 19, 18, 0, 0),
    },
]

SAMPLE_SLEEP_ROWS = [
    {
        "hours_slept": 8,
        "minutes_slept": 0,
        "good_sleep": True,
        "todays_date": datetime(2026, 11, 20, 7, 0, 0),
    },
    {
        "hours_slept": 6,
        "minutes_slept": 30,
        "good_sleep": False,
        "todays_date": datetime(2026, 11, 19, 7, 0, 0),
    },
]

SAMPLE_STREAK_ROWS = [
    {"streak": 5, "todays_date": date(2026, 11, 19)},
]

SAMPLE_WEATHER_ROWS = [
    {
        "todays_date": datetime(2026, 11, 20),
        "temperature_2m_min": 10,
        "temperature_2m_max": 17,
        "sunrise": datetime(2026, 11, 20, 4, 57, 0),
        "sunset": datetime(2026, 11, 20, 19, 34, 0),
        "daylight_duration": 13,
        "snowfall_sum": 0,
        "rain_sum": 4,
    },
]


# --- Expected analytics results ---

EXPECTED_TOTAL_STEPS = 13700
EXPECTED_TOTAL_SLEEP = (14, 30)  # (hours, minutes)
EXPECTED_TOTAL_CALORIES = 640
EXPECTED_TOTAL_MILES = "8.0"
EXPECTED_TOTAL_DAYS = 2
