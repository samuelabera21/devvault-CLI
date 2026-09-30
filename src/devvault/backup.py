import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from devvault.exceptions import CorruptedBackupError
from devvault.history import record_history
from devvault.storage import DEFAULT_PROFILE, load_config, normalize_config, save_config


def _calculate_checksum(data: dict[str, Any]) -> str:
    """Calculate SHA-256 checksum of payload data for corruption detection."""
    serialized = json.dumps(data, sort_keys=True)
    return hashlib.sha256(serialized.encode("utf-8")).hexdigest()


def create_backup(
    destination_file: Path | str,
    force: bool = False,
    config_file: Path | None = None,
) -> Path:
    """Create a verified configuration backup archive."""
    dest = Path(destination_file)
    if dest.is_dir():
        raise ValueError(f"Destination '{dest}' is a directory, not a file.")

    if dest.exists() and not force:
        raise FileExistsError(
            f"Backup file '{dest}' already exists. Use --force to overwrite."
        )

    config_data = load_config(config_file)
    checksum = _calculate_checksum(config_data)

    backup_payload: dict[str, Any] = {
        "devvault_backup_version": "1.0",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "checksum": checksum,
        "payload": config_data,
    }

    dest.parent.mkdir(parents=True, exist_ok=True)
    with dest.open("w", encoding="utf-8") as f:
        json.dump(backup_payload, f, indent=4)

    record_history(
        action="BACKUP_CREATE",
        profile=config_data.get("active_profile", DEFAULT_PROFILE),
        key=str(dest.name),
        is_secret=False,
        config_file=config_file,
    )

    return dest


def restore_backup(
    source_file: Path | str,
    force: bool = False,
    config_file: Path | None = None,
) -> None:
    """Validate and restore configuration from a backup archive."""
    src = Path(source_file)
    if not src.exists():
        raise FileNotFoundError(f"Backup file '{src}' not found.")

    if src.is_dir():
        raise ValueError(f"Source '{src}' is a directory, not a file.")

    try:
        with src.open("r", encoding="utf-8") as f:
            backup_data = json.load(f)
    except json.JSONDecodeError:
        raise CorruptedBackupError("Corrupted backup file: invalid JSON.")

    if not isinstance(backup_data, dict):
        raise CorruptedBackupError("Invalid backup format: expected JSON object.")

    if "payload" not in backup_data or "checksum" not in backup_data:
        raise CorruptedBackupError(
            "Invalid backup archive: missing payload or checksum."
        )

    payload = backup_data["payload"]
    expected_checksum = backup_data["checksum"]
    actual_checksum = _calculate_checksum(payload)

    if expected_checksum != actual_checksum:
        raise CorruptedBackupError(
            "Backup checksum mismatch. Data is corrupted or modified."
        )

    normalized = normalize_config(payload)
    save_config(normalized, config_file)

    record_history(
        action="BACKUP_RESTORE",
        profile=normalized.get("active_profile", DEFAULT_PROFILE),
        key=str(src.name),
        is_secret=False,
        config_file=config_file,
    )
