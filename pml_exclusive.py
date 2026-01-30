"""Deep dive into PML-exclusive data"""
from procmon_parser import ProcmonLogsReader

pml_path = r"F:\AI Project\AI Project\ProcBench\Logfile.PML"

print("=" * 70)
print("PML-EXCLUSIVE DATA (Not in CSV)")
print("=" * 70)

with open(pml_path, "rb") as f:
    reader = ProcmonLogsReader(f)
    
    # Collect samples with different features
    events_with_stack = 0
    events_with_details = 0
    unique_event_classes = set()
    sample_with_stack = None
    sample_with_details = None
    
    for i, event in enumerate(reader):
        unique_event_classes.add(event.event_class)
        
        if event.stacktrace and len(event.stacktrace) > 0:
            events_with_stack += 1
            if sample_with_stack is None:
                sample_with_stack = event
        
        if event.details and len(event.details) > 0:
            events_with_details += 1
            if sample_with_details is None:
                sample_with_details = event
    
    print(f"\n1. STACK TRACES (Critical for Injection Detection)")
    print(f"   Events with stack traces: {events_with_stack:,} / 53,429")
    if sample_with_stack:
        print(f"   Sample stack (first 5 addresses):")
        for addr in sample_with_stack.stacktrace[:5]:
            print(f"     0x{addr:016X}")
    
    print(f"\n2. DETAILED EVENT DATA")
    print(f"   Events with rich details: {events_with_details:,}")
    if sample_with_details:
        print(f"   Sample details dict: {dict(sample_with_details.details)}")
    
    print(f"\n3. EVENT CLASSES")
    print(f"   Unique classes found: {unique_event_classes}")
    class_names = {
        0: "Unknown",
        1: "Process",
        2: "Registry", 
        3: "File System",
        4: "Network"
    }
    for c in sorted(unique_event_classes):
        print(f"     Class {c}: {class_names.get(c, 'Other')}")
    
    print(f"\n4. TIMING PRECISION")
    print(f"   PML stores: Windows FILETIME (100-nanosecond intervals)")
    print(f"   CSV stores: Human-readable time string (loses precision)")
    
    print(f"\n5. DURATION (Execution Time)")
    print(f"   PML has 'duration' field for each operation")
    print(f"   CSV does NOT include operation duration")
    
    print(f"\n6. THREAD ID (TID)")
    print(f"   PML includes TID for thread-level analysis")
    print(f"   CSV only has PID (process level)")
