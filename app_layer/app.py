"""VitalX Gothic Dashboard — front-end application layer.

Builds the Dash layout and wires up callbacks for walk/sleep entry forms,
chart rendering, weather/Skyrim widgets, and history display. Communicates
with the backend service layer via read-only API calls; does not modify
database or service code.
"""

from pathlib import Path
import sys

sys.path.insert(
    0, str(Path(__file__).parent.parent)
)  # project root: makes api, skyrim importable
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))  # src/vitalx

import pandas as pd
from datetime import datetime, timedelta
from dash import Dash, dcc, html, Input, Output, State, callback_context
import plotly.graph_objects as go

from api.openmeteo.weather_api import get_weather_data
from src.vitalx.pg_backup import perform_daily_pg_backup
from src.vitalx.extraction import export_tables_to_spreadsheets
from src.vitalx.service import (
    did_sleep_eight_hours_last_night,
    get_latest_streak,
    get_total_sleep_time,
    get_total_steps,
    get_total_miles_walked,
    insert_sleep,
    insert_walk,
    update_streak,
    validate_streak,
    did_log_walk_today,
    did_log_sleep_today,
    get_walk_history,
    get_sleep_history,
    get_todays_steps,
    get_total_days,
    get_total_calories_burnt,
)
from src.vitalx.vitalx import VitalXSleep, VitalXWalk
from src.vitalx.exceptions import DatabaseError
from src.vitalx.logger import get_logger, setup_logging
from src.vitalx.quotes import get_random_quote
from skyrim.skyrim import skyrim_journey
from src.vitalx.validation import validate_walk, validate_sleep


setup_logging()
logger = get_logger(__name__)
app = Dash(__name__, prevent_initial_callbacks=False, suppress_callback_exceptions=True)
server = app.server


# Gothic colour palette
CRIMSON = "#B22222"
CRIMSON_GLOW = "#FF4D4D"
DARK_RED = "#8B0000"
OBSIDIAN = "#0A0A0A"
CHARCOAL = "#141414"
OFF_WHITE = "#F0E6E6"
MUTED = "#8A6D6D"
SUCCESS_GREEN = "#2D5A27"
WARNING_AMBER = "#B8860B"
ERROR_RED = "#FF4444"


# ──────────────────────────────────────────────────────────────
# Chart data helpers (read-only; compute from service layer)
# ──────────────────────────────────────────────────────────────
def _walk_history_df():
    """Load walk history into a DataFrame indexed by date.

    Returns an empty DataFrame with the expected columns when no rows exist.
    """
    rows = get_walk_history()
    if not rows:
        return pd.DataFrame(columns=["todays_date", "steps_walked", "walk_location"])
    df = pd.DataFrame(rows)
    df["todays_date"] = pd.to_datetime(df["todays_date"]).dt.date
    return df


def _sleep_history_df():
    """Load sleep history into a DataFrame indexed by date.

    Returns an empty DataFrame with the expected columns when no rows exist.
    """
    rows = get_sleep_history()
    if not rows:
        return pd.DataFrame(columns=["todays_date", "hours_slept", "good_sleep"])
    df = pd.DataFrame(rows)
    df["todays_date"] = pd.to_datetime(df["todays_date"]).dt.date
    return df


