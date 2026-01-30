"""
PML (Process Monitor Log) binary file parser.
Uses the procmon-parser library for parsing.
"""

import io
from datetime import datetime
from pathlib import Path
from typing import BinaryIO

from procmon_parser import ProcmonLogsReader

from app.models import ProcessEvent, ParsedLogFile
from app.parsers.base import BaseParser


class PMLParser(BaseParser):
    """Parser for native PML binary files from Process Monitor."""
    
    @property
    def supported_extensions(self) -> list[str]:
        return [".pml"]
    
    def parse(self, file_path: Path) -> ParsedLogFile:
        """Parse a PML file from disk."""
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        with open(file_path, "rb") as f:
            return self.parse_stream(f, file_path.name)
    
    def parse_stream(self, file_stream: BinaryIO, filename: str) -> ParsedLogFile:
        """Parse a PML file from a stream."""
        events: list[ProcessEvent] = []
        unique_processes: set[tuple[int, str]] = set()
        start_time: datetime | None = None
        end_time: datetime | None = None
        
        # Read stream into memory for procmon-parser
        content = file_stream.read()
        file_stream = io.BytesIO(content)
        
        try:
            reader = ProcmonLogsReader(file_stream)
            
            for event in reader:
                parsed_event = self._convert_event(event)
                events.append(parsed_event)
                
                # Track unique processes
                unique_processes.add((parsed_event.pid, parsed_event.process_name))
                
                # Track time range
                if start_time is None or parsed_event.timestamp < start_time:
                    start_time = parsed_event.timestamp
                if end_time is None or parsed_event.timestamp > end_time:
                    end_time = parsed_event.timestamp
                    
        except Exception as e:
            raise ValueError(f"Failed to parse PML file: {str(e)}") from e
        
        return ParsedLogFile(
            filename=filename,
            format="pml",
            event_count=len(events),
            process_count=len(unique_processes),
            start_time=start_time,
            end_time=end_time,
            events=events
        )
    
    def _convert_event(self, event) -> ProcessEvent:
        """Convert a procmon-parser event to our ProcessEvent model."""
        # Extract timestamp
        timestamp = self._extract_timestamp(event)
        
        # Extract process info - handle the special format from procmon-parser
        # Format: "C:\path\to\process.exe", 1234
        process_name, pid, image_path = self._parse_process_info(event)
        
        # Extract operation details
        operation = str(event.operation) if hasattr(event, "operation") else "Unknown"
        path = str(event.path) if hasattr(event, "path") and event.path else ""
        result = str(event.result) if hasattr(event, "result") else ""
        detail = str(event.detail) if hasattr(event, "detail") and event.detail else ""
        
        # Extract extended info
        tid = self._safe_get_int(event, "tid", "TID")
        duration = self._safe_get_float(event, "duration", "Duration")
        parent_pid = self._safe_get_int(event, "parent_pid", "Parent PID")
        command_line = self._safe_get(event, "command_line", "Command Line")
        user = self._safe_get(event, "user", "User")
        company = self._safe_get(event, "company", "Company")
        description = self._safe_get(event, "description", "Description")
        integrity = self._safe_get(event, "integrity", "Integrity")
        category = str(event.event_class) if hasattr(event, "event_class") else None
        
        # Extract stack trace if available
        stack_trace = None
        if hasattr(event, "stacktrace") and event.stacktrace:
            stack_trace = [str(addr) for addr in event.stacktrace]
        
        return ProcessEvent(
            timestamp=timestamp,
            process_name=process_name,
            pid=pid,
            operation=operation,
            path=path,
            result=result,
            detail=detail,
            tid=tid,
            duration=duration,
            parent_pid=parent_pid,
            command_line=command_line,
            user=user,
            image_path=image_path,
            company=company,
            description=description,
            integrity=integrity,
            category=category,
            stack_trace=stack_trace
        )
    
    def _parse_process_info(self, event) -> tuple[str, int, str | None]:
        """
        Parse the process attribute from procmon-parser.
        Format can be: "C:\\path\\process.exe", 1234
        
        Returns: (process_name, pid, image_path)
        """
        process_name = "Unknown"
        pid = 0
        image_path = None
        
        if hasattr(event, "process"):
            proc_str = str(event.process)
            
            # Try to parse the format: "path", pid
            if '"' in proc_str:
                parts = proc_str.split('"')
                if len(parts) > 1:
                    image_path = parts[1]
                    process_name = image_path.split('\\')[-1] if '\\' in image_path else image_path
                if len(parts) > 2:
                    # Extract PID from after the quotes
                    pid_str = parts[2].strip(', ')
                    try:
                        pid = int(pid_str)
                    except (ValueError, TypeError):
                        pid = 0
            else:
                # Simple format - just the name
                process_name = proc_str
        
        return process_name, pid, image_path
    
    def _extract_timestamp(self, event) -> datetime:
        """Extract timestamp from event, with fallback."""
        # Try various attribute names
        for attr in ["date_filetime", "timestamp", "time", "Time of Day"]:
            if hasattr(event, attr):
                val = getattr(event, attr)
                if val is not None:
                    if isinstance(val, datetime):
                        return val
                    # Handle Windows FILETIME (100-nanosecond intervals since 1601)
                    if isinstance(val, (int, float)):
                        try:
                            # Convert FILETIME to datetime
                            epoch = datetime(1601, 1, 1)
                            return epoch + __import__("datetime").timedelta(microseconds=val / 10)
                        except (ValueError, OverflowError):
                            pass
        
        # Default to now if no timestamp found
        return datetime.now()
    
    def _safe_get(self, event, *attrs) -> str | None:
        """Safely get an attribute from event object."""
        for attr in attrs:
            if hasattr(event, attr):
                val = getattr(event, attr)
                if val is not None:
                    return str(val)
        return None
    
    def _safe_get_int(self, event, *attrs) -> int | None:
        """Safely get an integer attribute."""
        val = self._safe_get(event, *attrs)
        if val is not None:
            try:
                return int(val)
            except (ValueError, TypeError):
                pass
        return None
    
    def _safe_get_float(self, event, *attrs) -> float | None:
        """Safely get a float attribute."""
        val = self._safe_get(event, *attrs)
        if val is not None:
            try:
                return float(val)
            except (ValueError, TypeError):
                pass
        return None
