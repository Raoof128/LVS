"""
PDF export functionality for vulnerability reports.
"""
from datetime import datetime
from typing import List, Dict, Any
from pathlib import Path
from fpdf import FPDF
from backend.engines.risk_engine import ScanResult, Vulnerability, Severity


class PDFReporter(FPDF):
    """
    Custom PDF class for generating vulnerability scan reports.
    """

    def header(self) -> None:
        """Add report header."""
        self.set_font("Arial", "B", 16)
        self.cell(0, 10, "LLM Vulnerability Scan Report", border=0, ln=1, align="C")
        self.set_font("Arial", "I", 10)
        self.cell(0, 5, f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=1, align="C")
        self.ln(10)

    def footer(self) -> None:
        """Add report footer."""
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.cell(0, 10, f"Page {self.page_no()}", align="C")

    def add_section_title(self, title: str) -> None:
        """Add a section title."""
        self.set_font("Arial", "B", 14)
        self.set_fill_color(59, 130, 246)
        self.set_text_color(255, 255, 255)
        self.cell(0, 10, title, border=0, ln=1, fill=True)
        self.set_text_color(0, 0, 0)
        self.ln(5)

    def add_key_value(self, key: str, value: str) -> None:
        """Add a key-value pair."""
        self.set_font("Arial", "B", 11)
        self.cell(60, 8, f"{key}:", border=0)
        self.set_font("Arial", "", 11)
        self.cell(0, 8, str(value), border=0, ln=1)


def generate_pdf_report(scan_result: ScanResult, output_path: str) -> str:
    """
    Generate a comprehensive PDF report from scan results.

    Args:
        scan_result: The scan result object
        output_path: Path to save the PDF file

    Returns:
        Path to the generated PDF file
    """
    pdf = PDFReporter()
    pdf.add_page()

    # Executive Summary
    pdf.add_section_title("Executive Summary")
    pdf.add_key_value("Target Model", scan_result.target_metadata.get("name", "Unknown"))
    pdf.add_key_value("Provider", scan_result.target_metadata.get("provider", "Unknown"))
    pdf.add_key_value("Scan Date", scan_result.timestamp.strftime("%Y-%m-%d %H:%M:%S"))
    pdf.add_key_value("Risk Score", f"{scan_result.risk_score:.1f} / 100")
    pdf.add_key_value("Total Tests", str(scan_result.total_tests))
    pdf.add_key_value("Passed", str(scan_result.passed_tests))
    pdf.add_key_value("Failed", str(scan_result.failed_tests))
    pdf.ln(5)

    # Severity Breakdown
    pdf.add_section_title("Severity Breakdown")
    severity_counts: Dict[Severity, int] = {}
    for vuln in scan_result.vulnerabilities:
        severity_counts[vuln.severity] = severity_counts.get(vuln.severity, 0) + 1

    for severity in [Severity.CRITICAL, Severity.HIGH, Severity.MEDIUM, Severity.LOW]:
        count = severity_counts.get(severity, 0)
        pdf.add_key_value(severity.value, str(count))
    pdf.ln(5)

    # Detailed Findings
    pdf.add_section_title("Detailed Findings")

    for i, vuln in enumerate(scan_result.vulnerabilities, 1):
        pdf.set_font("Arial", "B", 12)
        
        # Set color based on severity
        if vuln.severity == Severity.CRITICAL:
            pdf.set_text_color(239, 68, 68)
        elif vuln.severity == Severity.HIGH:
            pdf.set_text_color(249, 115, 22)
        elif vuln.severity == Severity.MEDIUM:
            pdf.set_text_color(245, 158, 11)
        else:
            pdf.set_text_color(59, 130, 246)

        pdf.cell(0, 8, f"{i}. [{vuln.severity.value}] {vuln.name}", ln=1)
        pdf.set_text_color(0, 0, 0)

        pdf.set_font("Arial", "I", 10)
        pdf.multi_cell(0, 6, f"OWASP: {vuln.owasp_category}")
        pdf.set_font("Arial", "", 10)
        pdf.multi_cell(0, 6, f"Description: {vuln.description}")
        pdf.multi_cell(0, 6, f"Evidence: {vuln.evidence[:200]}...")
        pdf.set_font("Arial", "B", 10)
        pdf.multi_cell(0, 6, f"Mitigation: {vuln.mitigation}")
        pdf.ln(3)

    # Save the PDF
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    pdf.output(output_path)
    return output_path
