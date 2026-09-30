from devvault.config import initialize_config, set_config
from devvault.diff import compare_profiles, format_diff_text
from devvault.profiles import create_profile


def test_diff_identical_profiles(tmp_path):
    cfg = tmp_path / "config.json"
    initialize_config(cfg)
    create_profile("staging", config_file=cfg)

    set_config("PORT", 8000, profile="default", config_file=cfg)
    set_config("PORT", 8000, profile="staging", config_file=cfg)

    diff = compare_profiles("default", "staging", config_file=cfg)
    assert diff["identical"] is True
    assert diff["added"] == []
    assert diff["removed"] == []
    assert diff["changed"] == {}


def test_diff_added_and_removed_keys(tmp_path):
    cfg = tmp_path / "config.json"
    initialize_config(cfg)
    create_profile("staging", config_file=cfg)

    set_config("OLD_KEY", "val", profile="default", config_file=cfg)
    set_config("NEW_KEY", "val2", profile="staging", config_file=cfg)

    diff = compare_profiles("default", "staging", config_file=cfg)
    assert diff["identical"] is False
    assert diff["added"] == ["NEW_KEY"]
    assert diff["removed"] == ["OLD_KEY"]


def test_diff_modified_values(tmp_path):
    cfg = tmp_path / "config.json"
    initialize_config(cfg)
    create_profile("staging", config_file=cfg)

    set_config("PORT", 8000, profile="default", config_file=cfg)
    set_config("PORT", 9000, profile="staging", config_file=cfg)

    diff = compare_profiles("default", "staging", config_file=cfg)
    assert diff["identical"] is False
    assert "PORT" in diff["changed"]
    assert diff["changed"]["PORT"]["default"] == 8000
    assert diff["changed"]["PORT"]["staging"] == 9000


def test_diff_secret_changes_no_value_leak(tmp_path):
    cfg = tmp_path / "config.json"
    initialize_config(cfg)
    create_profile("staging", config_file=cfg)

    set_config(
        "API_KEY", "secret_dev", is_secret=True, profile="default", config_file=cfg
    )
    set_config(
        "API_KEY", "secret_staging", is_secret=True, profile="staging", config_file=cfg
    )

    diff = compare_profiles("default", "staging", config_file=cfg)
    assert diff["identical"] is False
    assert "API_KEY" in diff["secret_changes"]

    formatted = format_diff_text(diff)
    # Ensure neither secret string leaked into formatted text
    assert "secret_dev" not in formatted
    assert "secret_staging" not in formatted
    assert "secret value differs" in formatted
