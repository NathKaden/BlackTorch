from __future__ import annotations
import logging
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from server.interfaces.routes.generation import router as generation_router
from server.interfaces.routes.websocket import router as websocket_router
from server.interfaces.routes.models import router as models_router
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s - %(message)s")
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000").split(",")
app = FastAPI(
    title="BlackTorch API",
    description="3D model generation API - optimized RTX (Blackwell)",
    version="0.1.0",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(generation_router)
app.include_router(websocket_router)
app.include_router(models_router)
@app.get("/health", tags=["meta"])
async def health() -> dict:
    return {"status": "ok", "service": "blacktorch-api"}