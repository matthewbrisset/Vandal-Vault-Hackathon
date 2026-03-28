"""Flask web server for Vandal Vault - connects HTML frontend to Python backend."""

import os
from flask import Flask, request, jsonify, send_from_directory
from pathlib import Path
from src.Backend.csv_writer import write_user_personal_finance, write_macro_economic_data
from src.Backend.user_advice_generator import generate_user_advice
from src.Backend.score_calculator import calculate_resilience_score

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
        "emergency_fund_months": 4,
        "investment_accounts": 30000,
        "retirement_accounts": 80000,
        "credit_score": 680,
        "debt_to_income_ratio": 0.4
    }
    """
    try:
        data = request.json
        
        # Validate required fields
        required_fields = [
            "total_savings", "total_debt", "monthly_income",
            "monthly_expenses", "emergency_fund_months", "credit_score",
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
            "emergency_fund_months": float(data["emergency_fund_months"]),
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
            debt_to_income_ratio=csv_data["debt_to_income_ratio"]
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


@app.route("/api/health", methods=["GET"])
def health_check():
    """Health check endpoint."""
    return jsonify({"status": "healthy", "service": "Vandal Vault API"}), 200


if __name__ == "__main__":
    print("🚀 Starting Vandal Vault Flask Server")
    print("📍 Open http://localhost:5000 in your browser")
    print("⚠️  Press Ctrl+C to stop the server\n")
    app.run(debug=True, host="localhost", port=5000)
