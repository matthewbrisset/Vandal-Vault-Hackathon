"""Pytest for Flask app endpoints."""

import pytest
import tempfile
import os
from io import BytesIO
from src.Backend.app import app


@pytest.fixture
def client():
    """Create a test client for the Flask app."""
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


class TestAPIEndpoints:
    """Test Flask API endpoints."""
    
    def test_health_check(self, client):
        """Test health check endpoint."""
        response = client.get("/api/health")
        assert response.status_code == 200
        data = response.get_json()
        assert data["status"] == "healthy"
        assert data["service"] == "Vandal Vault API"
    
    def test_calculate_score_success(self, client):
        """Test successful score calculation."""
        payload = {
            "user_id": "test_user",
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
        
        response = client.post("/api/calculate-score", json=payload)
        assert response.status_code == 200
        
        data = response.get_json()
        assert data["success"] is True
        assert data["user_id"] == "test_user"
        assert "score" in data
        assert 1 <= data["score"] <= 1000
        assert "advice" in data
        assert len(data["advice"]) > 0
    
    def test_calculate_score_missing_fields(self, client):
        """Test score calculation with missing required fields."""
        payload = {
            "user_id": "test_user",
            "total_savings": 25000,
            # Missing other required fields
        }
        
        response = client.post("/api/calculate-score", json=payload)
        assert response.status_code == 400
        data = response.get_json()
        assert "error" in data
        assert "Missing fields" in data["error"]
    
    def test_calculate_score_invalid_data_type(self, client):
        """Test score calculation with invalid data types."""
        payload = {
            "user_id": "test_user",
            "total_savings": "not_a_number",  # Should be numeric
            "total_debt": 15000,
            "monthly_income": 5000,
            "monthly_expenses": 3500,
            "emergency_fund_months": 4,
            "credit_score": 680,
            "debt_to_income_ratio": 0.4
        }
        
        response = client.post("/api/calculate-score", json=payload)
        assert response.status_code == 400
        data = response.get_json()
        assert "error" in data
    
    def test_macro_indicators_success(self, client):
        """Test successful macro indicator submission."""
        payload = {
            "inflation_rate": 3.2,
            "unemployment_rate": 4.1,
            "gdp_growth": 2.5,
            "fed_funds_rate": 5.25,
            "stock_market_index": 5200,
            "housing_market_trend": "neutral"
        }
        
        response = client.post("/api/macro-indicators", json=payload)
        assert response.status_code == 200
        
        data = response.get_json()
        assert data["success"] is True
        assert "Macro indicators saved" in data["message"]
    
    def test_macro_indicators_missing_fields(self, client):
        """Test macro indicators with missing fields."""
        payload = {
            "inflation_rate": 3.2,
            # Missing other required fields
        }
        
        response = client.post("/api/macro-indicators", json=payload)
        assert response.status_code == 400
        data = response.get_json()
        assert "error" in data
        assert "Missing fields" in data["error"]
    
    def test_parse_csv_success(self, client):
        """Test successful CSV parsing and form population."""
        # Create a temporary CSV file with personal and macro indicators
        csv_content = b"""total_savings,total_debt,monthly_income,monthly_expenses,investment_accounts,retirement_accounts,credit_score,debt_to_income_ratio,inflation,gdp,cci,market_performance
25000,15000,5000,3500,30000,80000,680,0.4,3.2,2.5,104.7,0.05"""
        
        data = {
            'file': (BytesIO(csv_content), 'test_financial.csv')
        }
        
        response = client.post("/api/parse-csv", data=data, content_type='multipart/form-data')
        assert response.status_code == 200
        
        result = response.get_json()
        assert result["success"] is True
        assert "data" in result
        assert result["data"]["total_savings"] == 25000
        assert result["data"]["monthly_income"] == 5000
        assert result["data"]["credit_score"] == 680
        # Check macro indicators are also parsed
        assert result["data"]["inflation"] == 3.2
        assert result["data"]["gdp"] == 2.5
        assert result["data"]["cci"] == 104.7
        assert result["data"]["market_performance"] == 0.05
    
    def test_parse_csv_missing_file(self, client):
        """Test CSV parsing without file."""
        response = client.post("/api/parse-csv", data={}, content_type='multipart/form-data')
        assert response.status_code == 400
        data = response.get_json()
        assert "error" in data
        assert "No file provided" in data["error"]
    
    def test_parse_csv_invalid_format(self, client):
        """Test CSV parsing with non-CSV file."""
        invalid_content = b"This is not a CSV file"
        
        data = {
            'file': (BytesIO(invalid_content), 'test.txt')
        }
        
        response = client.post("/api/parse-csv", data=data, content_type='multipart/form-data')
        assert response.status_code == 400
        result = response.get_json()
        assert "error" in result
    
    def test_macro_indicators_affect_score(self, client):
        """Test that different macro indicators produce different scores."""
        base_payload = {
            "user_id": "test_user",
            "total_savings": 25000,
            "total_debt": 15000,
            "monthly_income": 5000,
            "monthly_expenses": 3500,
            "investment_accounts": 30000,
            "retirement_accounts": 80000,
            "credit_score": 680,
            "debt_to_income_ratio": 0.4
        }
        
        # Test with good macro conditions
        good_macro = {**base_payload, "inflation": 2.0, "gdp": 3.5, "cci": 110.0, "market_performance": 0.10}
        response_good = client.post("/api/calculate-score", json=good_macro)
        score_good = response_good.get_json()["score"]
        
        # Test with poor macro conditions
        poor_macro = {**base_payload, "inflation": 5.0, "gdp": -1.0, "cci": 90.0, "market_performance": -0.10}
        response_poor = client.post("/api/calculate-score", json=poor_macro)
        score_poor = response_poor.get_json()["score"]
        
        # Good macro should score higher than poor macro (with same personal finances)
        assert score_good > score_poor, f"Good macro ({score_good}) should beat poor macro ({score_poor})"
    
    def test_fetch_macro_data_endpoint(self, client):
        """Test macro data fetching endpoint."""
        response = client.get("/api/fetch-macro-data")
        
        # Endpoint should return 200 or 503 (depending on API availability)
        assert response.status_code in [200, 503]
        
        data = response.get_json()
        assert "success" in data
        assert "message" in data
        
        if response.status_code == 200:
            assert data["success"] is True
            assert "data" in data
            # Should contain macro data fields
            assert any(k in data["data"] for k in ["inflation", "gdp", "market_performance"])


class TestResilienceScore:
    """Test resilience score calculation logic."""
    
    def test_score_with_high_emergency_fund(self):
        """Test score calculation with good emergency fund."""
        from src.Backend.score_calculator import calculate_resilience_score
        
        score = calculate_resilience_score(
            total_savings=100000,
            total_debt=5000,
            monthly_income=10000,
            monthly_expenses=5000,
            credit_score=800,
            investment_accounts=50000,
            retirement_accounts=200000,
            debt_to_income_ratio=0.2
        )
        assert score > 600, f"Good profile should score above 600, got {score}"
    
    def test_score_with_poor_emergency_fund(self):
        """Test score calculation with poor emergency fund."""
        from src.Backend.score_calculator import calculate_resilience_score
        
        score = calculate_resilience_score(
            total_savings=1000,
            total_debt=30000,
            monthly_income=3000,
            monthly_expenses=3000,
            credit_score=550,
            investment_accounts=0,
            retirement_accounts=5000,
            debt_to_income_ratio=1.5
        )
        assert score < 300, f"Poor profile should score below 300, got {score}"
    
    def test_score_range(self):
        """Test that score is always between 1 and 1000."""
        from src.Backend.score_calculator import calculate_resilience_score
        
        # Test extreme negative case
        score = calculate_resilience_score(
            total_savings=0,
            total_debt=100000,
            monthly_income=2000,
            monthly_expenses=3000,
            credit_score=300,
            investment_accounts=0,
            retirement_accounts=0,
            debt_to_income_ratio=50
        )
        assert 1 <= score <= 1000, f"Score {score} out of valid range"
        
        # Test extreme positive case
        score = calculate_resilience_score(
            total_savings=1000000,
            total_debt=1000,
            monthly_income=20000,
            monthly_expenses=5000,
            credit_score=850,
            investment_accounts=500000,
            retirement_accounts=1000000,
            debt_to_income_ratio=0.05
        )
        assert 1 <= score <= 1000, f"Score {score} out of valid range"
