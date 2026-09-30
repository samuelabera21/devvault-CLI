from devvault.config import initialize_config, remove_config, set_config
from devvault.history import get_history
from devvault.profiles import create_profile, set_active_profile


def test_history_logging(tmp_path):
    cfg = tmp_path / "config.json"
    initialize_config(cfg)

    set_config("PORT", 8000, config_file=cfg)
    set_config("SECRET_TOKEN", "super_secret", is_secret=True, config_file=cfg)
    remove_config("PORT", config_file=cfg)
    create_profile("staging", config_file=cfg)
    set_active_profile("staging", config_file=cfg)

    history = get_history(config_file=cfg)
    actions = [h["action"] for h in history]

    assert "INIT" in actions
    assert "SET" in actions
    assert "SET_SECRET" in actions
    assert "REMOVE" in actions
    assert "PROFILE_CREATE" in actions
    assert "PROFILE_USE" in actions

    # Verify no sensitive values leaked in history payloads
    for entry in history:
        assert "super_secret" not in str(entry)


def test_history_filtering_and_limit(tmp_path):
    cfg = tmp_path / "config.json"
    initialize_config(cfg)
    create_profile("dev", config_file=cfg)

    set_config("KEY1", "val1", profile="default", config_file=cfg)
    set_config("KEY2", "val2", profile="dev", config_file=cfg)
    set_config("KEY3", "val3", profile="dev", config_file=cfg)

    dev_hist = get_history(profile="dev", config_file=cfg)
    assert all(h["profile"] == "dev" for h in dev_hist)

    limited = get_history(limit=2, config_file=cfg)
    assert len(limited) == 2
