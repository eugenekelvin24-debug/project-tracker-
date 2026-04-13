from fastapi import FastAPI
from datetime import datetime
from pydantic import BaseModel
from typing import List
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session
from database import engine, ErrorLog

app = FastAPI()

@app.post("/logs/")
def create_log(log: ErrorLog):
    with Session(engine) as session:
        if not log.timestamp:
            log.timestamp = datetime.now()
        session.add(log)
        session.commit()
        session.refresh(log)
        return log

@app.get("/logs/")
def get_logs():
    with Session(engine) as session:
        # This part fetches all your saved error notes
        return session.exec(ErrorLog.__table__.select()).all()

#CORS origins 
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods =["*"],
    allow_headers =["*"],
)

#data blueprint
class Job(BaseModel):
    id: int 
    title: str 
    platform: str 
    budget: float
    deadline: str     #format: "YYYY-MM-DD"
    status: str = "pending"


# your temporary Database
jobs_db = []

@app.get("/jobs")
def get_all_jobs():
    return jobs_db

@app.post("/jobs")
def add_new_job(job: Job):
    jobs_db.append(job)
    return {"status": "success", "added": job}