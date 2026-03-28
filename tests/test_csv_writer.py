"""Pytest for csv_writer module - testing CSV writing functionality."""

import pytest
from pathlib import Path
import tempfile
import csv
from src.Backend.csv_writer import (
    CSVWriter,
    write_user_personal_finance,
    write_macro_economic_data,
    write_micro_economic_data
)


@pytest.fixture
def temp_data_dir():
    """Create temporary directory for test CSV files."""
    with tempfile.TemporaryDirectory() as temp_dir:
        yield temp_dir


class TestCSVWriter:
    """Test cases for CSVWriter class."""
    
    def test_write_personal_finance_creates_file(self, temp_data_dir):
        """Test writing personal finance data creates CSV file."""
        writer = CSVWriter(temp_data_dir)
        
        user_data = {
            "total_savings": 25000,
            "total_debt": 15000,
            "monthly_income": 5000,
            "monthly_expenses": 3500,
            "emergency_fund_months": 4,
            "investment_accounts": 30000,
            "retirement_accounts": 80000,
            "credit_score": 680,
            "debt_to_income_ratio": 0.4
        }
        
        file_path = writer.write_personal_finance("user_001", user_data, date="2026-03-28")
        
        assert file_path.exists()
        assert file_path.name == "user_001.csv"
        assert (Path(temp_data_dir) / "user_profiles" / "user_001.csv") == file_path
    
    def test_write_personal_finance_content(self, temp_data_dir):
        """Test personal finance CSV contains correct data."""
        writer = CSVWriter(temp_data_dir)
        
        user_data = {
            "total_savings": 25000,
            "total_debt": 15000,
            "monthly_income": 5000,
            "monthly_expenses": 3500,
            "emergency_fund_months": 4,
            "investment_accounts": 30000,
            "retirement_accounts": 80000,
            "credit_score": 680,
            "debt_to_income_ratio": 0.4
        }
        
        file_path = writer.write_personal_finance("user_001", user_data, date="2026-03-28")
        
        # Read and verify content
        with open(file_path, 'r') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
        
        assert len(rows) == 1
        assert rows[0]["user_id"] == "user_001"
        assert rows[0]["date"] == "2026-03-28"
        assert rows[0]["total_savings"] == "25000"
        assert rows[0]["credit_score"] == "680"
    
    def test_write_personal_finance_append_mode(self, temp_data_dir):
        """Test appending multiple user records."""
        writer = CSVWriter(temp_data_dir)
        
        user_data_1 = {
            "total_savings": 25000,
            "total_debt": 15000,
            "monthly_income": 5000,
            "monthly_expenses": 3500,
            "emergency_fund_months": 4,
            "investment_accounts": 30000,
            "retirement_accounts": 80000,
            "credit_score": 680,
            "debt_to_income_ratio": 0.4
        }
        
        user_data_2 = {
            "total_savings": 50000,
            "total_debt": 10000,
            "monthly_income": 6000,
            "monthly_expenses": 4000,
            "emergency_fund_months": 6,
            "investment_accounts": 50000,
            "retirement_accounts": 100000,
            "credit_score": 720,
            "debt_to_income_ratio": 0.3
        }
        
        file_path = writer.write_personal_finance("user_001", user_data_1, date="2026-03-28")
        writer.write_personal_finance("user_001", user_data_2, date="2026-03-29", overwrite=False)
        
        # Read and verify both records exist
        with open(file_path, 'r') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
        
        assert len(rows) == 2
        assert rows[0]["date"] == "2026-03-28"
        assert rows[1]["date"] == "2026-03-29"
        assert rows[0]["total_savings"] == "25000"
        assert rows[1]["total_savings"] == "50000"
    
    def test_write_personal_finance_overwrite_mode(self, temp_data_dir):
        """Test overwriting existing personal finance file."""
        writer = CSVWriter(temp_data_dir)
        
        user_data_1 = {
            "total_savings": 25000,
            "total_debt": 15000,
            "monthly_income": 5000,
            "monthly_expenses": 3500,
            "emergency_fund_months": 4,
            "investment_accounts": 30000,
            "retirement_accounts": 80000,
            "credit_score": 680,
            "debt_to_income_ratio": 0.4
        }
        
        user_data_2 = {
            "total_savings": 50000,
            "total_debt": 10000,
            "monthly_income": 6000,
            "monthly_expenses": 4000,
            "emergency_fund_months": 6,
            "investment_accounts": 50000,
            "retirement_accounts": 100000,
            "credit_score": 720,
            "debt_to_income_ratio": 0.3
        }
        
        writer.write_personal_finance("user_001", user_data_1, date="2026-03-28")
        file_path = writer.write_personal_finance("user_001", user_data_2, date="2026-03-29", overwrite=True)
        
        # Read and verify only new record exists
        with open(file_path, 'r') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
        
        assert len(rows) == 1
        assert rows[0]["date"] == "2026-03-29"
        assert rows[0]["total_savings"] == "50000"
    
    def test_write_macro_indicators_creates_file(self, temp_data_dir):
        """Test writing macro indicators CSV file."""
        writer = CSVWriter(temp_data_dir)
        
        macro_data = {
            "inflation_rate": 3.2,
            "unemployment_rate": 4.1,
            "gdp_growth": 2.5,
            "fed_funds_rate": 5.25,
            "stock_market_index": 5200,
            "housing_market_trend": "neutral"
        }
        
        file_path = writer.write_macro_indicators(macro_data, date="2026-03-28")
        
        assert file_path.exists()
        assert file_path.name == "macro_indicators.csv"
        assert (Path(temp_data_dir) / "economic_indicators" / "macro_indicators.csv") == file_path
    
    def test_write_macro_indicators_content(self, temp_data_dir):
        """Test macro indicators CSV contains correct data."""
        writer = CSVWriter(temp_data_dir)
        
        macro_data = {
            "inflation_rate": 3.2,
            "unemployment_rate": 4.1,
            "gdp_growth": 2.5,
            "fed_funds_rate": 5.25,
            "stock_market_index": 5200,
            "housing_market_trend": "neutral"
        }
        
        file_path = writer.write_macro_indicators(macro_data, date="2026-03-28")
        
        with open(file_path, 'r') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
        
        assert len(rows) == 1
        assert rows[0]["date"] == "2026-03-28"
        assert rows[0]["inflation_rate"] == "3.2"
        assert rows[0]["housing_market_trend"] == "neutral"
    
    def test_write_micro_indicators_creates_file(self, temp_data_dir):
        """Test writing micro indicators CSV file."""
        writer = CSVWriter(temp_data_dir)
        
        micro_data = {
            "industry": "tech",
            "job_market_trend": "strong",
            "sector_volatility": "high",
            "credit_availability": "loose",
            "wage_growth": 3.5
        }
        
        file_path = writer.write_micro_indicators(micro_data, date="2026-03-28")
        
        assert file_path.exists()
        assert file_path.name == "micro_indicators.csv"
        assert (Path(temp_data_dir) / "economic_indicators" / "micro_indicators.csv") == file_path
    
    def test_write_micro_indicators_content(self, temp_data_dir):
        """Test micro indicators CSV contains correct data."""
        writer = CSVWriter(temp_data_dir)
        
        micro_data = {
            "industry": "tech",
            "job_market_trend": "strong",
            "sector_volatility": "high",
            "credit_availability": "loose",
            "wage_growth": 3.5
        }
        
        file_path = writer.write_micro_indicators(micro_data, date="2026-03-28")
        
        with open(file_path, 'r') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
        
        assert len(rows) == 1
        assert rows[0]["date"] == "2026-03-28"
        assert rows[0]["industry"] == "tech"
        assert rows[0]["wage_growth"] == "3.5"


