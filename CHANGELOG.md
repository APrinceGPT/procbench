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

## [1.2.0] - 2026-02-01

### Added
- **Interactive Visualizations (Phase 2)**
  - **vis-network Process Graph**
    - Interactive network graph visualization of process relationships
    - Zoom, pan, and physics-based layout
    - Click-to-select nodes for details
    - Search and filter controls (All / Flagged / High Risk)
    - Node size scales with event count and risk score
    - Color-coded nodes by risk level (high=red, medium=orange, low=yellow)
    - Legend and node/edge count statistics
  - **Process Details Panel**
    - Slide-out panel showing selected process details
    - Risk score display with color-coded badge
    - Legitimacy indicator (legitimate/suspicious/malicious)
    - Image path and event count information
    - Behavior tags display
    - Quick action buttons (View Details, Copy Info)
  - **Chart.js Timeline Visualization**
    - Bar chart showing risk scores over time
    - Click-to-select events for details
    - Tooltips with process name, PID, and description
    - Color-coded bars by risk level
    - Responsive design with proper legends
  - **Timeline Entry Card**
    - Details card for selected timeline events
    - Anomaly indicator badge
    - Timestamp display
    - Event description

### Changed
- **Process Tree Page** (`/investigate/tree`)
  - Complete redesign with graph + details panel layout
  - Replaced text-based tree with vis-network graph
  - Added collapsible details panel
  - Modern page header with icon
  - Loading, error, and empty state handling

- **Timeline Page** (`/investigate/timeline`)
  - Complete redesign with chart + list dual view
  - Added view mode toggle (Chart / List)
  - Statistics header (Events, Anomalies, High Risk counts)
  - Filter controls bar
  - Chart.js bar chart for visual analysis
  - Redesigned list view with timeline styling
  - Entry details card panel

### Technical
- Added `graph-utils.ts` for vis-network data transformation
- Added Chart.js as dependency for timeline charts
- Copied vis-network library to static folder for browser access
- All components follow Svelte 5 runes pattern
- Fully typed with TypeScript

---

## [1.1.0] - 2026-02-01

### Added
- **Modern UI Design System (Phase 1)**
  - Centralized design tokens (`design-tokens.ts`) for colors, spacing, typography
  - Glass morphism CSS utilities (`glass.css`) with backdrop blur effects
  - New reusable UI components:
    - `GlassCard` - Elevated glass panels with variants (default/elevated/interactive/subtle)
    - `Button` - Modern buttons with variants (primary/secondary/ghost/danger) and loading state
    - `Badge` - Risk level and status indicators with glow effects
    - `SearchInput` - Search input with icon, clear button, and loading state
    - `Skeleton` - Loading placeholders with shimmer animation
  - Gradient accents (blue to purple) for branding
  - Color-coded risk levels (high=red, medium=orange, low=yellow, success=green)

### Changed
- **Svelte 5 Migration**
  - Updated all components to use Svelte 5 runes mode (`$state`, `$derived`, `$props`)
  - Replaced `$:` reactive statements with `$derived`
  - Updated event handlers to new syntax (`onclick` instead of `on:click`)

- **UI Modernization**
  - Redesigned Sidebar with glass morphism and gradient logo
  - Updated root layout with gradient background
  - Modernized upload page with glass cards and entrance animations
  - Enhanced dashboard with animated stats grid and color-coded cards
  - Improved `RiskGauge` with SVG glow effects and better needle design
  - Redesigned `FindingCard` and `FindingList` with glass styling and hover animations

### Fixed
- Tailwind CSS v4 compatibility issues with layout
- API port mismatch between frontend and backend (now 8000)
- Analysis ID cache synchronization issues
- ARIA role warnings for interactive elements

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
  - Python/FastAPI backend with REST API
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
