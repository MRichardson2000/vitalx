import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent / "src"))
from dash import Dash, dcc, html
from dash.dependencies import Input, Output, State
from src.vitalx.vitalx import VitalXWalk, VitalXSleep
from datetime import datetime
from src.vitalx.service import (
    insert_walk,
    insert_sleep,
    get_total_steps,
    get_total_sleep_time,
    get_latest_streak,
    update_streak_call_point,
    validate_streak,
    reset_streak,
)

app = Dash(__name__, prevent_initial_callbacks=False)
server = app.server


def create_layout():
    return html.Div(
        children=[
            html.H3(
                f"Hey Marcus, enter todays VitalX stats - {datetime.now().strftime('%Y-%m-%d')}"
            ),
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
        ]
    )


@app.callback(  # type: ignore[misc]
    Output("walk_input_section", "style"),
    Output("sleep_input_section", "style"),
    Output("walk_totals_section", "style"),
    Output("sleep_totals_section", "style"),
    Output("streak_section", "style"),
    Input("entry_mode", "value"),
)
def toggle_sections(mode: str | None):
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


@app.callback(  # type: ignore[misc]
    Output("total_steps_output", "children"),
    Input("entry_mode", "value"),
)
def update_total_steps(mode: str | None):
    if mode == "walk":
        return f"Total steps: {get_total_steps()}"
    return ""


@app.callback(  # type: ignore[misc]
    Output("streak_output", "children"),
    Input("entry_mode", "value"),
    Input("submit_walk", "n_clicks"),
)
def update_streak(mode: str | None, _):
    if mode == "walk":
        streak = get_latest_streak()
        return f"Current streak: {streak} day{'s' if streak != 1 else ''}🔥"
    return ""


@app.callback(  # type: ignore[misc]
    Output("total_sleep_output", "children"),
    Input("entry_mode", "value"),
)
def update_total_sleep(mode: str | None):
    if mode == "sleep":
        hours, minutes = get_total_sleep_time()
        return f"Total time slept: {hours}h {minutes}m"
    return ""


@app.callback(  # type: ignore[misc]
    Output("walk_output", "children"),
    Input("submit_walk", "n_clicks"),
    State("walk_location", "value"),
    State("walk_steps", "value"),
    State("walk_calories", "value"),
    prevent_initial_call=True,
)
def submit_walk(n: int, location: str, steps: int, calories: int):
    """n is required for dash."""
    walk = VitalXWalk(
        steps_walked=int(steps),
        calories_burnt=int(calories),
        walk_location=location,
    )
    valid = validate_streak(walk.steps_walked)
    if valid:
        update_streak_call_point()
    else:
        reset_streak()
    insert_walk(walk)
    return "Walk entry saved!"


@app.callback(  # type: ignore[misc]
    Output("sleep_output", "children"),
    Input("submit_sleep", "n_clicks"),
    State("sleep_hours", "value"),
    State("sleep_minutes", "value"),
    State("sleep_quality", "value"),
    prevent_initial_call=True,
)
def submit_sleep(n: int, hours: int, minutes: int, quality: str):
    sleep = VitalXSleep(
        hours_slept=int(hours),
        minutes_slept=int(minutes),
        good_sleep=bool(quality),
    )
    insert_sleep(sleep)
    return "Sleep entry saved!"


app.layout = create_layout()


def main():
    app.run(debug=True)  # type: ignore[misc]


if __name__ == "__main__":
    main()
