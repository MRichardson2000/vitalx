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
    submit_walk,
    submit_sleep,
    toggle_sleep_quality,
    refresh_stats,
    update_history,
    update_date,
    update_quote,
)
from vitalx.exceptions import ValidationError, DatabaseError


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


class TestSubmitWalk:
    """Test walk submission callback behaviour, including error handling."""

    @patch("app_layer.app.did_log_walk_today", return_value=False)
    @patch("app_layer.app.insert_walk")
    @patch("app_layer.app.validate_walk")
    @patch("app_layer.app.validate_streak", return_value=True)
    @patch("app_layer.app.update_streak")
    @patch("app_layer.app.export_tables_to_spreadsheets")
    @patch("app_layer.app.perform_daily_pg_backup")
    def test_submit_walk_success_streak_maintained(
        self,
        mock_backup,
        mock_export,
        mock_update_streak,
        mock_validate_streak,
        mock_validate_walk,
        mock_insert_walk,
        mock_did_log,
    ):
        msg, *_ignored, cls = submit_walk(1, "Park", "7500", "300", "4.2")
        assert "Walk recorded! Streak maintained" in msg
        assert cls == "output-message visible success"
        mock_insert_walk.assert_called_once()
        mock_update_streak.assert_called_once()

    @patch("app_layer.app.did_log_walk_today", return_value=False)
    @patch("app_layer.app.insert_walk")
    @patch("app_layer.app.validate_walk")
    @patch("app_layer.app.validate_streak", return_value=False)
    @patch("app_layer.app.update_streak")
    @patch("app_layer.app.export_tables_to_spreadsheets")
    @patch("app_layer.app.perform_daily_pg_backup")
    def test_submit_walk_success_streak_broken(
        self,
        mock_backup,
        mock_export,
        mock_update_streak,
        mock_validate_streak,
        mock_validate_walk,
        mock_insert_walk,
        mock_did_log,
    ):
        msg, *_ignored, cls = submit_walk(1, "Park", "100", "300", "4.2")
        assert "below streak threshold" in msg
        assert cls == "output-message visible success"
        mock_update_streak.assert_not_called()

    @patch("app_layer.app.did_log_walk_today", return_value=True)
    def test_submit_walk_duplicate_today(self, mock_did_log):
        msg, *_ignored, cls = submit_walk(1, "Park", "7500", "300", "4.2")
        assert "already logged" in msg
        assert cls == "output-message visible info"

    @patch("app_layer.app.did_log_walk_today", return_value=False)
    def test_submit_walk_invalid_steps_type_error(self, mock_did_log):
        msg, *_ignored, cls = submit_walk(1, "Park", "not-a-number", "300", "4.2")
        assert "Invalid input" in msg
        assert cls == "output-message visible error"

    @patch("app_layer.app.did_log_walk_today", return_value=False)
    def test_submit_walk_missing_values(self, mock_did_log):
        msg, *_ignored, cls = submit_walk(1, None, None, None, None)
        assert "Invalid input" in msg
        assert cls == "output-message visible error"

    @patch("app_layer.app.did_log_walk_today", return_value=False)
    def test_submit_walk_blank_location(self, mock_did_log):
        msg, *_ignored, cls = submit_walk(1, "   ", "7500", "300", "4.2")
        assert "Invalid input" in msg
        assert cls == "output-message visible error"

    @patch("app_layer.app.did_log_walk_today", return_value=False)
    @patch(
        "app_layer.app.validate_walk",
        side_effect=ValidationError("Steps walked must be greater than 0"),
    )
    def test_submit_walk_validation_error(self, mock_validate_walk, mock_did_log):
        msg, *_ignored, cls = submit_walk(1, "Park", "0", "300", "4.2")
        assert "Invalid input" in msg
        assert cls == "output-message visible error"

    @patch("app_layer.app.did_log_walk_today", return_value=False)
    @patch("app_layer.app.insert_walk", side_effect=DatabaseError("connection lost"))
    def test_submit_walk_database_error(self, mock_insert_walk, mock_did_log):
        msg, *_ignored, cls = submit_walk(1, "Park", "7500", "300", "4.2")
        assert "Failed to save walk" in msg
        assert cls == "output-message visible error"

    def test_submit_walk_no_clicks(self):
        msg, *_ignored, cls = submit_walk(0, "Park", "7500", "300", "4.2")
        assert msg == ""
        assert cls == "output-message"


