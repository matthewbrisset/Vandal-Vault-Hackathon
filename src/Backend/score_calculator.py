"""Score Calculator for Vandal Vault - calculates recession resilience score.

Scoring Weights (total 100%):
- Debt to income ratio: 10%
- Expense to income ratio: 10%
- Credit score: 5%
- Savings: 10%
- Liquid investments: 10%
- Illiquid investments: 5%
- Stockpiles: 5%
- Inflation: 15%
- GDP: 10%
- CCI (Consumer Confidence Index): 10%
- Market performance: 10%
"""

# Scoring Weights (as percentages)
SCORE_WEIGHTS = {
    "debt_to_income_ratio": 0.10,
    "expense_to_income_ratio": 0.10,
    "credit_score": 0.05,
    "savings": 0.10,
    "liquid_investments": 0.10,
    "illiquid_investments": 0.05,
    "stockpiles": 0.05,
    "inflation": 0.15,
    "gdp": 0.10,
    "cci": 0.10,  # Consumer Confidence Index
    "market_performance": 0.10,
}


def calculate_debt_to_income_score(debt_to_income_ratio: float) -> int:
    """Calculate score for debt-to-income ratio (0-100).
    
    Lower ratio = better score
    - ≤0.2: 100 (excellent)
    - 0.2-0.4: 80-100 (good)
    - 0.4-0.6: 60-80 (fair)
    - 0.6-1.0: 40-60 (poor)
    - >1.0: 0-40 (very poor)
    """
    if debt_to_income_ratio <= 0.2:
        return 100
    elif debt_to_income_ratio <= 0.4:
        return max(80, 100 - (debt_to_income_ratio - 0.2) * 100)
    elif debt_to_income_ratio <= 0.6:
        return max(60, 80 - (debt_to_income_ratio - 0.4) * 100)
    elif debt_to_income_ratio <= 1.0:
        return max(40, 60 - (debt_to_income_ratio - 0.6) * 50)
    else:
        return max(0, 40 - (debt_to_income_ratio - 1.0) * 20)


def calculate_expense_to_income_score(monthly_expenses: float, monthly_income: float) -> int:
    """Calculate score for expense-to-income ratio (0-100).
    
    Lower ratio = better score
    - ≤0.5: 100 (excellent, 50% savings rate)
    - 0.5-0.7: 80-100 (good, 30-50% savings)
    - 0.7-0.85: 60-80 (fair, 15-30% savings)
    - 0.85-1.0: 20-60 (poor, 0-15% savings)
    - >1.0: 0-20 (very poor, spending more than income)
    """
    if monthly_income == 0:
        return 0
    
    ratio = monthly_expenses / monthly_income
    
    if ratio <= 0.5:
        return 100
    elif ratio <= 0.7:
        return max(80, 100 - (ratio - 0.5) * 100)
    elif ratio <= 0.85:
        return max(60, 80 - (ratio - 0.7) * 133)
    elif ratio <= 1.0:
        return max(20, 60 - (ratio - 0.85) * 267)
    else:
        return max(0, 20 - (ratio - 1.0) * 20)


