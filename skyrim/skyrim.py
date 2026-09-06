from vitalx.service import get_walk_history
from datetime import datetime
from pathlib import Path
from typing import Any
import json


######################################################################
# Utilities
######################################################################


STATE_FILE = (Path(__file__).parent / "state.json").resolve()


SKYRIM_CITIES = [
    {"id": 0, "from": "whiterun", "to": "falkreath", "steps_required": 55000},
    {"id": 1, "from": "falkreath", "to": "markarth", "steps_required": 140000},
    {"id": 2, "from": "markarth", "to": "solitude", "steps_required": 250000},
    {"id": 3, "from": "solitude", "to": "morthal", "steps_required": 295000},
    {"id": 4, "from": "morthal", "to": "dawnstar", "steps_required": 55000},
    {"id": 5, "from": "dawnstar", "to": "winterhold", "steps_required": 80000},
    {"id": 6, "from": "winterhold", "to": "windhelm", "steps_required": 65000},
    {"id": 7, "from": "windhelm", "to": "riften", "steps_required": 120000},
    {"id": 8, "from": "riften", "to": "whiterun", "steps_required": 135000},
]


######################################################################
# Functionality
######################################################################


def load_state() -> dict[str, Any]:
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
        "loop_times": 0,
    }
    save_state(default_state)
    return default_state


def save_state(state: dict[str, Any]) -> None:
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=4)


def skyrim_journey(
    locations: list[dict[str, Any]] = SKYRIM_CITIES,
) -> tuple[str, str, int, int]:
    state = load_state()
    current_steps = 0
    walk_history = get_walk_history()
    check_date = datetime.now().date()
    if state["last_checked_date"] != check_date.isoformat():
        for x in walk_history:
            walk_date = x["todays_date"]
            if isinstance(walk_date, str):
                walk_date = datetime.strptime(walk_date, "%Y-%m-%d %H:%M:%S.%f").date()
            elif isinstance(walk_date, datetime):
                walk_date = walk_date.date()
            if walk_date == check_date:
                current_steps += x["steps_walked"]
        state["steps"] += current_steps
        state["last_checked_date"] = check_date.isoformat()
    current_location = locations[state["id_count"]]
    required_steps = current_location["steps_required"]
    while state["steps"] >= required_steps:
        state["steps"] -= required_steps
        state["id_count"] += 1
        if state["id_count"] == len(locations):
            state["id_count"] = 0
            state["loop_times"] += 1
        current_location = locations[state["id_count"]]
        required_steps = current_location["steps_required"]
    remaining = required_steps - state["steps"]
    save_state(state)
    return (
        current_location["from"],
        current_location["to"],
        remaining,
        state["loop_times"],
    )


def main() -> None:
    print(skyrim_journey())


if __name__ == "__main__":
    main()
