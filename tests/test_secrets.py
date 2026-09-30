import pytest

from devvault.config import (
    get_all_entries,
    get_config,
    initialize_config,
    list_config,
    list_secrets,
    remove_config,
    set_config,
)
from devvault.exceptions import SecretMaskedError


def test_set_and_get_secret(tmp_path):
    cfg = tmp_path / "config.json"
    initialize_config(cfg)

    set_config("API_KEY", "secret_12345", is_secret=True, config_file=cfg)

    # Calling get_config without show_secret=True must raise SecretMaskedError
    with pytest.raises(SecretMaskedError):
        get_config("API_KEY", show_secret=False, config_file=cfg)

    # Calling with show_secret=True returns plaintext
    val = get_config("API_KEY", show_secret=True, config_file=cfg)
    assert val == "secret_12345"


def test_list_secrets(tmp_path):
    cfg = tmp_path / "config.json"
    initialize_config(cfg)

    set_config("PUBLIC_KEY", "hello", is_secret=False, config_file=cfg)
    set_config("SECRET_KEY", "super_secret", is_secret=True, config_file=cfg)

    all_keys = list_config(config_file=cfg)
    assert all_keys == ["PUBLIC_KEY", "SECRET_KEY"]

    secrets_only = list_secrets(config_file=cfg)
    assert secrets_only == ["SECRET_KEY"]


def test_get_all_entries_masking(tmp_path):
    cfg = tmp_path / "config.json"
    initialize_config(cfg)

    set_config("APP_NAME", "VaultApp", is_secret=False, config_file=cfg)
    set_config("API_SECRET", "super_secret_value", is_secret=True, config_file=cfg)

    # Masked
    masked_entries = get_all_entries(reveal_secrets=False, config_file=cfg)
    assert masked_entries["APP_NAME"] == "VaultApp"
    assert masked_entries["API_SECRET"] == "********"

    # Revealed
    revealed_entries = get_all_entries(reveal_secrets=True, config_file=cfg)
    assert revealed_entries["API_SECRET"] == "super_secret_value"


def test_remove_secret(tmp_path):
    cfg = tmp_path / "config.json"
    initialize_config(cfg)

    set_config("TOKEN", "my_token", is_secret=True, config_file=cfg)
    assert "TOKEN" in list_secrets(config_file=cfg)

    removed = remove_config("TOKEN", config_file=cfg)
    assert removed is True
    assert "TOKEN" not in list_secrets(config_file=cfg)