def weekly_steps_chart():
    """Build a 7-day steps line chart from walk history."""
    df = _walk_history_df()
    fig = go.Figure()
    if df.empty:
        fig.update_layout(
            title="No walk data yet",
            paper_bgcolor=CHARCOAL,
            plot_bgcolor=CHARCOAL,
            font_color=OFF_WHITE,
        )
        return fig

    today = datetime.now().date()
    start = today - timedelta(days=6)
    date_range = [d.date() for d in pd.date_range(start, today, freq="D")]
    daily = (
        df.groupby("todays_date")["steps_walked"]
        .sum()
        .reindex(date_range, fill_value=0)
    )

    fig.add_trace(
        go.Scatter(
            x=[str(d) for d in daily.index],
            y=daily.values,
            mode="lines+markers",
            line=dict(color=CRIMSON, width=3),
            marker=dict(size=8, color=CRIMSON_GLOW, line=dict(width=2, color=OBSIDIAN)),
            fill="tozeroy",
            fillcolor="rgba(178, 34, 34, 0.15)",
        )
    )
    fig.update_layout(
        title="Steps — Last 7 Days",
        xaxis_title="Date",
        yaxis_title="Steps",
        paper_bgcolor=CHARCOAL,
        plot_bgcolor=CHARCOAL,
        font_color=OFF_WHITE,
        xaxis=dict(gridcolor=DARK_RED, tickangle=45),
        yaxis=dict(gridcolor=DARK_RED),
        margin=dict(t=60, b=60, l=60, r=40),
        height=320,
    )
    return fig


def monthly_sleep_chart():
    """Build a 30-day average sleep-hours bar chart from sleep history."""
    df = _sleep_history_df()
    fig = go.Figure()
    if df.empty:
        fig.update_layout(
            title="No sleep data yet",
            paper_bgcolor=CHARCOAL,
            plot_bgcolor=CHARCOAL,
            font_color=OFF_WHITE,
        )
        return fig

    today = datetime.now().date()
    start = today - timedelta(days=29)
    date_range = [d.date() for d in pd.date_range(start, today, freq="D")]
    daily = (
        df.assign(hours=df["hours_slept"] + df.get("minutes_slept", 0) / 60)
        .groupby("todays_date")["hours"]
        .mean()
        .reindex(date_range, fill_value=0)
    )

    colors = [SUCCESS_GREEN if v >= 8 else CRIMSON for v in daily.values]
    fig.add_trace(
        go.Bar(
            x=[str(d) for d in daily.index],
            y=daily.values,
            marker_color=colors,
            marker_line=dict(width=1, color=OBSIDIAN),
        )
    )
    fig.update_layout(
        title="Avg Sleep — Last 30 Days",
        xaxis_title="Date",
        yaxis_title="Hours",
        paper_bgcolor=CHARCOAL,
        plot_bgcolor=CHARCOAL,
        font_color=OFF_WHITE,
        xaxis=dict(gridcolor=DARK_RED, tickangle=45),
        yaxis=dict(gridcolor=DARK_RED, range=[0, max(12, daily.max() * 1.2)]),
        margin=dict(t=60, b=60, l=60, r=40),
        height=320,
    )
    return fig


def sleep_quality_pie():
    """Build an all-time good vs bad sleep pie chart."""
    df = _sleep_history_df()
    fig = go.Figure()
    if df.empty:
        fig.update_layout(
            title="No sleep data yet",
            paper_bgcolor=CHARCOAL,
            plot_bgcolor=CHARCOAL,
            font_color=OFF_WHITE,
        )
        return fig

    good = int(df["good_sleep"].sum()) if "good_sleep" in df.columns else 0
    bad = len(df) - good

    fig.add_trace(
        go.Pie(
            labels=["Good Sleep", "Bad Sleep"],
            values=[good, bad],
            marker=dict(
                colors=[SUCCESS_GREEN, CRIMSON], line=dict(color=OBSIDIAN, width=2)
            ),
            hole=0.4,
            textinfo="label+percent",
            textfont=dict(color=OFF_WHITE, size=12),
        )
    )
    fig.update_layout(
        title="Sleep Quality — All Time",
        paper_bgcolor=CHARCOAL,
        plot_bgcolor=CHARCOAL,
        font_color=OFF_WHITE,
        margin=dict(t=60, b=40, l=40, r=40),
        height=320,
        showlegend=True,
        legend=dict(font=dict(color=OFF_WHITE), bgcolor=CHARCOAL, bordercolor=DARK_RED),
    )
    return fig


