"""Pytest for Flask app endpoints."""

import pytest
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
            "emergency_fund_months": 4,
            "investment_accounts": 30000,
            "retirement_accounts": 80000,
            "credit_score": 680,
            "debt_to_income_ratio": 0.4
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
