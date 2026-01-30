"""Quick test to verify PML parsing works"""
from procmon_parser import ProcmonLogsReader
from collections import Counter

pml_path = r"F:\AI Project\AI Project\ProcBench\Logfile.PML"

print("Opening PML file...")
with open(pml_path, "rb") as f:
    reader = ProcmonLogsReader(f)
    
    count = 0
    processes = Counter()
    operations = Counter()
    
    print("Parsing events...")
    for event in reader:
        count += 1
        proc_str = str(event.process)
        if '"' in proc_str:
            proc_name = proc_str.split('"')[1].split('\\')[-1]
        else:
            proc_name = "unknown"
        processes[proc_name] += 1
        operations[event.operation] += 1
        
        if count % 10000 == 0:
            print(f"  Processed {count:,} events...")

print(f"\n=== PML PARSING SUCCESSFUL ===")
print(f"Total Events: {count:,}")
print(f"Unique Processes: {len(processes)}")
print(f"Unique Operations: {len(operations)}")
print(f"\nTop 10 Processes:")
for p, c in processes.most_common(10):
    print(f"  {p}: {c:,}")
print(f"\nTop 10 Operations:")
for o, c in operations.most_common(10):
    print(f"  {o}: {c:,}")
