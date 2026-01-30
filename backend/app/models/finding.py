"""
Pydantic models for detection findings.
"""

from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field


class Severity(str, Enum):
    """Finding severity levels."""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"


class FindingType(str, Enum):
    """Types of detection findings."""
    LOLBAS = "lolbas"
    SUSPICIOUS_PATH = "suspicious_path"
    PARENT_CHILD_ANOMALY = "parent_child_anomaly"
    PERSISTENCE = "persistence"
    CREDENTIAL_ACCESS = "credential_access"
    DEFENSE_EVASION = "defense_evasion"
    CUSTOM_RULE = "custom_rule"
    AI_DETECTION = "ai_detection"


class Finding(BaseModel):
    """A single detection finding."""
    
    # Identity
    id: str = Field(description="Unique finding ID")
    type: FindingType = Field(description="Finding type")
    severity: Severity = Field(description="Severity level")
    
    # Context
    process_name: str = Field(description="Process that triggered finding")
    pid: int = Field(description="Process ID")
    timestamp: datetime | None = Field(default=None, description="When the suspicious activity occurred")
    
    # Details
    title: str = Field(description="Short description")
    description: str = Field(description="Detailed explanation")
    evidence: list[str] = Field(default_factory=list, description="Supporting evidence")
    
    # References
    matched_rule: str | None = Field(default=None, description="Rule ID that triggered this")
    mitre_technique: str | None = Field(default=None, description="MITRE ATT&CK technique ID")
    mitre_tactic: str | None = Field(default=None, description="MITRE ATT&CK tactic")
    
    # Recommendations
    recommendation: str | None = Field(default=None, description="Suggested action")


class FindingSummary(BaseModel):
    """Summary of all findings from an analysis."""
    
    total_findings: int = Field(default=0, description="Total findings count")
    critical_count: int = Field(default=0, description="Critical severity count")
    high_count: int = Field(default=0, description="High severity count")
    medium_count: int = Field(default=0, description="Medium severity count")
    low_count: int = Field(default=0, description="Low severity count")
    info_count: int = Field(default=0, description="Info severity count")
    
    findings: list[Finding] = Field(default_factory=list, description="All findings")
    
    # Breakdown by type
    findings_by_type: dict[str, int] = Field(
        default_factory=dict,
        description="Count of findings by type"
    )
