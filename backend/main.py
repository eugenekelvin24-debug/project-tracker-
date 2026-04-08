from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

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
    return {"status": "success", "added": Job}