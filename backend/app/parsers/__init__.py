"""
Parsers package - unified interface for parsing PML, CSV, and XML files.
"""

from pathlib import Path
from typing import BinaryIO

from app.models import ParsedLogFile
from app.parsers.base import BaseParser
from app.parsers.pml_parser import PMLParser
from app.parsers.csv_parser import CSVParser
from app.parsers.xml_parser import XMLParser


class ParserFactory:
    """Factory for creating appropriate parsers based on file type."""
    
    _parsers: list[BaseParser] = [
        PMLParser(),
        CSVParser(),
        XMLParser(),
    ]
    
    @classmethod
    def get_parser(cls, filename: str) -> BaseParser:
        """
        Get the appropriate parser for a given filename.
        
        Args:
            filename: Name of the file to parse
            
        Returns:
            Parser instance that can handle the file
            
        Raises:
            ValueError: If no parser supports the file type
        """
        for parser in cls._parsers:
            if parser.can_parse(filename):
                return parser
        
        ext = Path(filename).suffix
        supported = ", ".join(
            ext for p in cls._parsers for ext in p.supported_extensions
        )
        raise ValueError(
            f"Unsupported file format: {ext}. Supported formats: {supported}"
        )
    
    @classmethod
    def parse_file(cls, file_path: Path) -> ParsedLogFile:
        """
        Parse a log file from disk.
        
        Args:
            file_path: Path to the log file
            
        Returns:
            ParsedLogFile with all events
        """
        parser = cls.get_parser(file_path.name)
        return parser.parse(file_path)
    
    @classmethod
    def parse_stream(cls, file_stream: BinaryIO, filename: str) -> ParsedLogFile:
        """
        Parse a log file from a stream.
        
        Args:
            file_stream: Binary stream of the file
            filename: Original filename
            
        Returns:
            ParsedLogFile with all events
        """
        parser = cls.get_parser(filename)
        return parser.parse_stream(file_stream, filename)
    
    @classmethod
    def supported_extensions(cls) -> list[str]:
        """Get list of all supported file extensions."""
        return [ext for p in cls._parsers for ext in p.supported_extensions]


# Convenience exports
def parse_log_file(file_path: Path) -> ParsedLogFile:
    """Parse a log file from disk."""
    return ParserFactory.parse_file(file_path)


def parse_log_stream(file_stream: BinaryIO, filename: str) -> ParsedLogFile:
    """Parse a log file from a stream."""
    return ParserFactory.parse_stream(file_stream, filename)


__all__ = [
    "BaseParser",
    "PMLParser",
    "CSVParser",
    "XMLParser",
    "ParserFactory",
    "parse_log_file",
    "parse_log_stream",
]
