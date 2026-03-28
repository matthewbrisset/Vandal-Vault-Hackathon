"""
Updated Score Calculator for Vandal Vault
- Calculates a base Personal Score.
- Multiplies by a Macro Economic Factor.
"""

# Personal Scoring Weights (must sum to 1.0)
PERSONAL_WEIGHTS = {
    "debt_to_income_ratio": 0.20,
    "expense_to_income_ratio": 0.20,
    "credit_score": 0.10,
    "savings": 0.20,
    "liquid_investments": 0.15,
    "illiquid_investments": 0.10,
    "stockpiles": 0.05,
}

def calculate_debt_to_income_score(debt_to_income_ratio: float) -> int:
    if debt_to_income_ratio <= 0.2: return 100
    elif debt_to_income_ratio <= 0.4: return max(80, 100 - (debt_to_income_ratio - 0.2) * 100)
    elif debt_to_income_ratio <= 0.6: return max(60, 80 - (debt_to_income_ratio - 0.4) * 100)
    elif debt_to_income_ratio <= 1.0: return max(40, 60 - (debt_to_income_ratio - 0.6) * 50)
    else: return max(0, 40 - (debt_to_income_ratio - 1.0) * 20)

def calculate_expense_to_income_score(monthly_expenses: float, monthly_income: float) -> int:
    if monthly_income == 0: return 0
    ratio = monthly_expenses / monthly_income
    if ratio <= 0.5: return 100
    elif ratio <= 0.7: return max(80, 100 - (ratio - 0.5) * 100)
    elif ratio <= 0.85: return max(60, 80 - (ratio - 0.7) * 133)
    elif ratio <= 1.0: return max(20, 60 - (ratio - 0.85) * 267)
    else: return max(0, 20 - (ratio - 1.0) * 20)

def calculate_credit_score_component(credit_score: int) -> int:
    if credit_score >= 750: return 100
    elif credit_score >= 700: return 90 + (credit_score - 700) // 5
    elif credit_score >= 650: return 75 + (credit_score - 650) // 6
    elif credit_score >= 600: return 50 + (credit_score - 600) // 4
    else: return max(0, 50 - (600 - credit_score) // 4)

def calculate_savings_score(total_savings: float, monthly_expenses: float) -> int:
    if monthly_expenses == 0: return 0
    months_saved = total_savings / monthly_expenses
    if months_saved >= 12: return 100
    elif months_saved >= 6: return 80 + (months_saved - 6) * (20 / 6)
    elif months_saved >= 3: return 60 + (months_saved - 3) * (20 / 3)
    elif months_saved >= 1: return 40 + (months_saved - 1) * 10
    else: return months_saved * 40

def calculate_investment_score(investment_accounts: float, monthly_income: float) -> int:
    if monthly_income == 0: return 0
    months = investment_accounts / monthly_income
    if months >= 36: return 100
    elif months >= 24: return 80 + (months - 24) * (20 / 12)
    elif months >= 12: return 60 + (months - 12) * (20 / 12)
    elif months >= 6: return 40 + (months - 6) * (20 / 6)
    else: return months * (40 / 6)

def calculate_macro_multiplier(inflation: float, gdp: float, cci: float, market: float) -> float:
    """
    Calculates a multiplier based on macro factors.
    Neutral economy (score 50) = 1.0x
    Great economy (score 100) = 1.5x
    Poor economy (score 0) = 0.5x
    """
    inf_score = max(0, 100 - abs(inflation * 20))
    gdp_score = max(0, min(100, gdp * 20))
    cci_score = max(0, min(100, cci / 1.5))
    mkt_score = max(0, min(100, market * 10))
    
    avg_macro_score = (inf_score + gdp_score + cci_score + mkt_score) / 4
    # Scale 0-100 to 0.5-1.5 multiplier
    return 0.5 + (avg_macro_score / 100)

def calculate_resilience_score(
    total_savings, total_debt, monthly_income, monthly_expenses, credit_score,
    investment_accounts, retirement_accounts, debt_to_income_ratio,
    inflation, gdp, cci, market_performance
):
    if debt_to_income_ratio is None:
        debt_to_income_ratio = total_debt / monthly_income if monthly_income > 0 else 10

    # 1. Calculate Personal Score (0-100)
    personal_score = (
        calculate_debt_to_income_score(debt_to_income_ratio) * PERSONAL_WEIGHTS["debt_to_income_ratio"] +
        calculate_expense_to_income_score(monthly_expenses, monthly_income) * PERSONAL_WEIGHTS["expense_to_income_ratio"] +
        calculate_credit_score_component(credit_score) * PERSONAL_WEIGHTS["credit_score"] +
        calculate_savings_score(total_savings, monthly_expenses) * PERSONAL_WEIGHTS["savings"] +
        calculate_investment_score(investment_accounts, monthly_income) * PERSONAL_WEIGHTS["liquid_investments"] +
        calculate_investment_score(retirement_accounts, monthly_income) * 0.7 * PERSONAL_WEIGHTS["illiquid_investments"] +
        min(100, (total_savings / max(monthly_expenses, 1)) * 10) * PERSONAL_WEIGHTS["stockpiles"]
    )

    # 2. Calculate Macro Multiplier
    multiplier = calculate_macro_multiplier(inflation, gdp, cci, market_performance)

    # 3. Final Multiplied Score
    final_score = (personal_score * multiplier) * 10  # Scale to 0-1000 range
    
    return int(max(1, min(1000, final_score)))
