"""
Main analyzer - orchestrates parsing, detection, and AI analysis.
"""

import logging
import time
from pathlib import Path
from typing import BinaryIO
from uuid import uuid4

from app.config import settings
from app.models import (
    ParsedLogFile,
    ProcessInfo,
    ProcessTreeNode,
    AnalysisResult,
    FindingSummary,
)
from app.parsers import parse_log_file, parse_log_stream
from app.detection import DetectionEngine
from app.ai import AIClient
from app.analysis.process_tree import build_process_tree
from app.analysis.timeline import generate_timeline


logger = logging.getLogger(__name__)


class Analyzer:
    """
    Main analysis orchestrator.
    Coordinates parsing, detection, AI analysis, and result generation.
    """
    
    def __init__(self, use_ai: bool = True):
        """
        Initialize the analyzer.
        
        Args:
            use_ai: Whether to use AI for process analysis
        """
        self.use_ai = use_ai and bool(settings.openai_api_key)
        self.detection_engine = DetectionEngine()
        self.ai_client = AIClient() if self.use_ai else None
    
    def analyze_file(self, file_path: Path) -> AnalysisResult:
        """
        Analyze a log file from disk.
        
        Args:
            file_path: Path to the PML/CSV/XML file
            
        Returns:
            Complete analysis result
        """
        start_time = time.time()
        analysis_id = f"ANL-{uuid4().hex[:12].upper()}"
        
        logger.info(f"Starting analysis {analysis_id} for {file_path.name}")
        
        # Parse the file
        logger.info("Parsing log file...")
        parsed = parse_log_file(file_path)
        logger.info(f"Parsed {parsed.event_count:,} events from {parsed.process_count} processes")
        
        # Run analysis pipeline
        result = self._run_analysis(analysis_id, parsed, file_path.name, start_time)
        
        return result
    
    def analyze_stream(self, file_stream: BinaryIO, filename: str) -> AnalysisResult:
        """
        Analyze a log file from a stream.
        
        Args:
            file_stream: Binary file stream
            filename: Original filename
            
        Returns:
            Complete analysis result
        """
        start_time = time.time()
        analysis_id = f"ANL-{uuid4().hex[:12].upper()}"
        
        logger.info(f"Starting analysis {analysis_id} for {filename}")
        
        # Parse the stream
        logger.info("Parsing log stream...")
        parsed = parse_log_stream(file_stream, filename)
        logger.info(f"Parsed {parsed.event_count:,} events from {parsed.process_count} processes")
        
        # Run analysis pipeline
        result = self._run_analysis(analysis_id, parsed, filename, start_time)
        
        return result
    
    def _run_analysis(
        self,
        analysis_id: str,
        parsed: ParsedLogFile,
        filename: str,
        start_time: float
    ) -> AnalysisResult:
        """Run the full analysis pipeline."""
        
        # Step 1: Detection engine
        logger.info("Running detection engine...")
        processes, findings = self.detection_engine.analyze_events(parsed.events)
        logger.info(f"Detection complete: {len(processes)} processes, {findings.total_findings} findings")
        
        flagged_count = sum(1 for p in processes if p.is_flagged)
        logger.info(f"Flagged {flagged_count} processes for further analysis")
        
        # Step 2: AI analysis (if enabled)
        if self.use_ai and flagged_count > 0:
            logger.info("Running AI analysis on flagged processes...")
            try:
                processes = self.ai_client.analyze_processes(processes, only_flagged=True)
                stats = self.ai_client.get_stats()
                logger.info(f"AI analysis complete: {stats['total_requests']} requests, {stats['total_tokens']} tokens")
            except Exception as e:
                logger.error(f"AI analysis failed: {e}")
        
        # Step 3: Build process tree
        logger.info("Building process tree...")
        process_tree = build_process_tree(processes)
        
        # Step 4: Calculate summary statistics
        high_risk = sum(1 for p in processes if p.risk_score >= 70)
        medium_risk = sum(1 for p in processes if 30 <= p.risk_score < 70)
        low_risk = sum(1 for p in processes if p.risk_score < 30)
        
        # Get top threats
        top_threats = sorted(
            [p for p in processes if p.risk_score > 0],
            key=lambda p: p.risk_score,
            reverse=True
        )[:10]
        
        # Calculate duration
        duration = time.time() - start_time
        
        logger.info(f"Analysis {analysis_id} complete in {duration:.2f}s")
        
        return AnalysisResult(
            analysis_id=analysis_id,
            filename=filename,
            status="completed",
            total_events=parsed.event_count,
            total_processes=len(processes),
            flagged_processes=flagged_count,
            analysis_duration_seconds=duration,
            processes=processes,
            process_tree=process_tree,
            high_risk_count=high_risk,
            medium_risk_count=medium_risk,
            low_risk_count=low_risk,
            top_threats=top_threats,
        )


def analyze_file(file_path: Path, use_ai: bool = True) -> AnalysisResult:
    """Convenience function to analyze a file."""
    analyzer = Analyzer(use_ai=use_ai)
    return analyzer.analyze_file(file_path)


def analyze_stream(file_stream: BinaryIO, filename: str, use_ai: bool = True) -> AnalysisResult:
    """Convenience function to analyze a stream."""
    analyzer = Analyzer(use_ai=use_ai)
    return analyzer.analyze_stream(file_stream, filename)
