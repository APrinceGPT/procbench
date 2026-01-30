"""
XML file parser for Process Monitor exported XML files.
"""

import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path
from typing import BinaryIO

from app.models import ProcessEvent, ParsedLogFile
from app.parsers.base import BaseParser


class XMLParser(BaseParser):
    """Parser for XML files exported from Process Monitor."""
    
    @property
    def supported_extensions(self) -> list[str]:
        return [".xml"]
    
    def parse(self, file_path: Path) -> ParsedLogFile:
        """Parse an XML file from disk."""
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        with open(file_path, "rb") as f:
            return self.parse_stream(f, file_path.name)
    
    def parse_stream(self, file_stream: BinaryIO, filename: str) -> ParsedLogFile:
        """Parse an XML file from a stream."""
        events: list[ProcessEvent] = []
        unique_processes: set[tuple[int, str]] = set()
        start_time: datetime | None = None
        end_time: datetime | None = None
        
        try:
            # Parse XML incrementally to handle large files
            context = ET.iterparse(file_stream, events=["end"])
            
            for event_type, elem in context:
                # Process Monitor XML uses <event> tags
                if elem.tag.lower() == "event":
                    try:
                        parsed_event = self._convert_element(elem)
                        events.append(parsed_event)
                        
                        # Track unique processes
                        unique_processes.add((parsed_event.pid, parsed_event.process_name))
                        
                        # Track time range
                        if start_time is None or parsed_event.timestamp < start_time:
                            start_time = parsed_event.timestamp
                        if end_time is None or parsed_event.timestamp > end_time:
                            end_time = parsed_event.timestamp
                            
                    except Exception:
                        # Skip malformed events
                        pass
                    
                    # Clear element to save memory
                    elem.clear()
                    
        except ET.ParseError as e:
            raise ValueError(f"Failed to parse XML file: {str(e)}") from e
        
        return ParsedLogFile(
            filename=filename,
            format="xml",
            event_count=len(events),
            process_count=len(unique_processes),
            start_time=start_time,
            end_time=end_time,
            events=events
        )
    
    def _convert_element(self, elem: ET.Element) -> ProcessEvent:
        """Convert an XML event element to ProcessEvent."""
        # Helper to get element text
        def get_text(tag: str) -> str:
            child = elem.find(tag)
            if child is None:
                # Try case-insensitive
                for c in elem:
                    if c.tag.lower() == tag.lower():
                        return c.text or ""
            return child.text if child is not None and child.text else ""
        
        def get_int(tag: str) -> int:
            text = get_text(tag)
            try:
                return int(text) if text else 0
            except ValueError:
                return 0
        
        # Parse standard fields
        timestamp = self._parse_timestamp(get_text("Time_of_Day") or get_text("TimeOfDay"))
        process_name = get_text("Process_Name") or get_text("ProcessName") or "Unknown"
        pid = get_int("PID")
        operation = get_text("Operation") or "Unknown"
        path = get_text("Path")
        result = get_text("Result")
        detail = get_text("Detail")
        
        # Extended fields
        parent_pid = get_int("Parent_PID") or get_int("ParentPID") or None
        command_line = get_text("Command_Line") or get_text("CommandLine") or None
        user = get_text("User") or None
        image_path = get_text("Image_Path") or get_text("ImagePath") or None
        company = get_text("Company") or None
        description = get_text("Description") or None
        integrity = get_text("Integrity") or None
        
        return ProcessEvent(
            timestamp=timestamp,
            process_name=process_name,
            pid=pid,
            operation=operation,
            path=path,
            result=result,
            detail=detail,
            parent_pid=parent_pid if parent_pid != 0 else None,
            command_line=command_line,
            user=user,
            image_path=image_path,
            company=company,
            description=description,
            integrity=integrity
        )
    
    def _parse_timestamp(self, time_str: str) -> datetime:
        """Parse timestamp from XML time string."""
        if not time_str:
            return datetime.now()
        
        formats = [
            "%I:%M:%S.%f %p",
            "%H:%M:%S.%f",
            "%H:%M:%S",
            "%Y-%m-%dT%H:%M:%S.%f",
            "%Y-%m-%dT%H:%M:%S",
            "%Y-%m-%d %H:%M:%S.%f",
            "%Y-%m-%d %H:%M:%S",
        ]
        
        for fmt in formats:
            try:
                parsed = datetime.strptime(time_str.strip(), fmt)
                if parsed.year == 1900:
                    today = datetime.now().date()
                    parsed = parsed.replace(year=today.year, month=today.month, day=today.day)
                return parsed
            except ValueError:
                continue
        
        return datetime.now()
