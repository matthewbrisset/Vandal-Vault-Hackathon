# Vandal Vault - Recession Readiness Score Calculator

A financial advisory tool that calculates your recession readiness score (1-1000) and provides AI-powered recommendations using Groq API.

## Quick Start
- Command to host server: python -m src.Backend.app
- localhost:5000

### Prerequisites
- Python 3.9 or higher
- Groq API key (get free at https://console.groq.com)

### Setup (Windows)
```powershell
.\setup.ps1
```

### Setup (macOS/Linux)
```bash
chmod +x setup.sh
./setup.sh
```

## What the Setup Script Does
1. ✓ Creates a Python virtual environment
2. ✓ Installs all dependencies from `requirements.txt`
3. ✓ Creates `.env` file for API configuration
4. ✓ Ready to run!

## After Setup
1. Edit `.env` and add your `GROQ_API_KEY`:
   ```
   GROQ_API_KEY=your_actual_key_here
   ```

2. Run the test with sample data:
   ```bash
   pytest tests/test_user_advice_generator.py -v -s
   ```

## Project Structure
```
src/backend/
  ├── csv_parser.py          # CSV loading and parsing
  ├── user_advice_generator.py # Groq API integration
  └── __init__.py

tests/
  └── test_user_advice_generator.py  # Test suite

data/
  └── test_data/             # Sample CSV files
      ├── low_income.csv
      ├── medium_income.csv
      └── high_income.csv
```

## Usage

### Basic Example
```python
from src.backend.csv_parser import CSVParser
from src.backend.user_advice_generator import generate_user_advice

# Load financial data from CSV
parser = CSVParser("data/financial_data.csv")
record = parser.get_record(0)

# Generate AI advice
advice = generate_user_advice(record)
print(advice)
```

## API Documentation

### CSVParser
Loads and parses CSV files with financial data.

```python
parser = CSVParser("file.csv")
record = parser.get_record(0)          # Get first record
all = parser.get_all_records()         # Get all records
column = parser.get_column("savings")  # Get column data
```

### UserAdviceGenerator
Generates financial advice using Groq API.

```python
generator = UserAdviceGenerator(api_key="your_key")
advice = generator.generate_advice(financial_record)
```

## Running Tests
```bash
pytest tests/test_user_advice_generator.py -v -s
```

## Troubleshooting

**"GROQ_API_KEY not found"**
- Make sure you've edited `.env` with your actual API key

**"Module not found"**
- Make sure you've run the setup script to install dependencies
- Verify virtual environment is activated

**"CSV file not found"**
- Use full paths or relative paths from project root
- Example: `data/test_data/low_income.csv`

## Notes
- Virtual environment is in `.gitignore` - each teammate creates their own
- `.env` file is git-ignored for security - keep your API key private
- Test CSV files are included for quick testing

## Contributors
Vandal Vault Team
