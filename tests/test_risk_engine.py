"""
Unit tests for the risk engine.
"""
import pytest
from datetime import datetime
from backend.engines.risk_engine import RiskEngine, Vulnerability, Severity, ScanResult


class TestRiskEngine:
    """Test suite for RiskEngine."""

    def test_risk_score_calculation(self) -> None:
        """Test risk score calculation logic."""
        vulns = [
            Vulnerability(
                module="Test",
                name="Critical Issue",
                severity=Severity.CRITICAL,
                description="Test",
                evidence="Test",
                mitigation="Test",
                owasp_category="LLM01: Prompt Injection"
            ),
            Vulnerability(
                module="Test",
                name="High Issue",
                severity=Severity.HIGH,
                description="Test",
                evidence="Test",
                mitigation="Test",
                owasp_category="LLM02: Insecure Output Handling"
            ),
        ]
        
        score = RiskEngine.calculate_risk_score(vulns)
        assert score == 17.0  # 10 (critical) + 7 (high)

    def test_risk_score_capped_at_100(self) -> None:
        """Test that risk score is capped at 100."""
        # Create many critical vulnerabilities
        vulns = [
            Vulnerability(
                module="Test",
                name=f"Issue {i}",
                severity=Severity.CRITICAL,
                description="Test",
                evidence="Test",
                mitigation="Test",
                owasp_category="LLM01: Prompt Injection"
            )
            for i in range(20)
        ]
        
        score = RiskEngine.calculate_risk_score(vulns)
        assert score == 100.0

    def test_owasp_mapping(self) -> None:
        """Test OWASP category mapping."""
        vulns = [
            Vulnerability(
                module="Test",
                name="Issue 1",
                severity=Severity.HIGH,
                description="Test",
                evidence="Test",
                mitigation="Test",
                owasp_category="LLM01: Prompt Injection"
            ),
            Vulnerability(
                module="Test",
                name="Issue 2",
                severity=Severity.MEDIUM,
                description="Test",
                evidence="Test",
                mitigation="Test",
                owasp_category="LLM01: Prompt Injection"
            ),
        ]
        
        mapping = RiskEngine.map_to_owasp(vulns)
        assert "LLM01: Prompt Injection" in mapping
        assert len(mapping["LLM01: Prompt Injection"]) == 2
