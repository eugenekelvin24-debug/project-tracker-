from fastapi import APIRouter
from database import Job, engine
from sqlmodel import Session, select
from datetime import datetime

router = APIRouter(prefix="/jobs", tags=["Jobs"])

@router.post("/")
def create_job(job: Job):
    with Session(engine) as session:
        if isinstance(job.date_added, str):
            job.date_added = datetime.now()
            job.deadline = None
        session.add(job)
        session.commit()
        session.refresh(job)
        return job
    
@router.get("/")
def get_job():
    with Session(engine) as session:
        # This part fetches all your saved jobs
        return session.exec(select(Job)).all()