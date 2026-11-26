"""Unit tests for skyrim.skyrim (Skyrim journey logic).

What to test:
- load_state returns default state when state.json doesn't exist
- load_state returns saved state when state.json exists
- load_state handles corrupted JSON gracefully (returns default state)
- save_state writes the state dict to state.json as valid JSON
- skyrim_journey returns a tuple of (origin, destination, steps_remaining, loops)
- skyrim_journey advances to the next city when steps are sufficient
- skyrim_journey loops back to Whiterun after reaching the final city
- skyrim_journey saves state after each call (side effect)
- skyrim_journey handles today-vs-yesterday step tracking correctly
- SKYRIM_CITIES has the expected number of entries and structure

Suggested mocks:
- Monkeypatch skyrim.STATE_FILE to a temporary path (tmp_path)
- Monkeypatch skyrim.get_todays_steps to return a fixed value
- Monkeypatch skyrim.load_state / save_state to control state without touching disk
"""

from datetime import datetime
from skyrim.skyrim import (
    load_state,
    save_state,
    skyrim_journey,
    SKYRIM_CITIES,
    STATE_FILE,
)


def test_load_state_returns_default_when_file_missing(tmp_path, monkeypatch):
    """
    When state.json doesn't exist, load_state should create and return the default state.
    Hint: monkeypatch STATE_FILE to a path under tmp_path that doesn't exist yet.
    Default state: {"id_count": 0, "steps": 0, "last_checked_date": None,
    "last_todays_steps": 0, "loop_times": 0}
    """
    pass


def test_load_state_returns_saved_state(tmp_path, monkeypatch):
    """
    When state.json exists with valid JSON, load_state should return it.
    Hint: write a known state to the file first, then call load_state and compare.
    """
    pass


def test_load_state_handles_corrupted_json(tmp_path, monkeypatch):
    """
    When state.json contains invalid JSON, load_state should return the default state
    (and not crash).
    Hint: write invalid JSON to the file, then call load_state.
    """
    pass


def test_save_state_writes_valid_json(tmp_path, monkeypatch):
    """
    save_state should write the state dict to STATE_FILE as valid JSON.
    Hint: call save_state with a known dict, then read the file back and parse it.
    """
    pass


def test_skyrim_journey_returns_tuple_of_four():
    """
    skyrim_journey() should return a tuple of (str, str, int, int).
    Hint: mock get_todays_steps and load_state/save_state, then check the return type.
    """
    pass


def test_skyrim_journey_advances_city_when_steps_sufficient():
    """
    When total steps exceed the current leg's steps_required, the journey should
    advance to the next city.
    Hint: set up state with enough steps to complete the current leg.
    """
    pass


def test_skyrim_journey_loops_back_to_whiterun():
    """
    After completing the final leg (Riften -> Whiterun), the journey should loop
    back to Whiterun -> Falkreath and increment loop_times.
    """
    pass


def test_skyrim_journey_saves_state():
    """
    skyrim_journey should call save_state as a side effect.
    Hint: mock save_state and assert it was called with the expected state dict.
    """
    pass


def test_skyrim_journey_today_vs_yesterday_steps():
    """
    If last_checked_date equals today, new_steps should be
    latest_db_steps - last_todays_steps (not double-counted).
    If last_checked_date differs from today, new_steps = latest_db_steps.
    """
    pass


def test_skyrm_cities_has_nine_entries():
    """
    SKYRIM_CITIES should have exactly 9 city legs.
    Hint: assert len(SKYRIM_CITIES) == 9.
    """
    pass


def test_skyrim_journey_origin_and_destination_are_strings():
    """
    The first two elements of the returned tuple should be non-empty strings.
    """
    pass
