import base64
import os
from pathlib import Path

from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

from devvault.exceptions import (
    InvalidPassphraseError,
    VaultError,
    VaultLockedError,
    VaultNotInitializedError,
)
from devvault.storage import load_config, save_config

# In-memory active key cache for the current session
_ACTIVE_FERNET_KEY: str | None = None
VERIFICATION_STRING = "DEVVAULT_VERIFY_OK"


def _derive_fernet_key(passphrase: str, salt: bytes) -> str:
    """Derive a URL-safe base64-encoded 32-byte key from passphrase and salt."""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100_000,
    )
    key_bytes = kdf.derive(passphrase.encode("utf-8"))
    return base64.urlsafe_b64encode(key_bytes).decode("utf-8")


def set_session_key(fernet_key: str | None) -> None:
    """Set the active encryption key for the current process session."""
    global _ACTIVE_FERNET_KEY
    _ACTIVE_FERNET_KEY = fernet_key


def get_session_key() -> str | None:
    """Retrieve active session key, checking env var DEVVAULT_KEY as fallback."""
    global _ACTIVE_FERNET_KEY
    if _ACTIVE_FERNET_KEY:
        return _ACTIVE_FERNET_KEY
    env_key = os.environ.get("DEVVAULT_KEY")
    if env_key:
        return env_key
    return None


def init_vault(passphrase: str, config_file: Path | None = None) -> None:
    """Initialize the encryption vault with a passphrase."""
    if not passphrase:
        raise ValueError("Vault passphrase cannot be empty.")

    config = load_config(config_file)
    vault_data = config.get("vault", {})

    if vault_data.get("initialized"):
        raise VaultError("Vault is already initialized.")

    salt = os.urandom(16)
    salt_b64 = base64.b64encode(salt).decode("utf-8")
    fernet_key = _derive_fernet_key(passphrase, salt)

    f = Fernet(fernet_key.encode("utf-8"))
    token = f.encrypt(VERIFICATION_STRING.encode("utf-8")).decode("utf-8")

    config["vault"] = {
        "initialized": True,
        "salt": salt_b64,
        "verifier": token,
    }
    save_config(config, config_file)
    set_session_key(fernet_key)


def unlock_vault(passphrase: str, config_file: Path | None = None) -> str:
    """Unlock the vault using passphrase and set active session key."""
    if not passphrase:
        raise ValueError("Vault passphrase cannot be empty.")

    config = load_config(config_file)
    vault_data = config.get("vault", {})

    if not vault_data.get("initialized"):
        raise VaultNotInitializedError(
            "Vault is not initialized. Run 'devvault vault init' first."
        )

    salt_b64 = vault_data.get("salt")
    verifier = vault_data.get("verifier")

    if not salt_b64 or not verifier:
        raise VaultError("Vault data is corrupted.")

    salt = base64.b64decode(salt_b64.encode("utf-8"))
    fernet_key = _derive_fernet_key(passphrase, salt)

    try:
        f = Fernet(fernet_key.encode("utf-8"))
        decrypted = f.decrypt(verifier.encode("utf-8")).decode("utf-8")
        if decrypted != VERIFICATION_STRING:
            raise InvalidPassphraseError("Invalid passphrase.")
    except (InvalidToken, Exception):
        raise InvalidPassphraseError("Invalid passphrase.")

    set_session_key(fernet_key)
    return fernet_key


def lock_vault() -> None:
    """Lock the vault by clearing session key."""
    set_session_key(None)


def get_vault_status(config_file: Path | None = None) -> dict[str, bool]:
    """Get the current vault initialization and lock status."""
    try:
        config = load_config(config_file)
        vault_data = config.get("vault", {})
        initialized = bool(vault_data.get("initialized", False))
    except FileNotFoundError:
        initialized = False
    unlocked = bool(get_session_key() is not None)
    return {
        "initialized": initialized,
        "unlocked": unlocked,
    }


def encrypt_secret(
    plaintext: str,
    key: str | None = None,
    config_file: Path | None = None,
) -> str:
    """Encrypt a plaintext string using the active or provided Fernet key."""
    active_key = key or get_session_key()
    if not active_key:
        status = get_vault_status(config_file)
        if not status["initialized"]:
            raise VaultNotInitializedError(
                "Vault is not initialized. Run 'devvault vault init' first."
            )
        raise VaultLockedError("Vault is locked. Unlock the vault or set DEVVAULT_KEY.")

    f = Fernet(active_key.encode("utf-8"))
    return f.encrypt(plaintext.encode("utf-8")).decode("utf-8")


def decrypt_secret(
    encrypted_token: str,
    key: str | None = None,
    config_file: Path | None = None,
) -> str:
    """Decrypt an encrypted token using the active or provided Fernet key."""
    active_key = key or get_session_key()
    if not active_key:
        status = get_vault_status(config_file)
        if not status["initialized"]:
            raise VaultNotInitializedError(
                "Vault is not initialized. Run 'devvault vault init' first."
            )
        raise VaultLockedError("Vault is locked. Unlock the vault or set DEVVAULT_KEY.")

    try:
        f = Fernet(active_key.encode("utf-8"))
        return f.decrypt(encrypted_token.encode("utf-8")).decode("utf-8")
    except InvalidToken:
        raise VaultError("Failed to decrypt secret: invalid key or corrupted data.")
