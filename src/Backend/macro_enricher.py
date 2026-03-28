# src/Backend/macro_enricher.py
from .macro.yahoo_fetcher import fetch_yahoo_indicators
from .macro.fred_fetcher import fetch_fred_indicators
from .macro.normalizer import calculate_macro_risk

def get_macro_context() -> tuple[float, str]:
    """
    Main entry point for your teammates to call.
    Returns:
        macro_risk_score: float (0.0–1.0)
        macro_prompt_block: str (inject this into Groq prompt)
    """
    yahoo = fetch_yahoo_indicators()
    fred  = fetch_fred_indicators()
    risk  = calculate_macro_risk(yahoo, fred)

    prompt_block = f"""
--- Current Economic Conditions ---
VIX (Market Fear Index):     {yahoo.get('vix')}
10-Year Treasury Yield:      {yahoo.get('treasury_10yr')}%
Unemployment Rate:           {fred.get('unemployment_rate')}%
Federal Funds Rate:          {fred.get('fed_funds_rate')}%
30-Year Mortgage Rate:       {fred.get('mortgage_rate_30yr')}%
Credit Card Delinquency:     {fred.get('credit_delinquency')}%
Macro Risk Score:            {risk} / 1.0  ({'🔴 High' if risk > 0.6 else '🟡 Moderate' if risk > 0.3 else '🟢 Low'})

Use these conditions to adjust the Recession Readiness Score and tailor advice accordingly.
---
"""
    return risk, prompt_block
