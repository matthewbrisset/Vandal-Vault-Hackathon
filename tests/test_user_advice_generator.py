"""Pytest for UserAdviceGenerator with test data."""

import pytest
from pathlib import Path
from src.Backend.csv_parser import CSVParser
from src.Backend.user_advice_generator import generate_user_advice


def test_generate_advice_from_csv_files():
    """Test generating advice from all test CSV files and output results."""
    test_files = [
        ("data/test_data/low_income.csv", "Low Income Profile"),
        ("data/test_data/medium_income.csv", "Medium Income Profile"),
        ("data/test_data/high_income.csv", "High Income Profile"),
    ]
    
    # Create output file
    output_file = Path("test_advice_output.txt")
    
    with open(output_file, 'w') as f:
        for csv_file, profile_name in test_files:
            output = f"\n{'='*60}\n"
            output += f"Testing: {profile_name}\n"
            output += f"File: {csv_file}\n"
            output += f"{'='*60}\n"
            
            # Load CSV
            parser = CSVParser(csv_file)
            record = parser.get_record(0)
            
            # Generate advice
            advice = generate_user_advice(record)
            
            # Build output
            output += f"\nFinancial Data:\n"
            output += f"  Total Savings: ${record['total_savings']:,.2f}\n"
            output += f"  Total Debt: ${record['total_debt']:,.2f}\n"
            output += f"  Monthly Income: ${record['monthly_income']:,.2f}\n"
            output += f"  Monthly Expenses: ${record['monthly_expenses']:,.2f}\n"
            output += f"  Emergency Fund: {record['emergency_fund_months']} months\n"
            output += f"  Credit Score: {record['credit_score']}\n"
            output += f"  Debt-to-Income Ratio: {record['debt_to_income_ratio']}\n"
            output += f"\nAI Advice:\n"
            output += advice + "\n"
            
            # Write to file
            f.write(output)
            
            # Also print to console
            print(output)
            
            # Assert advice is not empty
            assert advice is not None
            assert len(advice) > 0
    
    print(f"\n✓ Test output saved to: test_advice_output.txt")
