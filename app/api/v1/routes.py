from fastapi import APIRouter
from app.api.v1 import candles
from app.api.v1.holdings import router as holdings_router
from app.api.v1.alerts import router as alerts_router

router = APIRouter()
router.include_router(candles.router)
router.include_router(holdings_router)
router.include_router(alerts_router, prefix="/api/v1")