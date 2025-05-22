from app.db.models.pricing import PriceCandle
from sqlalchemy.orm import Session

def store_candles(db: Session, symbol: str, bars: list):
    for bar in bars:
        candle = PriceCandle(
            timestamp=bar["t"],
            open=bar["o"],
            high=bar["h"],
            low=bar["l"],
            close=bar["c"],
            volume=bar["v"],
        )
        db.merge(candle)
    db.commit()