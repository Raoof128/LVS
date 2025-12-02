"""
API endpoints for vulnerability scanning and reporting.
"""
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime
from pathlib import Path

from ..engines.target_wrapper import MockLLM, APITargetLLM
from ..engines.risk_engine import RiskEngine, ScanResult
from ..engines.prompt_injection import PromptInjectionScanner
from ..engines.data_leakage import DataLeakageScanner
from ..engines.hallucination import HallucinationScanner
from ..engines.insecure_output import InsecureOutputScanner
from ..engines.data_poisoning import DataPoisoningScanner
from ..engines.supply_chain import SupplyChainScanner
from ..engines.excessive_agency import ExcessiveAgencyScanner
from ..engines.overreliance import OverrelianceScanner
from ..engines.model_theft import ModelTheftScanner
from ..engines.mitigation_engine import MitigationEngine
from ..utils.pdf_export import generate_pdf_report
from ..utils.logger import setup_logger

logger = setup_logger(__name__)

router = APIRouter()


class ScanRequest(BaseModel):
    """Request model for vulnerability scans."""

    target_type: str = "mock"  # mock or api
    target_url: Optional[str] = None
    api_key: Optional[str] = None
    model_name: Optional[str] = "gpt-3.5-turbo"


# In-memory storage for demo purposes
scan_history: List[ScanResult] = []


@router.post("/scan", response_model=ScanResult)
async def run_scan(request: ScanRequest) -> ScanResult:
    """
    Triggers a full OWASP Top 10 vulnerability scan on the target LLM.

    Args:
        request: Scan configuration

    Returns:
        Complete scan results with vulnerabilities and risk score
    """
    logger.info(f"Starting scan for target type: {request.target_type}")

    # 1. Initialize Target
    if request.target_type == "mock":
        target = MockLLM()
    else:
        if not request.api_key or not request.target_url:
            raise HTTPException(status_code=400, detail="API key and URL required for API targets")
        target = APITargetLLM(request.api_key, request.target_url, request.model_name)

    # 2. Initialize ALL Scanner Modules (OWASP Top 10)
    scanners = [
        PromptInjectionScanner(),  # LLM01
        InsecureOutputScanner(),  # LLM02
        DataPoisoningScanner(),  # LLM03
        DataLeakageScanner(),  # LLM06
        SupplyChainScanner(),  # LLM05
        ExcessiveAgencyScanner(),  # LLM08
        HallucinationScanner(),  # LLM09
        OverrelianceScanner(),  # LLM09
        ModelTheftScanner(),  # LLM10
    ]

    all_vulnerabilities = []
    passed = 0
    failed = 0

    # 3. Run All Scans
    for scanner in scanners:
        logger.info(f"Running scanner: {scanner.__class__.__name__}")
        try:
            vulns = scanner.scan(target)
            if vulns:
                failed += 1
                all_vulnerabilities.extend(vulns)
                logger.warning(f"{scanner.__class__.__name__} found {len(vulns)} vulnerabilities")
            else:
                passed += 1
                logger.info(f"{scanner.__class__.__name__} passed")
        except Exception as e:
            logger.error(f"Error running {scanner.__class__.__name__}: {str(e)}")

    # 4. Calculate Risk
    risk_score = RiskEngine.calculate_risk_score(all_vulnerabilities)

    # 5. Compile Result
    result = ScanResult(
        target_metadata=target.get_metadata(),
        timestamp=datetime.now(),
        risk_score=risk_score,
        vulnerabilities=all_vulnerabilities,
        passed_tests=passed,
        failed_tests=failed,
        total_tests=passed + failed,
    )

    scan_history.append(result)
    logger.info(f"Scan complete. Risk Score: {risk_score}, Vulnerabilities: {len(all_vulnerabilities)}")
    return result


@router.get("/history", response_model=List[ScanResult])
async def get_history() -> List[ScanResult]:
    """
    Retrieve scan history.

    Returns:
        List of all previous scan results
    """
    return scan_history


@router.get("/mitigations/{scan_index}")
async def get_mitigations(scan_index: int) -> dict:
    """
    Get mitigation recommendations for a specific scan.

    Args:
        scan_index: Index of the scan in history

    Returns:
        Mitigation recommendations report
    """
    if scan_index >= len(scan_history):
        raise HTTPException(status_code=404, detail="Scan not found")

    scan = scan_history[scan_index]
    report = MitigationEngine.generate_report(scan.vulnerabilities)
    return report


@router.get("/export/pdf/{scan_index}")
async def export_pdf(scan_index: int) -> FileResponse:
    """
    Export a scan report as PDF.

    Args:
        scan_index: Index of the scan in history

    Returns:
        PDF file download
    """
    if scan_index >= len(scan_history):
        raise HTTPException(status_code=404, detail="Scan not found")

    scan = scan_history[scan_index]
    
    # Generate PDF
    reports_dir = Path("reports")
    reports_dir.mkdir(exist_ok=True)
    
    filename = f"llm_scan_report_{scan.timestamp.strftime('%Y%m%d_%H%M%S')}.pdf"
    filepath = reports_dir / filename
    
    generate_pdf_report(scan, str(filepath))
    
    logger.info(f"Generated PDF report: {filepath}")
    return FileResponse(
        path=str(filepath),
        filename=filename,
        media_type="application/pdf"
    )
