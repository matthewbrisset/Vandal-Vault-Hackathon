# src/Backend/macro/yahoo_fetcher.py
import yfinance as yf
from datetime import datetime
from macro.cache import ttl_cache

@ttl_cache(key="yahoo")
def fetch_yahoo_indicators() -> dict:
    """Fetch real-time market indicators from Yahoo Finance."""
    
    tickers = {
        "vix":           "^VIX",    # Market fear/volatility
        "treasury_10yr": "^TNX",    # 10-year treasury yield
        "treasury_3mo":  "^IRX",    # 3-month treasury (short term rates)
        "sp500":         "^GSPC",   # Broad market health
    }

    result = {}
    for key, symbol in tickers.items():
        try:
            ticker = yf.Ticker(symbol)
            hist = ticker.history(period="5d")
            result[key] = round(float(hist["Close"].dropna().iloc[-1]), 4)
        except Exception as e:
            print(f"[yahoo] Warning: Could not fetch {symbol}: {e}")
            result[key] = None

    result["timestamp"] = datetime.utcnow().isoformat()
    return result
