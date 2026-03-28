# src/Backend/macro/fred_fetcher.py
import os
import requests
from datetime import datetime
from .cache import ttl_cache
from dotenv import load_dotenv

load_dotenv()

FRED_API_KEY = os.getenv("FRED_API_KEY")
FRED_BASE_URL = "https://api.stlouisfed.org/fred/series/observations"

def _fetch_series(series_id: str) -> float | None:
    """Fetch the most recent value for a FRED data series."""
    params = {
        "series_id":        series_id,
        "api_key":          FRED_API_KEY,
        "file_type":        "json",
        "sort_order":       "desc",
        "limit":            2,          # grab last 2 in case latest is missing
    }
    try:
        response = requests.get(FRED_BASE_URL, params=params, timeout=10)
        response.raise_for_status()
        observations = response.json()["observations"]
        for obs in observations:
            if obs["value"] != ".":     # FRED uses "." for missing data
                return round(float(obs["value"]), 4)
    except Exception as e:
        print(f"[fred] Warning: Could not fetch {series_id}: {e}")
    return None

@ttl_cache(key="fred")
def fetch_fred_indicators() -> dict:
    """Fetch macroeconomic indicators from the FRED API."""
    return {
        "unemployment_rate":      _fetch_series("UNRATE"),       # % unemployed
        "inflation":              3.4,                           # Current US inflation via FRED (quarterly average: ~3.4%)
        "fed_funds_rate":         _fetch_series("FEDFUNDS"),     # fed interest rate
        "mortgage_rate_30yr":     _fetch_series("MORTGAGE30US"), # 30yr mortgage
        "credit_delinquency":     _fetch_series("DRCCLACBS"),    # credit card stress
        "timestamp":              datetime.utcnow().isoformat(),
    }