def location_pie():
    """Build a favourite walk locations pie chart (top 5 locations excluding work)."""
    df = _walk_history_df()
    fig = go.Figure()
    if df.empty or "walk_location" not in df.columns:
        fig.update_layout(
            title="No walk locations yet",
            paper_bgcolor=CHARCOAL,
            plot_bgcolor=CHARCOAL,
            font_color=OFF_WHITE,
        )
        return fig
    df = df.loc[(df.walk_location != "Work")]
    loc_counts = df["walk_location"].value_counts().head(5)
    fig.add_trace(
        go.Pie(
            labels=loc_counts.index.tolist(),
            values=loc_counts.values.tolist(),
            marker=dict(
                colors=[
                    CRIMSON,
                    DARK_RED,
                    CRIMSON_GLOW,
                    "#5A1111",
                    "#8B0000",
                    "#4A0000",
                ],
                line=dict(color=OBSIDIAN, width=2),
            ),
            hole=0.4,
            textinfo="label+percent",
            textfont=dict(color=OFF_WHITE, size=11),
        )
    )
    fig.update_layout(
        title="Favourite Walk Locations - Excluding Work 😁",
        paper_bgcolor=CHARCOAL,
        plot_bgcolor=CHARCOAL,
        font_color=OFF_WHITE,
        margin=dict(t=60, b=40, l=40, r=40),
        height=320,
        showlegend=True,
        legend=dict(font=dict(color=OFF_WHITE), bgcolor=CHARCOAL, bordercolor=DARK_RED),
    )
    return fig


def stat_card(icon, label, value, value_class="", card_class=""):
    """Build a stat card component showing an icon, label, and value."""
    cls = f"stat-card {card_class}".strip()
    val_cls = f"stat-value {value_class}".strip()
    return html.Div(
        className=cls,
        children=[
            html.Div(icon, className="stat-icon"),
            html.Div(label, className="stat-label"),
            html.Div(value, className=val_cls),
        ],
    )


def status_card(title, badge_text, badge_class, detail_text, detail_class=""):
    """Build a status card component with a title, badge, and detail text."""
    return html.Div(
        className=f"status-card {badge_class}",
        children=[
            html.Div(title, className="stat-label"),
            html.Span(badge_text, className=f"status-badge {badge_class}"),
            html.Div(detail_text, className=f"stat-value {detail_class}"),
        ],
    )


