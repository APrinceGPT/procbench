"""
Pydantic models for detection rules.
"""

from enum import Enum
from pydantic import BaseModel, Field


class RuleConditionType(str, Enum):
    """Types of rule conditions."""
    PROCESS_NAME = "process_name"
    PROCESS_PATH = "process_path"
    COMMAND_LINE = "command_line"
    PARENT_PROCESS = "parent_process"
    REGISTRY_PATH = "registry_path"
    FILE_PATH = "file_path"
    NETWORK_DESTINATION = "network_destination"


class RuleCondition(BaseModel):
    """A single condition within a rule."""
    
    field: RuleConditionType = Field(description="Field to match against")
    operator: str = Field(default="contains", description="Match operator: equals, contains, regex, startswith, endswith")
    value: str = Field(description="Value to match")
    case_sensitive: bool = Field(default=False, description="Case sensitive matching")


class DetectionRule(BaseModel):
    """A detection rule definition."""
    
    # Identity
    id: str = Field(description="Unique rule ID")
    name: str = Field(description="Human-readable name")
    description: str = Field(description="What this rule detects")
    
    # Classification
    severity: str = Field(default="medium", description="Rule severity")
    category: str = Field(description="Rule category: lolbas, suspicious_path, etc.")
    enabled: bool = Field(default=True, description="Whether rule is active")
    
    # Conditions
    conditions: list[RuleCondition] = Field(description="Conditions that must match")
    condition_logic: str = Field(default="and", description="How to combine conditions: and, or")
    
    # References
    mitre_technique: str | None = Field(default=None, description="MITRE ATT&CK technique")
    mitre_tactic: str | None = Field(default=None, description="MITRE ATT&CK tactic")
    references: list[str] = Field(default_factory=list, description="External references")
    
    # Response
    recommendation: str | None = Field(default=None, description="Recommended action")


class RuleSet(BaseModel):
    """Collection of detection rules."""
    
    name: str = Field(description="Rule set name")
    version: str = Field(default="1.0.0", description="Rule set version")
    description: str = Field(default="", description="Rule set description")
    rules: list[DetectionRule] = Field(default_factory=list, description="All rules")
    
    @property
    def enabled_rules(self) -> list[DetectionRule]:
        """Get only enabled rules."""
        return [r for r in self.rules if r.enabled]
