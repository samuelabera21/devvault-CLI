import json
from pathlib import Path
from typing import Any

DEFAULT_PROFILE: str = "default"


def get_global_config_file() -> Path:
    """Return the path to the user-global DevVault configuration file."""
    return Path.home() / ".devvault" / "config.json"


def get_project_config_file(start_path: Path | None = None) -> Path | None:
    """Find a project-local .devvault/config.json in current or parent directories."""
    current = (start_path or Path.cwd()).resolve()
    for parent in [current, *current.parents]:
        candidate = parent / ".devvault" / "config.json"
        if candidate.exists() and candidate.is_file():
            return candidate
        # Stop at filesystem root
        if parent.parent == parent:
            break
    return None


def get_config_file() -> Path:
    """Return project config file if available, otherwise global config file."""
    project_cfg = get_project_config_file()
    if project_cfg is not None:
        return project_cfg
    return get_global_config_file()


def normalize_profile_data(raw: Any) -> dict[str, Any]:
    """Normalize profile dictionary into standardized structure."""
    if not isinstance(raw, dict):
        return {"values": {}, "secrets": {}}

    if "values" in raw and isinstance(raw["values"], dict):
        secrets = raw.get("secrets", {})
        return {
            "values": dict(raw["values"]),
            "secrets": dict(secrets) if isinstance(secrets, dict) else {},
        }

    # Backward compatibility: legacy flat format {KEY: VALUE}
    return {
        "values": dict(raw),
        "secrets": {},
    }


def normalize_config(raw_data: Any) -> dict[str, Any]:
    """Normalize raw JSON data into the full DevVault storage schema."""
    if not isinstance(raw_data, dict):
        raise ValueError("DevVault configuration file is corrupted.")

    normalized: dict[str, Any] = {
        "active_profile": raw_data.get("active_profile", DEFAULT_PROFILE),
        "profiles": {},
        "vault": raw_data.get("vault", {"initialized": False}),
        "history": raw_data.get("history", []),
        "schema": raw_data.get("schema", {}),
        "templates": raw_data.get("templates", {}),
    }

    if "profiles" in raw_data and isinstance(raw_data["profiles"], dict):
        for prof_name, prof_data in raw_data["profiles"].items():
            normalized["profiles"][prof_name] = normalize_profile_data(prof_data)
    else:
        # Legacy single flat config
        normalized["profiles"][DEFAULT_PROFILE] = normalize_profile_data(raw_data)

    if DEFAULT_PROFILE not in normalized["profiles"]:
        normalized["profiles"][DEFAULT_PROFILE] = {"values": {}, "secrets": {}}

    return normalized


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

    config_file.parent.mkdir(parents=True, exist_ok=True)
    with config_file.open("w", encoding="utf-8") as file:
        json.dump(config, file, indent=4)
