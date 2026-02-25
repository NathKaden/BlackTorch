from __future__ import annotations
from dataclasses import dataclass
from server.domain.entities import Job
from server.domain.repositories import AbstractJobRepository
@dataclass
class GetModelStatusResult:
    job_id: str
    status: str
    progress: int
    error_message: str | None
class GetModelStatus:
    def __init__(self, job_repository: AbstractJobRepository) -> None:
        self._job_repo = job_repository
    async def execute(self, job_id: str) -> GetModelStatusResult | None:
        job: Job | None = await self._job_repo.get_by_id(job_id)
        if job is None:
            return None
        return GetModelStatusResult(
            job_id=job.id,
            status=job.status.value,
            progress=job.progress,
            error_message=job.error_message,
        )