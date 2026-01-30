"""
Suspicious path detection module.
"""

import re
from pathlib import PureWindowsPath


# Suspicious path patterns
SUSPICIOUS_PATHS = [
    # User temp directories
    (r"\\temp\\[^\\]+\.exe$", 30, "Executable in Temp folder"),
    (r"\\tmp\\[^\\]+\.exe$", 30, "Executable in Tmp folder"),
    (r"\\appdata\\local\\temp\\", 25, "Running from AppData/Local/Temp"),
    
    # User profile locations
    (r"\\appdata\\roaming\\[^\\]+\.exe$", 20, "Executable directly in AppData/Roaming"),
    (r"\\appdata\\local\\[^\\]+\.exe$", 20, "Executable directly in AppData/Local"),
    (r"\\downloads\\[^\\]+\.exe$", 15, "Executable in Downloads folder"),
    (r"\\desktop\\[^\\]+\.exe$", 10, "Executable on Desktop"),
    
    # Public directories
    (r"\\users\\public\\", 25, "Running from Public folder"),
    (r"c:\\public\\", 25, "Running from C:\\Public"),
    
    # ProgramData suspicious patterns
    (r"\\programdata\\[^\\]+\.exe$", 20, "Executable directly in ProgramData"),
    
    # Root of system drive
    (r"^c:\\[^\\]+\.exe$", 20, "Executable at root of C:"),
    
    # Recycle bin
    (r"\\\$recycle\.bin\\", 35, "Running from Recycle Bin"),
    (r"\\recycler\\", 35, "Running from Recycler"),
    
    # Hidden/system folders
    (r"\\system volume information\\", 35, "Running from System Volume Information"),
    (r"\\\$windows\.~bt\\", 20, "Running from Windows upgrade folder"),
    (r"\\\$windows\.~ws\\", 20, "Running from Windows upgrade folder"),
    
    # Common malware hiding spots
    (r"\\intel\\logs\\", 25, "Running from Intel folder (common malware location)"),
    (r"\\perflogs\\", 25, "Running from PerfLogs (rarely used legitimately)"),
    
    # Network paths
    (r"^\\\\[^\\]+\\", 15, "Running from network share"),
    
    # Unusual names
    (r"\\[a-f0-9]{32}\.exe$", 25, "Executable with hash-like name"),
    (r"\\[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}\.exe$", 25, "Executable with GUID name"),
    
    # Double extensions
    (r"\.[a-z]{3,4}\.exe$", 30, "Double extension (e.g., .pdf.exe)"),
    
    # Very long paths (potential evasion)
    (r"\\[^\\]{200,}\\", 15, "Very long path component"),
]

# File access patterns that are suspicious
SUSPICIOUS_FILE_ACCESS = [
    # Credential stores
    (r"\\windows\\system32\\config\\sam$", 40, "SAM database access", "credential_access"),
    (r"\\windows\\system32\\config\\system$", 35, "SYSTEM registry hive access", "credential_access"),
    (r"\\windows\\system32\\config\\security$", 35, "SECURITY registry hive access", "credential_access"),
    (r"\\windows\\ntds\\ntds\.dit$", 45, "NTDS.dit access (AD credentials)", "credential_access"),
    (r"\\users\\[^\\]+\\appdata\\local\\google\\chrome\\user data\\[^\\]+\\login data$", 35, "Chrome password access", "credential_access"),
    (r"\\users\\[^\\]+\\appdata\\roaming\\mozilla\\firefox\\profiles\\[^\\]+\\logins\.json$", 35, "Firefox password access", "credential_access"),
    
    # Security-related
    (r"\\windows\\system32\\drivers\\etc\\hosts$", 20, "Hosts file access", "defense_evasion"),
    (r"\\windows\\system32\\lsass\.exe$", 40, "LSASS access", "credential_access"),
    
    # Persistence locations
    (r"\\microsoft\\windows\\start menu\\programs\\startup\\", 25, "Startup folder access", "persistence"),
    (r"\\appdata\\roaming\\microsoft\\windows\\start menu\\programs\\startup\\", 25, "User startup folder", "persistence"),
    
    # Shadow copies
    (r"\\\\\\?\\globalroot\\device\\harddiskvolumeshadowcopy", 30, "Shadow copy access", "credential_access"),
]


def analyze_path(image_path: str | None) -> tuple[int, list[str], list[str]]:
    """
    Analyze an executable path for suspicious patterns.
    
    Returns: (risk_score, reasons, behavior_tags)
    """
    if not image_path:
        return 0, [], []
    
    risk_score = 0
    reasons = []
    behavior_tags = []
    
    path_lower = image_path.lower().replace("/", "\\")
    
    for pattern, score, description in SUSPICIOUS_PATHS:
        if re.search(pattern, path_lower, re.IGNORECASE):
            risk_score += score
            reasons.append(description)
    
    return risk_score, reasons, behavior_tags


def analyze_file_access(file_path: str) -> tuple[int, str | None, str | None]:
    """
    Analyze a file access for suspicious patterns.
    
    Returns: (risk_score, reason, behavior_tag)
    """
    if not file_path:
        return 0, None, None
    
    path_lower = file_path.lower().replace("/", "\\")
    
    for pattern, score, description, tag in SUSPICIOUS_FILE_ACCESS:
        if re.search(pattern, path_lower, re.IGNORECASE):
            return score, description, tag
    
    return 0, None, None


def is_suspicious_path(path: str) -> bool:
    """Check if a path is suspicious."""
    risk, _, _ = analyze_path(path)
    return risk > 0


def get_path_risk(path: str) -> int:
    """Get the risk score for a path."""
    risk, _, _ = analyze_path(path)
    return risk
