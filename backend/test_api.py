"""
Test script for API endpoints.
"""

import sys
from pathlib import Path
import requests
import time

BASE_URL = "http://127.0.0.1:8080"


def test_api():
    """Test the API endpoints."""
    print("=" * 60)
    print("ProcBench API Test")
    print("=" * 60)
    
    # Test health endpoint
    print("\n[1/5] Testing health endpoint...")
    try:
        resp = requests.get(f"{BASE_URL}/api/v1/health")
        resp.raise_for_status()
        data = resp.json()
        print(f"    ✅ Health check passed: {data}")
    except Exception as e:
        print(f"    ❌ Health check failed: {e}")
        return
    
    # Test supported formats
    print("\n[2/5] Testing supported formats endpoint...")
    try:
        resp = requests.get(f"{BASE_URL}/api/v1/supported-formats")
        resp.raise_for_status()
        data = resp.json()
        print(f"    ✅ Supported formats: {data['formats']}")
        print(f"    ✅ Max file size: {data['max_file_size_mb']} MB")
    except Exception as e:
        print(f"    ❌ Supported formats failed: {e}")
    
    # Test file upload and analysis
    print("\n[3/5] Testing file upload and analysis...")
    pml_path = Path(__file__).parent.parent / "Logfile.PML"
    
    if not pml_path.exists():
        print(f"    ⚠️ Skipping - PML file not found: {pml_path}")
        return
    
    try:
        with open(pml_path, "rb") as f:
            files = {"file": (pml_path.name, f, "application/octet-stream")}
            start = time.time()
            resp = requests.post(f"{BASE_URL}/api/v1/analyze", files=files)
            elapsed = time.time() - start
            resp.raise_for_status()
            data = resp.json()
            print(f"    ✅ Analysis started: {data['analysis_id']}")
            print(f"    ✅ Status: {data['status']}")
            print(f"    ✅ Time: {elapsed:.2f}s")
            
            analysis_id = data['analysis_id']
    except Exception as e:
        print(f"    ❌ File upload failed: {e}")
        return
    
    # Test get analysis results
    print(f"\n[4/5] Testing get analysis results...")
    try:
        resp = requests.get(f"{BASE_URL}/api/v1/analysis/{analysis_id}")
        resp.raise_for_status()
        data = resp.json()
        print(f"    ✅ Analysis ID: {data['analysis_id']}")
        print(f"    ✅ Total Events: {data['total_events']:,}")
        print(f"    ✅ Total Processes: {data['total_processes']}")
        print(f"    ✅ Flagged: {data['flagged_processes']}")
        print(f"    ✅ High Risk: {data['high_risk_count']}")
        print(f"    ✅ Duration: {data['analysis_duration_seconds']:.2f}s")
        
        if data['top_threats']:
            print(f"\n    Top Threat: {data['top_threats'][0]['process_name']}")
            print(f"    Risk Score: {data['top_threats'][0]['risk_score']}")
    except Exception as e:
        print(f"    ❌ Get analysis failed: {e}")
    
    # Test get processes
    print(f"\n[5/5] Testing get processes endpoint...")
    try:
        resp = requests.get(f"{BASE_URL}/api/v1/analysis/{analysis_id}/processes?flagged_only=true")
        resp.raise_for_status()
        data = resp.json()
        print(f"    ✅ Flagged processes: {data['total']}")
        for proc in data['processes'][:3]:
            print(f"       - {proc['process_name']} (Risk: {proc['risk_score']})")
    except Exception as e:
        print(f"    ❌ Get processes failed: {e}")
    
    print(f"\n{'=' * 60}")
    print("API test complete!")
    print("=" * 60)


if __name__ == "__main__":
    test_api()
