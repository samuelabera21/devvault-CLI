from pathlib import Path
from typing import Any

from devvault.config import _resolve_profile, get_all_entries
from devvault.exceptions import SchemaError
from devvault.storage import load_config, save_config

VALID_TYPES = {"string", "integer", "int", "float", "number", "boolean", "bool"}


def set_schema_rule(
    key: str, rule: dict[str, Any], config_file: Path | None = None
) -> None:
    """Set a validation schema rule for a key."""
    if not isinstance(rule, dict):
        raise SchemaError("Schema rule must be a dictionary.")

    rule_type = rule.get("type")
    if rule_type and str(rule_type).lower() not in VALID_TYPES:
        valid_list = ", ".join(sorted(VALID_TYPES))
        raise SchemaError(
            f"Invalid schema type '{rule_type}'. Valid types: {valid_list}"
        )

    config = load_config(config_file)
    schema = config.setdefault("schema", {})
    schema[key] = rule
    save_config(config, config_file)


def get_schema(config_file: Path | None = None) -> dict[str, Any]:
    """Retrieve the configuration schema."""
    config = load_config(config_file)
    return dict(config.get("schema", {}))


def validate_profile(
    profile: str | None = None,
    schema_override: dict[str, Any] | None = None,
    config_file: Path | None = None,
) -> list[str]:
    """Validate profile against the schema. Returns list of error messages."""
    config = load_config(config_file)
    target_profile, _ = _resolve_profile(config, profile)
    schema = (
        schema_override if schema_override is not None else config.get("schema", {})
    )

    if not schema:
        return []

    # Check entries (secrets are revealed internally for type checks without leaking)
    entries = get_all_entries(
        profile=target_profile, reveal_secrets=True, config_file=config_file
    )

    errors: list[str] = []

    for rule_key, rule in schema.items():
        if not isinstance(rule, dict):
            continue

        is_required = bool(rule.get("required", False))
        expected_type = str(rule.get("type", "")).lower() if rule.get("type") else None
        min_val = rule.get("min")
        max_val = rule.get("max")
        allowed_vals = rule.get("allowed_values")

        if rule_key not in entries:
            if is_required:
                errors.append(f"Missing required key '{rule_key}'.")
            continue

        val = entries[rule_key]

        # Type checks
        if expected_type in ("boolean", "bool"):
            if not isinstance(val, bool):
                errors.append(
                    f"Key '{rule_key}': expected boolean, got {type(val).__name__}."
                )
        elif expected_type in ("integer", "int"):
            if not isinstance(val, int) or isinstance(val, bool):
                errors.append(
                    f"Key '{rule_key}': expected integer, got {type(val).__name__}."
                )
        elif expected_type in ("float", "number"):
            if not isinstance(val, (int, float)) or isinstance(val, bool):
                errors.append(
                    f"Key '{rule_key}': expected number, got {type(val).__name__}."
                )
        elif expected_type == "string":
            if not isinstance(val, str):
                errors.append(
                    f"Key '{rule_key}': expected string, got {type(val).__name__}."
                )

        # Range checks on numbers
        if isinstance(val, (int, float)) and not isinstance(val, bool):
            if min_val is not None and val < min_val:
                errors.append(f"Key '{rule_key}': value must be at least {min_val}.")
            if max_val is not None and val > max_val:
                errors.append(f"Key '{rule_key}': value must be at most {max_val}.")

        # Allowed values
        if allowed_vals is not None and isinstance(allowed_vals, list):
            if val not in allowed_vals:
                errors.append(f"Key '{rule_key}': value must be one of {allowed_vals}.")

    return errors


def run_validation(
    profile: str | None = None,
    config_file: Path | None = None,
) -> tuple[str, list[str]]:
    """Run validation and return (target_profile, errors)."""
    config = load_config(config_file)
    target_profile, _ = _resolve_profile(config, profile)
    errors = validate_profile(profile=target_profile, config_file=config_file)
    return target_profile, errors
