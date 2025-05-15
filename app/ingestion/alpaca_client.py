import requests
from pydantic import BaseModel, Field, ValidationError
from datetime import datetime
from typing import List, Optional
import logging
import os

# ✅ Reason: Keeps API keys out of code and supports env-based config
ALPACA_API_KEY = os.getenv("ALPACA_API_KEY")
ALPACA_API_SECRET = os.getenv("ALPACA_API_SECRET")
BASE_URL = os.getenv("ALPACA_BASE_URL", "https://data.alpaca.markets/v2")


# ✅Defines strict data contract for price data
class PriceCandle(BaseModel):
    t: datetime                     # timestamp
    o: float = Field(gt=0)          # open price
    h: float = Field(gt=0)          # high price
    l: float = Field(gt=0)          # low price
    c: float = Field(gt=0)          # close price
    v: int = Field(ge=0)            # volume (non-negative)


# ✅ Allows external validation and logging of ingestion results
class PriceFetchResult(BaseModel):
    symbol: str
    candles: List[PriceCandle]


def fetch_price_candles(symbol: str, start: str, end: str, timeframe: str = "1D") -> PriceFetchResult:
    """
    Fetch historical price candles from Alpaca
    
    - Meets requirement: Live data ingestion
    - Validates: Schema, types, out-of-range values
    - Clean design: separation of concerns (API call + validation)
    """
    headers = {
        "APCA-API-KEY-ID": ALPACA_API_KEY,
        "APCA-API-SECRET-KEY": ALPACA_API_SECRET
    }

    url = f"{BASE_URL}/stocks/{symbol}/bars"
    params = {
        "start": start.isoformat() + "Z" if isinstance(start, datetime) else start,
        "end": end.isoformat() + "Z" if isinstance(end, datetime) else end,
        "timeframe": timeframe,
        "limit": 1000
    }

    response = requests.get(url, headers=headers, params=params)
    if response.status_code != 200:
        logging.error(f"Alpaca API error: {response.status_code} {response.text}")
        raise Exception("Failed to fetch data from Alpaca")

    try:
        candles = [PriceCandle(**bar) for bar in response.json().get("bars", [])]
        return PriceFetchResult(symbol=symbol, candles=candles)
    except ValidationError as e:
        logging.error(f"Data validation failed for {symbol}: {e}")
        raise
