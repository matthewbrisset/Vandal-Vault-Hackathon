"""Pytest for score_calculator module."""

import pytest
from src.Backend.score_calculator import (
    calculate_resilience_score,
    calculate_debt_to_income_score,
    calculate_expense_to_income_score,
    calculate_credit_score_component,
    calculate_savings_score,
    calculate_investment_score,
)


class TestDebtToIncomeScore:
    """Test debt-to-income ratio scoring."""
    
    def test_excellent_dti(self):
        """Test excellent DTI (≤0.2)."""
        score = calculate_debt_to_income_score(0.15)
        assert score == 100
    
    def test_good_dti(self):
        """Test good DTI (0.2-0.4)."""
        score = calculate_debt_to_income_score(0.3)
        assert 80 <= score <= 100
    
    def test_fair_dti(self):
        """Test fair DTI (0.4-0.6)."""
        score = calculate_debt_to_income_score(0.5)
        assert 60 <= score <= 80
    
    def test_poor_dti(self):
        """Test poor DTI (>1.0)."""
        score = calculate_debt_to_income_score(1.5)
        assert 0 <= score <= 40


class TestExpenseToIncomeScore:
    """Test expense-to-income ratio scoring."""
    
    def test_excellent_eti(self):
        """Test excellent ETI (≤0.5, 50%+ savings rate)."""
        score = calculate_expense_to_income_score(2500, 5000)
        assert score == 100
    
    def test_good_eti(self):
        """Test good ETI (0.5-0.7)."""
        score = calculate_expense_to_income_score(3000, 5000)
        assert 80 <= score <= 100
    
    def test_overspending(self):
        """Test overspending (>1.0)."""
        score = calculate_expense_to_income_score(6000, 5000)
        assert 0 <= score <= 20


class TestCreditScore:
    """Test credit score component."""
    
    def test_excellent_credit(self):
        """Test excellent credit (750+)."""
        score = calculate_credit_score_component(800)
        assert score == 100
    
    def test_good_credit(self):
        """Test good credit (700-750)."""
        score = calculate_credit_score_component(720)
        assert 90 <= score <= 100
    
    def test_poor_credit(self):
        """Test poor credit (<600)."""
        score = calculate_credit_score_component(550)
        assert score < 50


class TestSavingsScore:
    """Test savings ratio scoring."""
    
    def test_excellent_savings(self):
        """Test 12+ months saved."""
        score = calculate_savings_score(120000, 10000)
        assert score == 100
    
    def test_good_savings(self):
        """Test 6-12 months saved."""
        score = calculate_savings_score(80000, 10000)
        assert 80 <= score <= 100
    
    def test_poor_savings(self):
        """Test <1 month saved."""
        score = calculate_savings_score(5000, 10000)
        assert 0 <= score <= 40


class TestInvestmentScore:
    """Test investment ratio scoring."""
    
    def test_excellent_investments(self):
        """Test 36+ months of investments."""
        score = calculate_investment_score(360000, 10000)
        assert score == 100
    
    def test_good_investments(self):
        """Test 24-36 months of investments."""
        score = calculate_investment_score(300000, 10000)
        assert 80 <= score <= 100


class TestOverallResilienceScore:
    """Test overall resilience score calculation."""
    
    def test_excellent_profile(self):
        """Test excellent financial profile."""
        score = calculate_resilience_score(
            total_savings=100000,
            total_debt=5000,
            monthly_income=8000,
            monthly_expenses=4000,
            credit_score=780,
            investment_accounts=150000,
            retirement_accounts=400000,
            debt_to_income_ratio=0.08,
            inflation=3.2,
            gdp=2.5,
            cci=104.7,
            market_performance=0.05
        )
        assert 650 <= score <= 1000, f"Excellent profile score {score} not in expected range"
    
    def test_poor_profile(self):
        """Test poor financial profile."""
        score = calculate_resilience_score(
            total_savings=5000,
            total_debt=35000,
            monthly_income=3500,
            monthly_expenses=3200,
            credit_score=580,
            investment_accounts=0,
            retirement_accounts=5000,
            debt_to_income_ratio=1.0,
            inflation=5.0,
            gdp=0.5,
            cci=90,
            market_performance=-0.10
        )
        assert 1 <= score <= 300, f"Poor profile score {score} not in expected range"
    
    def test_score_range(self):
        """Test that score is always between 1 and 1000."""
        # Extreme negative
        score = calculate_resilience_score(
            total_savings=0,
            total_debt=100000,
            monthly_income=2000,
            monthly_expenses=3000,
            credit_score=300,
            investment_accounts=0,
            retirement_accounts=0,
            debt_to_income_ratio=50
        )
        assert 1 <= score <= 1000
        
        # Extreme positive
        score = calculate_resilience_score(
            total_savings=1000000,
            total_debt=1000,
            monthly_income=20000,
            monthly_expenses=5000,
            credit_score=850,
            investment_accounts=500000,
            retirement_accounts=1000000,
            debt_to_income_ratio=0.05
        )
        assert 1 <= score <= 1000
    
    def test_medium_income_profile(self):
        """Test medium income profile."""
        score = calculate_resilience_score(
            total_savings=25000,
            total_debt=15000,
            monthly_income=5000,
            monthly_expenses=3500,
            credit_score=680,
            investment_accounts=30000,
            retirement_accounts=80000,
            debt_to_income_ratio=0.4
        )
        assert 300 <= score <= 700, f"Medium profile score {score} not in expected range"
    
    def test_macro_economic_impact(self):
        """Test that macroeconomic factors impact score."""
        base_score = calculate_resilience_score(
            total_savings=25000,
            total_debt=15000,
            monthly_income=5000,
            monthly_expenses=3500,
            credit_score=680,
            investment_accounts=30000,
            retirement_accounts=80000,
            debt_to_income_ratio=0.4,
            inflation=3.2,
            gdp=2.5,
            cci=104.7,
            market_performance=0.05
        )
        
        # Same profile in bad economy
        bad_econ_score = calculate_resilience_score(
            total_savings=25000,
            total_debt=15000,
            monthly_income=5000,
            monthly_expenses=3500,
            credit_score=680,
            investment_accounts=30000,
            retirement_accounts=80000,
            debt_to_income_ratio=0.4,
            inflation=8.0,
            gdp=-2.0,
            cci=80,
            market_performance=-0.30
        )
        
        # Bad economy should result in lower score
        assert bad_econ_score < base_score
