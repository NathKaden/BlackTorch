from __future__ import annotations
import logging
import shutil
from pathlib import Path
logger = logging.getLogger(__name__)
STORAGE_ROOT = Path("server/infrastructure/storage/models")
class StorageAdapter:
    def __init__(self, storage_root: str | Path = STORAGE_ROOT) -> None:
        self._root = Path(storage_root)
        self._root.mkdir(parents=True, exist_ok=True)
    def save(self, source_path: str | Path, job_id: str) -> Path:
        src = Path(source_path)
        dest = self._root / f"{job_id}.glb"
        shutil.move(str(src), dest)
        logger.info("Model saved: %s", dest)
        return dest
    def get_path(self, job_id: str) -> Path | None:
        p = self._root / f"{job_id}.glb"
        return p if p.exists() else None
    def get_url(self, job_id: str, base_url: str = "http://localhost:8000") -> str:
        return f"{base_url}/api/v1/models/{job_id}/download"
    def delete(self, job_id: str) -> None:
        p = self._root / f"{job_id}.glb"
        if p.exists():
            p.unlink()
            logger.info("Model deleted: %s", p)