# Vandal Vault: Recession Readiness Score

## Overview
A financial advisory tool that calculates your **Recession Readiness Score** (1-1000) and provides AI-powered advice to help you survive economic downturns and periods of high inflation. The score acts like a credit score, but for economic resilience.

## Core Concept
Using personal financial data and macro/micro economic indicators, the system evaluates how prepared you are for an economic crash and provides actionable guidance to improve your financial stability.

## Key Features

### 1. Recession Readiness Score (1-1000)
- **1-100**: High risk during economic downturn
- **101-500**: Moderate risk, needs preparation
- **501-750**: Good resilience, some vulnerable areas
- **751-1000**: Excellent economic preparedness

### 2. AI-Powered Analysis
- Parse financial and economic data using Groq API
- Generate personalized financial advice based on individual circumstances
- Provide specific action items to improve readiness score

### 3. Score Tracking
- Track score changes over time
- Understand which metrics improved or declined
- Monitor trends in personal financial health

## Tech Stack

### Packages
- **Groq API**: LLM for intelligent data analysis and financial advice generation
- **Yahoo Finance**: Real-time micro and macro economic indicators
- **Plaid**: Personal financial data aggregation and account linking
- **pandas**: CSV data processing and manipulation

## Implementation Plan

### Phase 1: Proof of Concept (MVP)
- Build CLI tool that accepts CSV file input
- CSV contains financial indicators (savings, debt, income, expenses, etc.)
- Groq LLM processes data and generates:
  - Recession Readiness Score (1-1000)
  - Financial advice tailored to the user
  - Score change metrics (up/down from previous assessment)

### Phase 2: Economic Indicators Integration
- Integrate Yahoo Finance for macro indicators (inflation, interest rates, VIX, etc.)
- Enrich analysis with real-time economic data
- Adjust scoring model based on current economic conditions

### Phase 3: Web Interface
- Build responsive web UI (React/Vue/Svelte)
- User dashboard showing Recession Readiness Score
- Historical score tracking and visualizations
- Financial advice recommendations display
- CSV file upload for desktop use
- Foundation for Plaid integration UI

### Phase 4: Full Integration
- Connect Plaid API for automatic personal finance data collection
- Real-time account monitoring and financial health updates
- Continuous scoring and notifications
- Mobile app support

## Data Flow

```
CSV Input (POC) / Plaid (Phase 3)
    ↓
Financial Data Aggregation
    ↓
Yahoo Finance Economic Indicators
    ↓
Groq LLM Processing
    ↓
Output:
  - Recession Readiness Score
  - Financial Advice
  - Score Change Indicator
```

## Success Criteria
✓ CLI tool accepts and processes CSV files  
✓ Generates recession readiness score (1-1000)  
✓ Provides actionable financial advice  
✓ Tracks and reports score changes  
✓ Foundation for future Plaid/Yahoo Finance integration