# Layout
def create_layout():
    """Assemble the full VitalX dashboard layout."""
    return html.Div(
        className="container",
        children=[
            # Header
            html.Div(
                className="header",
                children=[
                    html.Div(
                        className="header-inner",
                        children=[
                            html.Div(
                                className="header-top",
                                children=[
                                    html.Div(
                                        className="app-title",
                                        children=[
                                            html.Span("VITALX"),
                                            html.Span(className="crimson-dot"),
                                        ],
                                    ),
                                    html.Div(id="current-date", className="date-badge"),
                                ],
                            ),
                            html.Div(
                                id="daily-quote",
                                className="quote",
                                children=f'"{get_random_quote()}"',
                            ),
                        ],
                    ),
                ],
            ),
            # Main content
            html.Main(
                children=[
                    # Stat Cards
                    html.Div(
                        id="stat-grid",
                        className="stat-grid",
                    ),
                    # Today Status
                    html.Div(
                        id="status-grid",
                        className="status-grid",
                    ),
                    # Entry Forms
                    html.Div(
                        className="entry-grid",
                        children=[
                            html.Div(
                                className="form-card",
                                children=[
                                    html.Div(
                                        className="form-header",
                                        children=[
                                            html.Div(
                                                "Walk Entry", className="form-title"
                                            ),
                                        ],
                                    ),
                                    html.Div(
                                        className="form-group",
                                        children=[
                                            html.Label("Location"),
                                            dcc.Input(
                                                id="walk-location",
                                                type="text",
                                                placeholder="Where did you walk?",
                                            ),
                                            html.Div(
                                                id="walk-location-error",
                                                className="error-text",
                                            ),
                                        ],
                                    ),
                                    html.Div(
                                        className="form-group",
                                        children=[
                                            html.Label("Steps"),
                                            dcc.Input(
                                                id="walk-steps",
                                                type="number",
                                                placeholder="e.g. 7500",
                                                min=0,
                                                step=1,
                                            ),
                                            html.Div(
                                                id="walk-steps-error",
                                                className="error-text",
                                            ),
                                        ],
                                    ),
                                    html.Div(
                                        className="form-group",
                                        children=[
                                            html.Label("Calories"),
                                            dcc.Input(
                                                id="walk-calories",
                                                type="number",
                                                placeholder="e.g. 300",
                                                min=0,
                                                step=1,
                                            ),
                                            html.Div(
                                                id="walk-calories-error",
                                                className="error-text",
                                            ),
                                        ],
                                    ),
                                    html.Div(
                                        className="form-group",
                                        children=[
                                            html.Label("Miles"),
                                            dcc.Input(
                                                id="walk-miles",
                                                type="number",
                                                placeholder="e.g. 4.2",
                                                min=0,
                                                step=0.1,
                                            ),
                                            html.Div(
                                                id="walk-miles-error",
                                                className="error-text",
                                            ),
                                        ],
                                    ),
                                    html.Button(
                                        "Submit Walk",
                                        id="submit-walk",
                                        n_clicks=0,
                                        className="submit-btn",
                                    ),
                                    html.Div(
                                        id="walk-output", className="output-message"
                                    ),
                                ],
                            ),
                            html.Div(
                                className="form-card",
                                children=[
                                    html.Div(
                                        className="form-header",
                                        children=[
                                            html.Div(
                                                "Sleep Entry", className="form-title"
                                            ),
                                        ],
                                    ),
                                    html.Div(
                                        className="form-group",
                                        children=[
                                            html.Label("Hours"),
                                            dcc.Input(
                                                id="sleep-hours",
                                                type="number",
                                                placeholder="e.g. 7",
                                                min=0,
                                                step=1,
                                            ),
                                            html.Div(
                                                id="sleep-hours-error",
                                                className="error-text",
                                            ),
                                        ],
                                    ),
                                    html.Div(
                                        className="form-group",
                                        children=[
                                            html.Label("Minutes"),
                                            dcc.Input(
                                                id="sleep-minutes",
                                                type="number",
                                                placeholder="e.g. 30",
                                                min=0,
                                                step=1,
                                            ),
                                            html.Div(
                                                id="sleep-minutes-error",
                                                className="error-text",
                                            ),
                                        ],
                                    ),
                                    html.Div(
                                        className="form-group quality-toggle",
                                        children=[
                                            html.Button(
                                                "Good Sleep",
                                                id="sleep-quality-good",
                                                n_clicks=0,
                                                className="quality-btn active",
                                            ),
                                            html.Button(
                                                "Bad Sleep",
                                                id="sleep-quality-bad",
                                                n_clicks=0,
                                                className="quality-btn",
                                            ),
                                            dcc.Store(
                                                id="sleep-quality-store", data=True
                                            ),
                                        ],
                                    ),
                                    html.Button(
                                        "Submit Sleep",
                                        id="submit-sleep",
                                        n_clicks=0,
                                        className="submit-btn",
                                    ),
                                    html.Div(
                                        id="sleep-output", className="output-message"
                                    ),
                                ],
                            ),
                        ],
                    ),
                    # Widgets
                    html.Div(
                        className="widget-grid",
                        children=[
                            html.Div(
                                className="widget-card",
                                children=[
                                    html.Div(
                                        "Today's Weather", className="widget-title"
                                    ),
                                    html.Div(
                                        id="weather-display",
                                        children="Loading weather...",
                                    ),
                                ],
                            ),
                            html.Div(
                                className="widget-card",
                                children=[
                                    html.Div(
                                        "The Dragonborn's Journey",
                                        className="widget-title",
                                    ),
                                    html.Div(
                                        id="skyrim-display",
                                        children="Loading journey...",
                                    ),
                                ],
                            ),
                        ],
                    ),
                    # Analytics
                    html.Div(
                        className="analytics-section",
                        children=[
                            html.Div(
                                className="section-header",
                                children=[
                                    html.H2("Analytics"),
                                    html.Div(id="last-updated", className="text-muted"),
                                ],
                            ),
                            html.Div(
                                className="chart-grid",
                                children=[
                                    html.Div(
                                        className="chart-card",
                                        children=[dcc.Graph(id="weekly-steps-chart")],
                                    ),
                                    html.Div(
                                        className="chart-card",
                                        children=[dcc.Graph(id="monthly-sleep-chart")],
                                    ),
                                    html.Div(
                                        className="chart-card",
                                        children=[dcc.Graph(id="sleep-quality-pie")],
                                    ),
                                    html.Div(
                                        className="chart-card",
                                        children=[dcc.Graph(id="location-pie")],
                                    ),
                                ],
                            ),
                        ],
                    ),
                    # History
                    html.Div(
                        className="history-card",
                        children=[
                            html.H2("Recent Entries"),
                            html.Div(id="history-table"),
                        ],
                    ),
                    # Toast container
                    html.Div(id="toast-container", className="toast-container"),
                    # Auto-refresh interval - I don't want it to be 30 seconds at the moment. when I want to put it back change it to 30000
                    dcc.Interval(
                        id="refresh-interval", interval=300000000, n_intervals=0
                    ),
                ],
            ),
        ],
    )


