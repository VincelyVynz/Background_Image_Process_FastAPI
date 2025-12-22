from enum import Enum
from dataclasses import dataclass
from datetime import datetime
import uuid
from typing import Optional


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
    output_path: str or None
    created_at: datetime
    started_at: datetime or None
    finished_at: datetime or None
    error: str or None


class JobManager:
    def __init__(self):
        self.jobs = {}

    def create_job(self, input_path):

        job = Job(
            job_id=str(uuid.uuid4()),
            status=JobState.PENDING,
            input_path=input_path,
            output_path=None,
            created_at=datetime.now(),
            started_at=None,
            finished_at=None,
            error=None
        )
        self.jobs[job.job_id] = job
        return job.job_id

    def get_job(self, job_id):

        if job_id in self.jobs:
            return self.jobs[job_id]
        else:
            return None

    def update_status(self, job_id, job_status, error):
        job = self.get_job(job_id)
        if job:
            job.status = job_status
            if job_status == JobState.RUNNING:
                job.started_at = datetime.now()

            elif job_status == JobState.COMPLETED:
                job.finished_at = datetime.now()
            elif job_status == JobState.FAILED:
                job.finished_at = datetime.now()
                job.error = error

