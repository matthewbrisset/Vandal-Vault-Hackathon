# src/Backend/macro/normalizer.py

# Thresholds for converting raw values → 0.0 (safe) to 1.0 (crisis)
THRESHOLDS = {
    "vix":                {"low": 15, "moderate": 25, "high": 35, "extreme": 50},
    "unemployment_rate":  {"low": 4,  "moderate": 6,  "high": 8,  "extreme": 12},
    "cpi_yoy":            {"low": 2,  "moderate": 4,  "high": 7,  "extreme": 10},
    "fed_funds_rate":     {"low": 1,  "moderate": 3,  "high": 5,  "extreme": 8},
    "mortgage_rate_30yr": {"low": 4,  "moderate": 6,  "high": 8,  "extreme": 10},
    "credit_delinquency": {"low": 2,  "moderate": 4,  "high": 6,  "extreme": 10},
}

WEIGHTS = {
    "vix":                0.20,
    "unemployment_rate":  0.25,
    "cpi_yoy":            0.20,
    "fed_funds_rate":     0.15,
    "mortgage_rate_30yr": 0.10,
    "credit_delinquency": 0.10,
}

def _normalize(value: float, key: str) -> float:
    """Convert a raw value to a 0.0–1.0 risk score using defined thresholds."""
    if value is None:
        return 0.5             # assume moderate risk if data missing
    t = THRESHOLDS[key]
    if value <= t["low"]:      return 0.0
    if value <= t["moderate"]: return 0.25
    if value <= t["high"]:     return 0.60
    if value <= t["extreme"]:  return 0.85
    return 1.0

def calculate_macro_risk(yahoo: dict, fred: dict, cpi_year_ago: float = None) -> float:
    """
    Returns a single macro risk float between 0.0 and 1.0.
    0.0 = excellent economic conditions
    1.0 = severe recession / crisis
    """
    # Calculate CPI year-over-year % change if we have a previous value
    cpi_current = fred.get("cpi")
    if cpi_current and cpi_year_ago:
        cpi_yoy = round((cpi_current - cpi_year_ago) / cpi_year_ago * 100, 4)
    else:
        cpi_yoy = 3.5          # fallback to moderate inflation assumption

    raw = {
        "vix":                yahoo.get("vix"),
        "unemployment_rate":  fred.get("unemployment_rate"),
        "cpi_yoy":            cpi_yoy,
        "fed_funds_rate":     fred.get("fed_funds_rate"),
        "mortgage_rate_30yr": fred.get("mortgage_rate_30yr"),
        "credit_delinquency": fred.get("credit_delinquency"),
    }

    weighted_score = sum(
        _normalize(raw[key], key) * WEIGHTS[key]
        for key in WEIGHTS
    )

    return round(weighted_score, 4)
