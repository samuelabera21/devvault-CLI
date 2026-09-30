from pathlib import Path
from typing import Any

from devvault.exceptions import (
    ConfigKeyNotFoundError,
    ProfileNotFoundError,
    SecretMaskedError,
)
from devvault.history import record_history
from devvault.security import (
    decrypt_secret,
    encrypt_secret,
    get_vault_status,
)
from devvault.storage import (
    DEFAULT_PROFILE,
    get_config_file,
    load_config,
    save_config,
)

MASKED_SECRET_PLACEHOLDER: str = "********"


def validate_key(key: str) -> None:
    """Validate that a configuration key follows naming rules."""
    if not key:
        raise ValueError("Configuration key cannot be empty.")

    if not (key[0].isalpha() or key[0] == "_"):
        raise ValueError("Configuration key must start with a letter or underscore.")

    if not key.replace("_", "").isalnum():
        raise ValueError(
            "Configuration key can only contain letters, numbers, and underscores."
        )


def parse_value(value: str) -> bool | int | float | str:
    """Parse a string representation into typed primitive value."""
    if value.lower() == "true":
        return True

    if value.lower() == "false":
        return False

    try:
        return int(value)
    except ValueError:
        pass

    try:
        return float(value)
    except ValueError:
        pass

    return value


def initialize_config(config_file: Path | None = None) -> None:
    if config_file is None:
        config_file = get_config_file()

    if config_file.exists():
        raise FileExistsError("DevVault is already initialized.")

    config_file.parent.mkdir(parents=True, exist_ok=True)
    initial_data = {
        "active_profile": DEFAULT_PROFILE,
        "profiles": {
            DEFAULT_PROFILE: {
                "values": {},
                "secrets": {},
            },
        },
        "vault": {"initialized": False},
        "history": [],
        "schema": {},
        "templates": {},
    }
    save_config(initial_data, config_file)
    record_history(
        action="INIT",
        profile=DEFAULT_PROFILE,
        key="config",
        is_secret=False,
        config_file=config_file,
    )


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

    prof_data = profiles[target_profile]
    # Ensure standard dictionary structure
    if not isinstance(prof_data, dict) or (
        "values" not in prof_data and "secrets" not in prof_data
    ):
        profiles[target_profile] = {
            "values": dict(prof_data) if isinstance(prof_data, dict) else {},
            "secrets": {},
        }

    return target_profile, profiles[target_profile]


def set_config(
    key: str,
    value: Any,
    is_secret: bool = False,
    profile: str | None = None,
    config_file: Path | None = None,
) -> None:
    """Set a configuration value, optionally marked as a sensitive secret."""
    validate_key(key)
    config = load_config(config_file)
    target_profile, profile_data = _resolve_profile(config, profile)

    values_dict = profile_data.setdefault("values", {})
    secrets_dict = profile_data.setdefault("secrets", {})

    if is_secret:
        str_val = str(value)
        status = get_vault_status(config_file)
        if status["initialized"]:
            stored_val = encrypt_secret(str_val, config_file=config_file)
            encrypted = True
        else:
            stored_val = str_val
            encrypted = False

        secrets_dict[key] = {
            "encrypted": encrypted,
            "value": stored_val,
        }
        values_dict.pop(key, None)
    else:
        values_dict[key] = value
        secrets_dict.pop(key, None)

    save_config(config, config_file)
    record_history(
        action="SET_SECRET" if is_secret else "SET",
        profile=target_profile,
        key=key,
        is_secret=is_secret,
        config_file=config_file,
    )


def get_config(
    key: str,
    profile: str | None = None,
    show_secret: bool = False,
    config_file: Path | None = None,
) -> Any:
    """Get configuration value. Secrets require explicit show_secret=True."""
    config = load_config(config_file)
    target_profile, profile_data = _resolve_profile(config, profile)

    values_dict = profile_data.get("values", {})
    secrets_dict = profile_data.get("secrets", {})

    if key in values_dict:
        return values_dict[key]

    if key in secrets_dict:
        if not show_secret:
            raise SecretMaskedError(
                f"Key '{key}' is a secret. Use 'devvault secret get {key}' "
                "or --show to reveal."
            )
        sec_info = secrets_dict[key]
        if isinstance(sec_info, dict) and sec_info.get("encrypted"):
            return decrypt_secret(sec_info["value"], config_file=config_file)
        elif isinstance(sec_info, dict):
            return sec_info.get("value", "")
        return str(sec_info)

    raise ConfigKeyNotFoundError(f"Key '{key}' not found.")


def list_config(
    profile: str | None = None,
    include_secrets: bool = True,
    config_file: Path | None = None,
) -> list[str]:
    """List configuration keys in the specified profile preserving insertion order."""
    config = load_config(config_file)
    _, profile_data = _resolve_profile(config, profile)

    keys = list(profile_data.get("values", {}).keys())
    if include_secrets:
        for sec_k in profile_data.get("secrets", {}).keys():
            if sec_k not in keys:
                keys.append(sec_k)
    return keys


def list_secrets(
    profile: str | None = None,
    config_file: Path | None = None,
) -> list[str]:
    """List only secret keys in the specified profile."""
    config = load_config(config_file)
    _, profile_data = _resolve_profile(config, profile)
    return list(profile_data.get("secrets", {}).keys())


def remove_config(
    key: str,
    profile: str | None = None,
    config_file: Path | None = None,
) -> bool:
    """Remove a key from either normal values or secrets."""
    config = load_config(config_file)
    target_profile, profile_data = _resolve_profile(config, profile)

    values_dict = profile_data.get("values", {})
    secrets_dict = profile_data.get("secrets", {})

    is_secret = key in secrets_dict
    removed = False

    if key in values_dict:
        del values_dict[key]
        removed = True
    elif key in secrets_dict:
        del secrets_dict[key]
        removed = True

    if removed:
        save_config(config, config_file)
        record_history(
            action="REMOVE",
            profile=target_profile,
            key=key,
            is_secret=is_secret,
            config_file=config_file,
        )

    return removed


def get_all_entries(
    profile: str | None = None,
    reveal_secrets: bool = False,
    config_file: Path | None = None,
) -> dict[str, Any]:
    """Return entries with secrets masked unless reveal_secrets=True."""
    config = load_config(config_file)
    _, profile_data = _resolve_profile(config, profile)

    result: dict[str, Any] = dict(profile_data.get("values", {}))
    for sec_key, sec_data in profile_data.get("secrets", {}).items():
        if reveal_secrets:
            if isinstance(sec_data, dict) and sec_data.get("encrypted"):
                result[sec_key] = decrypt_secret(
                    sec_data["value"], config_file=config_file
                )
            elif isinstance(sec_data, dict):
                result[sec_key] = sec_data.get("value", "")
            else:
                result[sec_key] = str(sec_data)
        else:
            result[sec_key] = MASKED_SECRET_PLACEHOLDER

    return result
