"""Entity - ThreeDModel"""
from __future__ import annotations
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
@dataclass
class ThreeDModel:
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    job_id: str = ""
    glb_path: str = ""
    thumbnail_path: str | None = None
    prompt_text: str = ""
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))