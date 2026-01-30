"""
Test script for verifying detection engine functionality.
"""

import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent))

from app.parsers import parse_log_file
from app.detection import DetectionEngine


def test_detection():
    """Test detection engine with real log file."""
    base_path = Path(__file__).parent.parent
    pml_path = base_path / "Logfile.PML"
    
    print("=" * 60)
    print("ProcBench Detection Engine Test")
    print("=" * 60)
    
    if not pml_path.exists():
        print(f"❌ PML file not found: {pml_path}")
        return
    
    # Parse the log file
    print(f"\n[1/3] Parsing {pml_path.name}...")
    parsed = parse_log_file(pml_path)
    print(f"    ✅ Parsed {parsed.event_count:,} events from {parsed.process_count} processes")
    
    # Run detection engine
    print(f"\n[2/3] Running detection engine...")
    engine = DetectionEngine()
    processes, summary = engine.analyze_events(parsed.events)
    
    print(f"    ✅ Analyzed {len(processes)} processes")
    print(f"    ✅ Generated {summary.total_findings} findings")
    
    # Display findings summary
    print(f"\n[3/3] Findings Summary:")
    print(f"    {'─' * 50}")
    print(f"    🔴 Critical: {summary.critical_count}")
    print(f"    🟠 High:     {summary.high_count}")
    print(f"    🟡 Medium:   {summary.medium_count}")
    print(f"    🔵 Low:      {summary.low_count}")
    print(f"    ⚪ Info:     {summary.info_count}")
    
    print(f"\n    Findings by Type:")
    for ftype, count in sorted(summary.findings_by_type.items(), key=lambda x: -x[1]):
        print(f"    • {ftype}: {count}")
    
    # Show flagged processes
    flagged = [p for p in processes if p.is_flagged]
    print(f"\n    Flagged Processes: {len(flagged)}")
    
    # Show top 10 by risk
    print(f"\n📋 Top 10 Riskiest Processes:")
    print(f"    {'─' * 50}")
    sorted_procs = sorted(processes, key=lambda p: p.risk_score, reverse=True)[:10]
    
    for i, proc in enumerate(sorted_procs, 1):
        risk_icon = "🔴" if proc.risk_score >= 50 else "🟠" if proc.risk_score >= 25 else "🟡" if proc.risk_score >= 10 else "🟢"
        print(f"    {i:2}. {risk_icon} [{proc.risk_score:3}] {proc.process_name} (PID: {proc.pid})")
        if proc.matched_rules:
            print(f"        Rules: {', '.join(proc.matched_rules[:3])}")
        if proc.behavior_tags:
            print(f"        Tags: {', '.join(proc.behavior_tags)}")
    
    # Show sample findings
    print(f"\n📋 Sample Findings (first 5):")
    print(f"    {'─' * 50}")
    for i, finding in enumerate(summary.findings[:5], 1):
        sev_icon = {"critical": "🔴", "high": "🟠", "medium": "🟡", "low": "🔵", "info": "⚪"}.get(finding.severity.value, "❔")
        print(f"    {i}. {sev_icon} [{finding.severity.value.upper():8}] {finding.title}")
        print(f"       Process: {finding.process_name} (PID: {finding.pid})")
        print(f"       {finding.description[:80]}...")
    
    print(f"\n{'=' * 60}")
    print("Detection engine test complete!")
    print("=" * 60)


if __name__ == "__main__":
    test_detection()