class TestSubmitSleep:
    """Test sleep submission callback behaviour, including error handling."""

    @patch("app_layer.app.did_log_sleep_today", return_value=False)
    @patch("app_layer.app.insert_sleep")
    @patch("app_layer.app.validate_sleep")
    def test_submit_sleep_success_good(
        self, mock_validate_sleep, mock_insert_sleep, mock_did_log
    ):
        msg, *_ignored, cls = submit_sleep(1, "8", "0", True)
        assert "Sleep recorded: 8h 0m — Good sleep" in msg
        assert cls == "output-message visible success"

    @patch("app_layer.app.did_log_sleep_today", return_value=False)
    @patch("app_layer.app.insert_sleep")
    @patch("app_layer.app.validate_sleep")
    def test_submit_sleep_success_bad(
        self, mock_validate_sleep, mock_insert_sleep, mock_did_log
    ):
        msg, *_ignored, cls = submit_sleep(1, "6", "30", False)
        assert "Bad sleep" in msg
        assert cls == "output-message visible success"

    @patch("app_layer.app.did_log_sleep_today", return_value=True)
    def test_submit_sleep_duplicate_today(self, mock_did_log):
        msg, *_ignored, cls = submit_sleep(1, "8", "0", True)
        assert "already logged" in msg
        assert cls == "output-message visible info"

    @patch("app_layer.app.did_log_sleep_today", return_value=False)
    def test_submit_sleep_invalid_hours(self, mock_did_log):
        msg, *_ignored, cls = submit_sleep(1, "not-a-number", "0", True)
        assert "Invalid input" in msg
        assert cls == "output-message visible error"

    @patch("app_layer.app.did_log_sleep_today", return_value=False)
    def test_submit_sleep_missing_values(self, mock_did_log):
        msg, *_ignored, cls = submit_sleep(1, None, None, True)
        assert "Invalid input" in msg
        assert cls == "output-message visible error"

    @patch("app_layer.app.did_log_sleep_today", return_value=False)
    @patch(
        "app_layer.app.validate_sleep",
        side_effect=ValidationError("Hours slept cannot be blank"),
    )
    def test_submit_sleep_validation_error(self, mock_validate_sleep, mock_did_log):
        msg, *_ignored, cls = submit_sleep(1, "0", "0", True)
        assert "Invalid input" in msg
        assert cls == "output-message visible error"

    @patch("app_layer.app.did_log_sleep_today", return_value=False)
    @patch("app_layer.app.insert_sleep", side_effect=DatabaseError("connection lost"))
    def test_submit_sleep_database_error(self, mock_insert_sleep, mock_did_log):
        msg, *_ignored, cls = submit_sleep(1, "8", "0", True)
        assert "Failed to save sleep" in msg
        assert cls == "output-message visible error"

    def test_submit_sleep_no_clicks(self):
        msg, *_ignored, cls = submit_sleep(0, "8", "0", True)
        assert msg == ""
        assert cls == "output-message"


class TestToggleSleepQuality:
    """Test the sleep quality toggle callback."""

    @patch("app_layer.app.callback_context")
    def test_no_trigger_defaults_to_good(self, mock_ctx):
        mock_ctx.triggered = []
        data, good_cls, bad_cls = toggle_sleep_quality(None, None)
        assert data is True
        assert good_cls == "quality-btn active"
        assert bad_cls == "quality-btn"

    @patch("app_layer.app.callback_context")
    def test_bad_button_triggered(self, mock_ctx):
        mock_ctx.triggered = [{"prop_id": "sleep-quality-bad.n_clicks"}]
        data, good_cls, bad_cls = toggle_sleep_quality(0, 1)
        assert data is False
        assert good_cls == "quality-btn"
        assert bad_cls == "quality-btn active bad"

    @patch("app_layer.app.callback_context")
    def test_good_button_triggered(self, mock_ctx):
        mock_ctx.triggered = [{"prop_id": "sleep-quality-good.n_clicks"}]
        data, good_cls, bad_cls = toggle_sleep_quality(1, 0)
        assert data is True
        assert good_cls == "quality-btn active"
        assert bad_cls == "quality-btn"


