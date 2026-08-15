import sys
from datetime import datetime
from pathlib import Path
sys.path.append(str(Path(__file__).parent / "src"))
import pandas as pd
from dash import Dash, dcc, html
from dash.dependencies import Input, Output, State
from api.openmeteo.weather_api import get_weather_data
from src.vitalx.service import (
    did_sleep_eight_hours_last_night,
    get_latest_streak,
    get_total_sleep_time,
    get_total_steps,
    insert_sleep,
    insert_walk,
    update_streak,
    validate_streak,
)
from src.vitalx.vitalx import VitalXSleep, VitalXWalk
from vitalx.exceptions import DatabaseError
from vitalx.logger import get_logger, setup_logging


setup_logging()
logger = get_logger(__name__)
app = Dash(__name__, prevent_initial_callbacks=False)
server = app.server


def create_layout():
    return html.Div(
        children=[
            html.H3(f"VitalX - Good Morning Mr Richardson - Have a blessed day!"),
            html.Div(
                id="walk_totals_section",
                children=[
                    html.Div(id="total_steps_output"),
                ],
                style={"display": "none", "marginBottom": "20px"},
            ),
            html.Div(
                id="streak_section",
                children=[
                    html.Div(id="streak_output"),
                ],
                style={"display": "none", "marginBottom": "20px"},
            ),
            html.Div(
                id="sleep_totals_section",
                children=[
                    html.Div(id="total_sleep_output"),
                    html.Div(id="fatigue_status"),
                ],
                style={"display": "none", "marginBottom": "20px"},
            ),
            html.Div(
                children=[
                    html.Label("Select entry type:"),
                    dcc.Dropdown(
                        id="entry_mode",
                        options=[
                            {"label": "Walk", "value": "walk"},
                            {"label": "Sleep", "value": "sleep"},
                        ],
                        placeholder="Choose what you're logging...",
                        clearable=False,
                        style={"width": "300px"},
                    ),
                ],
                style={"marginBottom": "20px"},
            ),
            html.Div(
                id="walk_input_section",
                children=[
                    html.H4("Walk Entry"),
                    dcc.Input(id="walk_location", type="text", placeholder="Location"),
                    dcc.Input(id="walk_steps", type="text", placeholder="Steps walked"),
                    dcc.Input(
                        id="walk_calories", type="text", placeholder="Calories burned"
                    ),
                    dcc.Input(
                        id="walk_miles", type="number", placeholder="Miles walked"
                    ),
                    html.Button("Submit Walk", id="submit_walk", n_clicks=0),
                    html.Div(id="walk_output", style={"marginTop": "10px"}),
                ],
                style={"display": "none"},
            ),
            html.Div(
                id="sleep_input_section",
                children=[
                    html.H4("Sleep Entry"),
                    dcc.Input(id="sleep_hours", type="text", placeholder="Hours"),
                    dcc.Input(id="sleep_minutes", type="text", placeholder="Minutes"),
                    dcc.Dropdown(
                        id="sleep_quality",
                        options=[
                            {"label": "Good Sleep", "value": True},
                            {"label": "Bad Sleep", "value": False},
                        ],
                        placeholder="Sleep quality",
                        clearable=False,
                        style={"width": "200px"},
                    ),
                    html.Button("Submit Sleep", id="submit_sleep", n_clicks=0),
                    html.Div(id="sleep_output", style={"marginTop": "10px"}),
                ],
                style={"display": "none"},
            ),
            html.Div(
                id="weather_section",
                children=[
                    html.H4("Today's Weather"),
                    html.Div(id="Weather"),
                ],
                style={
                    "marginBottom": "20px",
                    "padding": "10px",
                    "border": "1px solid #ccc",
                },
            ),
        ]
    )


@app.callback(
    Output("walk_input_section", "style"),
    Output("sleep_input_section", "style"),
    Output("walk_totals_section", "style"),
    Output("sleep_totals_section", "style"),
    Output("streak_section", "style"),
    Input("entry_mode", "value"),
)
def toggle_sections(mode: str | None):
    if mode:
        logger.debug("User Switched entry mode to: %s", mode)
    if mode == "walk":
        return (
            {"display": "block"},
            {"display": "none"},
            {"display": "block"},
            {"display": "none"},
            {"display": "block"},
        )
    if mode == "sleep":
        return (
            {"display": "none"},
            {"display": "block"},
            {"display": "none"},
            {"display": "block"},
            {"display": "none"},
        )
    return (
        {"display": "none"},
        {"display": "none"},
        {"display": "none"},
        {"display": "none"},
        {"display": "none"},
    )


@app.callback(
    Output("total_steps_output", "children"),
    Input("entry_mode", "value"),
)
def update_total_steps(mode: str | None):
    if mode == "walk":
        return f"Total steps: {get_total_steps()}"
    return ""


