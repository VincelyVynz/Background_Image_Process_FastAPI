from fastapi import APIRouter, UploadFile, HTTPException, File
import os
import shutil
import uuid
from typing import List

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


@router.post("/upload", response_model=list[JobStatusResponse])
def upload_images(files: List[UploadFile] = File(...)):
    if not files:
        raise HTTPException(status_code=400, detail="No files uploaded")

    session_id = str(uuid.uuid4())
    responses = []

    for file in files:
        if not file.filename:
            continue

        input_path = os.path.join(UPLOAD_FOLDER, file.filename)

        with open(input_path, "wb") as f:
            shutil.copyfileobj(file.file, f)

        name, ext = os.path.splitext(file.filename)
        output_filename = f"{name}_greyscale{ext}"
        output_path = os.path.join(OUTPUT_FOLDER, output_filename)

        job_id = job_manager.create_job(
            input_path=input_path,
            output_path=output_path,
            session_id=session_id
        )

        responses.append(
            JobStatusResponse(
                session_id=session_id,
                job_id=job_id,
                status=JobState.PENDING.value,
                input_path=input_path,
                output_path=output_path,
                error=None,
            )
        )

    return responses


@router.get("/jobs/{job_id}", response_model=JobStatusResponse)
def get_job_status(job_id: str):
    job = job_manager.get_job(job_id)

    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    return JobStatusResponse(
        session_id=job.session_id,
        job_id=job.job_id,
        status=job.status.value,
        input_path=job.input_path,
        output_path=job.output_path,
        error=job.error,
    )