class TestRefreshStats:
    """Test the refresh_stats callback aggregates service data correctly."""

    @patch("app_layer.app.get_total_steps", return_value=10_000)
    @patch("app_layer.app.get_total_calories_burnt", return_value=500)
    @patch("app_layer.app.get_total_miles_walked", return_value="10.5")
    @patch("app_layer.app.get_total_sleep_time", return_value=(7, 30))
    @patch("app_layer.app.get_latest_streak", return_value=5)
    @patch("app_layer.app.get_total_days", return_value=10)
    @patch("app_layer.app.did_log_walk_today", return_value=True)
    @patch("app_layer.app.did_log_sleep_today", return_value=False)
    @patch("app_layer.app.get_todays_steps", return_value=3_000)
    @patch("app_layer.app.get_walk_history", return_value=[])
    @patch("app_layer.app.did_sleep_eight_hours_last_night", return_value=True)
    def test_refresh_stats_returns_expected_structure(
        self,
        mock_fatigue,
        mock_walk_history,
        mock_todays_steps,
        mock_slept_today,
        mock_walked_today,
        mock_total_days,
        mock_streak,
        mock_sleep_time,
        mock_miles,
        mock_calories,
        mock_steps,
    ):
        stats, status, walk_msg, sleep_msg, walk_cls, sleep_cls = refresh_stats(0)
        assert len(stats) == 6
        assert len(status) == 2
        assert walk_msg == ""
        assert sleep_msg == ""
        assert walk_cls == "output-message"
        assert sleep_cls == "output-message"


class TestUpdateHistory:
    """Test the history table callback."""

    @patch("app_layer.app.get_walk_history")
    @patch("app_layer.app.get_sleep_history")
    def test_update_history_mixes_walk_and_sleep(
        self, mock_sleep_history, mock_walk_history
    ):
        mock_walk_history.return_value = [
            {
                "todays_date": datetime.now(),
                "steps_walked": 7500,
                "walk_location": "Park",
            },
        ]
        mock_sleep_history.return_value = [
            {
                "todays_date": datetime.now(),
                "hours_slept": 8,
                "minutes_slept": 0,
                "good_sleep": True,
            },
        ]
        result = update_history(0)
        assert result is not None

    @patch("app_layer.app.get_walk_history", return_value=[])
    @patch("app_layer.app.get_sleep_history", return_value=[])
    def test_update_history_empty(self, mock_sleep_history, mock_walk_history):
        result = update_history(0)
        assert result is not None

    @patch("app_layer.app.get_walk_history", side_effect=Exception("db down"))
    @patch("app_layer.app.get_sleep_history", return_value=[])
    def test_update_history_database_error(self, mock_sleep_history, mock_walk_history):
        result = update_history(0)
        assert result is not None


class TestSimpleCallbacks:
    """Test the lightweight date and quote callbacks."""

    def test_update_date(self):
        result = update_date(0)
        assert result == datetime.now().strftime("%A, %d %B %Y")

    def test_update_quote(self):
        result = update_quote(0)
        assert result.startswith('"')
        assert result.endswith('"')


class TestChartEdgeCases:
    """Test chart helpers with incomplete or unusual data."""

    @patch("app_layer.app.get_sleep_history")
    def test_monthly_sleep_chart_missing_minutes_column(self, mock_sleep_history):
        """Sleep rows without a minutes_slept column must not break the chart."""
        mock_sleep_history.return_value = [
            {"todays_date": datetime.now(), "hours_slept": 8, "good_sleep": True},
        ]
        fig = monthly_sleep_chart()
        assert fig is not None

    @patch("app_layer.app.get_walk_history")
    def test_location_pie_excludes_work(self, mock_walk_history):
        mock_walk_history.return_value = [
            {
                "todays_date": datetime.now(),
                "steps_walked": 7500,
                "walk_location": "Work",
            },
            {
                "todays_date": datetime.now(),
                "steps_walked": 7500,
                "walk_location": "Park",
            },
        ]
        fig = location_pie()
        assert fig is not None


