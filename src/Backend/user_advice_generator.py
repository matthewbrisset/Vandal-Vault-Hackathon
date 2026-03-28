"""User advice generator using Groq API."""

import os
from typing import Optional
from dotenv import load_dotenv
from groq import Groq
from src.Backend.csv_parser import FinancialRecord

# Load environment variables from .env file
load_dotenv()


class UserAdviceGenerator:
    """Generates financial advice using Groq API based on financial records."""
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize the UserAdviceGenerator.
        
        Args:
            api_key: Groq API key (uses GROQ_API_KEY env var if not provided)
            
        Raises:
            ValueError: If API key is not provided and not in environment
        """
        self.api_key = api_key or os.getenv("GROQ_API_KEY")
        
        if not self.api_key:
            raise ValueError(
                "Groq API key required. Provide via api_key parameter or set GROQ_API_KEY environment variable"
            )
        
        self.client = Groq(api_key=self.api_key)
        self.model = "llama-3.3-70b-versatile"
    
    def _build_prompt(self, record: FinancialRecord, macro_indicators: dict = None) -> str:
        """Build a prompt from financial record and optional macro indicators.
        
        Args:
            record: FinancialRecord containing financial data
            macro_indicators: Optional dict with keys: inflation, gdp, cci, market_performance
            
        Returns:
            Formatted prompt string for Groq
        """
        prompt = """You are a financial advisor specializing in recession preparedness. 
Analyze the following financial profile and economic context to provide practical advice for improving economic resilience.

FINANCIAL PROFILE:
"""
        
        # Add all available fields from the record
        for key in ['total_savings', 'total_debt', 'monthly_income', 'monthly_expenses', 
                    'emergency_fund_months', 'investment_accounts', 'retirement_accounts',
                    'credit_score', 'debt_to_income_ratio']:
            value = record.get(key)
            if value is not None:
                # Format currency fields
                if 'savings' in key or 'debt' in key or 'income' in key or 'expenses' in key or 'accounts' in key:
                    prompt += f"- {key.replace('_', ' ').title()}: ${value:,.2f}\n"
                elif 'months' in key:
                    prompt += f"- {key.replace('_', ' ').title()}: {value:.1f} months\n"
                elif 'ratio' in key:
                    prompt += f"- {key.replace('_', ' ').title()}: {value:.2f}\n"
                elif 'score' in key:
                    prompt += f"- {key.replace('_', ' ').title()}: {value}\n"
                else:
                    prompt += f"- {key.replace('_', ' ').title()}: {value}\n"
        
        # Add economic context
        if macro_indicators:
            prompt += "\nECONOMIC CONTEXT (Current Macro Indicators):\n"
            if macro_indicators.get('inflation') is not None:
                prompt += f"- Inflation Rate: {macro_indicators.get('inflation', 3.2):.1f}%\n"
            if macro_indicators.get('gdp') is not None:
                prompt += f"- GDP Growth: {macro_indicators.get('gdp', 2.5):.1f}%\n"
            if macro_indicators.get('cci') is not None:
                prompt += f"- Consumer Confidence Index: {macro_indicators.get('cci', 104.7):.1f}\n"
            if macro_indicators.get('market_performance') is not None:
                prompt += f"- Market Performance: {macro_indicators.get('market_performance', 0.05):.1f}%\n"
        
        prompt += """
Provide financial advice in the following EXACT format with exactly 3 bullet points per category:

HIGH PRIORITY:
- [Critical action 1]
- [Critical action 2]
- [Critical action 3]

MEDIUM PRIORITY:
- [Important action 1]
- [Important action 2]
- [Important action 3]

LOOKING GOOD:
- [Strength to maintain 1]
- [Strength to maintain 2]
- [Strength to maintain 3]"""
        
        return prompt
    
    def generate_advice(self, record: FinancialRecord, macro_indicators: dict = None) -> str:
        """Generate financial advice from a FinancialRecord.
        
        Args:
            record: FinancialRecord containing financial data
            macro_indicators: Optional dict with keys: inflation, gdp, cci, market_performance
            
        Returns:
            String containing AI-generated financial advice
            
        Raises:
            Exception: If API call fails
        """
        prompt = self._build_prompt(record, macro_indicators=macro_indicators)
        
        try:
            message = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.7,
                max_tokens=500,
            )
            
            return message.choices[0].message.content
        
        except Exception as e:
            raise Exception(f"Failed to generate advice from Groq API: {e}")


def generate_user_advice(record: FinancialRecord, macro_indicators: dict = None, api_key: Optional[str] = None) -> str:
    """Convenience function to generate advice from a FinancialRecord.
    
    Args:
        record: FinancialRecord containing financial data
        macro_indicators: Optional dict with keys: inflation, gdp, cci, market_performance
        api_key: Optional Groq API key (uses GROQ_API_KEY env var if not provided)
        
    Returns:
        String containing AI-generated financial advice
    """
    generator = UserAdviceGenerator(api_key=api_key)
    return generator.generate_advice(record, macro_indicators=macro_indicators)
