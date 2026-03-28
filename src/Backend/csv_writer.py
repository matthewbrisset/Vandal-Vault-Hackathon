"""CSV Writer for Vandal Vault - handles personal finance and economic indicator data."""

import csv
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime


class CSVWriter:
    """Handle writing CSV files for personal finance and economic indicators."""
    
    def __init__(self, base_path: str = "data"):
        """Initialize CSV writer with base data directory.
        
        Args:
            base_path: Root directory for storing CSVs (default: 'data')
        """
        self.base_path = Path(base_path)
        self.user_profiles_dir = self.base_path / "user_profiles"
        self.economic_indicators_dir = self.base_path / "economic_indicators"
        
        # Create directories if they don't exist
        self.user_profiles_dir.mkdir(parents=True, exist_ok=True)
        self.economic_indicators_dir.mkdir(parents=True, exist_ok=True)
    
    def write_personal_finance(
        self,
        user_id: str,
        data: Dict[str, Any],
        date: Optional[str] = None,
        overwrite: bool = False
    ) -> Path:
        """Write personal finance data for a user.
        
        Args:
            user_id: Unique user identifier
            data: Dictionary containing personal finance fields
                - total_savings (float)
                - total_debt (float)
                - monthly_income (float)
                - monthly_expenses (float)
                - emergency_fund_months (float)
                - investment_accounts (float)
                - retirement_accounts (float)
                - credit_score (int)
                - debt_to_income_ratio (float)
            date: ISO format date (default: current date)
            overwrite: If True, overwrite existing file; if False, append
            
        Returns:
            Path to the created/updated CSV file
        """
        if date is None:
            date = datetime.now().isoformat().split('T')[0]
        
        file_path = self.user_profiles_dir / f"{user_id}.csv"
        
        # Prepare data with user_id and date
        row_data = {
            "user_id": user_id,
            "date": date,
            **data
        }
        
        # Define field order
        fieldnames = [
            "user_id", "date", "total_savings", "total_debt", "monthly_income",
            "monthly_expenses", "emergency_fund_months", "investment_accounts",
            "retirement_accounts", "credit_score", "debt_to_income_ratio"
        ]
        
        # Write or append to CSV
        file_exists = file_path.exists()
        mode = 'w' if (overwrite or not file_exists) else 'a'
        
        with open(file_path, mode, newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            if mode == 'w' or not file_exists:
                writer.writeheader()
            
            writer.writerow(row_data)
        
        return file_path
    
    def write_macro_indicators(
        self,
        data: Dict[str, Any],
        date: Optional[str] = None,
        append: bool = True
    ) -> Path:
        """Write macroeconomic indicators (inflation, unemployment, GDP, etc).
        
        Args:
            data: Dictionary containing macro indicator fields
                - inflation_rate (float)
                - unemployment_rate (float)
                - gdp_growth (float)
                - fed_funds_rate (float)
                - stock_market_index (float)
                - housing_market_trend (str)
            date: ISO format date (default: current date)
            append: If True, append to existing; if False, overwrite
            
        Returns:
            Path to the macro indicators CSV
        """
        if date is None:
            date = datetime.now().isoformat().split('T')[0]
        
        file_path = self.economic_indicators_dir / "macro_indicators.csv"
        
        row_data = {
            "date": date,
            **data
        }
        
        fieldnames = [
            "date", "inflation_rate", "unemployment_rate", "gdp_growth",
            "fed_funds_rate", "stock_market_index", "housing_market_trend"
        ]
        
        file_exists = file_path.exists()
        mode = 'a' if (append and file_exists) else 'w'
        
        with open(file_path, mode, newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            if mode == 'w' or not file_exists:
                writer.writeheader()
            
            writer.writerow(row_data)
        
        return file_path
    
    def write_micro_indicators(
        self,
        data: Dict[str, Any],
        date: Optional[str] = None,
        append: bool = True
    ) -> Path:
        """Write microeconomic indicators (industry, job market, sector, credit, wages).
        
        Args:
            data: Dictionary containing micro indicator fields
                - industry (str)
                - job_market_trend (str)
                - sector_volatility (str)
                - credit_availability (str)
                - wage_growth (float)
            date: ISO format date (default: current date)
            append: If True, append to existing; if False, overwrite
            
        Returns:
            Path to the micro indicators CSV
        """
        if date is None:
            date = datetime.now().isoformat().split('T')[0]
        
        file_path = self.economic_indicators_dir / "micro_indicators.csv"
        
        row_data = {
            "date": date,
            **data
        }
        
        fieldnames = [
            "date", "industry", "job_market_trend", "sector_volatility",
            "credit_availability", "wage_growth"
        ]
        
        file_exists = file_path.exists()
        mode = 'a' if (append and file_exists) else 'w'
        
        with open(file_path, mode, newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            if mode == 'w' or not file_exists:
                writer.writeheader()
            
            writer.writerow(row_data)
        
        return file_path


def write_user_personal_finance(
    user_id: str,
    data: Dict[str, Any],
    date: Optional[str] = None,
    base_path: str = "data"
) -> Path:
    """Convenience function to write personal finance data.
    
    Args:
        user_id: Unique user identifier
        data: Personal finance data dictionary
        date: ISO format date (default: current date)
        base_path: Root data directory
        
    Returns:
        Path to the created CSV file
    """
    writer = CSVWriter(base_path)
    return writer.write_personal_finance(user_id, data, date)


def write_macro_economic_data(
    data: Dict[str, Any],
    date: Optional[str] = None,
    base_path: str = "data"
) -> Path:
    """Convenience function to write macro indicators (from Yahoo Finance, etc).
    
    Args:
        data: Macro indicator data dictionary
        date: ISO format date (default: current date)
        base_path: Root data directory
        
    Returns:
        Path to the macro indicators CSV
    """
    writer = CSVWriter(base_path)
    return writer.write_macro_indicators(data, date)


def write_micro_economic_data(
    data: Dict[str, Any],
    date: Optional[str] = None,
    base_path: str = "data"
) -> Path:
    """Convenience function to write micro indicators.
    
    Args:
        data: Micro indicator data dictionary
        date: ISO format date (default: current date)
        base_path: Root data directory
        
    Returns:
        Path to the micro indicators CSV
    """
    writer = CSVWriter(base_path)
    return writer.write_micro_indicators(data, date)