def calculate_credit_score_component(credit_score: int) -> int:
    """Calculate score based on credit score (0-100).
    
    - 750+: 100
    - 700-750: 90-100
    - 650-700: 75-90
    - 600-650: 50-75
    - <600: 0-50
    """
    if credit_score >= 750:
        return 100
    elif credit_score >= 700:
        return 90 + (credit_score - 700) // 5
    elif credit_score >= 650:
        return 75 + (credit_score - 650) // 6
    elif credit_score >= 600:
        return 50 + (credit_score - 600) // 4
    else:
        return max(0, 50 - (600 - credit_score) // 4)


def calculate_savings_score(total_savings: float, monthly_expenses: float) -> int:
    """Calculate score based on savings ratio (0-100).
    
    Savings as months of expenses
    - ≥12 months: 100
    - 6-12 months: 80-100
    - 3-6 months: 60-80
    - 1-3 months: 40-60
    - 0-1 month: 0-40
    """
    if monthly_expenses == 0:
        return 0
    
    months_saved = total_savings / monthly_expenses
    
    if months_saved >= 12:
        return 100
    elif months_saved >= 6:
        return 80 + (months_saved - 6) * (20 / 6)
    elif months_saved >= 3:
        return 60 + (months_saved - 3) * (20 / 3)
    elif months_saved >= 1:
        return 40 + (months_saved - 1) * 10
    else:
        return months_saved * 40


def calculate_investment_score(investment_accounts: float, monthly_income: float) -> int:
    """Calculate score for liquid investments as ratio of monthly income.
    
    - ≥36 months: 100
    - 24-36 months: 80-100
    - 12-24 months: 60-80
    - 6-12 months: 40-60
    - 0-6 months: 0-40
    """
    if monthly_income == 0:
        return 0
    
    months = investment_accounts / monthly_income
    
    if months >= 36:
        return 100
    elif months >= 24:
        return 80 + (months - 24) * (20 / 12)
    elif months >= 12:
        return 60 + (months - 12) * (20 / 12)
    elif months >= 6:
        return 40 + (months - 6) * (20 / 6)
    else:
        return months * (40 / 6)


def calculate_macro_economic_score(inflation: float, gdp: float, cci: float, market: float) -> int:
    """Calculate composite macro economic score (0-100).
    
    Lower inflation = better
    Higher GDP growth = better
    Higher CCI = better
    Higher market performance = better
    """
    # Normalize individual scores
    inflation_score = max(0, 100 - abs(inflation * 20))  # Target ~2.5% inflation
    gdp_score = max(0, min(100, gdp * 20))  # Target ~5% growth = 100
    cci_score = max(0, min(100, cci / 1.5))  # Target CCI of 100+ = 100
    market_score = max(0, min(100, market * 10))  # Positive returns = higher score
    
    return int((inflation_score + gdp_score + cci_score + market_score) / 4)


def calculate_resilience_score(
    total_savings: float,
    total_debt: float,
    monthly_income: float,
    monthly_expenses: float,
    credit_score: int,
    investment_accounts: float = 0,
    retirement_accounts: float = 0,
    debt_to_income_ratio: float = None,
    inflation: float = 3.2,
    gdp: float = 2.5,
    cci: float = 104.7,
    market_performance: float = 0.05,
) -> int:
    """Calculate overall recession resilience score (1-1000).
    
    Args:
        total_savings: Total liquid savings ($)
        total_debt: Total debt ($)
        monthly_income: Monthly income ($)
        monthly_expenses: Monthly expenses ($)
        credit_score: Credit score (300-850)
        investment_accounts: Total liquid investments ($)
        retirement_accounts: Retirement accounts ($)
        debt_to_income_ratio: Debt-to-income ratio (optional, calculated if None)
        inflation: Current inflation rate (%)
        gdp: GDP growth rate (%)
        cci: Consumer Confidence Index
        market_performance: Market performance rate (0.05 = 5%)
        
    Returns:
        Score between 1 and 1000
    """
    
    # Calculate debt-to-income ratio if not provided
    if debt_to_income_ratio is None:
        if monthly_income == 0:
            debt_to_income_ratio = 10
        else:
            debt_to_income_ratio = total_debt / monthly_income
    
    # Calculate individual component scores (0-100 scale)
    dti_score = calculate_debt_to_income_score(debt_to_income_ratio)
    eti_score = calculate_expense_to_income_score(monthly_expenses, monthly_income)
    credit_component = calculate_credit_score_component(credit_score)
    savings_component = calculate_savings_score(total_savings, monthly_expenses)
    liquid_investments = calculate_investment_score(investment_accounts, monthly_income)
    illiquid_investments = calculate_investment_score(retirement_accounts, monthly_income) * 0.7  # Less valuable
    stockpiles = min(100, (total_savings / max(monthly_expenses, 1)) * 10)  # Scaled stockpile score
    macro_score = calculate_macro_economic_score(inflation, gdp, cci, market_performance)
    
    # Weight and sum all components
    weighted_score = (
        dti_score * SCORE_WEIGHTS["debt_to_income_ratio"] +
        eti_score * SCORE_WEIGHTS["expense_to_income_ratio"] +
        credit_component * SCORE_WEIGHTS["credit_score"] +
        savings_component * SCORE_WEIGHTS["savings"] +
        liquid_investments * SCORE_WEIGHTS["liquid_investments"] +
        illiquid_investments * SCORE_WEIGHTS["illiquid_investments"] +
        stockpiles * SCORE_WEIGHTS["stockpiles"] +
        macro_score * (
            SCORE_WEIGHTS["inflation"] +
            SCORE_WEIGHTS["gdp"] +
            SCORE_WEIGHTS["cci"] +
            SCORE_WEIGHTS["market_performance"]
        )
    )
    
    # Scale from 0-100 to 1-1000
    final_score = int((weighted_score / 100) * 1000)
    
    # Ensure score is between 1 and 1000
    return max(1, min(1000, final_score))
