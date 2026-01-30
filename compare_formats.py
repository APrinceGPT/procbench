"""Compare PML vs CSV format differences"""
from procmon_parser import ProcmonLogsReader
import csv
import os

pml_path = r"F:\AI Project\AI Project\ProcBench\Logfile.PML"
csv_path = r"F:\AI Project\AI Project\ProcBench\Logfile.CSV"

print("=" * 70)
print("PML vs CSV COMPARISON")
print("=" * 70)

# File sizes
pml_size = os.path.getsize(pml_path) / (1024*1024)
csv_size = os.path.getsize(csv_path) / (1024*1024)
print(f"\n📁 FILE SIZES:")
print(f"   PML: {pml_size:.2f} MB")
print(f"   CSV: {csv_size:.2f} MB")
print(f"   Ratio: CSV is {csv_size/pml_size:.1f}x larger than PML")

# CSV Fields
print(f"\n📋 CSV FIELDS:")
with open(csv_path, 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    headers = next(reader)
    print(f"   Columns ({len(headers)}): {headers}")
    
    # Get one sample row
    sample = next(reader)
    print(f"\n   Sample CSV Row:")
    for h, v in zip(headers, sample):
        print(f"     {h}: {v[:80]}{'...' if len(v) > 80 else ''}")

# PML Fields
print(f"\n📋 PML FIELDS:")
with open(pml_path, "rb") as f:
    reader = ProcmonLogsReader(f)
    for event in reader:
        print(f"   Available attributes:")
        attrs = [a for a in dir(event) if not a.startswith('_')]
        for attr in attrs:
            try:
                val = getattr(event, attr)
                if not callable(val):
                    val_str = str(val)
                    print(f"     {attr}: {val_str[:60]}{'...' if len(val_str) > 60 else ''}")
            except:
                pass
        break

# Count events in both
print(f"\n📊 EVENT COUNTS:")
with open(csv_path, 'r', encoding='utf-8') as f:
    csv_count = sum(1 for _ in f) - 1  # minus header

with open(pml_path, "rb") as f:
    reader = ProcmonLogsReader(f)
    pml_count = sum(1 for _ in reader)

print(f"   PML Events: {pml_count:,}")
print(f"   CSV Events: {csv_count:,}")
print(f"   Match: {'Yes' if pml_count == csv_count else 'No - ' + str(abs(pml_count - csv_count)) + ' difference'}")