@app.callback(
    Output("streak_output", "children"),
    Input("entry_mode", "value"),
    Input("submit_walk", "n_clicks"),
)
def update_streak_ui(mode: str | None, _):
    if mode == "walk":
        streak = get_latest_streak()
        return f"Current streak: {streak} day{'s' if streak != 1 else ''}🔥"
    return ""


@app.callback(
    Output("total_sleep_output", "children"),
    Input("entry_mode", "value"),
)
def update_total_sleep(mode: str | None):
    if mode == "sleep":
        hours, minutes = get_total_sleep_time()
        return f"Total time slept: {hours}h {minutes}m"
    return ""


@app.callback(
    Output("walk_output", "children"),
    Input("submit_walk", "n_clicks"),
    State("walk_location", "value"),
    State("walk_steps", "value"),
    State("walk_calories", "value"),
    State("walk_miles", "value"),
    prevent_initial_call=True,
)
def submit_walk(n: int, location: str, steps: int, calories: int, miles: float):
    logger.info("Submission received for walk entry")
    walk = VitalXWalk(
        steps_walked=int(steps),
        calories_burnt=int(calories),
        miles_walked=float(miles) if miles else 0.0,
        walk_location=location,
    )
    valid = validate_streak(walk.steps_walked)
    try:
        insert_walk(walk)
        logger.info("Walk entry saved successfully for location: %s", location)
        if valid:
            update_streak()
            logger.info(
                "Walk passed the streak validation threshold (%d steps).", steps
            )
            return "Walk entry saved!"
        else:
            logger.warning(
                "Walk failed streak validation (%d steps). Triggering reset.", steps
            )
            return "Streak not updated due to failing validation"
    except Exception as e:
        logger.error("Failed to submit walk due to: %s", e)
        raise DatabaseError("Failed to submit walk entry")


@app.callback(
    Output("sleep_output", "children"),
    Input("submit_sleep", "n_clicks"),
    State("sleep_hours", "value"),
    State("sleep_minutes", "value"),
    State("sleep_quality", "value"),
    prevent_initial_call=True,
)
def submit_sleep(n: int, hours: int, minutes: int, quality: str):
    logger.info("Submission received for sleep entry.")
    sleep = VitalXSleep(
        hours_slept=int(hours),
        minutes_slept=int(minutes),
        good_sleep=bool(quality),
    )
    try:
        insert_sleep(sleep)
        logger.info(
            "Sleep entry saved successfully: %dh %dm",
            sleep.hours_slept,
            sleep.minutes_slept,
        )
        return "Sleep entry saved!"
    except Exception as e:
        logger.error("Failed to submit sleep entry: %s", e, exc_info=True)
        raise DatabaseError("Failed to save sleep entry")


@app.callback(
    Output("fatigue_status", "children"),
    Input("entry_mode", "value"),
    Input("submit_sleep", "n_clicks"),
)
def fatigue_status(mode, _) -> str:
    if mode != "sleep":
        return ""
    result = did_sleep_eight_hours_last_night()
    if result is None:
        return "No sleep data"
    if result is True:
        return "Today you are Energised! 😀"
    return "Warning! Fatigued!: 😞"


@app.callback(
    Output("Weather", "children"),
    Input("entry_mode", "value"),
)
def display_weather(mode: str | None):
    try:
        df = get_weather_data()
        if df.empty:
            return "No weather data available."
        row = df.iloc[0]
        date_str = pd.to_datetime(row["date"]).strftime("%Y-%m-%d")
        min_temp = int(round(row["temperature_2m_min"]))
        max_temp = int(round(row["temperature_2m_max"]))
        daylight_hrs = int(round(row["daylight_duration"] / 3600))
        rain_sum = int(round(row["rain_sum"]))
        snow_sum = int(round(row["snowfall_sum"]))
        sunrise_dt = pd.to_datetime(row["sunrise"], unit="s", utc=True)
        sunset_dt = pd.to_datetime(row["sunset"], unit="s", utc=True)
        items = [
            html.Li(f"Date: {date_str}"),
            html.Li(f"Temperature: Min temp - {min_temp}°C / Max Temp - {max_temp}°C"),
            html.Li(f"Sunrise: {sunrise_dt.strftime('%H:%M')} UTC"),
            html.Li(f"Sunset: {sunset_dt.strftime('%H:%M')} UTC"),
            html.Li(f"Daylight Duration: {daylight_hrs} hours"),
            html.Li(f"Rainfall: {rain_sum} mm") if rain_sum > 0 else None,
            html.Li(f"Snowfall: {snow_sum} cm") if snow_sum > 0 else None,
        ]
        return html.Ul(children=[item for item in items if item is not None])
    except Exception as e:
        logger.error("Failed to retrieve weather data: %s", e, exc_info=True)
        return f"Could not load weather data: {e}"


app.layout = create_layout()


def main():
    logger.info("Initialising VitalX Dash Application Server on localhost:8050")
    app.run(debug=True)


if __name__ == "__main__":
    main()
