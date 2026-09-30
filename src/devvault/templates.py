from pathlib import Path
from typing import Any

from devvault.config import _resolve_profile
from devvault.exceptions import TemplateError, TemplateNotFoundError
from devvault.history import record_history
from devvault.storage import load_config, save_config

BUILTIN_TEMPLATES: dict[str, dict[str, Any]] = {
    "python-api": {
        "APP_NAME": "python-api",
        "PORT": 8000,
        "DEBUG": True,
        "LOG_LEVEL": "INFO",
    },
    "fastapi": {
        "APP_NAME": "fastapi-service",
        "HOST": "0.0.0.0",
        "PORT": 8000,
        "DEBUG": True,
    },
    "django": {
        "DJANGO_SETTINGS_MODULE": "config.settings",
        "PORT": 8000,
        "DEBUG": True,
    },
    "node-api": {
        "NODE_ENV": "development",
        "PORT": 3000,
        "LOG_LEVEL": "debug",
    },
    "nextjs": {
        "NODE_ENV": "development",
        "PORT": 3000,
        "NEXT_PUBLIC_API_URL": "http://localhost:8000",
    },
}


def list_templates(config_file: Path | None = None) -> list[str]:
    """List all available built-in and user templates."""
    custom_templates: dict[str, Any] = {}
    try:
        config = load_config(config_file)
        custom_templates = config.get("templates", {})
    except Exception:
        pass

    all_names = set(BUILTIN_TEMPLATES.keys()) | set(custom_templates.keys())
    return sorted(all_names)


def get_template(name: str, config_file: Path | None = None) -> dict[str, Any]:
    """Retrieve template definition by name."""
    if name in BUILTIN_TEMPLATES:
        return dict(BUILTIN_TEMPLATES[name])

    config = load_config(config_file)
    custom_templates = config.get("templates", {})
    if name in custom_templates:
        return dict(custom_templates[name])

    raise TemplateNotFoundError(f"Template '{name}' not found.")


def create_template(
    name: str,
    data: dict[str, Any],
    config_file: Path | None = None,
) -> None:
    """Create a user configuration template."""
    if not name or not isinstance(name, str):
        raise ValueError("Template name cannot be empty.")

    if not isinstance(data, dict):
        raise TemplateError("Template data must be a dictionary.")

    config = load_config(config_file)
    templates = config.setdefault("templates", {})
    templates[name] = data
    save_config(config, config_file)


def apply_template(
    name: str,
    profile: str | None = None,
    force: bool = False,
    config_file: Path | None = None,
) -> tuple[str, int, int]:
    """Apply template values to the target profile."""
    template_data = get_template(name, config_file)
    config = load_config(config_file)
    target_profile, profile_data = _resolve_profile(config, profile)

    values_dict = profile_data.setdefault("values", {})
    applied_count = 0
    skipped_count = 0

    for key, value in template_data.items():
        if key in values_dict and not force:
            skipped_count += 1
        else:
            values_dict[key] = value
            applied_count += 1

    if applied_count > 0:
        save_config(config, config_file)
        record_history(
            action="TEMPLATE_APPLY",
            profile=target_profile,
            key=name,
            is_secret=False,
            config_file=config_file,
        )

    return target_profile, applied_count, skipped_count
