import time
from app.jobs.manager import JobManager, JobState
from app.utils.image_ops import process_image


job_manager = JobManager()

while True:
    job = job_manager.get_next_pending_job()

    if not job:
        time.sleep(1)
        continue

    job_manager.update_status(job.job_id, JobState.RUNNING)

    try:
        success = process_image(job.input_path, job.output_path)

        if success:
            job_manager.update_status(job.job_id, JobState.COMPLETED)
        else:
            job_manager.update_status(
                job.job_id,
                JobState.FAILED,
                error="Image processing returned False",
            )

    except Exception as e:
        job_manager.update_status(
            job.job_id,
            JobState.FAILED,
            error=str(e) or None,
        )

    time.sleep(1)
