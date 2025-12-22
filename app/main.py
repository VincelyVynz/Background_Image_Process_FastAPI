from contextlib import asynccontextmanager
from multiprocessing import Process, Manager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import routes
from app.jobs.manager import JobManager
from app.jobs.worker import run_worker


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("Starting up...")
    manager = Manager()
    shared_jobs = manager.dict()
    

    routes.job_manager = JobManager(shared_jobs)
    

    worker_process = Process(target=run_worker, args=(shared_jobs,))
    worker_process.start()
    
    yield
    
    print("Shutting down...")
    worker_process.terminate()
    worker_process.join()


app = FastAPI(title="Background Image Processor", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(routes.router)