app.layout = create_layout()


# Callbacks
@app.callback(
    Output("current-date", "children"),
    Input("refresh-interval", "n_intervals"),
)
def update_date(_):
    return datetime.now().strftime("%A, %d %B %Y")


@app.callback(
    Output("daily-quote", "children"),
    Input("refresh-interval", "n_intervals"),
)
def update_quote(_):
    return f'"{get_random_quote()}"'


@app.callback(
    [
        Output("stat-grid", "children"),
        Output("status-grid", "children"),
        Output("walk-output", "children", allow_duplicate=True),
        Output("sleep-output", "children", allow_duplicate=True),
        Output("walk-output", "className", allow_duplicate=True),
        Output("sleep-output", "className", allow_duplicate=True),
    ],
    Input("refresh-interval", "n_intervals"),
    prevent_initial_call=True,
)
def refresh_stats(_):
    """Refresh stat cards, status badges, and clear submission messages.

    Runs on the 30-second refresh interval. Fetches aggregated data from the
    service layer and resets the walk/sleep output message class names so
    transient status messages do not persist.
    """
    try:
        total_steps = get_total_steps()
    except Exception:
        total_steps = 0
    try:
        total_calories = get_total_calories_burnt()
    except Exception:
        total_calories = 0
    try:
        total_miles = get_total_miles_walked()
    except Exception:
        total_miles = "0.0"
    try:
        sleep_hours, sleep_minutes = get_total_sleep_time()
    except Exception:
        sleep_hours, sleep_minutes = 0, 0
    try:
        streak = get_latest_streak()
    except Exception:
        streak = 0
    try:
        days = get_total_days()
    except Exception:
        days = 0

    stats = [
        stat_card("👟", "Total Steps Walked", f"{total_steps:,}", "crimson"),
        stat_card("🍽️", "Total Calories Burnt", f"{total_calories}", "crimson"),
        stat_card("🏞️", "Total Miles Walked", total_miles, "crimson"),
        stat_card(
            "🌙", "Total Sleep Time", f"{sleep_hours}h {sleep_minutes}m", "crimson"
        ),
        stat_card("🔥", "Current Streak", f"{streak} days", "crimson", "streak-active"),
        stat_card("🌅", "Total Interaction Days", f"{days} days", "crimson"),
    ]

    try:
        walked_today = did_log_walk_today()
    except Exception:
        walked_today = False
    try:
        slept_today = did_log_sleep_today()
    except Exception:
        slept_today = False

    try:
        todays_steps = get_todays_steps()
    except Exception:
        todays_steps = 0

    # Compute yesterday's steps from walk history for the "not logged yet" state
    yesterdays_steps = 0
    try:
        walk_rows = get_walk_history()
        yesterday = (datetime.now().date() - timedelta(days=1)).isoformat()
        for row in walk_rows:
            row_date = str(pd.to_datetime(row["todays_date"]).date())
            if row_date == yesterday:
                yesterdays_steps += row.get("steps_walked", 0)
    except Exception:
        yesterdays_steps = 0

    try:
        fatigue = did_sleep_eight_hours_last_night()
    except Exception:
        fatigue = None

    if walked_today:
        walk_status = f"Logged Today — {todays_steps:,} steps"
        walk_detail = f"{todays_steps:,} steps"
    else:
        walk_status = "Not Logged Yet"
        walk_detail = f"Yesterday's Steps: {yesterdays_steps:,}"
    walk_badge = "logged" if walked_today else "pending"

    try:
        sleep_h, sleep_m = get_total_sleep_time()
    except Exception:
        sleep_h, sleep_m = 0, 0

    sleep_status = f"{sleep_h}h {sleep_m}m total" if slept_today else "Not Logged Yet"
    sleep_badge = "logged" if slept_today else "pending"

    if fatigue is True:
        fatigue_text = "Energised! 😀"
        fatigue_class = "green"
    elif fatigue is False:
        fatigue_text = "Warning! Fatigued! 😞"
        fatigue_class = "amber"
    else:
        fatigue_text = "No sleep data"
        fatigue_class = ""

    status = [
        status_card("Walk", walk_status, walk_badge, walk_detail, ""),
        status_card("Sleep", sleep_status, sleep_badge, fatigue_text, fatigue_class),
    ]

    return stats, status, "", "", "output-message", "output-message"


