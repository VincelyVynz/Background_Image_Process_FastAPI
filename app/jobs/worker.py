from manager import JobManager
import time
from app.utils.image_ops import process_image


job_manager = JobManager()


while True:
    job = job_manager.get_job()
    if job:
        job_manager.update_status(job.job_id,job_status= "running")
        try:
            success = process_image(job.input_path, job.output_path)
            if success:
                job_manager.update_status(job.job_id, job_status="completed")
            else:
                job_manager.update_status(job.job_id, job_status="failed")
        except Exception as e:
            job_manager.update_status(job.job_id, job_status="failed", error = str(e))

    time.sleep(1)