class TestConvenienceFunctions:
    """Test convenience functions for CSV writing."""
    
    def test_write_user_personal_finance(self, temp_data_dir):
        """Test convenience function for personal finance."""
        user_data = {
            "total_savings": 5000,
            "total_debt": 35000,
            "monthly_income": 3500,
            "monthly_expenses": 3200,
            "emergency_fund_months": 0.5,
            "investment_accounts": 0,
            "retirement_accounts": 5000,
            "credit_score": 580,
            "debt_to_income_ratio": 1.0
        }
        
        file_path = write_user_personal_finance("user_002", user_data, date="2026-03-28", base_path=temp_data_dir)
        
        assert file_path.exists()
        with open(file_path, 'r') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
        
        assert rows[0]["user_id"] == "user_002"
        assert rows[0]["credit_score"] == "580"
    
    def test_write_macro_economic_data(self, temp_data_dir):
        """Test convenience function for macro indicators."""
        macro_data = {
            "inflation_rate": 2.8,
            "unemployment_rate": 3.9,
            "gdp_growth": 3.1,
            "fed_funds_rate": 5.0,
            "stock_market_index": 5250,
            "housing_market_trend": "bullish"
        }
        
        file_path = write_macro_economic_data(macro_data, date="2026-03-28", base_path=temp_data_dir)
        
        assert file_path.exists()
        with open(file_path, 'r') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
        
        assert rows[0]["housing_market_trend"] == "bullish"
    
    def test_write_micro_economic_data(self, temp_data_dir):
        """Test convenience function for micro indicators."""
        micro_data = {
            "industry": "finance",
            "job_market_trend": "moderate",
            "sector_volatility": "medium",
            "credit_availability": "tight",
            "wage_growth": 2.5
        }
        
        file_path = write_micro_economic_data(micro_data, date="2026-03-28", base_path=temp_data_dir)
        
        assert file_path.exists()
        with open(file_path, 'r') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
        
        assert rows[0]["industry"] == "finance"
        assert rows[0]["wage_growth"] == "2.5"


class TestDirectoryCreation:
    """Test that required directories are created automatically."""
    
    def test_creates_user_profiles_directory(self, temp_data_dir):
        """Test that user_profiles directory is created."""
        writer = CSVWriter(temp_data_dir)
        
        user_profiles_dir = Path(temp_data_dir) / "user_profiles"
        assert user_profiles_dir.exists()
    
    def test_creates_economic_indicators_directory(self, temp_data_dir):
        """Test that economic_indicators directory is created."""
        writer = CSVWriter(temp_data_dir)
        
        indicators_dir = Path(temp_data_dir) / "economic_indicators"
        assert indicators_dir.exists()