@app.callback(
    Output("walk-output", "children"),
    Output("walk-location-error", "children"),
    Output("walk-steps-error", "children"),
    Output("walk-calories-error", "children"),
    Output("walk-miles-error", "children"),
    Output("walk-output", "className", allow_duplicate=True),
    Input("submit-walk", "n_clicks"),
    State("walk-location", "value"),
    State("walk-steps", "value"),
    State("walk-calories", "value"),
    State("walk-miles", "value"),
    prevent_initial_call=True,
)
def submit_walk(n_clicks, location, steps, calories, miles):
    """Handle walk form submission.

    Validates inputs, checks for duplicate today entries, persists the walk
    via the service layer, and returns a status message with the appropriate
    CSS class for visibility (success / info / error / hidden).
    """
    if not n_clicks:
        return "", "", "", "", "", "output-message"
    try:
        if did_log_walk_today():
            return (
                "You have already logged a walk today. Return on the morrow.",
                "",
                "",
                "",
                "",
                "output-message visible info",
            )

        walk = VitalXWalk(
            steps_walked=int(steps),
            calories_burnt=int(calories),
            miles_walked=float(miles),
            walk_location=location.strip(),
        )
        validate_walk(walk)
        insert_walk(walk)

        streak_valid = validate_streak(walk.steps_walked)
        if streak_valid:
            update_streak()
            msg = "Walk recorded! Streak maintained. 🔥"
        else:
            msg = "Walk recorded, but below streak threshold (6000 steps)."

        try:
            export_tables_to_spreadsheets()
            perform_daily_pg_backup()
        except Exception as backup_err:
            logger.error("Backup/export failed: %s", backup_err)

        return msg, "", "", "", "", "output-message visible success"

    except DatabaseError as e:
        return (
            f"Failed to save walk: {e}",
            "",
            "",
            "",
            "",
            "output-message visible error",
        )


