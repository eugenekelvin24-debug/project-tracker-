from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.errors import router as error_router
from routes.jobs import router as job_router
from ai_service import router as analyze_job

app = FastAPI()

#CORS origins 
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods =["*"],
    allow_headers =["*"],
)

app.include_router(analyze_job)
app.include_router(error_router)
app.include_router(job_router)

@app.get("/")
def root():
    return {"message": "Project Tracker API is Online"}