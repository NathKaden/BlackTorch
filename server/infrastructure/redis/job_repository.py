from __future__ import annotations
import json
from datetime import datetime
import redis.asyncio as aioredis
from server.domain.entities import Job
from server.domain.entities.job import JobStatus
from server.domain.repositories import AbstractJobRepository
JOB_KEY_PREFIX = "blacktorch:job:"
JOB_TTL = 60 * 60 * 24
class RedisJobRepository(AbstractJobRepository):
    def __init__(self, redis_url: str = "redis://localhost:6379") -> None:
        self._redis: aioredis.Redis = aioredis.from_url(redis_url, decode_responses=True)
    async def save(self, job: Job) -> None:
        data = {
            "id": job.id,
            "prompt_text": job.prompt_text,
            "status": job.status.value,
            "progress": job.progress,
            "created_at": job.created_at.isoformat(),
            "updated_at": job.updated_at.isoformat(),
            "error_message": job.error_message or "",
        }
        key = f"{JOB_KEY_PREFIX}{job.id}"
        await self._redis.set(key, json.dumps(data), ex=JOB_TTL)
    async def get_by_id(self, job_id: str) -> Job | None:
        raw = await self._redis.get(f"{JOB_KEY_PREFIX}{job_id}")
        if raw is None:
            return None
        data = json.loads(raw)
        return Job(
            id=data["id"],
            prompt_text=data["prompt_text"],
            status=JobStatus(data["status"]),
            progress=data["progress"],
            created_at=datetime.fromisoformat(data["created_at"]),
            updated_at=datetime.fromisoformat(data["updated_at"]),
            error_message=data["error_message"] or None,
        )