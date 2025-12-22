from fastapi import APIRouter, UploadFile, HTTPException
import os
import shutil

from app.jobs.manager import JobManager, JobState
from app.models.schemas import JobStatusResponse

router = APIRouter()

job_manager = JobManager()

UPLOAD_FOLDER = "app/storage/input"
OUTPUT_FOLDER = "app/storage/output"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)


@router.get("/health")
def health():
    return {"status": "OK"}


@router.post("/upload", response_model=JobStatusResponse)
def upload_image(file: UploadFile):
    if not file.filename:
        raise HTTPException(status_code=400, detail="Invalid file")

    input_path = os.path.join(UPLOAD_FOLDER, file.filename)

    with open(input_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    name, ext = os.path.splitext(file.filename)
    output_filename = f"{name}_greyscale{ext}"
    output_path = os.path.join(OUTPUT_FOLDER, output_filename)

    job_id = job_manager.create_job(
        input_path=input_path,
        output_path=output_path,
    )

    return JobStatusResponse(
        job_id=job_id,
        status=JobState.PENDING.value,
        error=  None
    )


@router.get("/jobs/{job_id}", response_model=JobStatusResponse)
def get_job_status(job_id: str):
    job = job_manager.get_job(job_id)

    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    return JobStatusResponse(
        job_id=job.job_id,
        status=job.status.value,
        error=job.error,
    )
