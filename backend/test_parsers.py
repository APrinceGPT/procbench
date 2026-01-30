"""
Test script for verifying parser functionality.
"""

import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent))

from app.parsers import parse_log_file, ParserFactory


def test_parsers():
    """Test all parsers with available log files."""
    base_path = Path(__file__).parent.parent
    
    test_files = [
        ("Logfile.PML", "pml"),
        ("Logfile.CSV", "csv"),
    ]
    
    print("=" * 60)
    print("ProcBench Parser Test")
    print("=" * 60)
    
    print(f"\nSupported extensions: {ParserFactory.supported_extensions()}")
    
    for filename, expected_format in test_files:
        file_path = base_path / filename
        
        if not file_path.exists():
            print(f"\n⚠️  Skipping {filename} - file not found")
            continue
        
        print(f"\n{'─' * 60}")
        print(f"Testing: {filename}")
        print(f"{'─' * 60}")
        
        try:
            result = parse_log_file(file_path)
            
            print(f"✅ Format detected: {result.format}")
            print(f"✅ Events parsed: {result.event_count:,}")
            print(f"✅ Unique processes: {result.process_count}")
            
            if result.start_time:
                print(f"✅ Time range: {result.start_time} to {result.end_time}")
            
            if result.duration_seconds:
                print(f"✅ Duration: {result.duration_seconds:.2f} seconds")
            
            # Show sample events
            if result.events:
                print(f"\n📋 Sample events (first 3):")
                for i, event in enumerate(result.events[:3]):
                    print(f"   {i+1}. [{event.operation}] {event.process_name} (PID: {event.pid})")
                    if event.path:
                        print(f"      Path: {event.path[:80]}...")
            
            # Check for PML-exclusive data
            if result.format == "pml":
                events_with_stack = sum(1 for e in result.events if e.stack_trace)
                events_with_duration = sum(1 for e in result.events if e.duration is not None)
                print(f"\n📊 PML-exclusive data:")
                print(f"   Events with stack traces: {events_with_stack:,}")
                print(f"   Events with duration: {events_with_duration:,}")
                
        except Exception as e:
            print(f"❌ Error parsing {filename}: {e}")
            import traceback
            traceback.print_exc()
    
    print(f"\n{'=' * 60}")
    print("Parser test complete!")
    print("=" * 60)


if __name__ == "__main__":
    test_parsers()
