from pathlib import Path
import shutil
from datetime import datetime
from utils import ensure_dir, timestamped_dirname, normalize_path


def perform_backup(name: str, src: str, backup_root: str, when: datetime | None = None) -> str:
    when = when or datetime.now()
    ts = timestamped_dirname(when)

    # Normalize both the backup root and source to OS-native (Linux/WSL) paths
    nbackup_root = normalize_path(backup_root)
    nsrc = normalize_path(src)

    dest_base = Path(nbackup_root) / name / ts
    ensure_dir(str(dest_base))

    src_p = Path(nsrc)
    if not src_p.exists():
        raise FileNotFoundError(f"Source does not exist: {nsrc}")

    # Copy directory tree into the timestamped folder.
    shutil.copytree(str(src_p), str(dest_base), dirs_exist_ok=True)

    return str(dest_base.resolve())
