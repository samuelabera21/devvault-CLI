from pathlib import Path
from typing import Any

from devvault.config import _resolve_profile, get_all_entries
from devvault.history import record_history
from devvault.storage import load_config


def format_dotenv_value(value: Any) -> str:
    """Format a Python primitive value into a safe dotenv-compatible string."""
    if isinstance(value, bool):
        return "true" if value else "false"

    if isinstance(value, (int, float)):
        return str(value)

    str_val = str(value)
    if str_val == "":
        return '""'

    # Check if quoting is needed for spaces, hashes, equals, quotes, or newlines
    needs_quotes = any(
        ch in str_val for ch in (" ", "\t", "#", "=", "\n", "\r", '"', "'")
    )

    if needs_quotes:
        if '"' not in str_val:
            return f'"{str_val}"'
        elif "'" not in str_val:
            return f"'{str_val}'"
        else:
            escaped = str_val.replace('"', '\\"')
            return f'"{escaped}"'

    return str_val


def format_dotenv(entries: dict[str, Any]) -> str:
    """Format dictionary entries into dotenv lines."""
    lines = [f"{key}={format_dotenv_value(val)}" for key, val in entries.items()]
    if lines:
        return "\n".join(lines) + "\n"
    return ""


def export_env_file(
    file_path: Path | str,
    profile: str | None = None,
    force: bool = False,
    config_file: Path | None = None,
) -> tuple[str, int]:
    """Export configuration entries from the target profile to a dotenv file."""
    path = Path(file_path)

    if path.is_dir():
        raise ValueError(f"Path '{file_path}' is a directory, not a file.")

    if path.exists() and not force:
        raise FileExistsError(
            f"File '{file_path}' already exists. Use --force to overwrite."
        )

    config = load_config(config_file)
    target_profile, _ = _resolve_profile(config, profile)

    entries = get_all_entries(
        profile=target_profile, reveal_secrets=True, config_file=config_file
    )

    content = format_dotenv(entries)
    path.write_text(content, encoding="utf-8")

    record_history(
        action="EXPORT",
        profile=target_profile,
        key=str(path.name),
        is_secret=False,
        config_file=config_file,
    )

    return target_profile, len(entries)
