from fastapi import APIRouter
from app.api.v1.candles import router as candles_router

router = APIRouter()
router.include_router(candles_router, prefix="/api/v1", tags=["Candles"])