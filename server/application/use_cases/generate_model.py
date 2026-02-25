from __future__ import annotations
from dataclasses import dataclass
from server.domain.entities import Job, Prompt
from server.domain.repositories import AbstractJobRepository
from server.infrastructure.redis.job_queue import JobQueue
@dataclass
class GenerateModelCommand:
    text: str
    negative_text: str = ""
@dataclass
class GenerateModelResult:
    job_id: str
class GenerateModelFromText:
    def __init__(
        self,
        job_repository: AbstractJobRepository,
        job_queue: JobQueue,
    ) -> None:
        self._job_repo = job_repository
        self._job_queue = job_queue
    async def execute(self, command: GenerateModelCommand) -> GenerateModelResult:
        prompt = Prompt(text=command.text, negative_text=command.negative_text)
        job = Job(prompt_text=prompt.text)
        await self._job_repo.save(job)
        await self._job_queue.enqueue(job.id, prompt.text, prompt.negative_text)
        return GenerateModelResult(job_id=job.id)