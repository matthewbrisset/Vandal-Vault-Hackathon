"""Flask web server for Vandal Vault - connects HTML frontend to Python backend."""

import os
import io
import tempfile
from flask import Flask, request, jsonify, send_from_directory
from pathlib import Path
from src.Backend.csv_writer import write_user_personal_finance, write_macro_economic_data
from src.Backend.user_advice_generator import generate_user_advice
from src.Backend.score_calculator import calculate_resilience_score
from src.Backend.csv_parser import CSVParser

# Try to import macro_enricher for real economic data
try:
    from src.Backend.macro.yahoo_fetcher import fetch_yahoo_indicators
    from src.Backend.macro.fred_fetcher import fetch_fred_indicators
    MACRO_AVAILABLE = True
    print("✅ Macro data fetchers successfully imported!")
except Exception as e:
    print(f"⚠️  Macro data fetchers not available: {type(e).__name__}: {e}")
    MACRO_AVAILABLE = False

# Get the project root directory (where index.html is located)
PROJECT_ROOT = Path(__file__).parent.parent.parent
STATIC_DIR = PROJECT_ROOT

app = Flask(__name__, static_folder=str(STATIC_DIR), static_url_path="")


@app.route("/")
def index():
    """Serve the main HTML page."""
    return send_from_directory(str(STATIC_DIR), "index.html")


@app.route("/api/calculate-score", methods=["POST"])
def calculate_score():
    """Handle personal finance form submission and generate advice.
    
    Expected JSON payload:
    {
        "user_id": "user_001",
        "total_savings": 25000,
        "total_debt": 15000,
        "monthly_income": 5000,
        "monthly_expenses": 3500,
        "investment_accounts": 30000,
        "retirement_accounts": 80000,
        "credit_score": 680,
        "debt_to_income_ratio": 0.4,
        "inflation": 3.2,
        "gdp": 2.5,
        "cci": 104.7,
        "market_performance": 0.05
    }
    """
    try:
        data = request.json
        
        # Validate required fields
        required_fields = [
            "total_savings", "total_debt", "monthly_income",
            "monthly_expenses", "credit_score",
            "debt_to_income_ratio"
        ]
        
        missing = [f for f in required_fields if f not in data]
        if missing:
            return jsonify({"error": f"Missing fields: {missing}"}), 400
        
        # Get user ID (default if not provided)
        user_id = data.get("user_id", "default_user")
        
        # Prepare data for CSV writing
        csv_data = {
            "total_savings": float(data["total_savings"]),
            "total_debt": float(data["total_debt"]),
            "monthly_income": float(data["monthly_income"]),
            "monthly_expenses": float(data["monthly_expenses"]),
            "emergency_fund_months": float(data["total_savings"]) / float(data["monthly_expenses"]) if float(data["monthly_expenses"]) > 0 else 0,
            "investment_accounts": float(data.get("investment_accounts", 0)),
            "retirement_accounts": float(data.get("retirement_accounts", 0)),
            "credit_score": int(data["credit_score"]),
            "debt_to_income_ratio": float(data["debt_to_income_ratio"])
        }
        
        # Write to CSV
        write_user_personal_finance(user_id, csv_data)
        
        # Generate advice from Groq LLM
        advice = generate_user_advice(csv_data)
        
        # Calculate score using weighted scoring algorithm
        score = calculate_resilience_score(
            total_savings=csv_data["total_savings"],
            total_debt=csv_data["total_debt"],
            monthly_income=csv_data["monthly_income"],
            monthly_expenses=csv_data["monthly_expenses"],
            credit_score=csv_data["credit_score"],
            investment_accounts=csv_data["investment_accounts"],
            retirement_accounts=csv_data["retirement_accounts"],
            debt_to_income_ratio=csv_data["debt_to_income_ratio"],
            # Macro indicators with defaults
            inflation=float(data.get("inflation", 3.2)),
            gdp=float(data.get("gdp", 2.5)),
            cci=float(data.get("cci", 104.7)),
            market_performance=float(data.get("market_performance", 0.05))
        )
        
        return jsonify({
            "success": True,
            "user_id": user_id,
            "score": score,
            "advice": advice,
            "financial_data": csv_data
        }), 200
        
    except ValueError as e:
        return jsonify({"error": f"Invalid data types: {str(e)}"}), 400
    except Exception as e:
        return jsonify({"error": f"Server error: {str(e)}"}), 500


@app.route("/api/macro-indicators", methods=["POST"])
def add_macro_indicators():
    """Add macroeconomic indicators.
    
    Expected JSON payload:
    {
        "inflation_rate": 3.2,
        "unemployment_rate": 4.1,
        "gdp_growth": 2.5,
        "fed_funds_rate": 5.25,
        "stock_market_index": 5200,
        "housing_market_trend": "neutral"
    }
    """
    try:
        data = request.json
        
        required_fields = [
            "inflation_rate", "unemployment_rate", "gdp_growth",
            "fed_funds_rate", "stock_market_index", "housing_market_trend"
        ]
        
        missing = [f for f in required_fields if f not in data]
        if missing:
            return jsonify({"error": f"Missing fields: {missing}"}), 400
        
        macro_data = {
            "inflation_rate": float(data["inflation_rate"]),
            "unemployment_rate": float(data["unemployment_rate"]),
            "gdp_growth": float(data["gdp_growth"]),
            "fed_funds_rate": float(data["fed_funds_rate"]),
            "stock_market_index": float(data["stock_market_index"]),
            "housing_market_trend": str(data["housing_market_trend"])
        }
        
        write_macro_economic_data(macro_data)
        
        return jsonify({
            "success": True,
            "message": "Macro indicators saved",
            "data": macro_data
        }), 200
        
    except ValueError as e:
        return jsonify({"error": f"Invalid data types: {str(e)}"}), 400
    except Exception as e:
        return jsonify({"error": f"Server error: {str(e)}"}), 500


