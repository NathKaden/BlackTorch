from __future__ import annotations
import asyncio
import logging
import os
from server.infrastructure.adapters.threestudio_adapter import StableFast3DAdapter
from server.infrastructure.adapters.storage_adapter import StorageAdapter
from server.infrastructure.redis.job_queue import JobQueue
from server.infrastructure.redis.job_repository import RedisJobRepository
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s - %(message)s")
logger = logging.getLogger("blacktorch.worker")
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
async def process_job(
    payload: dict,
    adapter: StableFast3DAdapter,
    storage: StorageAdapter,
    job_repo: RedisJobRepository,
    job_queue: JobQueue,
) -> None:
    job_id: str = payload["job_id"]
    text: str = payload["text"]
    negative_text: str = payload.get("negative_text", "")
    job = await job_repo.get_by_id(job_id)
    if job is None:
        logger.warning("Job %s not found - skipping", job_id)
        return
    logger.info("Processing job %s: %r", job_id, text)
    job.mark_running()
    await job_repo.save(job)
    await job_queue.publish_status(job_id, {"id": job_id, "status": "RUNNING", "progress": 0})
    try:
        for pct in [20, 50, 80]:
            await asyncio.sleep(0.5)
            job.update_progress(pct)
            await job_repo.save(job)
            await job_queue.publish_status(job_id, {"id": job_id, "status": "RUNNING", "progress": pct})
        raw_path = await adapter.generate(job_id=job_id, text=text, negative_text=negative_text)
        storage.save(raw_path, job_id)
        job.mark_done()
        await job_repo.save(job)
        await job_queue.publish_status(job_id, {"id": job_id, "status": "DONE", "progress": 100})
        logger.info("Job %s completed", job_id)
    except Exception as exc:
        logger.exception("Job %s failed", job_id)
        job.mark_failed(str(exc))
        await job_repo.save(job)
        await job_queue.publish_status(job_id, {
            "id": job_id, "status": "FAILED", "progress": job.progress, "error_message": str(exc),
        })
async def run_worker() -> None:
    logger.info("BlackTorch Worker starting - Redis: %s", REDIS_URL)
    job_queue = JobQueue(REDIS_URL)
    job_repo = RedisJobRepository(REDIS_URL)
    adapter = StableFast3DAdapter()
    storage = StorageAdapter()
    logger.info("Worker ready - waiting for jobs...")
    while True:
        try:
            payload = await job_queue.dequeue(timeout=5)
            if payload is None:
                continue
            await process_job(payload, adapter, storage, job_repo, job_queue)
        except asyncio.CancelledError:
            break
        except Exception:
            logger.exception("Unexpected error in worker loop")
            await asyncio.sleep(1)
    await job_queue.close()
    logger.info("Worker stopped.")
if __name__ == "__main__":
    asyncio.run(run_worker())