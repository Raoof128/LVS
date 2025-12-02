"""
Unit tests for vulnerability scanner modules.
"""
import pytest
from backend.engines.target_wrapper import MockLLM
from backend.engines.prompt_injection import PromptInjectionScanner
from backend.engines.data_leakage import DataLeakageScanner
from backend.engines.hallucination import HallucinationScanner
from backend.engines.risk_engine import Severity


class TestPromptInjectionScanner:
    """Test suite for PromptInjectionScanner."""

    def test_detects_injection(self) -> None:
        """Test that scanner detects prompt injection vulnerabilities."""
        scanner = PromptInjectionScanner()
        target = MockLLM()
        vulns = scanner.scan(target)
        
        assert len(vulns) > 0
        assert any("Injection" in v.module for v in vulns)
        assert any(v.severity == Severity.HIGH or v.severity == Severity.CRITICAL for v in vulns)


class TestDataLeakageScanner:
    """Test suite for DataLeakageScanner."""

    def test_detects_leakage(self) -> None:
        """Test that scanner detects data leakage."""
        scanner = DataLeakageScanner()
        target = MockLLM()
        vulns = scanner.scan(target)
        
        assert len(vulns) > 0
        assert any("Leakage" in v.module for v in vulns)


class TestHallucinationScanner:
    """Test suite for HallucinationScanner."""

    def test_detects_hallucination(self) -> None:
        """Test that scanner detects hallucinations."""
        scanner = HallucinationScanner()
        target = MockLLM()
        vulns = scanner.scan(target)
        
        assert len(vulns) > 0
        assert any("Hallucination" in v.module for v in vulns)
        assert all(v.owasp_category == "LLM09: Overreliance" for v in vulns)
