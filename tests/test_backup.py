import json
import pytest

from devvault.backup import create_backup, restore_backup
from devvault.config import get_config, initialize_config, set_config
from devvault.exceptions import CorruptedBackupError
from devvault.profiles import create_profile


def test_backup_and_restore(tmp_path):
    src_cfg = tmp_path / "src_config.json"
    initialize_config(src_cfg)
    create_profile("staging", config_file=src_cfg)

    set_config("PORT", 8000, profile="default", config_file=src_cfg)
    set_config(
        "API_URL", "https://staging.internal", profile="staging", config_file=src_cfg
    )

    backup_file = tmp_path / "devvault.backup"
    create_backup(backup_file, config_file=src_cfg)

    assert backup_file.exists()

    # Restore into fresh destination config
    dest_cfg = tmp_path / "dest_config.json"
    initialize_config(dest_cfg)
    restore_backup(backup_file, config_file=dest_cfg)

    assert get_config("PORT", profile="default", config_file=dest_cfg) == 8000
    assert (
        get_config("API_URL", profile="staging", config_file=dest_cfg)
        == "https://staging.internal"
    )


def test_backup_overwrite_protection(tmp_path):
    cfg = tmp_path / "config.json"
    initialize_config(cfg)

    backup_file = tmp_path / "devvault.backup"
    create_backup(backup_file, config_file=cfg)

    with pytest.raises(FileExistsError):
        create_backup(backup_file, force=False, config_file=cfg)

    create_backup(backup_file, force=True, config_file=cfg)


def test_corrupted_backup_detection(tmp_path):
    cfg = tmp_path / "config.json"
    initialize_config(cfg)
    set_config("PORT", 8000, config_file=cfg)

    backup_file = tmp_path / "tampered.backup"
    create_backup(backup_file, config_file=cfg)

    # Tamper with payload
    data = json.loads(backup_file.read_text(encoding="utf-8"))
    data["payload"]["profiles"]["default"]["values"]["PORT"] = 9999
    backup_file.write_text(json.dumps(data), encoding="utf-8")

    dest_cfg = tmp_path / "dest.json"
    initialize_config(dest_cfg)

    with pytest.raises(CorruptedBackupError, match="checksum mismatch"):
        restore_backup(backup_file, config_file=dest_cfg)
