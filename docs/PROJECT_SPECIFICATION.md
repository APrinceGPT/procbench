# ProcBench - Project Specification Document

> **"Turn Process Noise into Threat Signal"**

---

## Document Information

| Field | Value |
|-------|-------|
| Project Name | ProcBench |
| Version | 1.0.0 |
| Document Version | 1.0 |
| Last Updated | January 31, 2026 |
| Status | Approved for Development |
| License | Open Source (MIT) |

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [Project Overview](#2-project-overview)
3. [Technical Architecture](#3-technical-architecture)
4. [Features Specification](#4-features-specification)
5. [User Interface Design](#5-user-interface-design)
6. [Detection Engine](#6-detection-engine)
7. [AI Integration](#7-ai-integration)
8. [Data Handling](#8-data-handling)
9. [API Specification](#9-api-specification)
10. [Testing Strategy](#10-testing-strategy)
11. [Deployment](#11-deployment)
12. [Future Roadmap](#12-future-roadmap)

---

## 1. Executive Summary

### 1.1 Purpose

ProcBench is an **AI-powered Process Monitor log analysis platform** designed to help SOC analysts identify malware and suspicious behaviors within Windows systems. By analyzing PML (Process Monitor Log) files, ProcBench provides:

- **Parent-child process relationship visualization**
- **AI-powered legitimacy assessment** of each process
- **Behavioral tagging** with reasoning
- **Guided investigation workflows** for analysts of all skill levels

### 1.2 Problem Statement

When a potential malware infection is suspected, SOC analysts often run Process Monitor to capture system activity. However:

- Raw PML files contain thousands of events (50,000+ typical)
- Manual analysis is time-consuming and error-prone
- Identifying malicious patterns requires deep expertise
- No existing tool provides AI-powered analysis of PML files

### 1.3 Solution

ProcBench automates the analysis of Process Monitor logs by:

1. Parsing native PML files (plus CSV/XML)
2. Building process relationship trees
3. Applying rule-based detection patterns
4. Enriching with AI-powered legitimacy assessment
5. Presenting findings in an intuitive, visual interface

### 1.4 Target Users

| User Level | Description | Primary Needs |
|------------|-------------|---------------|
| **SOC Analyst L1** | First-line triage | Quick verdicts, clear guidance |
| **SOC Analyst L2** | Investigation | Detailed analysis, process trees |
| **SOC Analyst L3** | Advanced hunting | Raw data access, custom rules |
| **Incident Responder** | Forensics | Timeline, IOC extraction |

---

## 2. Project Overview

### 2.1 Deployment Model

| Aspect | Specification |
|--------|---------------|
| **Type** | Cloud Web Application |
| **Access** | Browser-based (modern browsers) |
| **Hosting** | Cloud-hosted (containerized) |
| **Offline** | Not required |
| **Data Persistence** | Ephemeral (no long-term storage) |

### 2.2 Technology Stack

| Component | Technology | Justification |
|-----------|------------|---------------|
| **Frontend** | Svelte | Modern, fast, excellent DX |
| **Backend** | Go | Performance, concurrency, single binary |
| **AI Integration** | OpenAI-compatible API | Flexible, supports multiple providers |
| **Visualization** | D3.js / Chart.js | Interactive, modern charts |
| **PDF Export** | Go PDF library | Server-side PDF generation |
| **Containerization** | Docker | Consistent deployment |

### 2.3 Core Workflow

```
┌─────────────────────────────────────────────────────────────────────┐
│                        ProcBench Workflow                           │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────────┐ │
│  │  Upload  │───▶│  Parse   │───▶│  Detect  │───▶│   Analyze    │ │
│  │ PML File │    │  Events  │    │  (Rules) │    │    (AI)      │ │
│  └──────────┘    └──────────┘    └──────────┘    └──────────────┘ │
│                                                          │          │
│                                                          ▼          │
│                                         ┌────────────────────────┐ │
│                                         │   Visual Report +      │ │
│                                         │   PDF Export           │ │
│                                         └────────────────────────┘ │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 3. Technical Architecture

### 3.1 System Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                              Client Browser                              │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │                    Svelte Frontend Application                    │   │
│  │  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐   │   │
│  │  │ Upload  │ │Dashboard│ │ Process │ │Timeline │ │  Export │   │   │
│  │  │  View   │ │  View   │ │  Tree   │ │  View   │ │  View   │   │   │
│  │  └─────────┘ └─────────┘ └─────────┘ └─────────┘ └─────────┘   │   │
│  └─────────────────────────────────────────────────────────────────┘   │
└────────────────────────────────┬────────────────────────────────────────┘
                                 │ HTTPS
                                 ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                           Go Backend Server                              │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │                         API Layer (REST)                         │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                 │                                        │
│  ┌──────────────┬───────────────┼───────────────┬──────────────────┐   │
│  │              │               │               │                  │   │
│  ▼              ▼               ▼               ▼                  ▼   │
│ ┌────────┐ ┌─────────┐ ┌──────────────┐ ┌──────────┐ ┌───────────┐   │
│ │ Parser │ │Detection│ │  AI Service  │ │  Report  │ │  Config   │   │
│ │ Module │ │ Engine  │ │   Client     │ │Generator │ │  Manager  │   │
│ └────────┘ └─────────┘ └──────────────┘ └──────────┘ └───────────┘   │
│                                 │                                        │
│                                 ▼                                        │
│                    ┌──────────────────────┐                             │
│                    │   External AI API    │                             │
│                    │  (Rate Limited)      │                             │
│                    └──────────────────────┘                             │
└─────────────────────────────────────────────────────────────────────────┘
```

### 3.2 Component Specifications

#### 3.2.1 Parser Module

| Feature | Specification |
|---------|---------------|
| **Supported Formats** | PML (native binary), CSV, XML |
| **Max File Size** | 500 MB (default) |
| **Streaming** | Yes, for large files |
| **Output** | Normalized event structure |

**Parsed Event Structure:**
```go
type ProcessEvent struct {
    Timestamp     int64             `json:"timestamp"`
    ProcessName   string            `json:"process_name"`
    ProcessPath   string            `json:"process_path"`
    PID           int               `json:"pid"`
    TID           int               `json:"tid"`
    Operation     string            `json:"operation"`
    Path          string            `json:"path"`
    Result        string            `json:"result"`
    Duration      int64             `json:"duration"`
    EventClass    string            `json:"event_class"`
    Details       map[string]string `json:"details"`
    HasStackTrace bool              `json:"has_stack_trace"`
    StackTrace    []uint64          `json:"stack_trace,omitempty"`
}
```

#### 3.2.2 Detection Engine

| Feature | Specification |
|---------|---------------|
| **Mode** | Hybrid (Rules + AI) |
| **Rule Format** | YAML-based custom rules |
| **Built-in Rules** | LOLBAS, OWASP patterns, Sigma |
| **Custom Rules** | User-definable |
| **Output** | Flagged processes for AI analysis |

#### 3.2.3 AI Service Client

| Feature | Specification |
|---------|---------------|
| **Provider** | OpenAI-compatible API |
| **Rate Limiting** | Configurable (default: 10 req/min) |
| **Batching** | 10-15 processes per request |
| **Queue** | In-memory request queue |
| **Timeout** | 30 seconds per request |
| **Retry** | 3 attempts with exponential backoff |

#### 3.2.4 Report Generator

| Feature | Specification |
|---------|---------------|
| **Output Format** | PDF |
| **Sections** | Executive Summary, Findings, Process Tree, Timeline |
| **Styling** | Dark theme, print-optimized |
| **Charts** | Embedded as images |

### 3.3 Data Flow

```
┌─────────────────────────────────────────────────────────────────────────┐
│                           Data Flow                                      │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  PML File (500MB max)                                                   │
│       │                                                                 │
│       ▼                                                                 │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │                    1. PARSE                                      │   │
│  │    - Stream read binary PML                                      │   │
│  │    - Extract 50,000+ events                                      │   │
│  │    - Build process inventory (unique processes)                  │   │
│  │    - Map parent-child relationships                              │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│       │                                                                 │
│       ▼                                                                 │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │                    2. RULE-BASED DETECTION                       │   │
│  │    - Apply LOLBAS rules                                          │   │
│  │    - Check suspicious paths                                      │   │
│  │    - Analyze parent-child anomalies                              │   │
│  │    - Flag ~10-20% of processes as suspicious                     │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│       │                                                                 │
│       ▼                                                                 │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │                    3. AI ANALYSIS                                │   │
│  │    - Send ONLY flagged processes to AI                           │   │
│  │    - Batch requests (10-15 per call)                             │   │
│  │    - Receive: legitimacy, reasoning, behavior tags, risk score   │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│       │                                                                 │
│       ▼                                                                 │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │                    4. VISUALIZATION                              │   │
│  │    - Generate process tree                                       │   │
│  │    - Create timeline (anomalies only)                            │   │
│  │    - Build treemap heatmaps                                      │   │
│  │    - Render interactive dashboard                                │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│       │                                                                 │
│       ▼                                                                 │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │                    5. EXPORT                                     │   │
│  │    - Generate PDF report                                         │   │
│  │    - Include executive summary                                   │   │
│  │    - Print-optimized layout                                      │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 4. Features Specification

### 4.1 Core Features (v1.0)

| Feature | Priority | Description |
|---------|----------|-------------|
| **PML Parsing** | P0 | Parse native PML, CSV, XML files |
| **Process Tree** | P0 | Parent-child relationship visualization |
| **AI Legitimacy** | P0 | Assess each process as legitimate/suspicious/malicious |
| **Behavior Tagging** | P0 | Tag processes with behavior patterns |
| **Risk Scoring** | P0 | 0-100 risk score per process |
| **Timeline View** | P0 | Chronological view of anomalies |
| **Treemap Heatmaps** | P0 | File/registry access visualization |
| **Guided Investigation** | P0 | Step-by-step analysis workflow |
| **PDF Export** | P0 | Exportable analysis report |
| **Baseline Comparison** | P1 | Compare multiple PML files |
| **Custom Rules** | P1 | User-defined detection rules |
| **Multi-Skill Views** | P1 | L1/L2/L3 analyst views |

### 4.2 Feature Details

#### 4.2.1 Process Tree Visualization

**Purpose:** Show which process spawned which, color-coded by risk.

**Requirements:**
- Hierarchical tree structure
- Expandable/collapsible nodes
- Color coding: Red (malicious), Orange (suspicious), Green (legitimate)
- Click node to see details
- Zoom and pan support
- Filter by risk level

**Visual Specification:**
```
● explorer.exe [Risk: 5] ✓ LEGITIMATE
├── └── cmd.exe [Risk: 45] ⚠ SUSPICIOUS
│       └── powershell.exe [Risk: 78] 🚨 MALICIOUS
│           └── unknown.exe [Risk: 92] 🚨 MALICIOUS
├── └── notepad.exe [Risk: 3] ✓ LEGITIMATE
└── └── chrome.exe [Risk: 8] ✓ LEGITIMATE
```

#### 4.2.2 AI Legitimacy Assessment

**Purpose:** Provide expert-level assessment of each process.

**Output per Process:**
| Field | Type | Example |
|-------|------|---------|
| Legitimacy | Enum | LEGITIMATE / SUSPICIOUS / MALICIOUS / UNKNOWN |
| Risk Score | Integer | 0-100 |
| Reasoning | String | "Process running from Temp folder, accessing credential stores" |
| Behavior Tags | Array | ["persistence", "credential_access", "defense_evasion"] |
| MITRE Techniques | Array | ["T1059.001", "T1547.001"] (when applicable) |

#### 4.2.3 Timeline View

**Purpose:** Show chronological sequence of anomalous events.

**Requirements:**
- Show only anomaly events (not all 50K events)
- Interactive zoom (minute/hour/full range)
- Hover for event details
- Click to jump to process in tree
- Filter by severity

#### 4.2.4 Treemap Heatmaps

**Purpose:** Visualize which paths are most accessed.

**Types:**
| Heatmap | Shows |
|---------|-------|
| File Access | Directory tree sized by access count |
| Registry Access | Registry hive tree sized by access count |
| Operation Types | Operations sized by frequency |

**Requirements:**
- Treemap layout (not grid)
- Color by risk level
- Click to drill down
- Hover for details

#### 4.2.5 Guided Investigation Flow

**Purpose:** Walk analysts through the analysis step-by-step.

**Flow:**
```
Step 1: Upload → Step 2: Overview → Step 3: High Risk Review → 
Step 4: Process Tree → Step 5: Timeline → Step 6: Export
```

**Requirements:**
- Progress indicator
- Skip option for experienced users
- Contextual tips at each step
- "What to look for" guidance

#### 4.2.6 Baseline Comparison

**Purpose:** Compare a potentially infected system against a known-good baseline.

**Requirements:**
- Upload 2 PML files (baseline + current)
- Highlight new processes not in baseline
- Show processes with changed behavior
- Side-by-side diff view

#### 4.2.7 Custom Detection Rules

**Purpose:** Allow users to define their own detection patterns.

**Rule Format (YAML):**
```yaml
rules:
  - id: custom_001
    name: "Detect MyApp Abuse"
    description: "Flags when MyApp.exe spawns cmd.exe"
    severity: HIGH
    condition:
      parent_process: "MyApp.exe"
      child_process: "cmd.exe"
    tags:
      - "custom"
      - "myapp_abuse"
```

**Requirements:**
- YAML-based rule definition
- Rule import/export
- Rule testing interface
- Enable/disable individual rules

---

## 5. User Interface Design

### 5.1 Design System

| Aspect | Specification |
|--------|---------------|
| **Theme** | Dark only |
| **Primary Color** | #3B82F6 (Blue) |
| **Danger Color** | #EF4444 (Red) |
| **Warning Color** | #F59E0B (Orange) |
| **Success Color** | #10B981 (Green) |
| **Background** | #0F172A (Dark slate) |
| **Card Background** | #1E293B |
| **Text Primary** | #F1F5F9 |
| **Text Secondary** | #94A3B8 |
| **Font** | Inter, system-ui |
| **Monospace** | JetBrains Mono, Consolas |

### 5.2 Layout Structure

```
┌─────────────────────────────────────────────────────────────────────────┐
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │                         Top Navigation                          │   │
│  │  [Logo] ProcBench     [Dashboard] [Investigate] [Rules] [Help]  │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                                                         │
│  ┌───────────┬─────────────────────────────────────────────────────┐   │
│  │           │                                                     │   │
│  │  Sidebar  │                   Main Content                      │   │
│  │           │                                                     │   │
│  │  - Upload │     ┌─────────────────────────────────────────┐    │   │
│  │  - Summary│     │                                         │    │   │
│  │  - Tree   │     │          Active View                    │    │   │
│  │  - Timeline     │          (Dashboard/Tree/Timeline)      │    │   │
│  │  - Heatmap│     │                                         │    │   │
│  │  - Export │     │                                         │    │   │
│  │           │     └─────────────────────────────────────────┘    │   │
│  │           │                                                     │   │
│  │  ───────  │     ┌─────────────────────────────────────────┐    │   │
│  │  Filters  │     │         Detail Panel                    │    │   │
│  │  - Risk   │     │         (Selected item details)         │    │   │
│  │  - Type   │     └─────────────────────────────────────────┘    │   │
│  │           │                                                     │   │
│  └───────────┴─────────────────────────────────────────────────────┘   │
│                                                                         │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │                    Status Bar / Progress                        │   │
│  └─────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────┘
```

### 5.3 Skill Level Views

| View | Target | Content |
|------|--------|---------|
| **Simple (L1)** | Triage analysts | Summary cards, clear verdicts, action recommendations |
| **Standard (L2)** | Investigation | Process tree, timeline, detailed findings |
| **Advanced (L3)** | Threat hunters | Raw data, custom queries, all events |

**Toggle:** User can switch views via dropdown in navigation.

### 5.4 Guided Investigation Mode

**Step-by-step wizard overlay:**

```
┌─────────────────────────────────────────────────────────────────────────┐
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │                    Guided Investigation                         │   │
│  │                                                                 │   │
│  │   ● ─── ○ ─── ○ ─── ○ ─── ○ ─── ○                              │   │
│  │   Upload  Overview  Review  Tree  Timeline  Export              │   │
│  │                                                                 │   │
│  │  ┌───────────────────────────────────────────────────────────┐ │   │
│  │  │                                                           │ │   │
│  │  │   Step 1: Upload Your Process Monitor Log                │ │   │
│  │  │                                                           │ │   │
│  │  │   ┌─────────────────────────────────────────────────┐    │ │   │
│  │  │   │                                                 │    │ │   │
│  │  │   │     Drag & Drop PML, CSV, or XML file          │    │ │   │
│  │  │   │              (Max 500 MB)                       │    │ │   │
│  │  │   │                                                 │    │ │   │
│  │  │   └─────────────────────────────────────────────────┘    │ │   │
│  │  │                                                           │ │   │
│  │  │   💡 Tip: For best results, capture 5-30 minutes of      │ │   │
│  │  │          activity while reproducing the suspected        │ │   │
│  │  │          malware behavior.                               │ │   │
│  │  │                                                           │ │   │
│  │  └───────────────────────────────────────────────────────────┘ │   │
│  │                                                                 │   │
│  │           [Skip Guided Mode]              [Next →]              │   │
│  └─────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────┘
```

### 5.5 Onboarding & Training

**First-time user experience:**
1. Welcome modal with tool overview
2. Interactive tutorial (3-5 minutes)
3. Sample PML file for practice
4. Tooltips on first use of each feature
5. "What's this?" help icons throughout

**Help resources:**
- In-app documentation
- Video tutorials (embedded)
- Example reports
- Detection rule examples

---

## 6. Detection Engine

### 6.1 Rule-Based Detection

#### 6.1.1 Built-in Rule Categories

| Category | Description | Source |
|----------|-------------|--------|
| **LOLBAS** | Living-off-the-land binary detection | LOLBAS Project |
| **Suspicious Paths** | Executables in unusual locations | Internal |
| **Parent-Child Anomalies** | Unexpected process spawning | Internal |
| **Persistence Indicators** | Registry Run keys, Services, Tasks | MITRE ATT&CK |
| **Credential Access** | LSASS access, SAM registry | MITRE ATT&CK |
| **Defense Evasion** | Process hollowing indicators | MITRE ATT&CK |

#### 6.1.2 LOLBAS Detection

**Built-in list of monitored binaries:**
```
cmd.exe, powershell.exe, pwsh.exe, wscript.exe, cscript.exe,
mshta.exe, rundll32.exe, regsvr32.exe, certutil.exe, bitsadmin.exe,
msiexec.exe, installutil.exe, regasm.exe, regsvcs.exe, msbuild.exe,
cmstp.exe, wmic.exe, forfiles.exe, pcalua.exe, schtasks.exe
```

**Detection logic:**
- Flag if executing from non-standard paths
- Flag if spawned by suspicious parent
- Flag if accessing sensitive resources

#### 6.1.3 Suspicious Path Detection

**Flagged locations:**
```
%TEMP%\*.exe
%APPDATA%\*.exe
%LOCALAPPDATA%\*.exe
%USERPROFILE%\Downloads\*.exe
%PUBLIC%\*.exe
C:\ProgramData\*.exe (non-standard subdirs)
```

#### 6.1.4 Parent-Child Anomalies

**Suspicious relationships:**
| Parent | Unexpected Child | Concern |
|--------|------------------|---------|
| winword.exe | cmd.exe, powershell.exe | Macro execution |
| excel.exe | cmd.exe, powershell.exe | Macro execution |
| outlook.exe | cmd.exe, powershell.exe | Email-based attack |
| iexplore.exe | cmd.exe, powershell.exe | Browser exploit |
| svchost.exe | cmd.exe (direct) | Service abuse |
| wscript.exe | powershell.exe | Script-based attack |

### 6.2 Custom Rules

**Rule schema:**
```yaml
rule:
  id: string (required, unique)
  name: string (required)
  description: string (optional)
  severity: LOW | MEDIUM | HIGH | CRITICAL
  enabled: boolean (default: true)
  
  # Conditions (at least one required)
  conditions:
    process_name: string | regex
    process_path: string | regex
    parent_process: string | regex
    child_process: string | regex
    operation: string | regex
    path_accessed: string | regex
    registry_key: string | regex
    
  # Boolean operators
  operator: AND | OR (default: AND)
  
  # Output
  tags: [string]
  mitre_technique: string (optional)
```

**Example rules:**
```yaml
rules:
  - id: detect_encoded_powershell
    name: "Encoded PowerShell Execution"
    description: "Detects PowerShell with encoded command"
    severity: HIGH
    conditions:
      process_name: "powershell.exe"
      path_accessed: ".*-enc.*|-e .*"
    tags: ["execution", "obfuscation"]
    mitre_technique: "T1059.001"
    
  - id: lsass_access
    name: "LSASS Memory Access"
    description: "Process accessing LSASS memory"
    severity: CRITICAL
    conditions:
      path_accessed: ".*\\lsass.exe"
      operation: "ReadFile|CreateFile"
    tags: ["credential_access"]
    mitre_technique: "T1003.001"
```

---

## 7. AI Integration

### 7.1 Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        AI Integration Flow                               │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ┌─────────────────┐                                                    │
│  │ Flagged         │                                                    │
│  │ Processes       │                                                    │
│  │ (from rules)    │                                                    │
│  └────────┬────────┘                                                    │
│           │                                                             │
│           ▼                                                             │
│  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐    │
│  │   Batch Queue   │───▶│  Rate Limiter   │───▶│   AI API Call   │    │
│  │  (10-15/batch)  │    │ (configurable)  │    │                 │    │
│  └─────────────────┘    └─────────────────┘    └────────┬────────┘    │
│                                                          │              │
│                                                          ▼              │
│                                               ┌─────────────────┐      │
│                                               │  Parse Response │      │
│                                               │  - Legitimacy   │      │
│                                               │  - Risk Score   │      │
│                                               │  - Reasoning    │      │
│                                               │  - Behavior Tags│      │
│                                               └─────────────────┘      │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### 7.2 Configuration

**Environment variables:**
```env
# AI Provider Configuration
AI_PROVIDER=openai          # openai, azure, custom
AI_BASE_URL=https://api.example.com/v1
AI_API_KEY=sk-xxx
AI_MODEL=gpt-4

# Rate Limiting
AI_RATE_LIMIT_REQUESTS=10   # requests per minute
AI_RATE_LIMIT_TOKENS=10000  # tokens per minute
AI_BATCH_SIZE=15            # processes per request
AI_TIMEOUT_SECONDS=30       # request timeout
AI_MAX_RETRIES=3            # retry attempts
```

### 7.3 Prompt Engineering

**System prompt:**
```
You are an expert malware analyst examining Process Monitor data from a potentially compromised Windows system.

Your task is to assess each process for:
1. LEGITIMACY: Is this a legitimate Windows process or potentially malicious?
2. RISK LEVEL: How risky is this process behavior (0-100)?
3. REASONING: Explain your assessment in 1-2 sentences.
4. BEHAVIORS: Tag any concerning behaviors detected.

Consider:
- Is the executable path appropriate for this process?
- Are the operations typical for this process type?
- Are there suspicious parent-child relationships?
- Is it accessing sensitive resources (credentials, security, etc.)?

Always respond in the specified JSON format.
```

### 7.4 Error Handling

| Error | Handling |
|-------|----------|
| Rate limit exceeded | Queue and retry with backoff |
| Timeout | Retry up to 3 times |
| Invalid response | Fall back to rule-based assessment |
| API unavailable | Continue with rule-based only, warn user |

---

## 8. Data Handling

### 8.1 Input Specifications

| Format | Max Size | Parser |
|--------|----------|--------|
| PML (native) | 500 MB | Go PML parser |
| CSV | 500 MB | Standard CSV |
| XML | 500 MB | XML parser |

### 8.2 Data Lifecycle

```
Upload → Parse → Analyze → Display → Export → Delete
   │                                           │
   └───────────────────────────────────────────┘
                  Ephemeral
              (No persistent storage)
```

**Data retention:**
- Session-based only
- Deleted after PDF export or session end
- No server-side storage
- No user accounts or history

### 8.3 File Comparison

**Baseline comparison workflow:**
1. User uploads "baseline" PML (known-good state)
2. User uploads "current" PML (suspected infection)
3. System identifies:
   - New processes (in current, not in baseline)
   - Missing processes (in baseline, not in current)
   - Changed behavior (same process, different activity)

---

## 9. API Specification

### 9.1 REST Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/analyze` | Upload and analyze PML file |
| GET | `/api/v1/analysis/{id}` | Get analysis results |
| GET | `/api/v1/analysis/{id}/processes` | Get process list |
| GET | `/api/v1/analysis/{id}/tree` | Get process tree |
| GET | `/api/v1/analysis/{id}/timeline` | Get timeline data |
| GET | `/api/v1/analysis/{id}/export/pdf` | Export PDF report |
| POST | `/api/v1/compare` | Compare two PML files |
| GET | `/api/v1/rules` | Get detection rules |
| POST | `/api/v1/rules` | Add custom rule |
| DELETE | `/api/v1/rules/{id}` | Delete custom rule |

### 9.2 Request/Response Examples

**POST /api/v1/analyze**
```json
// Request: multipart/form-data with file

// Response:
{
  "analysis_id": "abc123",
  "status": "processing",
  "estimated_time_seconds": 45
}
```

**GET /api/v1/analysis/{id}**
```json
{
  "analysis_id": "abc123",
  "status": "complete",
  "summary": {
    "total_events": 53429,
    "unique_processes": 132,
    "high_risk": 5,
    "medium_risk": 12,
    "low_risk": 115
  },
  "findings": [
    {
      "process_name": "suspicious.exe",
      "process_path": "C:\\Users\\user\\AppData\\Local\\Temp\\suspicious.exe",
      "legitimacy": "MALICIOUS",
      "risk_score": 92,
      "reasoning": "Executable running from Temp folder, spawned by Word, accessing LSASS",
      "behavior_tags": ["execution", "credential_access", "persistence"],
      "mitre_techniques": ["T1059.001", "T1003.001", "T1547.001"],
      "parent_process": "WINWORD.EXE",
      "child_processes": ["cmd.exe", "powershell.exe"]
    }
  ]
}
```

---

## 10. Testing Strategy

### 10.1 Test Categories

| Category | Coverage | Tools |
|----------|----------|-------|
| **Unit Tests** | 80%+ | Go testing, Jest |
| **Integration Tests** | API endpoints | Go testing |
| **E2E Tests** | User workflows | Playwright |
| **Performance Tests** | Large file handling | Custom benchmarks |
| **Security Tests** | File upload, injection | OWASP ZAP |

### 10.2 Test Data

| Test File | Description | Purpose |
|-----------|-------------|---------|
| clean_system.pml | Normal Windows activity | Baseline testing |
| malware_sample.pml | Known malware activity | Detection testing |
| large_file.pml | 500MB file | Performance testing |
| edge_cases.pml | Unusual but valid events | Parser testing |

### 10.3 CI/CD Pipeline

```yaml
# .github/workflows/ci.yml
stages:
  - lint
  - test
  - build
  - security-scan
  - deploy-staging
  - e2e-tests
  - deploy-production
```

---

## 11. Deployment

### 11.1 Container Architecture

```dockerfile
# Multi-stage build
FROM golang:1.21 AS backend
WORKDIR /app
COPY backend/ .
RUN go build -o procbench

FROM node:20 AS frontend
WORKDIR /app
COPY frontend/ .
RUN npm ci && npm run build

FROM alpine:latest
COPY --from=backend /app/procbench /app/
COPY --from=frontend /app/build /app/static/
EXPOSE 8080
CMD ["/app/procbench"]
```

### 11.2 Environment Configuration

```env
# Server
PORT=8080
HOST=0.0.0.0
ENVIRONMENT=production

# AI
AI_PROVIDER=openai
AI_BASE_URL=https://api.example.com/v1
AI_API_KEY=sk-xxx
AI_MODEL=gpt-4
AI_RATE_LIMIT_REQUESTS=10

# Limits
MAX_FILE_SIZE_MB=500
MAX_CONCURRENT_ANALYSES=10

# Logging
LOG_LEVEL=info
LOG_FORMAT=json
```

---

## 12. Future Roadmap

### 12.1 Version 2.0 (Planned Features)

#### Live Threat Intelligence Integration

| Source | Integration Type | Data |
|--------|------------------|------|
| VirusTotal | API | Hash lookups |
| Abuse.ch | Feed sync | Known malicious hashes |
| MISP | STIX/TAXII | IOC feeds |
| AlienVault OTX | API | Pulse data |

**Architecture:**
```
┌─────────────────────────────────────────────────────────────────────────┐
│                    Threat Intelligence Module (v2)                       │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐    │
│  │  Intel Cache    │    │  Feed Syncer    │    │  Lookup Service │    │
│  │  (Redis/Memory) │◀───│  (Daily/Hourly) │    │  (On-demand)    │    │
│  └─────────────────┘    └─────────────────┘    └─────────────────┘    │
│           │                      ▲                      │              │
│           │                      │                      │              │
│           ▼                      │                      ▼              │
│  ┌─────────────────────────────────────────────────────────────────┐  │
│  │                     External Sources                             │  │
│  │  VirusTotal │ Abuse.ch │ MISP │ OTX │ Custom Feeds              │  │
│  └─────────────────────────────────────────────────────────────────┘  │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

#### Splunk Integration (Documented for v2)

**Integration method:** HTTP Event Collector (HEC)

**Configuration:**
```env
SPLUNK_ENABLED=true
SPLUNK_HEC_URL=https://splunk.example.com:8088
SPLUNK_HEC_TOKEN=xxx
SPLUNK_INDEX=procbench
SPLUNK_SOURCETYPE=procbench:analysis
```

**Payload sent to Splunk:**
```json
{
  "time": 1706745600,
  "source": "procbench",
  "sourcetype": "procbench:analysis",
  "event": {
    "analysis_id": "abc123",
    "file_name": "Logfile.PML",
    "analyst": "uploaded_by@example.com",
    "summary": {
      "total_events": 53429,
      "high_risk_count": 5,
      "medium_risk_count": 12
    },
    "findings": [
      {
        "process": "suspicious.exe",
        "risk_score": 85,
        "legitimacy": "MALICIOUS",
        "behavior_tags": ["persistence", "credential_access"],
        "mitre_techniques": ["T1547", "T1003"]
      }
    ]
  }
}
```

**When triggered:**
- On analysis completion
- When high-risk findings detected
- On PDF export

### 12.2 Version 3.0+ Ideas

| Feature | Description |
|---------|-------------|
| Real-time streaming | Analyze PML as it's being captured |
| Agent integration | Direct Procmon control from ProcBench |
| Team collaboration | Shared workspaces, comments, assignments |
| ML model training | Learn from analyst feedback |
| Automated remediation | Integration with EDR for response |

---

## Appendices

### Appendix A: Glossary

| Term | Definition |
|------|------------|
| **PML** | Process Monitor Log, native binary format from Sysinternals |
| **LOLBAS** | Living Off The Land Binaries And Scripts |
| **MITRE ATT&CK** | Knowledge base of adversary tactics and techniques |
| **IOC** | Indicator of Compromise |
| **EDR** | Endpoint Detection and Response |
| **SIEM** | Security Information and Event Management |
| **SOAR** | Security Orchestration, Automation, and Response |

### Appendix B: File Size Reference

| Capture Duration | Typical Events | Typical Size |
|------------------|----------------|--------------|
| 1 minute | 5,000-20,000 | 5-20 MB |
| 5 minutes | 50,000-100,000 | 30-100 MB |
| 30 minutes | 300,000-500,000 | 200-500 MB |
| 1 hour | 500,000-1,000,000 | 500 MB-1 GB |

### Appendix C: MITRE ATT&CK Techniques Mapped

| Technique ID | Name | Detection Method |
|--------------|------|------------------|
| T1059.001 | PowerShell | Process monitoring |
| T1059.003 | Windows Command Shell | Process monitoring |
| T1547.001 | Registry Run Keys | Registry access |
| T1003.001 | LSASS Memory | File access to lsass.exe |
| T1055 | Process Injection | Stack trace analysis |
| T1070.004 | File Deletion | File operation monitoring |
| T1105 | Ingress Tool Transfer | Network + file creation |

---

## Document Approval

| Role | Name | Date | Signature |
|------|------|------|-----------|
| Project Owner | | | |
| Technical Lead | | | |
| Security Review | | | |

---

*End of Document*