@app.callback(
    Output("sleep-output", "children"),
    Output("sleep-hours-error", "children"),
    Output("sleep-minutes-error", "children"),
    Output("sleep-output", "className", allow_duplicate=True),
    Input("submit-sleep", "n_clicks"),
    State("sleep-hours", "value"),
    State("sleep-minutes", "value"),
    State("sleep-quality-store", "data"),
    prevent_initial_call=True,
)
def submit_sleep(n_clicks, hours, minutes, quality):
    """Handle sleep form submission.

    Validates inputs, checks for duplicate today entries, persists the sleep
    record (with quality from the sleep-quality store) via the service layer,
    and returns a status message with the appropriate CSS class.
    """
    if not n_clicks:
        return "", "", "", "output-message"
    try:
        if did_log_sleep_today():
            return (
                "You have already logged sleep today. Return on the morrow.",
                "",
                "",
                "output-message visible info",
            )

        sleep = VitalXSleep(
            hours_slept=int(hours),
            minutes_slept=int(minutes),
            good_sleep=bool(quality),
        )
        validate_sleep(sleep)
        insert_sleep(sleep)
        msg = f"Sleep recorded: {hours}h {minutes}m — {'Good' if quality else 'Bad'} sleep 🌙"
        return msg, "", "", "output-message visible success"
    except DatabaseError as e:
        return f"Failed to save sleep: {e}", "", "", "output-message visible error"


@app.callback(
    Output("sleep-quality-store", "data"),
    Output("sleep-quality-good", "className"),
    Output("sleep-quality-bad", "className"),
    Input("sleep-quality-good", "n_clicks"),
    Input("sleep-quality-bad", "n_clicks"),
    prevent_initial_call=True,
)
def toggle_sleep_quality(good_clicks, bad_clicks):
    """Toggle between Good Sleep and Bad Sleep selection.

    Updates the sleep-quality store and toggles CSS classes on the two
    quality buttons so the active choice is visually highlighted.
    """
    ctx = callback_context
    if not ctx.triggered:
        return True, "quality-btn active", "quality-btn"
    button_id = ctx.triggered[0]["prop_id"].split(".")[0]
    if button_id == "sleep-quality-bad":
        return False, "quality-btn", "quality-btn active bad"
    return True, "quality-btn active", "quality-btn"


@app.callback(
    Output("weather-display", "children"),
    Input("refresh-interval", "n_intervals"),
)
def update_weather(_):
    try:
        df = get_weather_data()
        if df.empty:
            return "No weather data available."
        row = df.iloc[0]
        date_str = pd.to_datetime(row["date"]).strftime("%a, %d %b")
        min_temp = int(round(row["temperature_2m_min"]))
        max_temp = int(round(row["temperature_2m_max"]))
        sunrise = pd.to_datetime(row["sunrise"], unit="s", utc=True).strftime("%H:%M")
        sunset = pd.to_datetime(row["sunset"], unit="s", utc=True).strftime("%H:%M")
        rain = int(round(row["rain_sum"]))
        snow = int(round(row["snowfall_sum"]))

        items = [
            html.Div(
                className="weather-detail",
                children=[
                    html.Span("Date", className="weather-label"),
                    html.Span(date_str, className="weather-value"),
                ],
            ),
            html.Div(
                className="weather-detail",
                children=[
                    html.Span("Temperature", className="weather-label"),
                    html.Span(
                        f"{min_temp}°C / {max_temp}°C", className="weather-value"
                    ),
                ],
            ),
            html.Div(
                className="weather-detail",
                children=[
                    html.Span("Sunrise", className="weather-label"),
                    html.Span(sunrise, className="weather-value"),
                ],
            ),
            html.Div(
                className="weather-detail",
                children=[
                    html.Span("Sunset", className="weather-label"),
                    html.Span(sunset, className="weather-value"),
                ],
            ),
        ]
        if rain > 0:
            items.append(
                html.Div(
                    className="weather-detail",
                    children=[
                        html.Span("Rainfall", className="weather-label"),
                        html.Span(f"{rain} mm", className="weather-value"),
                    ],
                )
            )
        if snow > 0:
            items.append(
                html.Div(
                    className="weather-detail",
                    children=[
                        html.Span("Snowfall", className="weather-label"),
                        html.Span(f"{snow} cm", className="weather-value"),
                    ],
                )
            )
        return items
    except Exception as e:
        logger.error("Failed to retrieve weather: %s", e, exc_info=True)
        return f"Could not load weather: {e}"


