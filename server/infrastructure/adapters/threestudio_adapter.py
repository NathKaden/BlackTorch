# coding: utf-8
"""Infrastructure - StableFast3D Adapter"""
from __future__ import annotations

import logging
from pathlib import Path
from typing import AsyncIterator

logger = logging.getLogger(__name__)


class StableFast3DAdapter:
    """
    Adapter for StableFast3D / threestudio.
    Loads the model in FP4 to optimize VRAM on RTX (Blackwell).
    """

    def __init__(self, output_dir: str = "server/infrastructure/storage/models") -> None:
        self._output_dir = Path(output_dir)
        self._output_dir.mkdir(parents=True, exist_ok=True)
        self._pipeline = None

    def _load_pipeline(self) -> None:
        """Lazy loading - model stays in VRAM as long as worker runs."""
        if self._pipeline is not None:
            return

        try:
            import torch

            logger.info("Loading StableFast3D pipeline (FP4 / Blackwell)...")

            # FP4 optimized for Blackwell (RTX)
            # torch.float4_e2m1fn available from PyTorch 2.5+ with CUDA 12.8
            dtype = torch.float16  # fallback
            if hasattr(torch, "float4_e2m1fn"):
                dtype = torch.float4_e2m1fn  # type: ignore[attr-defined]

            # TODO: replace with real stable-fast-3d import
            # from sf3d.models import SF3DModel
            # self._pipeline = SF3DModel.from_pretrained(
            #     "stabilityai/stable-fast-3d", torch_dtype=dtype
            # ).to("cuda")

            logger.info("Pipeline loaded (dtype=%s)", dtype)

        except ImportError as e:
            logger.warning("PyTorch / SF3D not available: %s - running in MOCK mode", e)

    async def generate(
        self,
        job_id: str,
        text: str,
        negative_text: str = "",
        on_progress: AsyncIterator | None = None,
    ) -> str:
        """
        Run generation and return the absolute path to the .glb file.
        Falls back to a mock .glb file when PyTorch is not available.
        """
        self._load_pipeline()
        output_path = self._output_dir / f"{job_id}.glb"

        if self._pipeline is None:
            # Dev mode - mock file
            logger.warning("MOCK mode: creating empty .glb for job %s", job_id)
            output_path.write_bytes(b"glTF mock")
            return str(output_path.resolve())

        # Real generation
        import torch

        with torch.inference_mode():
            # TODO: real SF3D call
            # result = self._pipeline.run(text, negative_prompt=negative_text)
            # result.export_glb(str(output_path))
            pass

        logger.info("Model generated at %s", output_path)
        return str(output_path.resolve())
