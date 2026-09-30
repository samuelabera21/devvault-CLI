from pathlib import Path
from typing import Any

from devvault.exceptions import ConfigKeyNotFoundError, ProfileNotFoundError
from devvault.storage import (
    DEFAULT_PROFILE,
    get_config_file,
    load_config,
    save_config,
)


def initialize_config(config_file: Path | None = None) -> None:
    if config_file is None:
        config_file = get_config_file()

    if config_file.exists():
        raise FileExistsError("DevVault is already initialized.")

    config_file.parent.mkdir(parents=True, exist_ok=True)
    initial_data = {
        "active_profile": DEFAULT_PROFILE,
        "profiles": {
            DEFAULT_PROFILE: {},
        },
    }
    save_config(initial_data, config_file)


def _resolve_profile(
    config: dict[str, Any], profile: str | None = None
) -> tuple[str, dict[str, Any]]:
    target_profile = (
        profile
        if profile is not None
        else config.get("active_profile", DEFAULT_PROFILE)
    )
    profiles = config.get("profiles", {})
    if target_profile not in profiles:
        raise ProfileNotFoundError(f"Profile '{target_profile}' not found.")
    return target_profile, profiles[target_profile]


def set_config(
    key: str,
    value: Any,
    profile: str | None = None,
    config_file: Path | None = None,
) -> None:
    config = load_config(config_file)
    _, profile_data = _resolve_profile(config, profile)
    profile_data[key] = value
    save_config(config, config_file)


def get_config(
    key: str,
    profile: str | None = None,
    config_file: Path | None = None,
) -> Any:
    config = load_config(config_file)
    _, profile_data = _resolve_profile(config, profile)

    if key not in profile_data:
        raise ConfigKeyNotFoundError(f"Key '{key}' not found.")

    return profile_data[key]


def list_config(
    profile: str | None = None,
    config_file: Path | None = None,
) -> list[str]:
    config = load_config(config_file)
    _, profile_data = _resolve_profile(config, profile)
    return list(profile_data.keys())


def remove_config(
    key: str,
    profile: str | None = None,
    config_file: Path | None = None,
) -> bool:
    config = load_config(config_file)
    _, profile_data = _resolve_profile(config, profile)

    if key not in profile_data:
        return False

    del profile_data[key]
    save_config(config, config_file)

    return True
