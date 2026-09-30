"""Exceptions for DevVault."""


class DevVaultError(Exception):
    """Base exception for all DevVault errors."""


class ConfigKeyNotFoundError(DevVaultError):
    """Raised when a configuration key is not found."""


class ProfileNotFoundError(DevVaultError):
    """Raised when a specified profile does not exist."""


class ProfileAlreadyExistsError(DevVaultError):
    """Raised when attempting to create a profile that already exists."""


class ProfileError(DevVaultError):
    """Raised when a profile operation is invalid."""


class SecretMaskedError(DevVaultError):
    """Raised when a secret value is accessed without explicit authorization."""


class VaultError(DevVaultError):
    """Base exception for encryption vault errors."""


class VaultNotInitializedError(VaultError):
    """Raised when attempting a vault operation on an uninitialized vault."""


class VaultLockedError(VaultError):
    """Raised when attempting to access encrypted data while vault is locked."""


class InvalidPassphraseError(VaultError):
    """Raised when an invalid vault passphrase is provided."""


class ValidationError(DevVaultError):
    """Raised when configuration validation fails."""


class SchemaError(DevVaultError):
    """Raised when a configuration schema definition is invalid."""


class BackupError(DevVaultError):
    """Raised when backup or restore fails."""


class CorruptedBackupError(BackupError):
    """Raised when a backup archive is corrupted or invalid."""


class TemplateError(DevVaultError):
    """Raised when template operations fail."""


class TemplateNotFoundError(TemplateError):
    """Raised when a requested configuration template does not exist."""


class ExecutionError(DevVaultError):
    """Raised when running a child process fails."""