class TestSleepHistoryDF:
    """Test _sleep_history_df resilience against service-layer failures."""

    @patch(
        "app_layer.app.get_sleep_history", side_effect=Exception("db connection lost")
    )
    def test_sleep_history_df_handles_db_error(self, mock_history):
        """When get_sleep_history raises, _sleep_history_df returns empty DF instead of crashing."""
        from app_layer import app as app_module

        df = app_module._sleep_history_df()
        assert df.empty
        assert list(df.columns) == ["todays_date", "hours_slept", "good_sleep"]

    @patch("app_layer.app.get_sleep_history", return_value=[])
    def test_sleep_history_df_empty_when_no_rows(self, mock_history):
        """When get_sleep_history returns [], _sleep_history_df returns empty DF."""
        from app_layer import app as app_module

        df = app_module._sleep_history_df()
        assert df.empty


class TestRefreshStatsFatigue:
    """Test refresh_stats fatigue text distinguishes error vs no-data."""

    @patch(
        "app_layer.app.did_sleep_eight_hours_last_night",
        side_effect=Exception("missing SQL file"),
    )
    @patch(
        "app_layer.app.get_sleep_history",
        return_value=[
            {
                "todays_date": datetime.now(),
                "hours_slept": 8,
                "minutes_slept": 0,
                "good_sleep": True,
            }
        ],
    )
    @patch("app_layer.app.get_total_steps", return_value=0)
    @patch("app_layer.app.get_total_calories_burnt", return_value=0)
    @patch("app_layer.app.get_total_miles_walked", return_value="0.0")
    @patch("app_layer.app.get_total_sleep_time", return_value=(0, 0))
    @patch("app_layer.app.get_latest_streak", return_value=0)
    @patch("app_layer.app.get_total_days", return_value=0)
    @patch("app_layer.app.did_log_walk_today", return_value=False)
    @patch("app_layer.app.did_log_sleep_today", return_value=False)
    @patch("app_layer.app.get_todays_steps", return_value=0)
    @patch("app_layer.app.get_walk_history", return_value=[])
    def test_refresh_stats_unable_to_check_when_data_exists(
        self,
        mock_walk_history,
        mock_todays_steps,
        mock_slept_today,
        mock_walked_today,
        mock_total_days,
        mock_streak,
        mock_sleep_time,
        mock_miles,
        mock_calories,
        mock_steps,
        mock_sleep_history,
        mock_fatigue,
    ):
        """When fatigue check errors but sleep data exists, show 'Unable to check sleep quality'."""
        stats, status, *_ignored = refresh_stats(0)
        sleep_card = status[1]
        assert "Unable to check sleep quality" in str(sleep_card.children)

    @patch(
        "app_layer.app.did_sleep_eight_hours_last_night",
        side_effect=Exception("missing SQL file"),
    )
    @patch("app_layer.app.get_sleep_history", return_value=[])
    @patch("app_layer.app.get_total_steps", return_value=0)
    @patch("app_layer.app.get_total_calories_burnt", return_value=0)
    @patch("app_layer.app.get_total_miles_walked", return_value="0.0")
    @patch("app_layer.app.get_total_sleep_time", return_value=(0, 0))
    @patch("app_layer.app.get_latest_streak", return_value=0)
    @patch("app_layer.app.get_total_days", return_value=0)
    @patch("app_layer.app.did_log_walk_today", return_value=False)
    @patch("app_layer.app.did_log_sleep_today", return_value=False)
    @patch("app_layer.app.get_todays_steps", return_value=0)
    @patch("app_layer.app.get_walk_history", return_value=[])
    def test_refresh_stats_no_sleep_data_when_none_exists(
        self,
        mock_walk_history,
        mock_todays_steps,
        mock_slept_today,
        mock_walked_today,
        mock_total_days,
        mock_streak,
        mock_sleep_time,
        mock_miles,
        mock_calories,
        mock_steps,
        mock_sleep_history,
        mock_fatigue,
    ):
        """When fatigue check errors and no sleep data exists, show 'No sleep data'."""
        stats, status, *_ignored = refresh_stats(0)
        sleep_card = status[1]
        assert "No sleep data" in str(sleep_card.children)
