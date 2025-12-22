import time
from app.jobs.manager import JobManager, JobState
from app.utils.image_ops import process_image


def run_worker(jobs_dict):

    job_manager = JobManager(jobs_dict)
    print("Worker process started...")

    while True:
        job = job_manager.get_next_pending_job()

        if not job:
            time.sleep(1)
            continue

        print(f"Processing job {job.job_id}...")
        job_manager.update_status(job.job_id, JobState.RUNNING)

        try:
            success = process_image(job.input_path, job.output_path)

            if success:
                job_manager.update_status(job.job_id, JobState.COMPLETED)
                print(f"Job {job.job_id} completed.")
            else:
                job_manager.update_status(
                    job.job_id,
                    JobState.FAILED,
                    error="Image processing returned False",
                )
                print(f"Job {job.job_id} failed.")

        except Exception as e:
            job_manager.update_status(
                job.job_id,
                JobState.FAILED,
                error=str(e) or None,
            )
            print(f"Job {job.job_id} failed with exception: {e}")

        time.sleep(1)
