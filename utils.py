from pathlib import Path
import shutil
import os
from datetime import datetime
import re


def ensure_dir(path: str) -> Path:
    p = Path(path)
    p.mkdir(parents=True, exist_ok=True)
    return p


def timestamped_dirname(dt: datetime | None = None) -> str:
    dt = dt or datetime.now()
    return dt.strftime("%Y%m%d-%H%M%S")


def copy_tree(src: str, dst: str, *, dirs_exist_ok: bool = True) -> None:
    src_p = Path(src)
    dst_p = Path(dst)
    if not src_p.exists():
        raise FileNotFoundError(f"Source not found: {src}")
    shutil.copytree(src, dst, dirs_exist_ok=dirs_exist_ok)


def windows_to_unix_path(path: str) -> str:
    """Convert a Windows path like C:\\Users\\foo to /mnt/c/Users/foo if it looks like a Windows absolute path.
    If path doesn't look like Windows absolute, returns it unchanged.
    """
    if not isinstance(path, str):
        return path
    p = path.strip().strip('"')

    # If running on Windows, do not convert to /mnt/ paths
    if os.name == 'nt':
        return p

    # Match drive letter at start, e.g. C:\ or C:/. Also handle forward slashes after colon.
    m = re.match(r"^([A-Za-z]):[\\/](.*)$", p)
    if not m:
        return p
    drive = m.group(1).lower()
    rest = m.group(2).replace('\\', '/').replace(':', '')
    # Prepend /mnt/<drive>
    return f"/mnt/{drive}/{rest}"


def normalize_path(path: str) -> str:
    """Normalize input path: convert Windows-style to Unix and expand user."""
    p = windows_to_unix_path(path)
    return str(Path(p).expanduser())
