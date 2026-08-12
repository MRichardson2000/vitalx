from typing import Any
import openmeteo_requests
import pandas as pd
import requests_cache
from retry_requests import retry


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
    print(f"Coordinates: {response.Latitude()}°N {response.Longitude()}°E")
    print(f"Elevation: {response.Elevation()} m asl")
    print(f"Timezone: {response.Timezone()}{response.TimezoneAbbreviation()}")
    print(f"Timezone difference to GMT+0: {response.UtcOffsetSeconds()}s")
    daily = response.Daily()
    daily_temperature_2m_min = daily.Variables(0).ValuesAsNumpy()  # type: ignore
    daily_temperature_2m_max = daily.Variables(1).ValuesAsNumpy()  # type: ignore
    daily_sunrise = daily.Variables(2).ValuesAsNumpy()  # type: ignore
    daily_sunset = daily.Variables(3).ValuesAsNumpy()  # type: ignore
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
    daily_dataframe = pd.DataFrame(daily_data, index=None)
    return daily_dataframe


def clean_data() -> str:
    df = get_weather_data()
    df["date"] = df["date"].dt.strftime("%Y-%m-%d")
    df["temperature_2m_min"] = df["temperature_2m_min"].round().astype(int)
    df["temperature_2m_max"] = df["temperature_2m_max"].round().astype(int)
    df["daylight_duration"] = df["daylight_duration"] / 3600
    df["daylight_duration"] = df["daylight_duration"].round().astype(int)
    df["snowfall_sum"] = df["snowfall_sum"].round().astype(int)
    df["rain_sum"] = df["rain_sum"].round().astype(int)
    return df.to_string(index=False)


def main():
    print(clean_data())


if __name__ == "__main__":
    main()
