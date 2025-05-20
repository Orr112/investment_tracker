from app.db.models.candle import Candle
from sqlalchemy.orm import Session
from datetime import datetime

def store_candles(db: Session, symbol: str, bars: list):
    for bar in bars:
        candle = Candle(
            symbol=symbol,
            timestamp=datetime.fromisoformat(bar["t"].replace("Z", "+00:00")),
            open=bar["o"],
            high=bar["h"],
            low=bar["l"],
            close=bar["c"],
            volume=bar["v"],
        )
        db.add(candle)
    db.commit()