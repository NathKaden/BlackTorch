from __future__ import annotations
import json
import logging
import redis.asyncio as aioredis
logger = logging.getLogger(__name__)
JOB_QUEUE_KEY = "blacktorch:jobs:queue"
class JobQueue:
    def __init__(self, redis_url: str = "redis://localhost:6379") -> None:
        self._redis: aioredis.Redis = aioredis.from_url(redis_url, decode_responses=True)
    async def enqueue(self, job_id: str, text: str, negative_text: str = "") -> None:
        payload = json.dumps({"job_id": job_id, "text": text, "negative_text": negative_text})
        await self._redis.lpush(JOB_QUEUE_KEY, payload)
        logger.info("Job %s enqueued", job_id)
    async def dequeue(self, timeout: int = 5) -> dict | None:
        result = await self._redis.brpop(JOB_QUEUE_KEY, timeout=timeout)
        if result is None:
            return None
        _, raw = result
        return json.loads(raw)
    async def publish_status(self, job_id: str, payload: dict) -> None:
        channel = f"blacktorch:job:{job_id}:status"
        await self._redis.publish(channel, json.dumps(payload))
    async def close(self) -> None:
        await self._redis.aclose()