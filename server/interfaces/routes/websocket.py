from __future__ import annotations
import asyncio
import json
import logging
import os
import redis.asyncio as aioredis
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
logger = logging.getLogger(__name__)
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
router = APIRouter(prefix="/api/v1/ws", tags=["websocket"])
@router.websocket("/jobs/{job_id}")
async def job_status_ws(websocket: WebSocket, job_id: str) -> None:
    await websocket.accept()
    redis_client: aioredis.Redis = aioredis.from_url(REDIS_URL, decode_responses=True)
    pubsub = redis_client.pubsub()
    channel = f"blacktorch:job:{job_id}:status"
    try:
        await pubsub.subscribe(channel)
        async for message in pubsub.listen():
            if message["type"] != "message":
                continue
            data: dict = json.loads(message["data"])
            await websocket.send_json(data)
            if data.get("status") in ("DONE", "FAILED"):
                break
    except WebSocketDisconnect:
        pass
    except asyncio.CancelledError:
        pass
    finally:
        await pubsub.unsubscribe(channel)
        await redis_client.aclose()