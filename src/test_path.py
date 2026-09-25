from pathlib import Path

home = Path.home()
devvault_dir = home / ".devvault"

devvault_dir.mkdir(exist_ok=True)

config_file = devvault_dir / "config.json"

print("DevVault directory:", devvault_dir)
print("Exists:", devvault_dir.exists())