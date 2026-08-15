from typing import Any
import openmeteo_requests
import pandas as pd
import requests_cache
from retry_requests import retry
from src.vitalx.logger import get_logger, setup_logging
from src.vitalx.service import insert_weather
from src.vitalx.vitalx import Weather

setup_logging()
logger = get_logger(__name__)


def get_weather_data(
    url: str = "https://api.open-meteo.com/v1/forecast",
    latitude: float = 53.845,
    longitude: float = -1.95,
    forecast_days: int = 1,
) -> pd.DataFrame:
    cache_session = requests_cache.CachedSession(".cache", expire_after=3600)
    retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
    openmeteo = openmeteo_requests.Client(session=retry_session)  # type: ignore
    params: dict[str, Any] = {
        "latitude": latitude,
        "longitude": longitude,
        "daily": [
            "temperature_2m_min",
            "temperature_2m_max",
            "sunrise",
            "sunset",
            "daylight_duration",
            "snowfall_sum",
            "rain_sum",
        ],
        "timezone": "Europe/London",
        "forecast_days": forecast_days,
    }
    responses = openmeteo.weather_api(url, params)
    response = responses[0]
    daily = response.Daily()
    daily_temperature_2m_min = daily.Variables(0).ValuesAsNumpy()  # type: ignore
    daily_temperature_2m_max = daily.Variables(1).ValuesAsNumpy()  # type: ignore
    daily_sunrise = daily.Variables(2).ValuesInt64AsNumpy()  # type: ignore
    daily_sunset = daily.Variables(3).ValuesInt64AsNumpy()  # type: ignore
    daily_daylight_duration = daily.Variables(4).ValuesAsNumpy()  # type: ignore
    daily_snowfall_duration = daily.Variables(5).ValuesAsNumpy()  # type: ignore
    daily_rain_sum = daily.Variables(6).ValuesAsNumpy()  # type: ignore
    daily_data = {
        "date": pd.date_range(
            start=pd.to_datetime(daily.Time(), unit="s", utc=True),  # type: ignore
            end=pd.to_datetime(daily.TimeEnd(), unit="s", utc=True),  # type: ignore
            freq=pd.Timedelta(seconds=daily.Interval()),  # type: ignore
            inclusive="left",
        ).tz_convert(response.Timezone().decode())  # type: ignore
    }
    daily_data["temperature_2m_min"] = daily_temperature_2m_min  # type: ignore
    daily_data["temperature_2m_max"] = daily_temperature_2m_max  # type: ignore
    daily_data["sunrise"] = daily_sunrise  # type: ignore
    daily_data["sunset"] = daily_sunset  # type: ignore
    daily_data["daylight_duration"] = daily_daylight_duration  # type: ignore
    daily_data["snowfall_sum"] = daily_snowfall_duration  # type: ignore
    daily_data["rain_sum"] = daily_rain_sum  # type: ignore
    return pd.DataFrame(daily_data, index=None)


def write_to_db() -> None:
    df = get_weather_data()
    if df.empty:
        logger.warning("No weather data returned from API.")
        return
    row = df.iloc[0]
    todays_date = pd.to_datetime(row["date"]).to_pydatetime()
    sunrise = pd.to_datetime(row["sunrise"], unit="s", utc=True).to_pydatetime()
    sunset = pd.to_datetime(row["sunset"], unit="s", utc=True).to_pydatetime()
    weather_obj = Weather(
        todays_date=todays_date,
        temperature_2m_min=int(round(row["temperature_2m_min"])),
        temperature_2m_max=int(round(row["temperature_2m_max"])),
        sunrise=sunrise,
        sunset=sunset,
        daylight_duration=int(round(row["daylight_duration"] / 3600)),
        snowfall_sum=int(round(row["snowfall_sum"])),
        rain_sum=int(round(row["rain_sum"])),
    )
    try:
        insert_weather(weather_obj)
        logger.info("Successfully fetched and inserted weather data into DB.")
    except Exception as e:
        logger.error("Failed to insert weather into DB: %s", e, exc_info=True)


def main():
    write_to_db()


if __name__ == "__main__":
    main()
