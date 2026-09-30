from pathlib import Path
from typing import Any

from devvault.config import _resolve_profile, parse_value, validate_key
from devvault.storage import load_config, save_config


def parse_dotenv_line(line: str, line_num: int = 1) -> tuple[str, Any] | None:
    """Parse a single line from a dotenv file."""
    stripped = line.strip()
    if not stripped or stripped.startswith("#"):
        return None

    if "=" not in stripped:
        raise ValueError(f"Malformed line {line_num}: missing '=' separator.")

    raw_key, raw_val = stripped.split("=", 1)
    key = raw_key.strip()
    if not key:
        raise ValueError(f"Malformed line {line_num}: key cannot be empty.")

    validate_key(key)

    val = raw_val.strip()
    if len(val) >= 2 and (
        (val.startswith('"') and val.endswith('"'))
        or (val.startswith("'") and val.endswith("'"))
    ):
        val = val[1:-1]

    parsed_value = parse_value(val)
    return key, parsed_value


def parse_dotenv(content: str) -> dict[str, Any]:
    """Parse entire dotenv content into key-value pairs."""
    entries: dict[str, Any] = {}
    for line_num, line in enumerate(content.splitlines(), start=1):
        parsed = parse_dotenv_line(line, line_num)
        if parsed is not None:
            key, value = parsed
            entries[key] = value
    return entries


def import_env_file(
    file_path: Path | str,
    profile: str | None = None,
    force: bool = False,
    config_file: Path | None = None,
) -> tuple[str, int, int]:
    """Import key-value pairs from a dotenv file into the target profile."""
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"File '{file_path}' not found.")

    if path.is_dir():
        raise ValueError(f"Path '{file_path}' is a directory, not a file.")

    content = path.read_text(encoding="utf-8")
    entries = parse_dotenv(content)

    config = load_config(config_file)
    target_profile, profile_data = _resolve_profile(config, profile)

    imported_count = 0
    skipped_count = 0

    for key, value in entries.items():
        if key in profile_data and not force:
            skipped_count += 1
        else:
            profile_data[key] = value
            imported_count += 1

    if imported_count > 0:
        save_config(config, config_file)

    return target_profile, imported_count, skipped_count
