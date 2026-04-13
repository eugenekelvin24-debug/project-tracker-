from fastapi import APIRouter
from database import ErrorLog, engine
from sqlmodel import Session, select
from datetime import datetime

router = APIRouter(prefix="/errors", tags=["Errors"])

@router.post("/")
def create_error_log(log: ErrorLog):
    with Session(engine) as session:
        if isinstance(log.timestamp, str):
            log.timestamp = datetime.now()
        session.add(log)
        session.commit()
        session.refresh(log)
        return log

@router.get("/")
def get_error_logs():
    with Session(engine) as session:
        # This part fetches all your saved error notes
        return session.exec(select(ErrorLog)).all()