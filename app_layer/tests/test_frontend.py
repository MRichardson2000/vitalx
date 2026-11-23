"""Front-end tests for VitalX Gothic Dashboard (app_layer/)."""

import sys
from pathlib import Path

sys.path.insert(
    0, str(Path(__file__).parent.parent.parent)
)  # project root: makes app_layer importable

from unittest.mock import patch
from datetime import datetime

from app_layer.app import (
    weekly_steps_chart,
    monthly_sleep_chart,
    sleep_quality_pie,
    location_pie,
    stat_card,
    status_card,
    create_layout,
)


class TestStatCard:
    def test_stat_card_returns_div(self):
        card = stat_card("👟", "Total Steps", "10,000", "", "crimson")
        assert card is not None
        assert card.className == "stat-card crimson"


class TestStatusCard:
    def test_status_card_returns_div(self):
        card = status_card("Walk", "Logged Today", "logged", "7,500 steps", "")
        assert card is not None
        assert card.className == "status-card logged"


class TestCharts:
    def test_weekly_steps_chart_returns_figure(self):
        fig = weekly_steps_chart()
        assert fig is not None
        assert hasattr(fig, "data")

    def test_monthly_sleep_chart_returns_figure(self):
        fig = monthly_sleep_chart()
        assert fig is not None
        assert hasattr(fig, "data")

    def test_sleep_quality_pie_returns_figure(self):
        fig = sleep_quality_pie()
        assert fig is not None
        assert hasattr(fig, "data")

    def test_location_pie_returns_figure(self):
        fig = location_pie()
        assert fig is not None
        assert hasattr(fig, "data")


class TestLayout:
    def test_create_layout_returns_div(self):
        layout = create_layout()
        assert layout is not None
        assert layout.className == "container"


class TestWalkHistoryMock:
    """Test chart functions with mocked walk history data."""

    @patch("app_layer.app.get_walk_history")
    def test_weekly_steps_chart_with_data(self, mock_history):
        mock_history.return_value = [
            {
                "todays_date": datetime.now(),
                "steps_walked": 7500,
                "walk_location": "Park",
            },
            {
                "todays_date": datetime.now(),
                "steps_walked": 8200,
                "walk_location": "Mall",
            },
        ]
        fig = weekly_steps_chart()
        assert fig is not None

    @patch("app_layer.app.get_walk_history")
    def test_location_pie_with_data(self, mock_history):
        mock_history.return_value = [
            {
                "todays_date": datetime.now(),
                "steps_walked": 7500,
                "walk_location": "Park",
            },
            {
                "todays_date": datetime.now(),
                "steps_walked": 8200,
                "walk_location": "Park",
            },
            {
                "todays_date": datetime.now(),
                "steps_walked": 5000,
                "walk_location": "High Street",
            },
        ]
        fig = location_pie()
        assert fig is not None


class TestSleepHistoryMock:
    """Test chart functions with mocked sleep history data."""

    @patch("app_layer.app.get_sleep_history")
    def test_monthly_sleep_chart_with_data(self, mock_history):
        mock_history.return_value = [
            {
                "todays_date": datetime.now(),
                "hours_slept": 8,
                "minutes_slept": 0,
                "good_sleep": True,
            },
            {
                "todays_date": datetime.now(),
                "hours_slept": 6,
                "minutes_slept": 30,
                "good_sleep": False,
            },
        ]
        fig = monthly_sleep_chart()
        assert fig is not None

    @patch("app_layer.app.get_sleep_history")
    def test_sleep_quality_pie_with_data(self, mock_history):
        mock_history.return_value = [
            {
                "todays_date": datetime.now(),
                "hours_slept": 8,
                "minutes_slept": 0,
                "good_sleep": True,
            },
            {
                "todays_date": datetime.now(),
                "hours_slept": 6,
                "minutes_slept": 30,
                "good_sleep": False,
            },
            {
                "todays_date": datetime.now(),
                "hours_slept": 7,
                "minutes_slept": 0,
                "good_sleep": True,
            },
        ]
        fig = sleep_quality_pie()
        assert fig is not None
