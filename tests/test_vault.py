import pytest

from devvault.config import get_config, initialize_config, set_config
from devvault.exceptions import (
    InvalidPassphraseError,
    VaultError,
    VaultLockedError,
    VaultNotInitializedError,
)
from devvault.security import (
    get_vault_status,
    init_vault,
    lock_vault,
    unlock_vault,
)


def test_vault_init_and_status(tmp_path):
    cfg = tmp_path / "config.json"
    initialize_config(cfg)

    status_before = get_vault_status(cfg)
    assert status_before["initialized"] is False

    init_vault("master_password_123", config_file=cfg)

    status_after = get_vault_status(cfg)
    assert status_after["initialized"] is True
    assert status_after["unlocked"] is True


def test_vault_reinit_error(tmp_path):
    cfg = tmp_path / "config.json"
    initialize_config(cfg)

    init_vault("password", config_file=cfg)
    with pytest.raises(VaultError):
        init_vault("another_password", config_file=cfg)


def test_vault_lock_and_unlock(tmp_path):
    cfg = tmp_path / "config.json"
    initialize_config(cfg)

    init_vault("correct_passphrase", config_file=cfg)
    set_config("SECRET_API", "secret_payload", is_secret=True, config_file=cfg)

    # Lock vault
    lock_vault()
    status_locked = get_vault_status(cfg)
    assert status_locked["unlocked"] is False

    # Attempting to read decrypted secret while locked must raise VaultLockedError
    with pytest.raises(VaultLockedError):
        get_config("SECRET_API", show_secret=True, config_file=cfg)

    # Unlock with wrong passphrase
    with pytest.raises(InvalidPassphraseError):
        unlock_vault("wrong_passphrase", config_file=cfg)

    # Unlock with correct passphrase
    unlock_vault("correct_passphrase", config_file=cfg)
    assert (
        get_config("SECRET_API", show_secret=True, config_file=cfg) == "secret_payload"
    )


def test_vault_uninitialized_error(tmp_path):
    cfg = tmp_path / "config.json"
    initialize_config(cfg)

    with pytest.raises(VaultNotInitializedError):
        unlock_vault("any_passphrase", config_file=cfg)
