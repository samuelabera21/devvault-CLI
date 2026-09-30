import pytest

from devvault.config import get_config, initialize_config, set_config
from devvault.exceptions import (
    ProfileAlreadyExistsError,
    ProfileError,
    ProfileNotFoundError,
)
from devvault.profiles import (
    create_profile,
    delete_profile,
    get_active_profile,
    list_profiles,
    set_active_profile,
    validate_profile_name,
)


def test_validate_profile_name_valid():
    validate_profile_name("dev")
    validate_profile_name("staging_1")
    validate_profile_name("prod-us-east")
    validate_profile_name("_internal")


def test_validate_profile_name_invalid():
    invalid_names = [
        "",
        "dev env",
        "-invalid",
        "dev/staging",
        "dev@vault",
    ]
    for name in invalid_names:
        with pytest.raises(ValueError):
            validate_profile_name(name)


def test_create_and_list_profiles(tmp_path):
    config_file = tmp_path / "config.json"
    initialize_config(config_file)

    assert list_profiles(config_file) == ["default"]
    assert get_active_profile(config_file) == "default"

    create_profile("dev", config_file)
    create_profile("staging", config_file)

    assert list_profiles(config_file) == ["default", "dev", "staging"]


def test_create_duplicate_profile(tmp_path):
    config_file = tmp_path / "config.json"
    initialize_config(config_file)

    create_profile("dev", config_file)
    with pytest.raises(ProfileAlreadyExistsError):
        create_profile("dev", config_file)


def test_set_and_get_active_profile(tmp_path):
    config_file = tmp_path / "config.json"
    initialize_config(config_file)

    create_profile("dev", config_file)
    set_active_profile("dev", config_file)

    assert get_active_profile(config_file) == "dev"


def test_set_active_profile_not_found(tmp_path):
    config_file = tmp_path / "config.json"
    initialize_config(config_file)

    with pytest.raises(ProfileNotFoundError):
        set_active_profile("nonexistent", config_file)


def test_delete_profile(tmp_path):
    config_file = tmp_path / "config.json"
    initialize_config(config_file)

    create_profile("staging", config_file)
    assert "staging" in list_profiles(config_file)

    delete_profile("staging", config_file)
    assert "staging" not in list_profiles(config_file)


def test_delete_profile_not_found(tmp_path):
    config_file = tmp_path / "config.json"
    initialize_config(config_file)

    with pytest.raises(ProfileNotFoundError):
        delete_profile("does_not_exist", config_file)


def test_delete_active_profile_prevented(tmp_path):
    config_file = tmp_path / "config.json"
    initialize_config(config_file)

    create_profile("dev", config_file)
    set_active_profile("dev", config_file)

    with pytest.raises(ProfileError, match="Cannot delete the active profile"):
        delete_profile("dev", config_file)


def test_delete_only_default_profile_prevented(tmp_path):
    config_file = tmp_path / "config.json"
    initialize_config(config_file)

    with pytest.raises(ProfileError):
        delete_profile("default", config_file)


def test_profile_data_isolation(tmp_path):
    config_file = tmp_path / "config.json"
    initialize_config(config_file)

    create_profile("dev", config_file)
    create_profile("staging", config_file)

    set_config("DB_HOST", "localhost", profile="dev", config_file=config_file)
    set_config(
        "DB_HOST", "staging.db.internal", profile="staging", config_file=config_file
    )

    assert get_config("DB_HOST", profile="dev", config_file=config_file) == "localhost"
    assert (
        get_config("DB_HOST", profile="staging", config_file=config_file)
        == "staging.db.internal"
    )

    set_active_profile("dev", config_file)
    assert get_config("DB_HOST", config_file=config_file) == "localhost"

    set_active_profile("staging", config_file)
    assert get_config("DB_HOST", config_file=config_file) == "staging.db.internal"
