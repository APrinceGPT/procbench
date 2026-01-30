"""
CSV file parser for Process Monitor exported CSV files.
"""

import csv
import io
from datetime import datetime
from pathlib import Path
from typing import BinaryIO

from app.models import ProcessEvent, ParsedLogFile
from app.parsers.base import BaseParser


class CSVParser(BaseParser):
    """Parser for CSV files exported from Process Monitor."""
    
    @property
    def supported_extensions(self) -> list[str]:
        return [".csv"]
    
    def parse(self, file_path: Path) -> ParsedLogFile:
        """Parse a CSV file from disk."""
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        with open(file_path, "rb") as f:
            return self.parse_stream(f, file_path.name)
    
    def parse_stream(self, file_stream: BinaryIO, filename: str) -> ParsedLogFile:
        """Parse a CSV file from a stream."""
        events: list[ProcessEvent] = []
        unique_processes: set[tuple[int, str]] = set()
        start_time: datetime | None = None
        end_time: datetime | None = None
        
        # Decode stream to text
        content = file_stream.read()
        text_content = content.decode("utf-8-sig")  # Handle BOM
        text_stream = io.StringIO(text_content)
        
        # Parse CSV
        reader = csv.DictReader(text_stream)
        
        for row in reader:
            try:
                parsed_event = self._convert_row(row)
                events.append(parsed_event)
                
                # Track unique processes
                unique_processes.add((parsed_event.pid, parsed_event.process_name))
                
                # Track time range
                if start_time is None or parsed_event.timestamp < start_time:
                    start_time = parsed_event.timestamp
                if end_time is None or parsed_event.timestamp > end_time:
                    end_time = parsed_event.timestamp
                    
            except Exception:
                # Skip malformed rows
                continue
        
        return ParsedLogFile(
            filename=filename,
            format="csv",
            event_count=len(events),
            process_count=len(unique_processes),
            start_time=start_time,
            end_time=end_time,
            events=events
        )
    
    def _convert_row(self, row: dict) -> ProcessEvent:
        """Convert a CSV row to ProcessEvent."""
        # Standard Process Monitor CSV columns
        timestamp = self._parse_timestamp(row.get("Time of Day", ""))
        process_name = row.get("Process Name", "Unknown")
        pid = self._parse_int(row.get("PID", "0"))
        operation = row.get("Operation", "Unknown")
        path = row.get("Path", "")
        result = row.get("Result", "")
        detail = row.get("Detail", "")
        
        # Extended columns (may not be present)
        parent_pid = self._parse_int(row.get("Parent PID"))
        command_line = row.get("Command Line")
        user = row.get("User")
        image_path = row.get("Image Path")
        company = row.get("Company")
        description = row.get("Description")
        integrity = row.get("Integrity")
        
        return ProcessEvent(
            timestamp=timestamp,
            process_name=process_name,
            pid=pid,
            operation=operation,
            path=path,
            result=result,
            detail=detail,
            parent_pid=parent_pid,
            command_line=command_line,
            user=user,
            image_path=image_path,
            company=company,
            description=description,
            integrity=integrity
        )
    
    def _parse_timestamp(self, time_str: str) -> datetime:
        """Parse timestamp from CSV time string."""
        if not time_str:
            return datetime.now()
        
        # Process Monitor uses various time formats
        formats = [
            "%I:%M:%S.%f %p",  # 12-hour with AM/PM
            "%H:%M:%S.%f",     # 24-hour with microseconds
            "%H:%M:%S",        # 24-hour without microseconds
            "%Y-%m-%d %H:%M:%S.%f",
            "%Y-%m-%d %H:%M:%S",
        ]
        
        for fmt in formats:
            try:
                parsed = datetime.strptime(time_str.strip(), fmt)
                # If no date, use today
                if parsed.year == 1900:
                    today = datetime.now().date()
                    parsed = parsed.replace(year=today.year, month=today.month, day=today.day)
                return parsed
            except ValueError:
                continue
        
        # Default to now if parsing fails
        return datetime.now()
    
    def _parse_int(self, value: str | None) -> int:
        """Parse integer from string, defaulting to 0."""
        if not value:
            return 0
        try:
            return int(value)
        except (ValueError, TypeError):
            return 0
