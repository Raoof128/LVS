"""
Integration tests for the API endpoints.
"""
import pytest
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)


class TestScanAPI:
    """Test suite for scan API endpoints."""

    def test_root_endpoint(self) -> None:
        """Test root endpoint returns expected message."""
        response = client.get("/")
        assert response.status_code == 200
        assert "Scanner" in response.json()["message"]

    def test_scan_endpoint_mock(self) -> None:
        """Test scan endpoint with mock target."""
        response = client.post(
            "/api/v1/scan",
            json={"target_type": "mock"}
        )
        
        assert response.status_code == 200
        data = response.json()
        
        assert "risk_score" in data
        assert "vulnerabilities" in data
        assert "total_tests" in data
        assert data["total_tests"] > 0

    def test_history_endpoint(self) -> None:
        """Test history endpoint returns scan results."""
        # First, run a scan
        client.post("/api/v1/scan", json={"target_type": "mock"})
        
        # Then check history
        response = client.get("/api/v1/history")
        assert response.status_code == 200
        
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0

    def test_mitigations_endpoint(self) -> None:
        """Test mitigation recommendations endpoint."""
        # Run a scan first
        client.post("/api/v1/scan", json={"target_type": "mock"})
        
        # Get mitigations
        response = client.get("/api/v1/mitigations/0")
        assert response.status_code == 200
        
        data = response.json()
        assert "summary" in data
        assert "recommendations" in data

    def test_invalid_scan_index(self) -> None:
        """Test that invalid scan index returns 404."""
        response = client.get("/api/v1/mitigations/999")
        assert response.status_code == 404
