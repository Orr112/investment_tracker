from sqlalchemy import Column, DateTime, Float, Integer, String, UniqueConstraint
from app.db.database import Base
from datetime import datetime



class PriceCandle(Base):
    __tablename__ = "price_candles"

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String, index=True, nullable=False)
    timestamp = Column(DateTime, index=True, nullable=False)
    open = Column(Float, nullable=False)
    high = Column(Float, nullable=False)
    low = Column(Float, nullable=False)
    close = Column(Float, nullable=False)
    volume = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    __table_args__ = (
        UniqueConstraint("symbol", "timestamp", name="uq_symbol_timestamp"),
    )

    def __repr__(self):
        return(
            f"<PriceCandle(symbol='{self.symbol}', time='{self.timestamp}', "
            f"open={self.open}, high={self.high}, low={self.low}, close={self.close})>"

        )
