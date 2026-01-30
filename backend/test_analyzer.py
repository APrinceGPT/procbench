"""
Test script for the full analysis pipeline.
"""

import sys
import os
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent))

# Load environment variables
from dotenv import load_dotenv
env_path = Path(__file__).parent.parent / "env"
if env_path.exists():
    load_dotenv(env_path)

from app.analysis import analyze_file


def test_full_analysis():
    """Test the complete analysis pipeline."""
    base_path = Path(__file__).parent.parent
    pml_path = base_path / "Logfile.PML"
    
    print("=" * 70)
    print("ProcBench Full Analysis Test")
    print("=" * 70)
    
    if not pml_path.exists():
        print(f"❌ PML file not found: {pml_path}")
        return
    
    # Check if AI is configured
    api_key = os.environ.get("OPENAI_API_KEY", "")
    use_ai = bool(api_key)
    print(f"\n🤖 AI Analysis: {'Enabled' if use_ai else 'Disabled (no API key)'}")
    
    # Run analysis
    print(f"\n📂 Analyzing: {pml_path.name}")
    print("-" * 70)
    
    result = analyze_file(pml_path, use_ai=use_ai)
    
    # Display results
    print(f"\n📊 Analysis Results")
    print("=" * 70)
    print(f"  Analysis ID: {result.analysis_id}")
    print(f"  Status: {result.status}")
    print(f"  Duration: {result.analysis_duration_seconds:.2f} seconds")
    print(f"\n  Events Analyzed: {result.total_events:,}")
    print(f"  Unique Processes: {result.total_processes}")
    print(f"  Flagged Processes: {result.flagged_processes}")
    
    print(f"\n📈 Risk Distribution:")
    print(f"  🔴 High Risk (70+):   {result.high_risk_count}")
    print(f"  🟠 Medium Risk (30-69): {result.medium_risk_count}")
    print(f"  🟢 Low Risk (0-29):    {result.low_risk_count}")
    
    print(f"\n🎯 Top Threats:")
    print("-" * 70)
    for i, threat in enumerate(result.top_threats[:10], 1):
        risk_icon = "🔴" if threat.risk_score >= 70 else "🟠" if threat.risk_score >= 30 else "🟡"
        legit_icon = {
            "legitimate": "✅",
            "suspicious": "⚠️",
            "malicious": "🚨",
            "unknown": "❓"
        }.get(threat.legitimacy.value, "❓")
        
        print(f"\n  {i}. {risk_icon} {threat.process_name} (PID: {threat.pid})")
        print(f"     Risk Score: {threat.risk_score}/100  |  Legitimacy: {legit_icon} {threat.legitimacy.value.upper()}")
        
        if threat.image_path:
            print(f"     Path: {threat.image_path[:70]}...")
        
        if threat.behavior_tags:
            print(f"     Tags: {', '.join(threat.behavior_tags)}")
        
        if threat.matched_rules:
            print(f"     Rules: {', '.join(threat.matched_rules[:3])}")
        
        if threat.ai_reasoning:
            print(f"     AI: {threat.ai_reasoning[:100]}...")
    
    print(f"\n🌳 Process Tree Summary:")
    print("-" * 70)
    print(f"  Root processes: {len(result.process_tree)}")
    
    # Show first 3 tree roots
    for i, root in enumerate(result.process_tree[:3], 1):
        children_count = len(root.children)
        risk_icon = "🔴" if root.process.risk_score >= 70 else "🟠" if root.process.risk_score >= 30 else "🟢"
        print(f"  {i}. {risk_icon} {root.process.process_name} (Risk: {root.process.risk_score}, Children: {children_count})")
    
    print("\n" + "=" * 70)
    print("Analysis complete!")
    print("=" * 70)


if __name__ == "__main__":
    test_full_analysis()
