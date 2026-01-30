"""
Parent-child process relationship anomaly detection.
"""


# Expected parent-child relationships for Windows processes
# Format: {child_process: [expected_parents]}
EXPECTED_PARENTS = {
    # System processes
    "smss.exe": ["system"],
    "csrss.exe": ["smss.exe"],
    "wininit.exe": ["smss.exe"],
    "winlogon.exe": ["smss.exe"],
    "services.exe": ["wininit.exe"],
    "lsass.exe": ["wininit.exe"],
    "svchost.exe": ["services.exe"],
    
    # User shell
    "explorer.exe": ["userinit.exe", "winlogon.exe"],
    "userinit.exe": ["winlogon.exe"],
    
    # Security Center
    "securityhealthservice.exe": ["services.exe"],
    "msmpeng.exe": ["services.exe"],
    
    # Task manager
    "taskmgr.exe": ["explorer.exe"],
}

# Suspicious parent-child combinations
# Format: (parent, child, risk_increase, description)
SUSPICIOUS_COMBINATIONS = [
    # Office apps spawning interpreters
    ("winword.exe", "cmd.exe", 35, "Word spawning command prompt"),
    ("winword.exe", "powershell.exe", 40, "Word spawning PowerShell"),
    ("winword.exe", "wscript.exe", 40, "Word spawning Windows Script Host"),
    ("winword.exe", "cscript.exe", 40, "Word spawning Console Script Host"),
    ("winword.exe", "mshta.exe", 45, "Word spawning MSHTA"),
    
    ("excel.exe", "cmd.exe", 35, "Excel spawning command prompt"),
    ("excel.exe", "powershell.exe", 40, "Excel spawning PowerShell"),
    ("excel.exe", "wscript.exe", 40, "Excel spawning Windows Script Host"),
    ("excel.exe", "cscript.exe", 40, "Excel spawning Console Script Host"),
    ("excel.exe", "mshta.exe", 45, "Excel spawning MSHTA"),
    
    ("powerpnt.exe", "cmd.exe", 35, "PowerPoint spawning command prompt"),
    ("powerpnt.exe", "powershell.exe", 40, "PowerPoint spawning PowerShell"),
    
    ("outlook.exe", "cmd.exe", 35, "Outlook spawning command prompt"),
    ("outlook.exe", "powershell.exe", 40, "Outlook spawning PowerShell"),
    ("outlook.exe", "wscript.exe", 40, "Outlook spawning Windows Script Host"),
    
    # Browsers spawning interpreters
    ("iexplore.exe", "cmd.exe", 30, "IE spawning command prompt"),
    ("iexplore.exe", "powershell.exe", 35, "IE spawning PowerShell"),
    ("chrome.exe", "cmd.exe", 25, "Chrome spawning command prompt"),
    ("chrome.exe", "powershell.exe", 30, "Chrome spawning PowerShell"),
    ("firefox.exe", "cmd.exe", 25, "Firefox spawning command prompt"),
    ("firefox.exe", "powershell.exe", 30, "Firefox spawning PowerShell"),
    ("msedge.exe", "cmd.exe", 25, "Edge spawning command prompt"),
    ("msedge.exe", "powershell.exe", 30, "Edge spawning PowerShell"),
    
    # Script hosts spawning other interpreters
    ("wscript.exe", "powershell.exe", 35, "WScript spawning PowerShell"),
    ("cscript.exe", "powershell.exe", 35, "CScript spawning PowerShell"),
    ("mshta.exe", "powershell.exe", 40, "MSHTA spawning PowerShell"),
    ("mshta.exe", "cmd.exe", 35, "MSHTA spawning command prompt"),
    
    # PDF readers spawning interpreters
    ("acrord32.exe", "cmd.exe", 35, "Acrobat Reader spawning command prompt"),
    ("acrord32.exe", "powershell.exe", 40, "Acrobat Reader spawning PowerShell"),
    ("foxitreader.exe", "cmd.exe", 35, "Foxit Reader spawning command prompt"),
    ("foxitreader.exe", "powershell.exe", 40, "Foxit Reader spawning PowerShell"),
    
    # Services spawning user shells
    ("services.exe", "cmd.exe", 30, "Services spawning command prompt"),
    ("services.exe", "powershell.exe", 35, "Services spawning PowerShell"),
    
    # Suspicious svchost children
    ("svchost.exe", "cmd.exe", 20, "Svchost spawning command prompt"),
    ("svchost.exe", "powershell.exe", 25, "Svchost spawning PowerShell"),
    
    # WMI spawning interpreters
    ("wmiprvse.exe", "cmd.exe", 25, "WMI spawning command prompt"),
    ("wmiprvse.exe", "powershell.exe", 30, "WMI spawning PowerShell"),
    
    # Scheduled tasks
    ("taskeng.exe", "cmd.exe", 15, "Task Engine spawning command prompt"),
    ("taskeng.exe", "powershell.exe", 20, "Task Engine spawning PowerShell"),
    
    # Spoolsv exploitation
    ("spoolsv.exe", "cmd.exe", 35, "Print Spooler spawning command prompt"),
    ("spoolsv.exe", "powershell.exe", 40, "Print Spooler spawning PowerShell"),
    
    # Suspicious rundll32 children
    ("rundll32.exe", "cmd.exe", 30, "Rundll32 spawning command prompt"),
    ("rundll32.exe", "powershell.exe", 35, "Rundll32 spawning PowerShell"),
    
    # Notepad exploitation
    ("notepad.exe", "cmd.exe", 30, "Notepad spawning command prompt"),
    ("notepad.exe", "powershell.exe", 35, "Notepad spawning PowerShell"),
    
    # Calculator exploitation
    ("calc.exe", "cmd.exe", 40, "Calculator spawning command prompt"),
    ("calc.exe", "powershell.exe", 45, "Calculator spawning PowerShell"),
]


def check_parent_child(parent_name: str | None, child_name: str) -> tuple[int, str | None]:
    """
    Check if a parent-child relationship is suspicious.
    
    Returns: (risk_increase, description)
    """
    if not parent_name:
        return 0, None
    
    parent_lower = parent_name.lower()
    child_lower = child_name.lower()
    
    for parent, child, risk, description in SUSPICIOUS_COMBINATIONS:
        if parent_lower == parent.lower() and child_lower == child.lower():
            return risk, description
    
    return 0, None


def check_unexpected_parent(child_name: str, parent_name: str | None) -> tuple[int, str | None]:
    """
    Check if a process has an unexpected parent.
    
    Returns: (risk_increase, description)
    """
    if not parent_name:
        return 0, None
    
    child_lower = child_name.lower()
    parent_lower = parent_name.lower()
    
    if child_lower in EXPECTED_PARENTS:
        expected = [p.lower() for p in EXPECTED_PARENTS[child_lower]]
        if parent_lower not in expected:
            return 25, f"{child_name} has unexpected parent {parent_name} (expected: {', '.join(EXPECTED_PARENTS[child_lower])})"
    
    return 0, None


def analyze_parent_child(parent_name: str | None, child_name: str) -> tuple[int, list[str]]:
    """
    Analyze a parent-child relationship for anomalies.
    
    Returns: (risk_score, reasons)
    """
    risk_score = 0
    reasons = []
    
    # Check suspicious combinations
    risk, reason = check_parent_child(parent_name, child_name)
    if risk > 0:
        risk_score += risk
        reasons.append(reason)
    
    # Check unexpected parents
    risk, reason = check_unexpected_parent(child_name, parent_name)
    if risk > 0:
        risk_score += risk
        reasons.append(reason)
    
    return risk_score, reasons
