# Changelog

All notable changes to ProcBench will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

### Planned for v2.0
- Splunk HEC integration
- Live threat intelligence lookups (VirusTotal, Abuse.ch)
- STIX/TAXII feed support
- Webhook notifications

---

## [1.0.0] - TBD

### Added
- **Core Features**
  - PML, CSV, XML file parsing
  - Process tree visualization with parent-child relationships
  - AI-powered legitimacy assessment (LEGITIMATE / SUSPICIOUS / MALICIOUS)
  - Risk scoring (0-100) per process
  - Behavioral tagging with reasoning
  - MITRE ATT&CK technique mapping (where applicable)

- **Detection Engine**
  - LOLBAS detection rules
  - Suspicious path detection
  - Parent-child anomaly detection
  - Persistence indicator detection
  - Credential access detection
  - Custom YAML-based rule support

- **Visualizations**
  - Interactive process tree (zoom, pan, filter)
  - Timeline view (anomalies only)
  - Treemap heatmaps for file/registry access
  - Operation frequency charts

- **User Experience**
  - Dark theme interface
  - Guided investigation workflow (6 steps)
  - Multi-skill level views (L1/L2/L3)
  - Filtering and search across all data
  - Executive summary section
  - Print-friendly PDF export

- **Baseline Comparison**
  - Upload two PML files for comparison
  - Highlight new processes
  - Show changed behaviors

- **Onboarding**
  - Welcome modal for first-time users
  - Interactive tutorial
  - Sample PML file for practice
  - Contextual tooltips

- **Technical**
  - Go backend with REST API
  - Svelte frontend
  - Configurable AI rate limiting
  - Docker containerization
  - Comprehensive test suite

### Security
- File upload validation
- Size limits (500 MB default)
- Ephemeral data handling (no persistent storage)
- CORS configuration

---

## [0.1.0] - 2026-01-31

### Added
- Initial proof of concept
- Basic PML parsing
- Simple rule-based detection
- HTML report generation

---

[Unreleased]: https://github.com/yourusername/procbench/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/yourusername/procbench/compare/v0.1.0...v1.0.0
[0.1.0]: https://github.com/yourusername/procbench/releases/tag/v0.1.0
