# coding: utf-8
"""Infrastructure - StableFast3D Adapter"""
from __future__ import annotations

import logging
from pathlib import Path
from typing import Callable, Awaitable

try:
    import torch
    from sf3d.models.model import StableFast3D
    from diffusers import AutoPipelineForText2Image
    _TORCH_AVAILABLE = True
except ImportError:
    _TORCH_AVAILABLE = False

logger = logging.getLogger(__name__)


class StableFast3DAdapter:
    """
    Adapter for StableFast3D (Stability AI).
    Pipeline : text → image (SDXL-Turbo) → 3D mesh (.glb)
    Optimisé FP16 / Blackwell RTX 50xx.
    """

    def __init__(self, output_dir: str = "server/infrastructure/storage/models") -> None:
        self._output_dir = Path(output_dir)
        self._output_dir.mkdir(parents=True, exist_ok=True)
        self._sf3d = None
        self._txt2img = None

    def _load_pipeline(self) -> None:
        """Lazy loading — modèles gardés en VRAM tant que le worker tourne."""
        if self._sf3d is not None:
            return

        if not _TORCH_AVAILABLE:
            logger.warning("PyTorch / SF3D not available - running in MOCK mode")
            return

        try:
            device = "cuda" if torch.cuda.is_available() else "cpu"
            dtype = torch.float16

            logger.info("Loading StableFast3D pipeline (dtype=%s, device=%s)...", dtype, device)

            # 1) Chargement SF3D (image → mesh)
            self._sf3d = StableFast3D.from_pretrained(
                "stabilityai/stable-fast-3d",
                torch_dtype=dtype,
            ).to(device)
            self._sf3d.eval()

            # 2) Chargement SDXL-Turbo (texte → image)
            logger.info("Loading SDXL-Turbo (text → image)...")
            self._txt2img = AutoPipelineForText2Image.from_pretrained(
                "stabilityai/sdxl-turbo",
                torch_dtype=dtype,
                variant="fp16",
            ).to(device)

            logger.info("All pipelines loaded successfully.")

        except Exception as e:
            logger.warning("SF3D load failed: %s - running in MOCK mode", e)
            self._sf3d = None
            self._txt2img = None

    async def generate(
        self,
        job_id: str,
        text: str,
        negative_text: str = "",
        on_progress: Callable[[int], Awaitable[None]] | None = None,
    ) -> str:
        """
        Génère un mesh 3D depuis un prompt texte.
        Retourne le chemin absolu vers le fichier .glb généré.
        """
        self._load_pipeline()
        output_path = self._output_dir / f"{job_id}.glb"

        if self._sf3d is None or self._txt2img is None:
            logger.warning("MOCK mode: creating empty .glb for job %s", job_id)
            output_path.write_bytes(b"glTF mock")
            return str(output_path.resolve())


        device = "cuda" if torch.cuda.is_available() else "cpu"

        # Étape 1 : texte → image (SDXL-Turbo, 1 step)
        if on_progress:
            await on_progress(20)
        logger.info("Step 1/2 - Generating image from prompt: '%s'", text)
        with torch.inference_mode():
            image = self._txt2img(
                prompt=text,
                negative_prompt=negative_text,
                num_inference_steps=1,
                guidance_scale=0.0,
            ).images[0]

        # Étape 2 : image → mesh 3D (SF3D)
        if on_progress:
            await on_progress(60)
        logger.info("Step 2/2 - Generating 3D mesh from image...")
        with torch.inference_mode():
            mesh, _ = self._sf3d.run_image(
                image,
                bake_resolution=512,
                remesh="none",
            )

        # Export .glb
        if on_progress:
            await on_progress(90)
        mesh.export(str(output_path))
        logger.info("Model saved at %s", output_path)

        return str(output_path.resolve())
