from sqlmodel import Field, Session, SQLModel, create_engine
from datetime import datetime
from typing import Optional

#errors.db file created in folder
sqlite_url = "sqlite:///errors.db"
engine = create_engine(sqlite_url)

class ErrorLog(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    timestamp: Optional[datetime] = Field(default_factory=datetime.now)
    error_type: str
    user_notes: str
    status: str = "Unsolved"

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

if __name__ == "__main__":
    print("Attempting to create database...")
    create_db_and_tables()
    print("---------------------------------------")
    print("SUCCESS: Database 'errors.db' is ready!")
    print("---------------------------------------")
