"""
Main analyzer - orchestrates parsing, detection, and AI analysis.
"""

import logging
import os
import time
from collections import defaultdict
from pathlib import Path
from typing import BinaryIO
from uuid import uuid4

from app.config import settings
from app.models import (
    ParsedLogFile,
    ProcessEvent,
    ProcessInfo,
    ProcessTreeNode,
    PathHeatmapEntry,
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
    
    def _aggregate_path_heatmap(
        self, 
        events: list[ProcessEvent], 
        top_n: int = 50
    ) -> list[PathHeatmapEntry]:
        """
        Aggregate path access data from events for heatmap visualization.
        
        Args:
            events: List of process events
            top_n: Number of top paths to return
            
        Returns:
            List of PathHeatmapEntry sorted by access count
        """
        # Track access data per normalized path (directory level)
        path_data: dict[str, dict] = defaultdict(lambda: {
            "access_count": 0,
            "operation_types": defaultdict(int),
            "processes": set()
        })
        
        for event in events:
            if not event.path:
                continue
                
            # Normalize path to directory level for better aggregation
            # For files, get the parent directory; for directories, use as-is
            try:
                path = event.path.strip()
                if not path:
                    continue
                    
                # Handle registry paths
                if path.startswith("HK") or path.startswith("\\REGISTRY"):
                    # For registry, use the key path (up to 3 levels deep for grouping)
                    parts = path.replace("\\", "/").split("/")
                    normalized = "/".join(parts[:min(4, len(parts))])
                else:
                    # For file paths, use parent directory
                    normalized = os.path.dirname(path) or path
                    
                if not normalized:
                    continue
                    
                path_data[normalized]["access_count"] += 1
                path_data[normalized]["operation_types"][event.operation.value] += 1
                if event.process_name:
                    path_data[normalized]["processes"].add(event.process_name)
                    
            except Exception:
                # Skip malformed paths
                continue
        
        # Convert to PathHeatmapEntry objects
        entries = []
        for path, data in path_data.items():
            entries.append(PathHeatmapEntry(
                path=path,
                access_count=data["access_count"],
                operation_types=dict(data["operation_types"]),
                processes=list(data["processes"])[:10]  # Limit process list
            ))
        
        # Sort by access count and return top N
        entries.sort(key=lambda x: x.access_count, reverse=True)
        return entries[:top_n]
    
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
        
        # Step 4: Aggregate path heatmap data
        logger.info("Aggregating path access data...")
        path_heatmap = self._aggregate_path_heatmap(parsed.events)
        logger.info(f"Aggregated {len(path_heatmap)} path entries for heatmap")
        
        # Step 5: Calculate summary statistics
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
            path_heatmap=path_heatmap,
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