@app.route("/api/parse-csv", methods=["POST"])
def parse_csv():
    """Parse uploaded CSV file and return first record's financial data.
    
    Expects a multipart form data with 'file' containing CSV file.
    Returns the first data row mapped to form fields.
    """
    try:
        # Check if file is in request
        if 'file' not in request.files:
            return jsonify({"error": "No file provided"}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({"error": "No file selected"}), 400
        
        if not file.filename.endswith('.csv'):
            return jsonify({"error": "File must be a CSV file"}), 400
        
        # Read file contents and save to temporary file
        csv_content = file.read().decode('utf-8')
        
        # Create temporary file in system temp directory
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, encoding='utf-8') as temp_file:
            temp_file.write(csv_content)
            temp_path = temp_file.name
        
        try:
            # Parse CSV using CSVParser
            parser = CSVParser(temp_path)
            
            if not parser.records:
                return jsonify({"error": "CSV file is empty or contains no data rows"}), 400
            
            # Get first record
            first_record = parser.get_record(0)
            record_data = first_record.data
            
            # Map CSV fields to form field IDs (case-insensitive matching)
            form_data = {}
            field_mapping = {
                'total_savings': 'total_savings',
                'total_debt': 'total_debt',
                'monthly_income': 'monthly_income',
                'monthly_expenses': 'monthly_expenses',
                'investment_accounts': 'investment_accounts',
                'retirement_accounts': 'retirement_accounts',
                'credit_score': 'credit_score',
                'debt_to_income_ratio': 'debt_to_income_ratio',
                # Macro indicators
                'inflation': 'inflation',
                'gdp': 'gdp',
                'cci': 'cci',
                'market_performance': 'market_performance'
            }
            
            # Match CSV columns to form fields (case-insensitive)
            for csv_col in parser.headers:
                col_lower = csv_col.lower().strip()
                for form_field in field_mapping.keys():
                    if col_lower == form_field.lower() or col_lower.replace('_', ' ') == form_field.replace('_', ' '):
                        value = record_data.get(csv_col)
                        if value is not None:
                            form_data[field_mapping[form_field]] = value
            
            return jsonify({
                "success": True,
                "data": form_data,
                "headers": parser.headers,
                "message": f"Parsed CSV with {len(parser.records)} records"
            }), 200
            
        finally:
            # Clean up temp file
            try:
                os.remove(temp_path)
            except:
                pass
        
    except Exception as e:
        return jsonify({"error": f"Error parsing CSV: {str(e)}"}), 500




@app.route("/api/fetch-macro-data", methods=["GET"])
def fetch_macro_data():
    """Fetch real macroeconomic data from FRED and Yahoo Finance APIs.
    
    Returns:
    {
        "success": boolean,
        "data": {
            "inflation": float (inflation rate %),
            "gdp": float (GDP growth %),
            "cci": float (Consumer Confidence Index),
            "market_performance": float (S&P 500 return %),
            "vix": float (Market Volatility Index),
            "fed_funds_rate": float,
            "unemployment_rate": float
        },
        "source": "real-time economic data",
        "message": string
    }
    """
    if not MACRO_AVAILABLE:
        return jsonify({
            "success": False,
            "message": "Macro data fetchers not configured. Please install yfinance and configure FRED_API_KEY in .env",
            "data": None
        }), 503
    
    try:
        # Fetch real data from APIs
        yahoo_data = fetch_yahoo_indicators()
        fred_data = fetch_fred_indicators()
        
        # Map fetched data to form field names
        macro_data = {
            "inflation": fred_data.get("inflation", 3.2),  # Default fallback (PCE inflation %)
            "gdp": fred_data.get("gdp", 2.5),  # Default fallback
            "cci": 104.7,  # Not directly available, keeping default
            "market_performance": (yahoo_data.get("sp500", 5000) / 5000 - 1) * 100 if yahoo_data.get("sp500") else 0.05,
            "vix": yahoo_data.get("vix"),
            "fed_funds_rate": fred_data.get("fed_funds_rate"),
            "unemployment_rate": fred_data.get("unemployment_rate"),
            "mortgage_rate_30yr": fred_data.get("mortgage_rate_30yr")
        }
        
        return jsonify({
            "success": True,
            "data": macro_data,
            "source": "real-time FRED & Yahoo Finance APIs",
            "message": "Successfully fetched real-time macro indicators"
        }), 200
        
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Error fetching macro data: {str(e)}",
            "data": None
        }), 500


@app.route("/api/health", methods=["GET"])
def health_check():
    """Health check endpoint."""
    return jsonify({"status": "healthy", "service": "Vandal Vault API"}), 200


if __name__ == "__main__":
    print("🚀 Starting Vandal Vault Flask Server")
    print("📍 Open http://localhost:5000 in your browser")
    print("⚠️  Press Ctrl+C to stop the server\n")
    app.run(debug=True, host="localhost", port=5000)
