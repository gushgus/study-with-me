import json
from pathlib import Path
from typing import Any, Dict, List

DATA_FILE = Path(__file__).with_name("ddays.json")

Dday = Dict[str, Any]


def load_ddays() -> List[Dday]:
    """Load ddays from ddays.json.

    Returns an empty list if the file does not exist.
    """
    if not DATA_FILE.exists():
        return []

    try:
        with DATA_FILE.open("r", encoding="utf-8") as f:
            data = json.load(f)
    except (json.JSONDecodeError, OSError):
        return []

    if isinstance(data, list):
        return data

    return []


def save_ddays(ddays: List[Dday]) -> None:
    """Save the given ddays list to ddays.json."""
    with DATA_FILE.open("w", encoding="utf-8") as f:
        json.dump(ddays, f, ensure_ascii=False, indent=2)
