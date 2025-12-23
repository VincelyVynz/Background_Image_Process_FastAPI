from enum import Enum
from dataclasses import dataclass
from datetime import datetime
import uuid
from typing import Optional, Dict


class JobState(Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class Job:
    job_id: str
    status: JobState
    input_path: str
    output_path: str
    created_at: datetime
    started_at: Optional[datetime]
    finished_at: Optional[datetime]
    error: Optional[str]
    session_id: Optional[str] = None


class JobManager:
    def __init__(self, jobs_dict: Optional[Dict[str, Job]] = None):
        self.jobs: Dict[str, Job] = jobs_dict if jobs_dict is not None else {}

    def create_job(self, input_path: str, output_path: str, session_id: Optional[str] = None) -> str:
        job = Job(
            job_id=str(uuid.uuid4()),
            status=JobState.PENDING,
            input_path=input_path,
            output_path=output_path,
            created_at=datetime.now(),
            started_at=None,
            finished_at=None,
            error=None,
            session_id=session_id
        )
        self.jobs[job.job_id] = job
        return job.job_id

    def get_job(self, job_id: str) -> Optional[Job]:
        return self.jobs.get(job_id)

    def get_next_pending_job(self) -> Optional[Job]:
        for job in list(self.jobs.values()):
            if job.status == JobState.PENDING:
                return job
        return None

    def update_status(
        self,
        job_id: str,
        job_status: JobState,
        error: Optional[str] = None,
    ) -> None:
        job = self.get_job(job_id)
        if not job:
            return


        job.status = job_status

        if job_status == JobState.RUNNING:
            job.started_at = datetime.now()

        elif job_status in (JobState.COMPLETED, JobState.FAILED):
            job.finished_at = datetime.now()
            job.error = error
            

        self.jobs[job_id] = job
