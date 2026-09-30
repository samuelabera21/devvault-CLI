from pathlib import Path

from devvault import cli


def test_parse_value():
    assert cli.parse_value("true") is True
    assert cli.parse_value("false") is False
    assert cli.parse_value("123") == 123
    assert cli.parse_value("3.14") == 3.14
    assert cli.parse_value("hello") == "hello"


def test_validate_key():
    cli.validate_key("NAME")
    cli.validate_key("_NAME")
    cli.validate_key("DATABASE_URL_123")


def test_validate_key_invalid():
    invalid_keys = [
        "",
        "123NAME",
        "NAME-VALUE",
        "NAME VALUE",
    ]

    for key in invalid_keys:
        try:
            cli.validate_key(key)
        except ValueError:
            pass
        else:
            raise AssertionError(f"Expected ValueError for key: {key}")


def test_set_command(monkeypatch, capsys):
    saved = {}

    def fake_set_config(key, value, profile=None):
        saved[(key, profile)] = value

    monkeypatch.setattr(cli, "set_config", fake_set_config)

    cli.set_command("DEBUG", "true")
    assert saved[("DEBUG", None)] is True
    assert capsys.readouterr().out == "Saved DEBUG.\n"

    cli.set_command("PORT", "8000", profile="dev")
    assert saved[("PORT", "dev")] == 8000
    assert capsys.readouterr().out == "Saved PORT.\n"


def test_get_command(monkeypatch, capsys):
    monkeypatch.setattr(cli, "get_config", lambda key, profile=None: "Samuel")

    cli.get_command("NAME")
    assert capsys.readouterr().out == "Samuel\n"

    cli.get_command("NAME", profile="staging")
    assert capsys.readouterr().out == "Samuel\n"


def test_get_command_missing_key(monkeypatch, capsys):
    from devvault.exceptions import ConfigKeyNotFoundError

    def fake_get_config(key, profile=None):
        raise ConfigKeyNotFoundError(f"Key '{key}' not found.")

    monkeypatch.setattr(cli, "get_config", fake_get_config)

    cli.get_command("NAME")
    assert capsys.readouterr().out == "Error: Key 'NAME' not found.\n"


def test_list_command(monkeypatch, capsys):
    monkeypatch.setattr(
        cli,
        "list_config",
        lambda profile=None: ["KEY1", "KEY2"] if profile == "dev" else ["DEFAULT_KEY"],
    )

    cli.list_command()
    assert capsys.readouterr().out == "DEFAULT_KEY\n"

    cli.list_command(profile="dev")
    assert capsys.readouterr().out == "KEY1\nKEY2\n"


def test_remove_command(monkeypatch, capsys):
    monkeypatch.setattr(cli, "remove_config", lambda key, profile=None: True)

    cli.remove_command("DEBUG")
    assert capsys.readouterr().out == "Removed DEBUG.\n"

    cli.remove_command("DEBUG", profile="dev")
    assert capsys.readouterr().out == "Removed DEBUG.\n"


def test_remove_command_missing_key(monkeypatch, capsys):
    monkeypatch.setattr(cli, "remove_config", lambda key, profile=None: False)

    cli.remove_command("DEBUG")
    assert capsys.readouterr().out == "Key 'DEBUG' not found.\n"


def test_export_command(tmp_path, monkeypatch, capsys):
    output_file = tmp_path / "test.env"

    monkeypatch.setattr(
        cli,
        "export_env_file",
        lambda file_path, profile=None, force=False: ("default", 2),
    )

    cli.export_command(output_file, False)
    assert (
        capsys.readouterr().out
        == f"Exported 2 configuration entries to '{output_file}'.\n"
    )

    monkeypatch.setattr(
        cli,
        "export_env_file",
        lambda file_path, profile=None, force=False: ("staging", 1),
    )

    cli.export_command(output_file, True, profile="staging")
    assert (
        capsys.readouterr().out
        == f"Exported 1 configuration entries to '{output_file}'.\n"
    )


def test_import_command(tmp_path, monkeypatch, capsys):
    env_file = tmp_path / ".env"

    monkeypatch.setattr(
        cli,
        "import_env_file",
        lambda file_path, profile=None, force=False: ("default", 3, 0),
    )

    cli.import_command(env_file, force=False)
    assert (
        capsys.readouterr().out
        == "Imported 3 configuration entries into profile 'default'.\n"
    )

    monkeypatch.setattr(
        cli,
        "import_env_file",
        lambda file_path, profile=None, force=False: ("staging", 2, 1),
    )

    cli.import_command(env_file, force=False, profile="staging")
    out = capsys.readouterr().out
    assert "Imported 2 configuration entries into profile 'staging'." in out
    assert "Skipped 1 existing entries." in out


def test_info_command(monkeypatch, capsys):
    monkeypatch.setattr(
        cli,
        "get_config_file",
        lambda: Path("/home/user/.devvault/config.json"),
    )
    monkeypatch.setattr(
        cli,
        "load_config",
        lambda: {
            "active_profile": "default",
            "profiles": {
                "default": {"KEY1": "VAL1"},
                "dev": {"KEY2": "VAL2", "KEY3": "VAL3"},
            },
        },
    )

    cli.info_command()
    output = capsys.readouterr().out
    assert "Active profile: default" in output
    assert "Total profiles: 2" in output
    assert "Entries: 1" in output

    cli.info_command(profile="dev")
    output_dev = capsys.readouterr().out
    assert "Entries: 2" in output_dev


def test_profile_cli_commands(monkeypatch, capsys):
    monkeypatch.setattr(cli, "get_active_profile", lambda: "default")
    monkeypatch.setattr(cli, "list_profiles", lambda: ["default", "dev"])

    cli.profile_list_command()
    out = capsys.readouterr().out
    assert "* default\n  dev\n" == out

    cli.profile_current_command()
    assert capsys.readouterr().out == "default\n"

    created = []
    deleted = []
    switched = []
    monkeypatch.setattr(cli, "create_profile", lambda name: created.append(name))
    monkeypatch.setattr(cli, "delete_profile", lambda name: deleted.append(name))
    monkeypatch.setattr(cli, "set_active_profile", lambda name: switched.append(name))

    cli.profile_create_command("staging")
    assert created == ["staging"]
    assert capsys.readouterr().out == "Created profile 'staging'.\n"

    cli.profile_use_command("staging")
    assert switched == ["staging"]
    assert capsys.readouterr().out == "Switched to profile 'staging'.\n"

    cli.profile_delete_command("staging")
    assert deleted == ["staging"]
    assert capsys.readouterr().out == "Deleted profile 'staging'.\n"
