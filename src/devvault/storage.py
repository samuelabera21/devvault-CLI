import json
from pathlib import Path
from typing import Any

DEFAULT_PROFILE: str = "default"


def get_config_file() -> Path:
    return Path.home() / ".devvault" / "config.json"


def normalize_config(raw_data: Any) -> dict[str, Any]:
    """Normalize raw JSON data into the profile-based schema."""
    if not isinstance(raw_data, dict):
        raise ValueError("DevVault configuration file is corrupted.")

    if "profiles" in raw_data and isinstance(raw_data["profiles"], dict):
        active = raw_data.get("active_profile", DEFAULT_PROFILE)
        return {
            "active_profile": active,
            "profiles": raw_data["profiles"],
        }

    # Backward compatibility: legacy flat format {KEY: VALUE}
    return {
        "active_profile": DEFAULT_PROFILE,
        "profiles": {
            DEFAULT_PROFILE: dict(raw_data),
        },
    }


def load_config(config_file: Path | None = None) -> dict[str, Any]:
    if config_file is None:
        config_file = get_config_file()

    if not config_file.exists():
        raise FileNotFoundError(
            "DevVault is not initialized. Run 'devvault init' first."
        )

    try:
        with config_file.open("r", encoding="utf-8") as file:
            raw_data = json.load(file)
            return normalize_config(raw_data)
    except json.JSONDecodeError:
        raise ValueError("DevVault configuration file is corrupted.")


def save_config(config: dict[str, Any], config_file: Path | None = None) -> None:
    if config_file is None:
        config_file = get_config_file()

    with config_file.open("w", encoding="utf-8") as file:
        json.dump(config, file, indent=4)
