import re
from pathlib import Path

from devvault.exceptions import (
    ProfileAlreadyExistsError,
    ProfileError,
    ProfileNotFoundError,
)
from devvault.history import record_history
from devvault.storage import (
    DEFAULT_PROFILE,
    load_config,
    save_config,
)


def validate_profile_name(name: str) -> None:
    """Validate profile name format."""
    if not name or not isinstance(name, str):
        raise ValueError("Profile name cannot be empty.")

    if not (name[0].isalnum() or name[0] == "_"):
        raise ValueError(
            "Profile name must start with an alphanumeric character or underscore."
        )

    if not re.match(r"^[a-zA-Z0-9_-]+$", name):
        raise ValueError(
            "Profile name can only contain letters, numbers, underscores, and hyphens."
        )


def list_profiles(config_file: Path | None = None) -> list[str]:
    """Return a list of all profile names."""
    config = load_config(config_file)
    return list(config["profiles"].keys())


def get_active_profile(config_file: Path | None = None) -> str:
    """Return the currently active profile name."""
    config = load_config(config_file)
    return str(config.get("active_profile", DEFAULT_PROFILE))


def set_active_profile(name: str, config_file: Path | None = None) -> None:
    """Switch the active profile."""
    config = load_config(config_file)
    if name not in config["profiles"]:
        raise ProfileNotFoundError(f"Profile '{name}' not found.")

    config["active_profile"] = name
    save_config(config, config_file)
    record_history(
        action="PROFILE_USE",
        profile=name,
        key=name,
        is_secret=False,
        config_file=config_file,
    )


def create_profile(name: str, config_file: Path | None = None) -> None:
    """Create a new configuration profile."""
    validate_profile_name(name)
    config = load_config(config_file)

    if name in config["profiles"]:
        raise ProfileAlreadyExistsError(f"Profile '{name}' already exists.")

    config["profiles"][name] = {
        "values": {},
        "secrets": {},
    }
    save_config(config, config_file)
    record_history(
        action="PROFILE_CREATE",
        profile=name,
        key=name,
        is_secret=False,
        config_file=config_file,
    )


def delete_profile(name: str, config_file: Path | None = None) -> None:
    """Delete a configuration profile safely."""
    config = load_config(config_file)

    if name not in config["profiles"]:
        raise ProfileNotFoundError(f"Profile '{name}' not found.")

    active_profile = config.get("active_profile", DEFAULT_PROFILE)
    if name == active_profile:
        raise ProfileError(
            f"Cannot delete the active profile '{name}'. "
            "Switch to another profile first."
        )

    if name == DEFAULT_PROFILE and len(config["profiles"]) == 1:
        raise ProfileError(f"Cannot delete the default profile '{name}'.")

    del config["profiles"][name]
    save_config(config, config_file)
    record_history(
        action="PROFILE_DELETE",
        profile=name,
        key=name,
        is_secret=False,
        config_file=config_file,
    )
