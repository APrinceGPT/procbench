"""
API routes for ProcBench backend.
"""

import io
import logging
from typing import Any
from uuid import uuid4

from fastapi import APIRouter, File, UploadFile, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse, Response
from pydantic import BaseModel

from app.config import settings
from app.report import PDFGenerator
from app.analysis import Analyzer, generate_timeline, timeline_to_dict, tree_to_dict
from app.parsers import ParserFactory


logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1", tags=["analysis"])

# In-memory storage for analysis results (would be Redis/DB in production)
_analysis_cache: dict[str, dict[str, Any]] = {}


# Response Models
class AnalysisStartResponse(BaseModel):
    analysis_id: str
    status: str
    message: str


class AnalysisStatusResponse(BaseModel):
    analysis_id: str
    status: str
    progress: int
    message: str


class ProcessSummary(BaseModel):
    pid: int
    process_name: str
    image_path: str | None
    risk_score: int
    legitimacy: str
    behavior_tags: list[str]
    is_flagged: bool


class AnalysisSummaryResponse(BaseModel):
    analysis_id: str
    filename: str
    status: str
    total_events: int
    total_processes: int
    flagged_processes: int
    high_risk_count: int
    medium_risk_count: int
    low_risk_count: int
    analysis_duration_seconds: float


class HealthResponse(BaseModel):
    status: str
    version: str
    ai_enabled: bool


# Routes
@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    return HealthResponse(
        status="healthy",
        version="1.0.0",
        ai_enabled=bool(settings.openai_api_key)
    )


@router.get("/supported-formats")
async def get_supported_formats():
    """Get list of supported file formats."""
    return {
        "formats": ParserFactory.supported_extensions(),
        "max_file_size_mb": settings.max_file_size_mb
    }


@router.post("/analyze", response_model=AnalysisStartResponse)
async def analyze_file(
    file: UploadFile = File(...),
    background_tasks: BackgroundTasks = None
):
    """
    Upload and analyze a Process Monitor log file.
    Supports PML, CSV, and XML formats.
    """
    # Validate file format
    if not file.filename:
        raise HTTPException(status_code=400, detail="Filename is required")
    
    try:
        ParserFactory.get_parser(file.filename)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    # Check file size
    content = await file.read()
    file_size = len(content)
    
    if file_size > settings.max_file_size_bytes:
        raise HTTPException(
            status_code=413,
            detail=f"File too large. Maximum size is {settings.max_file_size_mb}MB"
        )
    
    # Generate analysis ID
    analysis_id = f"ANL-{uuid4().hex[:12].upper()}"
    
    # Initialize cache entry
    _analysis_cache[analysis_id] = {
        "status": "processing",
        "progress": 0,
        "filename": file.filename,
        "result": None,
        "error": None
    }
    
    # Run analysis
    try:
        logger.info(f"Starting analysis {analysis_id} for {file.filename}")
        
        analyzer = Analyzer(use_ai=True)
        file_stream = io.BytesIO(content)
        result = analyzer.analyze_stream(file_stream, file.filename)
        
        # Override the analysis_id to match our cache key
        result.analysis_id = analysis_id
        
        # Store result
        _analysis_cache[analysis_id]["status"] = "completed"
        _analysis_cache[analysis_id]["progress"] = 100
        _analysis_cache[analysis_id]["result"] = result
        
        logger.info(f"Analysis {analysis_id} completed successfully")
        
    except Exception as e:
        logger.error(f"Analysis {analysis_id} failed: {e}")
        _analysis_cache[analysis_id]["status"] = "failed"
        _analysis_cache[analysis_id]["error"] = str(e)
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")
    
    return AnalysisStartResponse(
        analysis_id=analysis_id,
        status="completed",
        message="Analysis completed successfully"
    )


@router.get("/analysis/{analysis_id}")
async def get_analysis(analysis_id: str):
    """Get the full analysis result."""
    if analysis_id not in _analysis_cache:
        raise HTTPException(status_code=404, detail="Analysis not found")
    
    cache = _analysis_cache[analysis_id]
    
    if cache["status"] == "failed":
        raise HTTPException(status_code=500, detail=cache["error"])
    
    if cache["status"] == "processing":
        return {"status": "processing", "progress": cache["progress"]}
    
    result = cache["result"]
    
    return {
        "analysis_id": result.analysis_id,
        "filename": result.filename,
        "status": result.status,
        "total_events": result.total_events,
        "total_processes": result.total_processes,
        "flagged_processes": result.flagged_processes,
        "high_risk_count": result.high_risk_count,
        "medium_risk_count": result.medium_risk_count,
        "low_risk_count": result.low_risk_count,
        "analysis_duration_seconds": result.analysis_duration_seconds,
        "top_threats": [
            {
                "pid": p.pid,
                "process_name": p.process_name,
                "image_path": p.image_path,
                "risk_score": p.risk_score,
                "legitimacy": p.legitimacy.value,
                "behavior_tags": p.behavior_tags,
                "ai_reasoning": p.ai_reasoning,
                "matched_rules": p.matched_rules,
            }
            for p in result.top_threats
        ]
    }


