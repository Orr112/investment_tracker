from fastapi import FastAPI
from app.api.v1.routes import router as api_router
from app.db.database import get_db
from dotenv import load_dotenv

load_dotenv(override=True)

app = FastAPI()

app.include_router(api_router)
