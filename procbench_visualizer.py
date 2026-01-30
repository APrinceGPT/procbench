"""
ProcBench Visualizer - Workbench-Style Diagram Output
Generates interactive HTML reports with process trees, observable graphs, and timelines
"""

from procmon_parser import ProcmonLogsReader
from pyvis.network import Network
from collections import defaultdict, Counter
from datetime import datetime
import json
import os

class ProcBenchVisualizer:
    def __init__(self, pml_path: str):
        self.pml_path = pml_path
        self.events = []
        self.processes = {}
        self.file_access = defaultdict(list)
        self.registry_access = defaultdict(list)
        self.anomalies = []
        
    def parse_pml(self, max_events=None):
        """Parse PML file and extract structured data"""
        print(f"[*] Parsing PML file: {self.pml_path}")
        
        with open(self.pml_path, "rb") as f:
            reader = ProcmonLogsReader(f)
            
            for i, event in enumerate(reader):
                if max_events and i >= max_events:
                    break
                    
                # Extract process info
                proc_str = str(event.process)
                if '"' in proc_str:
                    parts = proc_str.split('"')
                    proc_path = parts[1] if len(parts) > 1 else "unknown"
                    proc_name = proc_path.split('\\')[-1]
                    pid = parts[2].strip(', ') if len(parts) > 2 else "0"
                else:
                    proc_path = "unknown"
                    proc_name = "unknown"
                    pid = "0"
                
                event_data = {
                    'timestamp': event.date_filetime,
                    'process_name': proc_name,
                    'process_path': proc_path,
                    'pid': pid,
                    'operation': event.operation,
                    'path': event.path,
                    'result': event.result,
                    'tid': event.tid,
                    'duration': event.duration,
                    'event_class': str(event.event_class),
                    'details': dict(event.details) if event.details else {},
                    'has_stack': len(event.stacktrace) > 0 if event.stacktrace else False
                }
                
                self.events.append(event_data)
                
                # Track process info
                if proc_name not in self.processes:
                    self.processes[proc_name] = {
                        'path': proc_path,
                        'pids': set(),
                        'operations': Counter(),
                        'files_accessed': set(),
                        'first_seen': event.date_filetime,
                        'last_seen': event.date_filetime
                    }
                
                self.processes[proc_name]['pids'].add(pid)
                self.processes[proc_name]['operations'][event.operation] += 1
                self.processes[proc_name]['last_seen'] = event.date_filetime
                
                if event.path:
                    self.processes[proc_name]['files_accessed'].add(event.path)
                
                if i % 10000 == 0:
                    print(f"  Processed {i:,} events...")
        
        print(f"[+] Parsed {len(self.events):,} events from {len(self.processes)} unique processes")
        return self
    
    def detect_anomalies(self):
        """Rule-based anomaly detection"""
        print("[*] Running anomaly detection...")
        
        # Suspicious paths
        suspicious_paths = ['\\temp\\', '\\appdata\\local\\temp\\', '\\downloads\\']
        lolbas = ['cmd.exe', 'powershell.exe', 'wscript.exe', 'cscript.exe', 
                  'mshta.exe', 'rundll32.exe', 'regsvr32.exe', 'certutil.exe']
        
        for proc_name, data in self.processes.items():
            anomaly = None
            
            # Check for LOLBAS execution from suspicious locations
            if proc_name.lower() in lolbas:
                for path in suspicious_paths:
                    if path in data['path'].lower():
                        anomaly = {
                            'type': 'LOLBAS_SUSPICIOUS_PATH',
                            'severity': 'HIGH',
                            'process': proc_name,
                            'path': data['path'],
                            'description': f'Living-off-the-land binary {proc_name} executed from suspicious path',
                            'mitre': 'T1059 - Command and Scripting Interpreter'
                        }
                        break
            
            # Check for executables in temp folders
            if data['path'].lower().endswith('.exe'):
                for path in suspicious_paths:
                    if path in data['path'].lower():
                        anomaly = {
                            'type': 'EXE_IN_TEMP',
                            'severity': 'MEDIUM',
                            'process': proc_name,
                            'path': data['path'],
                            'description': f'Executable running from temporary directory',
                            'mitre': 'T1204 - User Execution'
                        }
                        break
            
            # Check for high registry activity (potential persistence)
            reg_ops = sum(1 for op, count in data['operations'].items() 
                         if 'Reg' in op for _ in range(count))
            if reg_ops > 100:
                anomaly = {
                    'type': 'HIGH_REGISTRY_ACTIVITY',
                    'severity': 'MEDIUM',
                    'process': proc_name,
                    'path': data['path'],
                    'description': f'Process has unusually high registry activity ({reg_ops} operations)',
                    'mitre': 'T1547 - Boot or Logon Autostart Execution'
                }
            
            if anomaly:
                self.anomalies.append(anomaly)
        
        print(f"[+] Detected {len(self.anomalies)} potential anomalies")
        return self
    
    def generate_observable_graph(self, output_path="observable_graph.html"):
        """Generate Workbench-style Observable Graph"""
        print("[*] Generating Observable Graph...")
        
        net = Network(height="800px", width="100%", bgcolor="#1a1a2e", font_color="white")
        net.force_atlas_2based()
        
        # Color scheme matching Workbench
        colors = {
            'process': '#4CAF50',      # Green
            'file': '#2196F3',          # Blue
            'registry': '#FF9800',      # Orange
            'anomaly': '#f44336',       # Red
            'system': '#9E9E9E'         # Gray
        }
        
        added_nodes = set()
        
        # Add process nodes
        for proc_name, data in list(self.processes.items())[:50]:  # Limit for visualization
            if proc_name not in added_nodes:
                # Check if process is anomalous
                is_anomaly = any(a['process'] == proc_name for a in self.anomalies)
                color = colors['anomaly'] if is_anomaly else colors['process']
                
                net.add_node(proc_name, 
                           label=proc_name,
                           title=f"Process: {proc_name}\nPath: {data['path']}\nPIDs: {', '.join(list(data['pids'])[:5])}\nOperations: {sum(data['operations'].values())}",
                           color=color,
                           shape='dot',
                           size=20 + min(sum(data['operations'].values()) // 100, 30))
                added_nodes.add(proc_name)
        
        # Add file nodes and edges (limit to most accessed)
        file_counts = Counter()
        for event in self.events:
            if event['path'] and 'File' in event['event_class']:
                file_counts[event['path']] += 1
        
        for filepath, count in file_counts.most_common(30):
            filename = filepath.split('\\')[-1][:30]
            if filename not in added_nodes:
                net.add_node(filename,
                           label=filename,
                           title=f"File: {filepath}\nAccess count: {count}",
                           color=colors['file'],
                           shape='square',
                           size=10)
                added_nodes.add(filename)
        
        # Add edges (process -> file relationships)
        edge_counts = Counter()
        for event in self.events:
            if event['path'] and event['process_name'] in added_nodes:
                filename = event['path'].split('\\')[-1][:30]
                if filename in added_nodes:
                    edge_key = (event['process_name'], filename)
                    edge_counts[edge_key] += 1
        
        for (src, dst), count in edge_counts.most_common(100):
            net.add_edge(src, dst, value=min(count, 10), title=f"Operations: {count}")
        
        # Add anomaly highlights
        for anomaly in self.anomalies:
            proc = anomaly['process']
            if proc in added_nodes:
                # Add MITRE technique node
                mitre = anomaly['mitre'].split(' - ')[0]
                if mitre not in added_nodes:
                    net.add_node(mitre,
                               label=mitre,
                               title=anomaly['description'],
                               color='#e91e63',
                               shape='triangle',
                               size=15)
                    added_nodes.add(mitre)
                net.add_edge(proc, mitre, color='#e91e63', dashes=True)
        
        # Save the graph
        net.save_graph(output_path)
        print(f"[+] Observable Graph saved to: {output_path}")
        return output_path
    
    def generate_html_report(self, output_path="procbench_report.html"):
        """Generate comprehensive Workbench-style HTML report"""
        print("[*] Generating HTML Report...")
        
        # Calculate statistics
        stats = {
            'total_events': len(self.events),
            'unique_processes': len(self.processes),
            'anomalies_found': len(self.anomalies),
            'high_severity': sum(1 for a in self.anomalies if a['severity'] == 'HIGH'),
            'medium_severity': sum(1 for a in self.anomalies if a['severity'] == 'MEDIUM'),
        }
        
        # Top processes by activity
        top_processes = sorted(
            [(name, sum(data['operations'].values())) for name, data in self.processes.items()],
            key=lambda x: x[1], reverse=True
        )[:10]
        
        # Operation breakdown
        all_operations = Counter()
        for data in self.processes.values():
            all_operations.update(data['operations'])
        
        html_content = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ProcBench Analysis Report</title>
    <script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
    <style>
        :root {{
            --bg-primary: #0d1117;
            --bg-secondary: #161b22;
            --bg-card: #21262d;
            --text-primary: #c9d1d9;
            --text-secondary: #8b949e;
            --accent-blue: #58a6ff;
            --accent-green: #3fb950;
            --accent-orange: #d29922;
            --accent-red: #f85149;
            --accent-purple: #a371f7;
            --border-color: #30363d;
        }}
        
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif;
            background: var(--bg-primary);
            color: var(--text-primary);
            line-height: 1.6;
        }}
        
        .container {{ max-width: 1400px; margin: 0 auto; padding: 20px; }}
        
        /* Header - Workbench Style */
        .header {{
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            padding: 30px;
            border-radius: 12px;
            margin-bottom: 24px;
            border: 1px solid var(--border-color);
        }}
        
        .header h1 {{
            font-size: 28px;
            margin-bottom: 8px;
            display: flex;
            align-items: center;
            gap: 12px;
        }}
        
        .header .subtitle {{
            color: var(--text-secondary);
            font-size: 14px;
        }}
        
        /* Score Badge - Like Workbench */
        .score-badge {{
            display: inline-flex;
            align-items: center;
            justify-content: center;
            width: 60px;
            height: 60px;
            border-radius: 50%;
            font-size: 24px;
            font-weight: bold;
            background: linear-gradient(135deg, var(--accent-red), #ff6b6b);
            color: white;
        }}
        
        .score-badge.medium {{
            background: linear-gradient(135deg, var(--accent-orange), #ffd93d);
        }}
        
        .score-badge.low {{
            background: linear-gradient(135deg, var(--accent-green), #6bcb77);
        }}
        
        /* Stats Grid */
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 16px;
            margin-bottom: 24px;
        }}
        
        .stat-card {{
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: 8px;
            padding: 20px;
            text-align: center;
        }}
        
        .stat-card .value {{
            font-size: 36px;
            font-weight: bold;
            color: var(--accent-blue);
        }}
        
        .stat-card .label {{
            color: var(--text-secondary);
            font-size: 14px;
            margin-top: 4px;
        }}
        
        .stat-card.danger .value {{ color: var(--accent-red); }}
        .stat-card.warning .value {{ color: var(--accent-orange); }}
        .stat-card.success .value {{ color: var(--accent-green); }}
        
        /* Sections */
        .section {{
            background: var(--bg-secondary);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            margin-bottom: 24px;
            overflow: hidden;
        }}
        
        .section-header {{
            background: var(--bg-card);
            padding: 16px 20px;
            border-bottom: 1px solid var(--border-color);
            font-size: 16px;
            font-weight: 600;
            display: flex;
            align-items: center;
            gap: 8px;
        }}
        
        .section-content {{
            padding: 20px;
        }}
        
        /* Anomaly Cards - Like Workbench Highlights */
        .anomaly-card {{
            background: var(--bg-card);
            border-left: 4px solid var(--accent-red);
            border-radius: 8px;
            padding: 16px;
            margin-bottom: 12px;
        }}
        
        .anomaly-card.medium {{ border-left-color: var(--accent-orange); }}
        
        .anomaly-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 8px;
        }}
        
        .anomaly-type {{
            font-weight: 600;
            font-size: 14px;
        }}
        
        .severity-badge {{
            padding: 4px 12px;
            border-radius: 12px;
            font-size: 12px;
            font-weight: 600;
        }}
        
        .severity-badge.high {{
            background: rgba(248, 81, 73, 0.2);
            color: var(--accent-red);
        }}
        
        .severity-badge.medium {{
            background: rgba(210, 153, 34, 0.2);
            color: var(--accent-orange);
        }}
        
        .mitre-tag {{
            display: inline-block;
            background: rgba(163, 113, 247, 0.2);
            color: var(--accent-purple);
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 12px;
            margin-top: 8px;
        }}
        
        /* Process Table */
        table {{
            width: 100%;
            border-collapse: collapse;
        }}
        
        th, td {{
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid var(--border-color);
        }}
        
        th {{
            background: var(--bg-card);
            font-weight: 600;
            font-size: 12px;
            text-transform: uppercase;
            color: var(--text-secondary);
        }}
        
        tr:hover {{
            background: rgba(88, 166, 255, 0.1);
        }}
        
        /* Timeline */
        .timeline {{
            position: relative;
            padding-left: 30px;
        }}
        
        .timeline::before {{
            content: '';
            position: absolute;
            left: 8px;
            top: 0;
            bottom: 0;
            width: 2px;
            background: var(--border-color);
        }}
        
        .timeline-item {{
            position: relative;
            padding-bottom: 20px;
        }}
        
        .timeline-item::before {{
            content: '';
            position: absolute;
            left: -26px;
            top: 4px;
            width: 12px;
            height: 12px;
            border-radius: 50%;
            background: var(--accent-blue);
            border: 2px solid var(--bg-primary);
        }}
        
        .timeline-item.anomaly::before {{
            background: var(--accent-red);
        }}
        
        /* Graph Container */
        .graph-container {{
            background: var(--bg-card);
            border-radius: 8px;
            padding: 20px;
            min-height: 400px;
        }}
        
        /* Mermaid Diagrams */
        .mermaid {{
            background: var(--bg-card);
            padding: 20px;
            border-radius: 8px;
        }}
        
        /* Responsive */
        @media (max-width: 768px) {{
            .stats-grid {{ grid-template-columns: 1fr 1fr; }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <!-- Header -->
        <div class="header">
            <h1>
                <span class="score-badge {'high' if stats['high_severity'] > 0 else 'medium' if stats['medium_severity'] > 0 else 'low'}">
                    {stats['high_severity'] + stats['medium_severity']}
                </span>
                ProcBench Analysis Report
            </h1>
            <div class="subtitle">
                Process Monitor Log Analysis | Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
            </div>
        </div>
        
        <!-- Stats Grid -->
        <div class="stats-grid">
            <div class="stat-card">
                <div class="value">{stats['total_events']:,}</div>
                <div class="label">Total Events</div>
            </div>
            <div class="stat-card">
                <div class="value">{stats['unique_processes']}</div>
                <div class="label">Unique Processes</div>
            </div>
            <div class="stat-card danger">
                <div class="value">{stats['high_severity']}</div>
                <div class="label">High Severity</div>
            </div>
            <div class="stat-card warning">
                <div class="value">{stats['medium_severity']}</div>
                <div class="label">Medium Severity</div>
            </div>
        </div>
        
        <!-- Anomalies Section (Highlights) -->
        <div class="section">
            <div class="section-header">
                🚨 Highlights - Detected Anomalies
            </div>
            <div class="section-content">
                {''.join(f"""
                <div class="anomaly-card {a['severity'].lower()}">
                    <div class="anomaly-header">
                        <span class="anomaly-type">{a['type']}</span>
                        <span class="severity-badge {a['severity'].lower()}">{a['severity']}</span>
                    </div>
                    <div style="color: var(--text-secondary); font-size: 14px;">
                        <strong>Process:</strong> {a['process']}<br>
                        <strong>Path:</strong> {a['path'][:80]}{'...' if len(a['path']) > 80 else ''}<br>
                        {a['description']}
                    </div>
                    <div class="mitre-tag">🎯 {a['mitre']}</div>
                </div>
                """ for a in self.anomalies) if self.anomalies else '<p style="color: var(--text-secondary);">No anomalies detected</p>'}
            </div>
        </div>
        
        <!-- Process Execution Flow (Mermaid) -->
        <div class="section">
            <div class="section-header">
                📊 Process Activity Flow
            </div>
            <div class="section-content">
                <div class="mermaid">
flowchart LR
    subgraph Processes
{chr(10).join(f'        {name.replace(".", "_").replace("-", "_")}["{name}\\n{count:,} ops"]' for name, count in top_processes[:8])}
    end
    
    subgraph Operations
        REG[("Registry\\n{all_operations.get('RegOpenKey', 0) + all_operations.get('RegQueryValue', 0):,}")]
        FILE[("Files\\n{all_operations.get('ReadFile', 0) + all_operations.get('CreateFile', 0):,}")]
        PROC[("Process\\n{all_operations.get('Process_Profiling', 0):,}")]
    end
    
{chr(10).join(f'    {name.replace(".", "_").replace("-", "_")} --> REG' for name, _ in top_processes[:4])}
{chr(10).join(f'    {name.replace(".", "_").replace("-", "_")} --> FILE' for name, _ in top_processes[:4])}
                </div>
            </div>
        </div>
        
        <!-- Top Processes Table -->
        <div class="section">
            <div class="section-header">
                🖥️ Impact Scope - Top Processes by Activity
            </div>
            <div class="section-content">
                <table>
                    <thead>
                        <tr>
                            <th>Process</th>
                            <th>Path</th>
                            <th>Operations</th>
                            <th>Files Accessed</th>
                            <th>Status</th>
                        </tr>
                    </thead>
                    <tbody>
                        {''.join(f"""
                        <tr>
                            <td><strong>{name}</strong></td>
                            <td style="font-size: 12px; color: var(--text-secondary);">{self.processes[name]['path'][:50]}...</td>
                            <td>{count:,}</td>
                            <td>{len(self.processes[name]['files_accessed'])}</td>
                            <td>{'<span style="color: var(--accent-red);">⚠️ Anomaly</span>' if any(a['process'] == name for a in self.anomalies) else '<span style="color: var(--accent-green);">✓ Normal</span>'}</td>
                        </tr>
                        """ for name, count in top_processes)}
                    </tbody>
                </table>
            </div>
        </div>
        
        <!-- Observable Graph Link -->
        <div class="section">
            <div class="section-header">
                🔗 Observable Graph
            </div>
            <div class="section-content">
                <p style="margin-bottom: 16px; color: var(--text-secondary);">
                    Interactive node-link diagram showing process-to-file relationships and anomaly connections.
                </p>
                <a href="observable_graph.html" target="_blank" style="
                    display: inline-block;
                    background: var(--accent-blue);
                    color: white;
                    padding: 12px 24px;
                    border-radius: 8px;
                    text-decoration: none;
                    font-weight: 600;
                ">Open Interactive Graph →</a>
            </div>
        </div>
        
        <!-- Operation Breakdown -->
        <div class="section">
            <div class="section-header">
                📈 Operation Breakdown
            </div>
            <div class="section-content">
                <div class="mermaid">
pie showData
    title Operations Distribution
    {chr(10).join(f'    "{op}" : {count}' for op, count in all_operations.most_common(8))}
                </div>
            </div>
        </div>
    </div>
    
    <script>
        mermaid.initialize({{ 
            startOnLoad: true,
            theme: 'dark',
            themeVariables: {{
                primaryColor: '#58a6ff',
                primaryTextColor: '#c9d1d9',
                primaryBorderColor: '#30363d',
                lineColor: '#8b949e',
                secondaryColor: '#21262d',
                tertiaryColor: '#161b22'
            }}
        }});
    </script>
</body>
</html>'''
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"[+] HTML Report saved to: {output_path}")
        return output_path


def main():
    pml_path = r"F:\AI Project\AI Project\ProcBench\Logfile.PML"
    output_dir = r"F:\AI Project\AI Project\ProcBench\output"
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    # Initialize visualizer
    viz = ProcBenchVisualizer(pml_path)
    
    # Parse and analyze
    viz.parse_pml()
    viz.detect_anomalies()
    
    # Generate visualizations
    viz.generate_observable_graph(os.path.join(output_dir, "observable_graph.html"))
    viz.generate_html_report(os.path.join(output_dir, "procbench_report.html"))
    
    print("\n" + "="*60)
    print("✅ ANALYSIS COMPLETE!")
    print("="*60)
    print(f"\n📊 Open these files in your browser:")
    print(f"   1. {os.path.join(output_dir, 'procbench_report.html')}")
    print(f"   2. {os.path.join(output_dir, 'observable_graph.html')}")


if __name__ == "__main__":
    main()
