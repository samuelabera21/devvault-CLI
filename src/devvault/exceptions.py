"""Exceptions for DevVault."""


class DevVaultError(Exception):
    """Base exception for DevVault errors."""


class ConfigKeyNotFoundError(DevVaultError):
    """Raised when a configuration key is not found."""


class ProfileNotFoundError(DevVaultError):
    """Raised when a specified profile does not exist."""


class ProfileAlreadyExistsError(DevVaultError):
    """Raised when attempting to create a profile that already exists."""


class ProfileError(DevVaultError):
    """Raised when a profile operation is invalid."""
