"""
Pydantic models for process analysis.
"""

from enum import Enum
from pydantic import BaseModel, Field


class LegitimacyStatus(str, Enum):
    """Legitimacy assessment of a process."""
    LEGITIMATE = "legitimate"
    SUSPICIOUS = "suspicious"
    MALICIOUS = "malicious"
    UNKNOWN = "unknown"


class BehaviorTag(str, Enum):
    """Common malware behavior tags."""
    PERSISTENCE = "persistence"
    CREDENTIAL_ACCESS = "credential_access"
    DEFENSE_EVASION = "defense_evasion"
    DISCOVERY = "discovery"
    LATERAL_MOVEMENT = "lateral_movement"
    COLLECTION = "collection"
    EXFILTRATION = "exfiltration"
    COMMAND_CONTROL = "command_control"
    EXECUTION = "execution"
    PRIVILEGE_ESCALATION = "privilege_escalation"
    INITIAL_ACCESS = "initial_access"
    IMPACT = "impact"


class ProcessInfo(BaseModel):
    """Aggregated information about a unique process."""
    
    # Identity
    pid: int = Field(description="Process ID")
    process_name: str = Field(description="Process name")
    image_path: str | None = Field(default=None, description="Full executable path")
    command_line: str | None = Field(default=None, description="Command line arguments")
    
    # Lineage
    parent_pid: int | None = Field(default=None, description="Parent process ID")
    parent_name: str | None = Field(default=None, description="Parent process name")
    children_pids: list[int] = Field(default_factory=list, description="Child process IDs")
    
    # Metadata
    user: str | None = Field(default=None, description="User account")
    integrity: str | None = Field(default=None, description="Integrity level")
    company: str | None = Field(default=None, description="Company from version info")
    description: str | None = Field(default=None, description="File description")
    
    # Activity summary
    event_count: int = Field(default=0, description="Total events from this process")
    file_operations: int = Field(default=0, description="File operation count")
    registry_operations: int = Field(default=0, description="Registry operation count")
    network_operations: int = Field(default=0, description="Network operation count")
    process_operations: int = Field(default=0, description="Process/thread operation count")
    
    # Accessed paths (summarized)
    accessed_files: list[str] = Field(default_factory=list, description="Key files accessed")
    accessed_registry: list[str] = Field(default_factory=list, description="Key registry paths")
    network_connections: list[str] = Field(default_factory=list, description="Network destinations")
    
    # Analysis results
    risk_score: int = Field(default=0, ge=0, le=100, description="Risk score 0-100")
    legitimacy: LegitimacyStatus = Field(
        default=LegitimacyStatus.UNKNOWN,
        description="Legitimacy assessment"
    )
    behavior_tags: list[str] = Field(default_factory=list, description="Behavior tags")
    ai_reasoning: str | None = Field(default=None, description="AI explanation")
    mitre_techniques: list[str] = Field(default_factory=list, description="MITRE ATT&CK IDs")
    
    # Detection flags
    is_flagged: bool = Field(default=False, description="Flagged by rule-based detection")
    matched_rules: list[str] = Field(default_factory=list, description="Rule IDs that matched")


class ProcessTreeNode(BaseModel):
    """Node in the process tree structure."""
    
    process: ProcessInfo = Field(description="Process information")
    children: list["ProcessTreeNode"] = Field(default_factory=list, description="Child processes")
    depth: int = Field(default=0, description="Depth in tree")


class PathHeatmapEntry(BaseModel):
    """Entry in the path heatmap showing access frequency."""
    
    path: str = Field(description="Directory or file path")
    access_count: int = Field(description="Number of accesses to this path")
    operation_types: dict[str, int] = Field(
        default_factory=dict, 
        description="Breakdown by operation type (e.g., CREATE_FILE: 5, READ_FILE: 3)"
    )
    processes: list[str] = Field(
        default_factory=list, 
        description="List of process names that accessed this path"
    )


class AnalysisResult(BaseModel):
    """Complete analysis result for a log file."""
    
    # Metadata
    analysis_id: str = Field(description="Unique analysis identifier")
    filename: str = Field(description="Original filename")
    status: str = Field(default="completed", description="Analysis status")
    
    # Statistics
    total_events: int = Field(description="Total events analyzed")
    total_processes: int = Field(description="Total unique processes")
    flagged_processes: int = Field(default=0, description="Processes flagged as suspicious/malicious")
    analysis_duration_seconds: float = Field(default=0, description="Time taken for analysis")
    
    # Results
    processes: list[ProcessInfo] = Field(default_factory=list, description="All process info")
    process_tree: list[ProcessTreeNode] = Field(default_factory=list, description="Process tree roots")
    
    # Summary
    high_risk_count: int = Field(default=0, description="Processes with risk > 70")
    medium_risk_count: int = Field(default=0, description="Processes with risk 30-70")
    low_risk_count: int = Field(default=0, description="Processes with risk < 30")
    
    # Path heatmap data
    path_heatmap: list[PathHeatmapEntry] = Field(
        default_factory=list, 
        description="Top accessed paths with frequency data"
    )
    
    # Top findings
    top_threats: list[ProcessInfo] = Field(default_factory=list, description="Top 10 risky processes")
