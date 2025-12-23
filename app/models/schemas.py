from pydantic import BaseModel
from typing import Optional, List

class ImageUploadRequest(BaseModel):
    filename: str

class JobStatusResponse(BaseModel):
    session_id: Optional[str] = None
    job_id: str
    status: str
    input_path: str
    output_path: Optional[str] = None
    error: str | None

class JobListResponse(BaseModel):
    jobs: List[JobStatusResponse]