@app.callback(
    Output("skyrim-display", "children"),
    Input("refresh-interval", "n_intervals"),
    Input("submit-walk", "n_clicks"),
)
def update_skyrim(_, __):
    try:
        origin, destination, remaining, loops = skyrim_journey()
        return [
            html.Div(
                f"From {origin.title()} to {destination.title()}",
                className="skyrim-route",
            ),
            html.Div(
                className="progress-container",
                children=[html.Div(className="progress-bar", id="skyrim-progress")],
            ),
            html.Div(
                className="skyrim-stats",
                children=[
                    html.Span(f"Steps remaining: {remaining:,}"),
                    html.Span(f"Loops: {loops}"),
                ],
            ),
        ]
    except Exception as e:
        logger.error("Failed to retrieve skyrim journey: %s", e, exc_info=True)
        return f"Could not load journey: {e}"


@app.callback(
    Output("weekly-steps-chart", "figure"),
    Input("refresh-interval", "n_intervals"),
)
def update_weekly_chart(_):
    return weekly_steps_chart()


@app.callback(
    Output("monthly-sleep-chart", "figure"),
    Input("refresh-interval", "n_intervals"),
)
def update_monthly_chart(_):
    return monthly_sleep_chart()


@app.callback(
    Output("sleep-quality-pie", "figure"),
    Input("refresh-interval", "n_intervals"),
)
def update_sleep_pie(_):
    return sleep_quality_pie()


@app.callback(
    Output("location-pie", "figure"),
    Input("refresh-interval", "n_intervals"),
)
def update_location_pie(_):
    return location_pie()


@app.callback(
    Output("history-table", "children"),
    Input("refresh-interval", "n_intervals"),
)
def update_history(_):
    try:
        walk_rows = get_walk_history()
        sleep_rows = get_sleep_history()
    except Exception as e:
        logger.error("Failed to load history: %s", e, exc_info=True)
        return html.P("Unable to load history.", className="text-muted")

    entries = []
    for row in walk_rows:
        entries.append(
            {
                "date": str(pd.to_datetime(row["todays_date"]).date()),
                "type": "Walk",
                "value": f"{row['steps_walked']:,} steps",
                "detail": row.get("walk_location", "—"),
            }
        )
    for row in sleep_rows:
        entries.append(
            {
                "date": str(pd.to_datetime(row["todays_date"]).date()),
                "type": "Sleep",
                "value": f"{row['hours_slept']}h {row.get('minutes_slept', 0)}m",
                "detail": "Good" if row.get("good_sleep") else "Bad",
            }
        )

    entries.sort(key=lambda x: x["date"], reverse=True)
    entries = entries[:15]

    rows_html = []
    for entry in entries:
        rows_html.append(
            html.Div(
                className="history-row",
                children=[
                    html.Span(entry["date"], className="history-cell date"),
                    html.Span(entry["type"], className="history-cell type"),
                    html.Span(entry["value"], className="history-cell value"),
                    html.Span(entry["detail"], className="history-cell detail"),
                ],
            )
        )

    if not rows_html:
        return html.P("No entries yet.", className="text-muted")

    return html.Div(
        children=[
            html.Div(
                className="history-header",
                children=[
                    html.Span("Date", className="history-cell"),
                    html.Span("Type", className="history-cell"),
                    html.Span("Value", className="history-cell"),
                    html.Span("Detail", className="history-cell"),
                ],
            ),
            *rows_html,
        ]
    )


def main():
    logger.info("Initialising VitalX Gothic Dashboard on localhost:8050")
    app.run(host="0.0.0.0", port=8050, debug=True)


if __name__ == "__main__":
    main()
