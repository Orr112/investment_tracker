from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker # type: ignore[import]
from sqlalchemy.orm import Session # pyright: ignore
from sqlalchemy.ext.declarative import declarative_base
from typing import Generator 
from dotenv import load_dotenv  # type: ignore[import]

import os

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/investment_db")

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)  # type: ignore # pyright: reportGeneralTypeIssues=false


Base = declarative_base()

# Original get_db() logic stays
def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Add ability to override in tests
def override_get_db():
    from tests.conftest import TestingSessionalLocal
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()