from fastapi import FastAPI
from app.api.v1.routes import router as api_router
from dotenv import load_dotenv

load_dotenv(override=True)

app = FastAPI()

app.include_router(api_router, prefix="/api/v1")