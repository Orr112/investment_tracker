from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from app.db.models.pricing import PriceCandle as CandleModel
from app.schemas.pricing import PriceCandleCreate, PriceCandleUpdate

def create_price_candle(db: Session, candle_data: PriceCandleCreate) ->  CandleModel:
    candle = CandleModel(**candle_data.dict())
    db.add(candle)
    db.commit()
    db.refresh(candle)
    return candle

def get_price_candles(
        db: Session,
        symbol: Optional[str] = None,
        start: Optional[datetime] = None,
        end: Optional[datetime] = None
) -> List[CandleModel] :
    query = db.query(CandleModel)

    if symbol:
        query = query.filter(CandleModel.symbol == symbol)
    if start:
        query = query.filter(CandleModel.timestamp >= start)
    if end:
        query = query.filter(CandleModel.timestamp <= end)

    return query.order_by(CandleModel.timestamp).all()

def get_price_candle_by_id(db: Session, candle_id: int) -> Optional[CandleModel]:
    return db.query(CandleModel).filter(CandleModel.id == candle_id).first()

def update_price_candle(db: Session, candle_id: int, update_data: PriceCandleUpdate) -> CandleModel:
    candle = db.query(CandleModel).get(candle_id)
    if not candle:
        return None

    for field, value in update_data.dict(exclude_unset=True).items():
        setattr(candle, field, value)

    db.commit()
    db.refresh(candle)
    return candle


def delete_price_candle(db: Session, candle_id: int) -> dict:
    candle = db.query(CandleModel).get(candle_id)
    if not candle:
        return {"error": "Candle not found"}

    db.delete(candle)
    db.commit()
    return {"status": "deleted", "id": candle_id}
