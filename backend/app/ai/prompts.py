"""
AI prompt templates for malware analysis.
"""

SYSTEM_PROMPT = """You are an expert malware analyst and digital forensics specialist examining Process Monitor data from a potentially compromised Windows system.

Your task is to assess each process for:
1. LEGITIMACY: Is this a legitimate Windows process or potentially malicious?
2. RISK LEVEL: How risky is this process behavior (0-100)?
3. REASONING: Explain your assessment in 1-2 sentences.
4. BEHAVIORS: Tag any concerning behaviors detected using MITRE ATT&CK categories.

Consider the following when assessing:
- Is the executable path appropriate for this process?
- Are the operations typical for this process type?
- Are there suspicious parent-child relationships?
- Is it accessing sensitive resources (credentials, security, etc.)?
- Does the command line contain encoded content or suspicious flags?
- Is it running from a temporary or user-writable location?

BEHAVIOR TAG OPTIONS:
- persistence: Registry run keys, scheduled tasks, services
- credential_access: LSASS, SAM, browser credentials
- defense_evasion: Process injection, hiding, masquerading
- discovery: System enumeration, network scanning
- lateral_movement: Remote services, pass-the-hash
- collection: Data staging, keylogging
- exfiltration: Data transfer, compression
- command_control: C2 communication patterns
- execution: Code execution, scripting
- privilege_escalation: Token manipulation, UAC bypass
- initial_access: Exploitation, phishing artifacts
- impact: Encryption, destruction

You must respond with valid JSON only. No explanations outside JSON."""


BATCH_ANALYSIS_PROMPT = """Analyze these {count} processes from a Windows system scan:

{process_data}

For EACH process, respond with this exact JSON structure:
{{
  "assessments": [
    {{
      "pid": <process_id>,
      "process_name": "<name>",
      "legitimacy": "legitimate" | "suspicious" | "malicious" | "unknown",
      "risk_score": <0-100>,
      "reasoning": "<1-2 sentence explanation>",
      "behavior_tags": ["<tag1>", "<tag2>"],
      "mitre_techniques": ["T1xxx.xxx"]
    }}
  ]
}}

Only return valid JSON, no markdown or explanations."""


def format_process_for_ai(process: dict) -> str:
    """Format a process for AI analysis."""
    lines = [
        f"Process: {process.get('process_name', 'Unknown')}",
        f"PID: {process.get('pid', 0)}",
        f"Path: {process.get('image_path', 'Unknown')}",
    ]
    
    if process.get('command_line'):
        lines.append(f"Command Line: {process['command_line'][:200]}")
    
    if process.get('parent_name'):
        lines.append(f"Parent: {process['parent_name']} (PID: {process.get('parent_pid', 'Unknown')})")
    
    if process.get('user'):
        lines.append(f"User: {process['user']}")
    
    if process.get('integrity'):
        lines.append(f"Integrity: {process['integrity']}")
    
    # Activity summary
    lines.append(f"Events: {process.get('event_count', 0)}")
    
    if process.get('file_operations'):
        lines.append(f"File Ops: {process['file_operations']}")
    
    if process.get('registry_operations'):
        lines.append(f"Registry Ops: {process['registry_operations']}")
    
    if process.get('network_operations'):
        lines.append(f"Network Ops: {process['network_operations']}")
    
    # Key accessed paths
    if process.get('accessed_files'):
        files = process['accessed_files'][:5]
        lines.append(f"Key Files: {', '.join(files[:3])[:150]}")
    
    if process.get('accessed_registry'):
        regs = process['accessed_registry'][:5]
        lines.append(f"Key Registry: {', '.join(regs[:3])[:150]}")
    
    # Prior detection results
    if process.get('matched_rules'):
        lines.append(f"Detection Rules Matched: {', '.join(process['matched_rules'])}")
    
    return "\n".join(lines)


def create_batch_prompt(processes: list[dict]) -> str:
    """Create a batch analysis prompt for multiple processes."""
    process_strs = []
    for i, proc in enumerate(processes, 1):
        process_strs.append(f"--- Process {i} ---")
        process_strs.append(format_process_for_ai(proc))
        process_strs.append("")
    
    process_data = "\n".join(process_strs)
    
    return BATCH_ANALYSIS_PROMPT.format(
        count=len(processes),
        process_data=process_data
    )
