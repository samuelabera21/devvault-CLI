from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from devvault.storage import load_config, save_config


def record_history(
    action: str,
    profile: str,
    key: str,
    is_secret: bool = False,
    config_file: Path | None = None,
) -> None:
    """Record an audit history entry with safe metadata (no sensitive values)."""
    config = load_config(config_file)
    history_list = config.setdefault("history", [])

    entry: dict[str, Any] = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "action": action.upper(),
        "profile": profile,
        "key": key,
        "is_secret": is_secret,
    }

    history_list.append(entry)
    save_config(config, config_file)


def get_history(
    profile: str | None = None,
    limit: int | None = None,
    config_file: Path | None = None,
) -> list[dict[str, Any]]:
    """Retrieve audit history entries, optionally filtered by profile and limit."""
    config = load_config(config_file)
    history_list = config.get("history", [])

    if profile is not None:
        history_list = [
            entry for entry in history_list if entry.get("profile") == profile
        ]

    # Return chronological or most recent
    if limit is not None and limit > 0:
        return list(history_list[-limit:])

    return list(history_list)
