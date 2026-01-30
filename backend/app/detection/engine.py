"""
Detection engine - orchestrates all detection modules.
"""

from collections import Counter, defaultdict
from uuid import uuid4

from app.models import (
    ProcessEvent,
    ProcessInfo,
    Finding,
    FindingSummary,
    Severity,
    FindingType,
    LegitimacyStatus,
)
from app.detection.lolbas import is_lolbas, get_lolbas_info, get_lolbas_risk
from app.detection.suspicious import analyze_path, analyze_file_access
from app.detection.parent_child import analyze_parent_child


class DetectionEngine:
    """
    Rule-based detection engine for Process Monitor logs.
    Analyzes events and produces findings.
    """
    
    def __init__(self):
        self.findings: list[Finding] = []
        self.process_risks: dict[str, int] = {}  # pid -> risk score
        self.process_flags: dict[str, list[str]] = defaultdict(list)  # pid -> reasons
    
    def analyze_events(self, events: list[ProcessEvent]) -> tuple[list[ProcessInfo], FindingSummary]:
        """
        Analyze a list of events and produce findings.
        
        Returns: (process_info_list, finding_summary)
        """
        # Group events by process
        process_events: dict[int, list[ProcessEvent]] = defaultdict(list)
        for event in events:
            process_events[event.pid].append(event)
        
        # Build process info objects
        process_infos: list[ProcessInfo] = []
        
        for pid, pid_events in process_events.items():
            if not pid_events:
                continue
            
            first_event = pid_events[0]
            process_info = self._build_process_info(pid, pid_events, first_event)
            
            # Analyze for suspicious patterns
            self._analyze_process(process_info, pid_events)
            
            process_infos.append(process_info)
        
        # Build parent-child relationships
        self._build_relationships(process_infos, events)
        
        # Generate finding summary
        summary = self._build_summary()
        
        return process_infos, summary
    
    def _build_process_info(
        self, pid: int, events: list[ProcessEvent], first_event: ProcessEvent
    ) -> ProcessInfo:
        """Build a ProcessInfo object from events."""
        # Count operations by type
        file_ops = 0
        registry_ops = 0
        network_ops = 0
        process_ops = 0
        
        accessed_files: list[str] = []
        accessed_registry: list[str] = []
        network_connections: list[str] = []
        
        for event in events:
            op = event.operation.lower() if event.operation else ""
            
            if "file" in op or "directory" in op:
                file_ops += 1
                if event.path and len(accessed_files) < 50:
                    accessed_files.append(event.path)
            elif "reg" in op:
                registry_ops += 1
                if event.path and len(accessed_registry) < 50:
                    accessed_registry.append(event.path)
            elif "tcp" in op or "udp" in op or "network" in op:
                network_ops += 1
                if event.path and len(network_connections) < 20:
                    network_connections.append(event.path)
            elif "process" in op or "thread" in op:
                process_ops += 1
        
        # Deduplicate paths (keep unique, preserve order)
        accessed_files = list(dict.fromkeys(accessed_files))[:20]
        accessed_registry = list(dict.fromkeys(accessed_registry))[:20]
        network_connections = list(dict.fromkeys(network_connections))[:10]
        
        return ProcessInfo(
            pid=pid,
            process_name=first_event.process_name,
            image_path=first_event.image_path,
            command_line=first_event.command_line,
            parent_pid=first_event.parent_pid,
            user=first_event.user,
            integrity=first_event.integrity,
            company=first_event.company,
            description=first_event.description,
            event_count=len(events),
            file_operations=file_ops,
            registry_operations=registry_ops,
            network_operations=network_ops,
            process_operations=process_ops,
            accessed_files=accessed_files,
            accessed_registry=accessed_registry,
            network_connections=network_connections,
        )
    
    def _analyze_process(self, process: ProcessInfo, events: list[ProcessEvent]) -> None:
        """Analyze a process for suspicious patterns."""
        risk_score = 0
        matched_rules: list[str] = []
        behavior_tags: list[str] = []
        
        # Check for LOLBAS
        if is_lolbas(process.process_name):
            lolbas_info = get_lolbas_info(process.process_name)
            risk_score += get_lolbas_risk(process.process_name)
            matched_rules.append(f"lolbas:{process.process_name.lower()}")
            
            self._add_finding(
                finding_type=FindingType.LOLBAS,
                severity=Severity.MEDIUM,
                process=process,
                title=f"LOLBAS Binary: {process.process_name}",
                description=f"{process.process_name} is a Living Off The Land binary. " +
                           f"{lolbas_info['description'] if lolbas_info else 'Could be abused by attackers.'}",
                evidence=[f"Process path: {process.image_path or 'Unknown'}"],
            )
        
        # Check path suspiciousness
        path_risk, path_reasons, _ = analyze_path(process.image_path)
        if path_risk > 0:
            risk_score += path_risk
            matched_rules.extend([f"suspicious_path:{r.lower().replace(' ', '_')}" for r in path_reasons])
            
            for reason in path_reasons:
                self._add_finding(
                    finding_type=FindingType.SUSPICIOUS_PATH,
                    severity=self._risk_to_severity(path_risk),
                    process=process,
                    title=f"Suspicious Path: {reason}",
                    description=f"{process.process_name} is running from a suspicious location.",
                    evidence=[f"Path: {process.image_path}"],
                )
        
        # Check file access patterns
        for file_path in process.accessed_files:
            file_risk, file_reason, file_tag = analyze_file_access(file_path)
            if file_risk > 0:
                risk_score += file_risk // 2  # Reduce to avoid over-weighting
                if file_tag and file_tag not in behavior_tags:
                    behavior_tags.append(file_tag)
                
                self._add_finding(
                    finding_type=FindingType.CREDENTIAL_ACCESS if file_tag == "credential_access" else FindingType.SUSPICIOUS_PATH,
                    severity=self._risk_to_severity(file_risk),
                    process=process,
                    title=file_reason or "Suspicious file access",
                    description=f"{process.process_name} accessed a sensitive file.",
                    evidence=[f"File accessed: {file_path}"],
                )
        
        # Check registry access for persistence
        for reg_path in process.accessed_registry:
            reg_lower = reg_path.lower()
            if any(key in reg_lower for key in ["run", "runonce", "startup"]):
                risk_score += 15
                if "persistence" not in behavior_tags:
                    behavior_tags.append("persistence")
                matched_rules.append("persistence:registry_run_key")
        
        # Update process with analysis results
        process.risk_score = min(risk_score, 100)  # Cap at 100
        process.matched_rules = matched_rules
        process.behavior_tags = behavior_tags
        process.is_flagged = risk_score >= 20
        
        # Set initial legitimacy based on risk
        if risk_score >= 70:
            process.legitimacy = LegitimacyStatus.SUSPICIOUS
        elif risk_score >= 40:
            process.legitimacy = LegitimacyStatus.SUSPICIOUS
        else:
            process.legitimacy = LegitimacyStatus.UNKNOWN
    
    def _build_relationships(
        self, processes: list[ProcessInfo], events: list[ProcessEvent]
    ) -> None:
        """Build parent-child relationships between processes."""
        pid_to_process = {p.pid: p for p in processes}
        
        # Find parent names
        for process in processes:
            if process.parent_pid and process.parent_pid in pid_to_process:
                parent = pid_to_process[process.parent_pid]
                process.parent_name = parent.process_name
                parent.children_pids.append(process.pid)
                
                # Check parent-child anomalies
                risk, reasons = analyze_parent_child(parent.process_name, process.process_name)
                if risk > 0:
                    process.risk_score = min(process.risk_score + risk, 100)
                    process.is_flagged = True
                    
                    for reason in reasons:
                        process.matched_rules.append(f"parent_child:{reason.lower().replace(' ', '_')[:30]}")
                        
                        self._add_finding(
                            finding_type=FindingType.PARENT_CHILD_ANOMALY,
                            severity=self._risk_to_severity(risk),
                            process=process,
                            title=f"Parent-Child Anomaly: {reason[:50]}",
                            description=reason,
                            evidence=[
                                f"Parent: {parent.process_name} (PID: {parent.pid})",
                                f"Child: {process.process_name} (PID: {process.pid})"
                            ],
                        )
    
    def _add_finding(
        self,
        finding_type: FindingType,
        severity: Severity,
        process: ProcessInfo,
        title: str,
        description: str,
        evidence: list[str],
        recommendation: str | None = None,
    ) -> None:
        """Add a finding to the list."""
        finding = Finding(
            id=f"FND-{uuid4().hex[:8].upper()}",
            type=finding_type,
            severity=severity,
            process_name=process.process_name,
            pid=process.pid,
            title=title,
            description=description,
            evidence=evidence,
            recommendation=recommendation,
        )
        self.findings.append(finding)
    
    def _risk_to_severity(self, risk: int) -> Severity:
        """Convert risk score to severity."""
        if risk >= 40:
            return Severity.HIGH
        elif risk >= 25:
            return Severity.MEDIUM
        elif risk >= 15:
            return Severity.LOW
        else:
            return Severity.INFO
    
    def _build_summary(self) -> FindingSummary:
        """Build a summary of all findings."""
        critical_count = sum(1 for f in self.findings if f.severity == Severity.CRITICAL)
        high_count = sum(1 for f in self.findings if f.severity == Severity.HIGH)
        medium_count = sum(1 for f in self.findings if f.severity == Severity.MEDIUM)
        low_count = sum(1 for f in self.findings if f.severity == Severity.LOW)
        info_count = sum(1 for f in self.findings if f.severity == Severity.INFO)
        
        # Count by type
        findings_by_type: dict[str, int] = {}
        for finding in self.findings:
            type_str = finding.type.value
            findings_by_type[type_str] = findings_by_type.get(type_str, 0) + 1
        
        return FindingSummary(
            total_findings=len(self.findings),
            critical_count=critical_count,
            high_count=high_count,
            medium_count=medium_count,
            low_count=low_count,
            info_count=info_count,
            findings=self.findings,
            findings_by_type=findings_by_type,
        )
