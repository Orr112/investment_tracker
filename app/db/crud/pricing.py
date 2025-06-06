from datetime import datetime
from typing import List, Optional

from sqlalchemy.orm import Session
from sqlalchemy.dialects.postgresql import insert

from app.db.models.pricing import PriceCandle as CandleModel
from app.schemas.pricing import PriceCandleCreate, PriceCandleUpdate


# 🔹 CREATE
def create_price_candle(db: Session, candle_data: PriceCandleCreate) -> CandleModel:
    candle = CandleModel(**candle_data.dict())
    db.add(candle)
    db.commit()
    db.refresh(candle)
    return candle


# 🔹 READ
def get_price_candle_by_id(db: Session, candle_id: int) -> Optional[CandleModel]:
    return db.query(CandleModel).filter(CandleModel.id == candle_id).first()


def get_price_candles(
    db: Session,
    symbol: Optional[str] = None,
    start: Optional[datetime] = None,
    end: Optional[datetime] = None
) -> List[CandleModel]:
    query = db.query(CandleModel)

    if symbol:
        query = query.filter(CandleModel.symbol == symbol)
    if start:
        query = query.filter(CandleModel.timestamp >= start)
    if end:
        query = query.filter(CandleModel.timestamp <= end)

    return query.order_by(CandleModel.timestamp).all()


def get_all_symbols(db: Session) -> List[str]:
    return [row[0] for row in db.query(CandleModel.symbol).distinct().all()]

def get_timestamps_for_symbol(db: Session, symbol: str) -> List[datetime]:
    return [row[0] for row in db.query(CandleModel.timestamp)
        .filter(CandleModel.symbol == symbol)
        .order_by(CandleModel.timestamp)
        .all()]


# 🔹 UPDATE
def update_price_candle(db: Session, candle_id: int, update_data: PriceCandleUpdate) -> Optional[CandleModel]:
    candle = db.query(CandleModel).get(candle_id)
    if not candle:
        return None

    for field, value in update_data.dict(exclude_unset=True).items():
        setattr(candle, field, value)

    db.commit()
    db.refresh(candle)
    return candle

def bulk_upsert_price_candles(db: Session, candles: list[dict]):
    if not candles:
        return

    stmt = insert(CandleModel).values(candles)
    stmt = stmt.on_conflict_do_nothing(index_elements=["symbol", "timestamp"])
    db.execute(stmt)
    db.commit()


# 🔹 DELETE
def delete_price_candle(db: Session, candle_id: int) -> dict:
    candle = db.query(CandleModel).get(candle_id)
    if not candle:
        return {"error": "Candle not found"}

    db.delete(candle)
    db.commit()
    return {"status": "deleted", "id": candle_id}
