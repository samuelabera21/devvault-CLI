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

    def fake_set_config(key, value):
        saved[key] = value

    monkeypatch.setattr(cli, "set_config", fake_set_config)

    cli.set_command("DEBUG", "true")

    assert saved["DEBUG"] is True
    assert capsys.readouterr().out == "Saved DEBUG.\n"


def test_get_command(monkeypatch, capsys):
    monkeypatch.setattr(cli, "get_config", lambda key: "Samuel")

    cli.get_command("NAME")

    assert capsys.readouterr().out == "Samuel\n"


def test_get_command_missing_key(monkeypatch, capsys):
    from devvault.exceptions import ConfigKeyNotFoundError

    def fake_get_config(key):
        raise ConfigKeyNotFoundError(f"Key '{key}' not found.")

    monkeypatch.setattr(cli, "get_config", fake_get_config)

    cli.get_command("NAME")

    assert capsys.readouterr().out == "Error: Key 'NAME' not found.\n"


def test_remove_command(monkeypatch, capsys):
    monkeypatch.setattr(cli, "remove_config", lambda key: True)

    cli.remove_command("DEBUG")

    assert capsys.readouterr().out == "Removed DEBUG.\n"


def test_remove_command_missing_key(monkeypatch, capsys):
    monkeypatch.setattr(cli, "remove_config", lambda key: False)

    cli.remove_command("DEBUG")

    assert capsys.readouterr().out == "Key 'DEBUG' not found.\n"


def test_export_command(tmp_path, monkeypatch, capsys):
    output_file = tmp_path / "test.env"

    monkeypatch.setattr(
        cli,
        "load_config",
        lambda: {"NAME": "Samuel", "DEBUG": True},
    )

    cli.export_command(output_file, False)

    assert output_file.read_text() == "NAME=Samuel\nDEBUG=True\n"
    assert capsys.readouterr().out == f"Exported configuration to {output_file}.\n"