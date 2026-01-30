"""
Base parser interface for log file parsers.
"""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import BinaryIO

from app.models import ParsedLogFile


class BaseParser(ABC):
    """Abstract base class for log file parsers."""
    
    @property
    @abstractmethod
    def supported_extensions(self) -> list[str]:
        """Return list of supported file extensions."""
        pass
    
    @abstractmethod
    def parse(self, file_path: Path) -> ParsedLogFile:
        """
        Parse a log file and return structured data.
        
        Args:
            file_path: Path to the log file
            
        Returns:
            ParsedLogFile containing all parsed events
            
        Raises:
            ValueError: If file format is invalid
            FileNotFoundError: If file doesn't exist
        """
        pass
    
    @abstractmethod
    def parse_stream(self, file_stream: BinaryIO, filename: str) -> ParsedLogFile:
        """
        Parse a log file from a stream.
        
        Args:
            file_stream: Binary file stream
            filename: Original filename for format detection
            
        Returns:
            ParsedLogFile containing all parsed events
        """
        pass
    
    def can_parse(self, filename: str) -> bool:
        """Check if this parser can handle the given filename."""
        ext = Path(filename).suffix.lower()
        return ext in self.supported_extensions
