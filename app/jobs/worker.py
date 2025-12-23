import time
import os
from concurrent.futures import ProcessPoolExecutor, Future
from typing import Dict

from app.jobs.manager import JobManager, JobState
from app.utils.image_ops import process_image


def process_image_task(input_path: str, output_path: str) -> bool:

    return process_image(input_path, output_path)


def run_worker(jobs_dict):
    job_manager = JobManager(jobs_dict)
    print(f"Worker process started (pid={os.getpid()})")


    with ProcessPoolExecutor() as executor:
        futures: Dict[str, Future] = {}

        while True:

            job = job_manager.get_next_pending_job()

            if job and job.job_id not in futures:
                print(f"Submitting job {job.job_id}...")
                job_manager.update_status(job.job_id, JobState.RUNNING)

                futures[job.job_id] = executor.submit(
                    process_image_task,
                    job.input_path,
                    job.output_path,
                )


            finished = [
                job_id for job_id, future in futures.items()
                if future.done()
            ]

            for job_id in finished:
                future = futures[job_id]

                try:
                    success = future.result()

                    if success:
                        job_manager.update_status(job_id, JobState.COMPLETED)
                        print(f"Job {job_id} completed.")
                    else:
                        job_manager.update_status(
                            job_id,
                            JobState.FAILED,
                            error="Image processing returned False",
                        )
                        print(f"Job {job_id} failed.")

                except Exception as e:
                    job_manager.update_status(
                        job_id,
                        JobState.FAILED,
                        error=str(e),
                    )
                    print(f"Job {job_id} failed with exception: {e}")

                del futures[job_id]

            time.sleep(1)
