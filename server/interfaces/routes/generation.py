from __future__ import annotations
from fastapi import APIRouter, Depends, HTTPException, status
from server.application.use_cases import GenerateModelFromText, GenerateModelCommand, GetModelStatus
from server.interfaces.schemas import GenerateRequest, GenerateResponse, JobStatusResponse
from server.interfaces.dependencies import get_generate_use_case, get_status_use_case
router = APIRouter(prefix="/api/v1", tags=["generation"])
@router.post("/generate", response_model=GenerateResponse, status_code=status.HTTP_202_ACCEPTED)
async def generate(
    body: GenerateRequest,
    use_case: GenerateModelFromText = Depends(get_generate_use_case),
) -> GenerateResponse:
    try:
        result = await use_case.execute(GenerateModelCommand(text=body.text, negative_text=body.negative_text))
        return GenerateResponse(job_id=result.job_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e))
@router.get("/jobs/{job_id}", response_model=JobStatusResponse)
async def get_job_status(
    job_id: str,
    use_case: GetModelStatus = Depends(get_status_use_case),
) -> JobStatusResponse:
    result = await use_case.execute(job_id)
    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job not found")
    return JobStatusResponse(
        id=result.job_id,
        status=result.status,
        progress=result.progress,
        error_message=result.error_message,
    )