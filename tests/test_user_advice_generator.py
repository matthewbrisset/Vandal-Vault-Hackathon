"""Pytest for UserAdviceGenerator with test data."""

import pytest
from src.Backend.csv_parser import CSVParser
from src.Backend.user_advice_generator import generate_user_advice


def test_generate_advice_from_csv_files():
    """Test generating advice from all test CSV files and output results."""
    test_files = [
        ("data/test_data/low_income.csv", "Low Income Profile"),
        ("data/test_data/medium_income.csv", "Medium Income Profile"),
        ("data/test_data/high_income.csv", "High Income Profile"),
    ]
    
    for csv_file, profile_name in test_files:
        print(f"\n{'='*60}")
        print(f"Testing: {profile_name}")
        print(f"File: {csv_file}")
        print(f"{'='*60}")
        
        # Load CSV
        parser = CSVParser(csv_file)
        record = parser.get_record(0)
        
        # Generate advice
        advice = generate_user_advice(record)
        
        # Output the AI response
        print(f"\nFinancial Data:")
        print(f"  Total Savings: ${record['total_savings']:,.2f}")
        print(f"  Total Debt: ${record['total_debt']:,.2f}")
        print(f"  Monthly Income: ${record['monthly_income']:,.2f}")
        print(f"  Monthly Expenses: ${record['monthly_expenses']:,.2f}")
        print(f"  Emergency Fund: {record['emergency_fund_months']} months")
        print(f"  Credit Score: {record['credit_score']}")
        print(f"  Debt-to-Income Ratio: {record['debt_to_income_ratio']}")
        
        print(f"\nAI Advice:")
        print(advice)
        
        # Assert advice is not empty
        assert advice is not None
        assert len(advice) > 0
