"""
Timeline generator - creates chronological event sequences.
"""

from datetime import datetime
from typing import NamedTuple

from app.models import ProcessEvent, ProcessInfo


class TimelineEntry(NamedTuple):
    """A single entry in the timeline."""
    timestamp: datetime
    process_name: str
    pid: int
    operation: str
    path: str
    risk_score: int
    is_anomaly: bool
    description: str


def generate_timeline(
    events: list[ProcessEvent],
    processes: list[ProcessInfo],
    anomalies_only: bool = True,
    max_entries: int = 500
) -> list[TimelineEntry]:
    """
    Generate a timeline of events.
    
    Args:
        events: All parsed events
        processes: Analyzed process info
        anomalies_only: If True, only include events from flagged processes
        max_entries: Maximum number of timeline entries
        
    Returns:
        List of timeline entries sorted by timestamp
    """
    # Create PID to process info lookup
    pid_to_info = {p.pid: p for p in processes}
    
    # Filter events
    if anomalies_only:
        flagged_pids = {p.pid for p in processes if p.is_flagged}
        events = [e for e in events if e.pid in flagged_pids]
    
    # Sort by timestamp
    events = sorted(events, key=lambda e: e.timestamp)
    
    # Generate entries
    entries: list[TimelineEntry] = []
    
    # Group consecutive similar events
    prev_key = None
    group_count = 0
    
    for event in events:
        process_info = pid_to_info.get(event.pid)
        risk = process_info.risk_score if process_info else 0
        is_flagged = process_info.is_flagged if process_info else False
        
        # Create grouping key to avoid duplicate entries
        key = (event.pid, event.operation, event.path[:100] if event.path else "")
        
        if key == prev_key:
            group_count += 1
            continue
        
        # Add previous group if it had multiple events
        if prev_key and group_count > 1 and entries:
            last = entries[-1]
            entries[-1] = TimelineEntry(
                timestamp=last.timestamp,
                process_name=last.process_name,
                pid=last.pid,
                operation=f"{last.operation} (x{group_count})",
                path=last.path,
                risk_score=last.risk_score,
                is_anomaly=last.is_anomaly,
                description=last.description
            )
        
        prev_key = key
        group_count = 1
        
        # Determine if this is an anomaly
        is_anomaly = risk >= 20 or _is_suspicious_operation(event)
        
        # Create description
        description = _create_description(event, process_info)
        
        entries.append(TimelineEntry(
            timestamp=event.timestamp,
            process_name=event.process_name,
            pid=event.pid,
            operation=event.operation,
            path=event.path[:200] if event.path else "",
            risk_score=risk,
            is_anomaly=is_anomaly,
            description=description
        ))
        
        if len(entries) >= max_entries:
            break
    
    return entries


def _is_suspicious_operation(event: ProcessEvent) -> bool:
    """Check if an operation is inherently suspicious."""
    op_lower = event.operation.lower() if event.operation else ""
    path_lower = event.path.lower() if event.path else ""
    
    # Process creation is always notable
    if "process create" in op_lower or "process start" in op_lower:
        return True
    
    # Sensitive file access
    sensitive_paths = ["\\sam", "\\ntds.dit", "\\lsass", "\\security", "\\system"]
    if any(sp in path_lower for sp in sensitive_paths):
        return True
    
    # Run key registry access
    if "reg" in op_lower and ("\\run" in path_lower or "\\runonce" in path_lower):
        return True
    
    return False


def _create_description(event: ProcessEvent, process_info: ProcessInfo | None) -> str:
    """Create a human-readable description for a timeline entry."""
    op = event.operation or "Unknown operation"
    name = event.process_name
    
    if "process create" in op.lower() or "process start" in op.lower():
        return f"{name} created a new process: {event.path.split(chr(92))[-1] if event.path else 'unknown'}"
    elif "reg" in op.lower() and event.path:
        key = event.path.split("\\")[-1] if event.path else "unknown key"
        return f"{name} accessed registry: {key}"
    elif "file" in op.lower() and event.path:
        file = event.path.split("\\")[-1] if event.path else "unknown file"
        return f"{name} {op}: {file}"
    elif "tcp" in op.lower() or "udp" in op.lower():
        return f"{name} network activity: {event.path or 'unknown destination'}"
    else:
        return f"{name}: {op}"


def timeline_to_dict(entries: list[TimelineEntry]) -> list[dict]:
    """Convert timeline entries to dictionary format."""
    return [
        {
            "timestamp": entry.timestamp.isoformat(),
            "process_name": entry.process_name,
            "pid": entry.pid,
            "operation": entry.operation,
            "path": entry.path,
            "risk_score": entry.risk_score,
            "is_anomaly": entry.is_anomaly,
            "description": entry.description
        }
        for entry in entries
    ]
