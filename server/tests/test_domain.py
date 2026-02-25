import pytest
from server.domain.entities import Job, Prompt
from server.domain.entities.job import JobStatus
def test_prompt_valid():
    p = Prompt(text="  A futuristic spaceship  ")
    assert p.text == "A futuristic spaceship"
def test_prompt_empty_raises():
    with pytest.raises(ValueError, match="empty"):
        Prompt(text="   ")
def test_prompt_too_long_raises():
    with pytest.raises(ValueError, match="1000"):
        Prompt(text="x" * 1001)
def test_job_lifecycle():
    job = Job(prompt_text="A dragon")
    assert job.status == JobStatus.PENDING
    job.mark_running()
    assert job.status == JobStatus.RUNNING
    job.update_progress(50)
    assert job.progress == 50
    job.mark_done()
    assert job.status == JobStatus.DONE
    assert job.progress == 100
def test_job_mark_failed():
    job = Job(prompt_text="A robot")
    job.mark_failed("CUDA OOM")
    assert job.status == JobStatus.FAILED
    assert job.error_message == "CUDA OOM"