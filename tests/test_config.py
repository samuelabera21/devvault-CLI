import pytest

from devvault.config import (
    get_config,
    initialize_config,
    list_config,
    remove_config,
    set_config,
)
from devvault.exceptions import ConfigKeyNotFoundError, ProfileNotFoundError
from devvault.profiles import create_profile


def test_set_config(tmp_path):
    config_file = tmp_path / "config.json"
    initialize_config(config_file)

    set_config("TEST_KEY", "hello", config_file=config_file)

    value = get_config("TEST_KEY", config_file=config_file)

    assert value == "hello"


def test_set_config_explicit_profile(tmp_path):
    config_file = tmp_path / "config.json"
    initialize_config(config_file)
    create_profile("production", config_file=config_file)

    set_config(
        "API_URL",
        "https://api.example.com",
        profile="production",
        config_file=config_file,
    )
    value = get_config("API_URL", profile="production", config_file=config_file)

    assert value == "https://api.example.com"


def test_get_config(tmp_path):
    config_file = tmp_path / "config.json"
    initialize_config(config_file)
    set_config("NAME", "Samuel", config_file=config_file)

    value = get_config("NAME", config_file=config_file)

    assert value == "Samuel"


def test_get_config_missing_key(tmp_path):
    config_file = tmp_path / "config.json"
    initialize_config(config_file)

    with pytest.raises(ConfigKeyNotFoundError):
        get_config("DOES_NOT_EXIST", config_file=config_file)


def test_get_config_nonexistent_profile(tmp_path):
    config_file = tmp_path / "config.json"
    initialize_config(config_file)

    with pytest.raises(ProfileNotFoundError):
        get_config("ANY_KEY", profile="nonexistent", config_file=config_file)


def test_list_config(tmp_path):
    config_file = tmp_path / "config.json"
    initialize_config(config_file)
    set_config("NAME", "Samuel", config_file=config_file)
    set_config("DEBUG", True, config_file=config_file)

    keys = list_config(config_file=config_file)

    assert list(keys) == ["NAME", "DEBUG"]


def test_list_config_with_profile(tmp_path):
    config_file = tmp_path / "config.json"
    initialize_config(config_file)
    create_profile("dev", config_file=config_file)
    set_config("PORT", 3000, profile="dev", config_file=config_file)

    keys = list_config(profile="dev", config_file=config_file)
    assert keys == ["PORT"]

    default_keys = list_config(config_file=config_file)
    assert default_keys == []


def test_remove_config(tmp_path):
    config_file = tmp_path / "config.json"
    initialize_config(config_file)
    set_config("NAME", "Samuel", config_file=config_file)
    set_config("DEBUG", True, config_file=config_file)

    removed = remove_config("NAME", config_file=config_file)

    assert removed is True
    assert get_config("DEBUG", config_file=config_file) is True


def test_remove_config_missing_key(tmp_path):
    config_file = tmp_path / "config.json"
    initialize_config(config_file)

    removed = remove_config("MISSING", config_file=config_file)
    assert removed is False


def test_initialize_config(tmp_path):
    config_file = tmp_path / "config.json"

    initialize_config(config_file)

    assert config_file.exists()


def test_initialize_config_already_exists(tmp_path):
    config_file = tmp_path / "config.json"
    initialize_config(config_file)

    with pytest.raises(FileExistsError):
        initialize_config(config_file)


def test_legacy_flat_config_backward_compatibility(tmp_path):
    # Test loading legacy config format: {"NAME": "Samuel", "DEBUG": true}
    config_file = tmp_path / "config.json"
    config_file.write_text('{"NAME": "Samuel", "DEBUG": true}', encoding="utf-8")

    assert get_config("NAME", config_file=config_file) == "Samuel"
    assert get_config("DEBUG", config_file=config_file) is True
    assert list_config(config_file=config_file) == ["NAME", "DEBUG"]

    # Writing a new key should preserve structure and data
    set_config("PORT", 8000, config_file=config_file)
    assert get_config("PORT", config_file=config_file) == 8000
