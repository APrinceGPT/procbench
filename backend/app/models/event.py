"""
Pydantic models for process events.
"""

from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field


class OperationType(str, Enum):
    """Types of operations captured by Process Monitor."""
    PROCESS_CREATE = "Process Create"
    PROCESS_START = "Process Start"
    PROCESS_EXIT = "Process Exit"
    THREAD_CREATE = "Thread Create"
    THREAD_EXIT = "Thread Exit"
    LOAD_IMAGE = "Load Image"
    CREATE_FILE = "CreateFile"
    CLOSE_FILE = "CloseFile"
    READ_FILE = "ReadFile"
    WRITE_FILE = "WriteFile"
    QUERY_DIRECTORY = "QueryDirectory"
    SET_DISPOSITION = "SetDispositionInformationFile"
    REG_OPEN_KEY = "RegOpenKey"
    REG_QUERY_VALUE = "RegQueryValue"
    REG_SET_VALUE = "RegSetValue"
    REG_CREATE_KEY = "RegCreateKey"
    REG_DELETE_KEY = "RegDeleteKey"
    REG_DELETE_VALUE = "RegDeleteValue"
    REG_CLOSE_KEY = "RegCloseKey"
    TCP_CONNECT = "TCP Connect"
    TCP_SEND = "TCP Send"
    TCP_RECEIVE = "TCP Receive"
    UDP_SEND = "UDP Send"
    UDP_RECEIVE = "UDP Receive"
    OTHER = "Other"


class ProcessEvent(BaseModel):
    """Represents a single event from Process Monitor."""
    
    # Core fields
    timestamp: datetime = Field(description="When the event occurred")
    process_name: str = Field(description="Name of the process")
    pid: int = Field(description="Process ID")
    operation: str = Field(description="Type of operation")
    path: str = Field(default="", description="File/registry path involved")
    result: str = Field(default="", description="Operation result")
    detail: str = Field(default="", description="Additional details")
    
    # Extended fields (from PML)
    tid: int | None = Field(default=None, description="Thread ID")
    duration: float | None = Field(default=None, description="Operation duration in seconds")
    parent_pid: int | None = Field(default=None, description="Parent process ID")
    command_line: str | None = Field(default=None, description="Full command line")
    user: str | None = Field(default=None, description="User account")
    session: int | None = Field(default=None, description="Session ID")
    image_path: str | None = Field(default=None, description="Full path to executable")
    company: str | None = Field(default=None, description="Company from file version info")
    description: str | None = Field(default=None, description="Description from file version info")
    version: str | None = Field(default=None, description="File version")
    architecture: str | None = Field(default=None, description="32-bit or 64-bit")
    integrity: str | None = Field(default=None, description="Integrity level")
    category: str | None = Field(default=None, description="Event category")
    
    # Stack trace (PML exclusive)
    stack_trace: list[str] | None = Field(default=None, description="Call stack addresses")
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class ParsedLogFile(BaseModel):
    """Container for all events parsed from a log file."""
    
    filename: str = Field(description="Original filename")
    format: str = Field(description="File format: pml, csv, or xml")
    event_count: int = Field(description="Total number of events")
    process_count: int = Field(description="Number of unique processes")
    start_time: datetime | None = Field(default=None, description="First event timestamp")
    end_time: datetime | None = Field(default=None, description="Last event timestamp")
    events: list[ProcessEvent] = Field(default_factory=list, description="All parsed events")
    
    @property
    def duration_seconds(self) -> float | None:
        """Calculate the capture duration in seconds."""
        if self.start_time and self.end_time:
            return (self.end_time - self.start_time).total_seconds()
        return None
