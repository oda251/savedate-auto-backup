import sys
from config import load_config
from watcher import start_watching


def main():
	cfg = load_config()
	targets = cfg["targets"]
	backup_folder = cfg["backup_folder"]
	print("Watching targets:")
	for k, v in targets.items():
		print(f" - {k}: {v}")

	# On startup, create initial backups if none exist for a target
	from pathlib import Path
	from backup import perform_backup
	from utils import normalize_path

	norm_backup_folder = normalize_path(backup_folder)
	for name, src in targets.items():
		nsrc = normalize_path(src)
		target_backup_dir = Path(norm_backup_folder) / name
		if not target_backup_dir.exists() or not any(target_backup_dir.iterdir()):
			print(f"No backups found for '{name}', creating initial backup...")
			try:
				dest = perform_backup(name, nsrc, norm_backup_folder)
				print(f"Initial backup created: {dest}")
			except Exception as e:
				print(f"Initial backup failed for '{name}': {e}")

	start_watching(targets, backup_folder)


if __name__ == '__main__':
	main()
