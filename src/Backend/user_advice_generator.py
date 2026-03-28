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
    
    def _build_prompt(self, record: FinancialRecord) -> str:
        """Build a prompt from financial record.
        
        Args:
            record: FinancialRecord containing financial data
            
        Returns:
            Formatted prompt string for Groq
        """
        prompt = """You are a financial advisor specializing in recession preparedness. 
Analyze the following financial profile and provide practical advice for improving economic resilience.

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
        
        prompt += "\nProvide 3-5 specific, actionable recommendations to improve their financial resilience during economic downturns."
        
        return prompt
    
    def generate_advice(self, record: FinancialRecord) -> str:
        """Generate financial advice from a FinancialRecord.
        
        Args:
            record: FinancialRecord containing financial data
            
        Returns:
            String containing AI-generated financial advice
            
        Raises:
            Exception: If API call fails
        """
        prompt = self._build_prompt(record)
        
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


def generate_user_advice(record: FinancialRecord, api_key: Optional[str] = None) -> str:
    """Convenience function to generate advice from a FinancialRecord.
    
    Args:
        record: FinancialRecord containing financial data
        api_key: Optional Groq API key (uses GROQ_API_KEY env var if not provided)
        
    Returns:
        String containing AI-generated financial advice
    """
    generator = UserAdviceGenerator(api_key=api_key)
    return generator.generate_advice(record)
