from enum import Enum
from typing import List, Dict, Any, Optional
from pydantic import BaseModel
from datetime import datetime

class Severity(str, Enum):
    CRITICAL = "Critical"
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"
    INFO = "Info"

class Vulnerability(BaseModel):
    module: str
    name: str
    severity: Severity
    description: str
    evidence: str
    mitigation: str
    owasp_category: str
    timestamp: datetime = datetime.now()

class ScanResult(BaseModel):
    target_metadata: Dict[str, Any]
    timestamp: datetime
    risk_score: float
    vulnerabilities: List[Vulnerability]
    passed_tests: int
    failed_tests: int
    total_tests: int

class RiskEngine:
    """
    Aggregates findings and calculates risk scores.
    """
    
    SEVERITY_WEIGHTS = {
        Severity.CRITICAL: 10.0,
        Severity.HIGH: 7.0,
        Severity.MEDIUM: 4.0,
        Severity.LOW: 1.0,
        Severity.INFO: 0.0
    }

    @staticmethod
    def calculate_risk_score(vulnerabilities: List[Vulnerability]) -> float:
        """
        Calculates a risk score from 0 to 100 based on vulnerabilities found.
        Simple additive model capped at 100.
        """
        score = 0.0
        for v in vulnerabilities:
            score += RiskEngine.SEVERITY_WEIGHTS[v.severity]
        
        return min(score, 100.0)

    @staticmethod
    def map_to_owasp(vulnerabilities: List[Vulnerability]) -> Dict[str, List[Vulnerability]]:
        """
        Groups vulnerabilities by OWASP Top 10 category.
        """
        mapping: Dict[str, List[Vulnerability]] = {}
        for v in vulnerabilities:
            if v.owasp_category not in mapping:
                mapping[v.owasp_category] = []
            mapping[v.owasp_category].append(v)
        return mapping
