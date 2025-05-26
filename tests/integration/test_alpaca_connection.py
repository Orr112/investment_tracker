import os
import pytest
from app.ingestion.alpaca_client import fetch_price_candles
from datetime import datetime
from dotenv import load_dotenv

load_dotenv(override=True)

@pytest.mark.integration
def test_alpaca_connection():
    api_key = os.getenv("ALPACA_API_KEY")
    api_secret = os.getenv("ALPACA_API_SECRET")

    assert api_key, "Missing ALPACA_API_KEY"
    assert api_secret, "Missing ALPACA_API_SECRET"

    # Attempt to fetch real data 
    symbol = "AAPL"
    start = datetime(2024, 1, 1)
    end = datetime(2024, 1, 3)

    result = fetch_price_candles(symbol=symbol, start=start, end=end)

    assert result.symbol == symbol
    assert isinstance(result.candles, list)
    assert len(result.candles) >0

    
