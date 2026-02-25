from __future__ import annotations
from fastapi import APIRouter, HTTPException, status
from fastapi.responses import FileResponse
from server.infrastructure.adapters.storage_adapter import StorageAdapter
router = APIRouter(prefix="/api/v1", tags=["models"])
_storage = StorageAdapter()
@router.get("/models/{job_id}/download")
async def download_model(job_id: str) -> FileResponse:
    path = _storage.get_path(job_id)
    if path is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Model not found")
    return FileResponse(path=str(path), media_type="model/gltf-binary", filename=f"{job_id}.glb")