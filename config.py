import yaml
from pathlib import Path
from typing import Dict, Any


def load_config(path: str = "target-folders.yaml") -> Dict[str, Any]:
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"Config file not found: {path}")
    with p.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}

    # Normalize keys
    targets = data.get("target-folders") or data.get("target_folders") or {}
    backup_folder = data.get("backup-folder") or data.get("backup_folder")
    if not isinstance(targets, dict):
        raise ValueError("`target-folders` must be a mapping of name -> path")
    if not backup_folder:
        raise ValueError("`backup-folder` must be set in config")

    # Expand paths
    resolved = {name: str(Path(path).expanduser()) for name, path in targets.items()}
    backup_folder = str(Path(backup_folder).expanduser())

    return {"targets": resolved, "backup_folder": backup_folder}
