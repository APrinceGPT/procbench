"""
LOLBAS (Living Off The Land Binaries and Scripts) detection.
"""

# LOLBAS binaries that are commonly abused by attackers
LOLBAS_BINARIES = {
    # Command interpreters
    "cmd.exe": {
        "risk_increase": 10,
        "description": "Windows Command Processor",
        "suspicious_when": ["spawned by Office apps", "encoded commands", "from unusual paths"]
    },
    "powershell.exe": {
        "risk_increase": 20,
        "description": "PowerShell scripting engine",
        "suspicious_when": ["encoded commands", "download cradle", "bypass flags"]
    },
    "pwsh.exe": {
        "risk_increase": 20,
        "description": "PowerShell Core",
        "suspicious_when": ["encoded commands", "download cradle", "bypass flags"]
    },
    
    # Script hosts
    "wscript.exe": {
        "risk_increase": 25,
        "description": "Windows Script Host",
        "suspicious_when": ["running VBS/JS from temp", "spawned by browser"]
    },
    "cscript.exe": {
        "risk_increase": 25,
        "description": "Console Script Host",
        "suspicious_when": ["running VBS/JS from temp", "spawned by browser"]
    },
    "mshta.exe": {
        "risk_increase": 30,
        "description": "HTML Application Host",
        "suspicious_when": ["any execution", "especially with URLs"]
    },
    
    # Binary execution proxies
    "rundll32.exe": {
        "risk_increase": 20,
        "description": "DLL execution utility",
        "suspicious_when": ["javascript protocol", "unusual DLL paths"]
    },
    "regsvr32.exe": {
        "risk_increase": 25,
        "description": "Register/unregister DLLs",
        "suspicious_when": ["remote script execution", "/s /n /u /i flags"]
    },
    "msiexec.exe": {
        "risk_increase": 15,
        "description": "Windows Installer",
        "suspicious_when": ["remote MSI", "quiet installation"]
    },
    
    # Development tools
    "msbuild.exe": {
        "risk_increase": 20,
        "description": "Microsoft Build Engine",
        "suspicious_when": ["any non-dev environment", "inline tasks"]
    },
    "installutil.exe": {
        "risk_increase": 25,
        "description": ".NET Installation Utility",
        "suspicious_when": ["any execution", "loading DLLs"]
    },
    "regasm.exe": {
        "risk_increase": 25,
        "description": "Assembly Registration Utility",
        "suspicious_when": ["any non-dev execution"]
    },
    "regsvcs.exe": {
        "risk_increase": 25,
        "description": ".NET Component Services",
        "suspicious_when": ["any non-dev execution"]
    },
    
    # System utilities
    "certutil.exe": {
        "risk_increase": 25,
        "description": "Certificate Utility",
        "suspicious_when": ["downloading files", "decoding base64"]
    },
    "bitsadmin.exe": {
        "risk_increase": 20,
        "description": "BITS Administration",
        "suspicious_when": ["downloading files", "persistence"]
    },
    "wmic.exe": {
        "risk_increase": 15,
        "description": "WMI Command-line",
        "suspicious_when": ["process creation", "remote execution"]
    },
    
    # Other LOLBins
    "cmstp.exe": {
        "risk_increase": 30,
        "description": "Connection Manager Profile Installer",
        "suspicious_when": ["any execution", "INF file execution"]
    },
    "forfiles.exe": {
        "risk_increase": 20,
        "description": "Batch file processor",
        "suspicious_when": ["executing commands"]
    },
    "pcalua.exe": {
        "risk_increase": 25,
        "description": "Program Compatibility Assistant",
        "suspicious_when": ["any execution"]
    },
    "schtasks.exe": {
        "risk_increase": 15,
        "description": "Task Scheduler",
        "suspicious_when": ["creating tasks", "persistence"]
    },
    "at.exe": {
        "risk_increase": 25,
        "description": "AT scheduler (deprecated)",
        "suspicious_when": ["any execution"]
    },
    "sc.exe": {
        "risk_increase": 15,
        "description": "Service Control Manager",
        "suspicious_when": ["creating services", "remote services"]
    },
    "reg.exe": {
        "risk_increase": 10,
        "description": "Registry Console Tool",
        "suspicious_when": ["modifying run keys", "security settings"]
    },
    "netsh.exe": {
        "risk_increase": 15,
        "description": "Network Shell",
        "suspicious_when": ["firewall changes", "port forwarding"]
    },
    "control.exe": {
        "risk_increase": 15,
        "description": "Control Panel",
        "suspicious_when": ["loading CPL from unusual locations"]
    },
    "explorer.exe": {
        "risk_increase": 5,
        "description": "Windows Explorer",
        "suspicious_when": ["spawning from unusual parents"]
    },
    "ieexec.exe": {
        "risk_increase": 30,
        "description": "IE Application Deployment",
        "suspicious_when": ["any execution"]
    },
    "dnscmd.exe": {
        "risk_increase": 25,
        "description": "DNS Server Manager",
        "suspicious_when": ["any execution on workstation"]
    },
    "ftp.exe": {
        "risk_increase": 20,
        "description": "FTP Client",
        "suspicious_when": ["any execution", "data exfiltration"]
    },
    "desktopimgdownldr.exe": {
        "risk_increase": 30,
        "description": "Desktop Image Downloader",
        "suspicious_when": ["any execution"]
    },
    "esentutl.exe": {
        "risk_increase": 25,
        "description": "Extensible Storage Engine Utility",
        "suspicious_when": ["copying files", "ntds.dit access"]
    },
    "expand.exe": {
        "risk_increase": 15,
        "description": "Cabinet File Expander",
        "suspicious_when": ["extracting to unusual locations"]
    },
    "extrac32.exe": {
        "risk_increase": 20,
        "description": "Cabinet File Extractor",
        "suspicious_when": ["any execution"]
    },
    "findstr.exe": {
        "risk_increase": 5,
        "description": "Find String Utility",
        "suspicious_when": ["searching for credentials"]
    },
    "gpscript.exe": {
        "risk_increase": 25,
        "description": "Group Policy Script",
        "suspicious_when": ["any non-GPO execution"]
    },
    "hh.exe": {
        "risk_increase": 25,
        "description": "HTML Help Executable",
        "suspicious_when": ["any execution"]
    },
    "infdefaultinstall.exe": {
        "risk_increase": 30,
        "description": "INF Default Installer",
        "suspicious_when": ["any execution"]
    },
    "makecab.exe": {
        "risk_increase": 15,
        "description": "Cabinet File Maker",
        "suspicious_when": ["creating archives for exfiltration"]
    },
    "mavinject.exe": {
        "risk_increase": 35,
        "description": "Application Verifier Injection",
        "suspicious_when": ["any execution"]
    },
    "microsoft.workflow.compiler.exe": {
        "risk_increase": 30,
        "description": "Workflow Compiler",
        "suspicious_when": ["any execution"]
    },
    "mmc.exe": {
        "risk_increase": 10,
        "description": "Management Console",
        "suspicious_when": ["loading non-standard snap-ins"]
    },
    "msconfig.exe": {
        "risk_increase": 10,
        "description": "System Configuration",
        "suspicious_when": ["command-line execution"]
    },
    "msdeploy.exe": {
        "risk_increase": 25,
        "description": "Web Deploy",
        "suspicious_when": ["any execution"]
    },
    "msdt.exe": {
        "risk_increase": 30,
        "description": "Diagnostics Troubleshooter",
        "suspicious_when": ["any execution", "Follina vulnerability"]
    },
    "msiexec.exe": {
        "risk_increase": 15,
        "description": "Windows Installer",
        "suspicious_when": ["remote MSI", "quiet install"]
    },
    "odbcconf.exe": {
        "risk_increase": 25,
        "description": "ODBC Configuration",
        "suspicious_when": ["any execution"]
    },
    "pcwrun.exe": {
        "risk_increase": 25,
        "description": "Program Compatibility Wizard",
        "suspicious_when": ["any execution"]
    },
    "presentationhost.exe": {
        "risk_increase": 25,
        "description": "WPF Host",
        "suspicious_when": ["any execution"]
    },
    "print.exe": {
        "risk_increase": 10,
        "description": "Print Spooler",
        "suspicious_when": ["command execution"]
    },
    "psr.exe": {
        "risk_increase": 15,
        "description": "Problem Steps Recorder",
        "suspicious_when": ["any execution"]
    },
    "rasautou.exe": {
        "risk_increase": 25,
        "description": "RAS AutoDial",
        "suspicious_when": ["any execution"]
    },
    "rdrleakdiag.exe": {
        "risk_increase": 30,
        "description": "Redirector Leak Diagnostic",
        "suspicious_when": ["any execution"]
    },
    "replace.exe": {
        "risk_increase": 10,
        "description": "File Replacement",
        "suspicious_when": ["replacing system files"]
    },
    "rpcping.exe": {
        "risk_increase": 15,
        "description": "RPC Ping",
        "suspicious_when": ["remote connections"]
    },
    "runscripthelper.exe": {
        "risk_increase": 30,
        "description": "Run Script Helper",
        "suspicious_when": ["any execution"]
    },
    "scriptrunner.exe": {
        "risk_increase": 30,
        "description": "Script Runner",
        "suspicious_when": ["any execution"]
    },
    "syncappvpublishingserver.exe": {
        "risk_increase": 30,
        "description": "App-V Publishing Server Sync",
        "suspicious_when": ["any execution"]
    },
    "te.exe": {
        "risk_increase": 25,
        "description": "Test Authoring Execution",
        "suspicious_when": ["any execution"]
    },
    "tracker.exe": {
        "risk_increase": 20,
        "description": "File Tracker",
        "suspicious_when": ["any execution"]
    },
    "tttracer.exe": {
        "risk_increase": 25,
        "description": "Time Travel Tracer",
        "suspicious_when": ["any execution"]
    },
    "verclsid.exe": {
        "risk_increase": 25,
        "description": "CLSID Verification",
        "suspicious_when": ["any execution"]
    },
    "wab.exe": {
        "risk_increase": 25,
        "description": "Windows Address Book",
        "suspicious_when": ["any execution"]
    },
    "winrm.cmd": {
        "risk_increase": 20,
        "description": "Windows Remote Management",
        "suspicious_when": ["remote connections"]
    },
    "winrm.exe": {
        "risk_increase": 20,
        "description": "Windows Remote Management",
        "suspicious_when": ["remote connections"]
    },
    "wlrmdr.exe": {
        "risk_increase": 25,
        "description": "WLR Reminder",
        "suspicious_when": ["any execution"]
    },
    "wmic.exe": {
        "risk_increase": 15,
        "description": "WMI Command-line",
        "suspicious_when": ["process creation", "remote execution"]
    },
    "workfolders.exe": {
        "risk_increase": 20,
        "description": "Work Folders",
        "suspicious_when": ["any execution"]
    },
    "wsl.exe": {
        "risk_increase": 15,
        "description": "Windows Subsystem for Linux",
        "suspicious_when": ["executing commands", "bypassing security"]
    },
    "wsreset.exe": {
        "risk_increase": 25,
        "description": "Windows Store Reset",
        "suspicious_when": ["any execution"]
    },
    "xwizard.exe": {
        "risk_increase": 30,
        "description": "Extensible Wizard Host",
        "suspicious_when": ["any execution"]
    },
}


def is_lolbas(process_name: str) -> bool:
    """Check if a process is a known LOLBAS binary."""
    return process_name.lower() in [k.lower() for k in LOLBAS_BINARIES.keys()]


def get_lolbas_info(process_name: str) -> dict | None:
    """Get LOLBAS information for a process."""
    name_lower = process_name.lower()
    for name, info in LOLBAS_BINARIES.items():
        if name.lower() == name_lower:
            return {**info, "name": name}
    return None


def get_lolbas_risk(process_name: str) -> int:
    """Get the risk increase for a LOLBAS binary."""
    info = get_lolbas_info(process_name)
    return info["risk_increase"] if info else 0
