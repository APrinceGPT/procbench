"""
Detection package - rule-based detection for malware patterns.
"""

from app.detection.engine import DetectionEngine
from app.detection.lolbas import is_lolbas, get_lolbas_info, get_lolbas_risk, LOLBAS_BINARIES
from app.detection.suspicious import analyze_path, analyze_file_access, is_suspicious_path
from app.detection.parent_child import analyze_parent_child, check_parent_child

__all__ = [
    "DetectionEngine",
    "is_lolbas",
    "get_lolbas_info",
    "get_lolbas_risk",
    "LOLBAS_BINARIES",
    "analyze_path",
    "analyze_file_access",
    "is_suspicious_path",
    "analyze_parent_child",
    "check_parent_child",
]