@router.get("/analysis/{analysis_id}/processes")
async def get_processes(analysis_id: str, flagged_only: bool = False):
    """Get list of processes from an analysis."""
    if analysis_id not in _analysis_cache:
        raise HTTPException(status_code=404, detail="Analysis not found")
    
    cache = _analysis_cache[analysis_id]
    
    if cache["status"] != "completed":
        raise HTTPException(status_code=400, detail="Analysis not completed")
    
    result = cache["result"]
    all_processes = result.processes
    
    if flagged_only:
        processes = [p for p in all_processes if p.is_flagged]
    else:
        processes = all_processes
    
    flagged_count = sum(1 for p in all_processes if p.is_flagged)
    
    return {
        "total": len(processes),
        "flagged": flagged_count,
        "processes": [
            {
                "pid": p.pid,
                "process_name": p.process_name,
                "image_path": p.image_path,
                "command_line": p.command_line,
                "parent_pid": p.parent_pid,
                "parent_name": p.parent_name,
                "risk_score": p.risk_score,
                "legitimacy": p.legitimacy.value,
                "behavior_tags": p.behavior_tags,
                "is_flagged": p.is_flagged,
                "matched_rules": p.matched_rules,
                "ai_reasoning": p.ai_reasoning,
                "event_count": p.event_count,
                "file_operations": p.file_operations,
                "registry_operations": p.registry_operations,
                "network_operations": p.network_operations,
            }
            for p in processes
        ]
    }


@router.get("/analysis/{analysis_id}/tree")
async def get_process_tree(analysis_id: str):
    """Get process tree from an analysis."""
    if analysis_id not in _analysis_cache:
        raise HTTPException(status_code=404, detail="Analysis not found")
    
    cache = _analysis_cache[analysis_id]
    
    if cache["status"] != "completed":
        raise HTTPException(status_code=400, detail="Analysis not completed")
    
    result = cache["result"]
    
    return {
        "tree": tree_to_dict(result.process_tree)
    }


@router.get("/analysis/{analysis_id}/timeline")
async def get_timeline(analysis_id: str, anomalies_only: bool = True, limit: int = 200):
    """Get timeline of events from an analysis."""
    if analysis_id not in _analysis_cache:
        raise HTTPException(status_code=404, detail="Analysis not found")
    
    cache = _analysis_cache[analysis_id]
    
    if cache["status"] != "completed":
        raise HTTPException(status_code=400, detail="Analysis not completed")
    
    # We need to regenerate timeline from cached events
    # In production, this would be stored or computed differently
    # For now, return a simplified timeline based on processes
    
    result = cache["result"]
    
    # Create simplified timeline from top threats
    timeline = []
    for proc in result.top_threats[:limit]:
        timeline.append({
            "timestamp": None,  # Would need event data
            "process_name": proc.process_name,
            "pid": proc.pid,
            "risk_score": proc.risk_score,
            "is_anomaly": proc.is_flagged,
            "description": proc.ai_reasoning or f"Process: {proc.process_name}",
        })
    
    return {
        "total": len(timeline),
        "timeline": timeline
    }


@router.delete("/analysis/{analysis_id}")
async def delete_analysis(analysis_id: str):
    """Delete an analysis result."""
    if analysis_id not in _analysis_cache:
        raise HTTPException(status_code=404, detail="Analysis not found")
    
    del _analysis_cache[analysis_id]
    
    return {"status": "deleted", "analysis_id": analysis_id}


@router.get("/analysis/{analysis_id}/report")
async def get_pdf_report(analysis_id: str):
    """Generate and download PDF report for an analysis."""
    if analysis_id not in _analysis_cache:
        raise HTTPException(status_code=404, detail="Analysis not found")
    
    cache = _analysis_cache[analysis_id]
    
    if cache["status"] != "completed":
        raise HTTPException(status_code=400, detail="Analysis not completed")
    
    result = cache["result"]
    
    # Build analysis summary for PDF
    analysis_summary = {
        "analysis_id": analysis_id,
        "filename": cache.get("filename", "Unknown"),
        "status": "completed",
        "total_events": result.total_events,
        "total_processes": result.total_processes,
        "flagged_processes": result.flagged_processes,
        "high_risk_count": result.high_risk_count,
        "medium_risk_count": result.medium_risk_count,
        "low_risk_count": result.low_risk_count,
        "analysis_duration_seconds": result.analysis_duration_seconds,
        "top_threats": [
            {
                "pid": p.pid,
                "process_name": p.process_name,
                "image_path": p.image_path,
                "risk_score": p.risk_score,
                "legitimacy": p.legitimacy,
                "behavior_tags": list(p.behavior_tags),
                "matched_rules": list(p.matched_rules),
                "ai_reasoning": p.ai_reasoning,
            }
            for p in result.top_threats
        ],
    }
    
    # Generate PDF
    generator = PDFGenerator()
    pdf_bytes = generator.generate(analysis_summary)
    
    # Return PDF response
    filename = f"procbench_report_{analysis_id}.pdf"
    
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f"attachment; filename={filename}"
        }
    )
