from __future__ import annotations
import os
from functools import lru_cache
from server.application.use_cases import GenerateModelFromText, GetModelStatus
from server.infrastructure.redis.job_queue import JobQueue
from server.infrastructure.redis.job_repository import RedisJobRepository
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
@lru_cache(maxsize=1)
def _job_repository() -> RedisJobRepository:
    return RedisJobRepository(REDIS_URL)
@lru_cache(maxsize=1)
def _job_queue() -> JobQueue:
    return JobQueue(REDIS_URL)
def get_generate_use_case() -> GenerateModelFromText:
    return GenerateModelFromText(
        job_repository=_job_repository(),
        job_queue=_job_queue(),
    )
def get_status_use_case() -> GetModelStatus:
    return GetModelStatus(job_repository=_job_repository())