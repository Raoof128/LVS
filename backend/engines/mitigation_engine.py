"""
Mitigation recommendation engine that provides actionable security guidance.
"""
from typing import List, Dict, Any
from ..engines.risk_engine import Vulnerability, Severity


class MitigationEngine:
    """
    Generates mitigation recommendations based on discovered vulnerabilities.
    """

    # OWASP Top 10 LLM Mitigation Library
    MITIGATION_LIBRARY: Dict[str, Dict[str, Any]] = {
        "LLM01: Prompt Injection": {
            "strategy": "Input Validation & Instruction Isolation",
            "controls": [
                "Implement strict input sanitization and validation",
                "Use separate channels for system instructions vs user data",
                "Apply output encoding and content filtering",
                "Use privilege bracketing for system commands",
                "Implement prompt shields and guardrails",
            ],
        },
        "LLM02: Insecure Output Handling": {
            "strategy": "Output Sanitization & Validation",
            "controls": [
                "Encode all model outputs before rendering",
                "Implement content security policies (CSP)",
                "Apply context-aware output filtering",
                "Use sandboxing for code execution",
                "Validate outputs against expected schemas",
            ],
        },
        "LLM03: Training Data Poisoning": {
            "strategy": "Data Provenance & Quality Assurance",
            "controls": [
                "Verify training data sources and provenance",
                "Implement data quality checks and anomaly detection",
                "Use differential privacy techniques",
                "Conduct adversarial robustness testing",
                "Maintain audit trails for training data",
            ],
        },
        "LLM04: Model Denial of Service": {
            "strategy": "Resource Management & Rate Limiting",
            "controls": [
                "Implement rate limiting per user/API key",
                "Set maximum token limits for inputs/outputs",
                "Use request queuing and prioritization",
                "Monitor resource consumption metrics",
                "Apply circuit breakers for cascading failures",
            ],
        },
        "LLM05: Supply Chain Vulnerabilities": {
            "strategy": "Supply Chain Security & Verification",
            "controls": [
                "Verify plugin and dependency signatures",
                "Use Software Bill of Materials (SBOM)",
                "Implement plugin sandboxing",
                "Conduct third-party security audits",
                "Maintain allow-lists for approved components",
            ],
        },
        "LLM06: Sensitive Information Disclosure": {
            "strategy": "Data Minimization & Access Control",
            "controls": [
                "Scrub PII/secrets from training and prompt data",
                "Implement output filtering for sensitive patterns",
                "Use data loss prevention (DLP) tools",
                "Apply role-based access control (RBAC)",
                "Conduct regular security audits",
            ],
        },
        "LLM07: Insecure Plugin Design": {
            "strategy": "Secure Plugin Architecture",
            "controls": [
                "Validate all plugin inputs/outputs",
                "Implement least-privilege access for plugins",
                "Use type checking and schema validation",
                "Sandbox plugin execution environments",
                "Audit plugin behavior and logs",
            ],
        },
        "LLM08: Excessive Agency": {
            "strategy": "Action Authorization & Human-in-the-Loop",
            "controls": [
                "Require explicit user consent for high-risk actions",
                "Implement action allow-lists",
                "Use step-by-step confirmations",
                "Log all autonomous actions",
                "Apply blast radius limits",
            ],
        },
        "LLM09: Overreliance": {
            "strategy": "Transparency & Uncertainty Communication",
            "controls": [
                "Display confidence scores with outputs",
                "Use retrieval-augmented generation (RAG)",
                "Provide source citations",
                "Implement fact-checking mechanisms",
                "Educate users on model limitations",
            ],
        },
        "LLM10: Model Theft": {
            "strategy": "Model Protection & Monitoring",
            "controls": [
                "Implement rate limiting and usage quotas",
                "Use watermarking and fingerprinting",
                "Monitor for extraction attempts",
                "Apply model obfuscation techniques",
                "Enforce strict API authentication",
            ],
        },
    }

    @staticmethod
    def generate_report(vulnerabilities: List[Vulnerability]) -> Dict[str, Any]:
        """
        Generate a comprehensive mitigation report.

        Args:
            vulnerabilities: List of discovered vulnerabilities

        Returns:
            Structured mitigation report
        """
        report: Dict[str, Any] = {
            "summary": {
                "total_vulnerabilities": len(vulnerabilities),
                "critical": sum(1 for v in vulnerabilities if v.severity == Severity.CRITICAL),
                "high": sum(1 for v in vulnerabilities if v.severity == Severity.HIGH),
                "medium": sum(1 for v in vulnerabilities if v.severity == Severity.MEDIUM),
                "low": sum(1 for v in vulnerabilities if v.severity == Severity.LOW),
            },
            "recommendations": [],
        }

        # Group by OWASP category
        categories = set(v.owasp_category for v in vulnerabilities)

        for category in categories:
            if category in MitigationEngine.MITIGATION_LIBRARY:
                mitigation = MitigationEngine.MITIGATION_LIBRARY[category]
                report["recommendations"].append(
                    {
                        "category": category,
                        "strategy": mitigation["strategy"],
                        "controls": mitigation["controls"],
                        "affected_vulnerabilities": [
                            v.name for v in vulnerabilities if v.owasp_category == category
                        ],
                    }
                )

        return report
