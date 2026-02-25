"""Entity - Job & JobStatus"""
from __future__ import annotations
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
class JobStatus(str, Enum):
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    DONE = "DONE"
    FAILED = "FAILED"
@dataclass
class Job:
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    prompt_text: str = ""
    status: JobStatus = JobStatus.PENDING
    progress: int = 0
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    error_message: str | None = None
    def mark_running(self) -> None:
        self.status = JobStatus.RUNNING
        self.updated_at = datetime.now(timezone.utc)
    def update_progress(self, progress: int) -> None:
        self.progress = max(0, min(100, progress))
        self.updated_at = datetime.now(timezone.utc)
    def mark_done(self) -> None:
        self.status = JobStatus.DONE
        self.progress = 100
        self.updated_at = datetime.now(timezone.utc)
    def mark_failed(self, reason: str) -> None:
        self.status = JobStatus.FAILED
        self.error_message = reason
        self.updated_at = datetime.now(timezone.utc)