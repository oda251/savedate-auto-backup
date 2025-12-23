import time
import threading
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from typing import Dict
from datetime import datetime
from backup import perform_backup
from utils import normalize_path


class ChangeHandler(FileSystemEventHandler):
    """Handles filesystem events and debounces them into a single backup call."""
    DEBOUNCE_SECONDS = 2.0

    def __init__(self, name: str, orig_path: str, watch_path: str, backup_root: str):
        super().__init__()
        self.name = name
        self.orig_path = orig_path
        self.watch_path = watch_path
        self.backup_root = backup_root
        self._timer = None
        self._lock = threading.Lock()

    def _schedule_backup(self):
        with self._lock:
            if self._timer is not None:
                try:
                    self._timer.cancel()
                except Exception:
                    pass
            self._timer = threading.Timer(self.DEBOUNCE_SECONDS, self._do_backup)
            self._timer.daemon = True
            self._timer.start()

    def _do_backup(self):
        when = datetime.now()
        try:
            dest = perform_backup(self.name, self.watch_path, self.backup_root, when=when)
            print(f"Backed up {self.watch_path} -> {dest}")
        except Exception as e:
            print(f"Backup failed for {self.watch_path}: {e}")

    def on_any_event(self, event):
        # Debounce any filesystem event into a single backup call
        self._schedule_backup()


def start_watching(targets: Dict[str, str], backup_root: str):
    observer = Observer()
    handlers = []
    for name, path in targets.items():
        # Normalize path (convert Windows-style to WSL-like if needed)
        npath = normalize_path(path)
        # Skip non-existent paths
        try:
            from pathlib import Path
            if not Path(npath).exists():
                print(f"Warning: watch path does not exist, skipping: {path} -> {npath}")
                continue
        except Exception:
            print(f"Warning: invalid path, skipping: {path}")
            continue
        handler = ChangeHandler(name, path, npath, backup_root)
        # Use normalized path for scheduling, handler keeps original string for naming
        observer.schedule(handler, npath, recursive=True)
        handlers.append(handler)

    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
