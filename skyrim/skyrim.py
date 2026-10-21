from vitalx.service import get_todays_steps
from datetime import datetime
from pathlib import Path
from typing import Any
import json


######################################################################
# Utilities
######################################################################


STATE_FILE = (Path(__file__).parent / "state.json").resolve()


SKYRIM_CITIES = [
    {"id": 0, "from": "whiterun", "to": "falkreath", "steps_required": 22000},
    {"id": 1, "from": "falkreath", "to": "markarth", "steps_required": 45000},
    {"id": 2, "from": "markarth", "to": "solitude", "steps_required": 50000},
    {"id": 3, "from": "solitude", "to": "morthal", "steps_required": 25000},
    {"id": 4, "from": "morthal", "to": "dawnstar", "steps_required": 28000},
    {"id": 5, "from": "dawnstar", "to": "winterhold", "steps_required": 32000},
    {"id": 6, "from": "winterhold", "to": "windhelm", "steps_required": 26000},
    {"id": 7, "from": "windhelm", "to": "riften", "steps_required": 38000},
    {"id": 8, "from": "riften", "to": "whiterun", "steps_required": 42000},
]


######################################################################
# Functionality
######################################################################


def load_state() -> dict[str, Any]:
    """
    Load the application state from state.json.

    Attempts to read and parse the state file. If the file does not exist
    or contains invalid json, it generates, saves, and returns a default
    state dictionary.

    Returns:
        dict[str, Any]: The application state containing the following keys:
            - id_count (int): Current id counter to indicate which city you're in.
            - steps (int): Total recorded steps.
            - last_checked_date (str | None): The last recorded check-in date.
            - loop_times (int): Number of loops around Skryim.

    Side Effects:
        Creates a new `state.json` file on disk if one does not already exist.
    """
    if STATE_FILE.exists():
        try:
            with open(STATE_FILE, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            pass
    default_state = {
        "id_count": 0,
        "steps": 0,
        "last_checked_date": None,
        "last_todays_steps": 0,
        "loop_times": 0,
    }
    save_state(default_state)
    return default_state


def save_state(state: dict[str, Any]) -> None:
    """Opens the state json file in write mode and writes in the state passed in from load_state()"""
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=4)


def skyrim_journey(
    locations: list[dict[str, Any]] = SKYRIM_CITIES,
) -> tuple[str, str, int, int]:
    """Process walk history, update state, and advance the Skyrim journey.

    Loads the current application state, pulls today's walk history, and
    adds any new steps if they haven't been recorded for today yet. It then
    advances the user along the Skyrim city route based on total accumulated
    steps, looping back to the start if the final destination is reached.

    Args:
        locations (list[dict[str, Any]]): A list of dictionary objects representing
            the path between cities. Defaults to `SKYRIM_CITIES`.

    Returns:
        tuple[str, str, int, int]: A tuple containing:
            - Origin city name (str)
            - Destination city name (str)
            - Remaining steps needed to reach the destination (int)
            - Number of full map loops completed (int)

    Side Effects:
        Updates and saves the application state to disk via `save_state()`.
    """
    state = load_state()
    today = datetime.now().date().isoformat()
    current_steps = state["steps"]
    current_id = state["id_count"] % len(locations)
    loop_times = state["loop_times"]
    last_checked_date = state["last_checked_date"]
    last_todays_steps = state["last_todays_steps"] or 0
    latest_db_steps = max(0, get_todays_steps())
    if last_checked_date != today:
        new_steps = latest_db_steps
    else:
        new_steps = max(0, latest_db_steps - last_todays_steps)
    current_steps += new_steps
    while current_steps >= locations[current_id]["steps_required"]:
        current_steps -= locations[current_id]["steps_required"]
        current_id += 1
        if current_id >= len(locations):
            current_id = 0
            loop_times += 1
    save_state(
        {
            "id_count": current_id,
            "steps": current_steps,
            "last_checked_date": today,
            "last_todays_steps": latest_db_steps,
            "loop_times": loop_times,
        }
    )
    current_leg = locations[current_id]
    steps_remaining = current_leg["steps_required"] - current_steps
    return (current_leg["from"], current_leg["to"], steps_remaining, loop_times)


def main() -> None:
    print(skyrim_journey())


if __name__ == "__main__":
    main()
