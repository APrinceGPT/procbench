# ProcBench

> **"Turn Process Noise into Threat Signal"**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python)](https://python.org)
[![Svelte](https://img.shields.io/badge/Svelte-5.0+-FF3E00?logo=svelte)](https://svelte.dev)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind-4.0+-06B6D4?logo=tailwindcss)](https://tailwindcss.com)

---

## 🎯 What is ProcBench?

**ProcBench** is an AI-powered Process Monitor log analysis platform designed for SOC analysts and incident responders. It transforms raw PML files into actionable threat intelligence through:

- 🌳 **Process Tree Visualization** - See parent-child relationships at a glance
- 🤖 **AI-Powered Legitimacy Assessment** - Every process analyzed and scored
- 🏷️ **Behavioral Tagging** - Automatic tagging with MITRE ATT&CK mapping
- 📊 **Interactive Visualizations** - Timelines, treemaps, and heatmaps
- 📋 **Guided Investigation** - Step-by-step workflow for all skill levels
- 📄 **PDF Reports** - Export findings for documentation

---

## 🚀 Quick Start

### Using Docker (Recommended)

```bash
docker run -p 8000:8000 ghcr.io/yourusername/procbench:latest
```

Open http://localhost:8000 in your browser.

### From Source

```bash
# Clone repository
git clone https://github.com/yourusername/procbench.git
cd procbench

# Backend
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000

# Frontend (separate terminal)
cd frontend
npm install
npm run dev
```

---

## 📸 Screenshots

### Dashboard View
*Summary of analysis with risk breakdown and key findings*

### Process Tree
*Interactive parent-child process visualization*

### Timeline View
*Chronological view of anomalous events*

### PDF Export
*Print-ready analysis report*

---

## ✨ Modern UI Design System

ProcBench features a modern glass morphism design with:

### Design Tokens
- **Centralized theming** via TypeScript design tokens
- **Consistent color palette** with risk-level coding (red/orange/yellow/green)
- **Gradient accents** (blue to purple) for branding
- **Glass morphism surfaces** with backdrop blur effects

### UI Components
| Component | Description |
|-----------|-------------|
| `GlassCard` | Elevated glass panels with hover states |
| `Button` | Primary/secondary/ghost/danger variants with loading state |
| `Badge` | Risk level and status indicators |
| `SearchInput` | Modern search with icon and clear button |
| `Skeleton` | Loading placeholders with shimmer animation |
| `RiskGauge` | SVG semicircular gauge with glow effects |

### Animations
- **Entrance animations** with staggered delays
- **Hover interactions** with scale/translate transforms
- **Glow effects** on focus and hover
- **Smooth transitions** (150-300ms)

### Tech Stack
- **Svelte 5** with runes mode (`$state`, `$derived`, `$props`)
- **SvelteKit 2** for routing and SSR
- **Tailwind CSS 4** for utility classes
- **TypeScript** for type safety

---

## 🔧 Features

### For SOC Analyst L1 (Triage)
- ✅ Clear LEGITIMATE / SUSPICIOUS / MALICIOUS verdicts
- ✅ Risk scores (0-100) for quick prioritization
- ✅ Guided investigation workflow
- ✅ Action recommendations

### For SOC Analyst L2 (Investigation)
- ✅ Detailed process trees with relationships
- ✅ Timeline of events with filtering
- ✅ Behavioral tags with explanations
- ✅ File/Registry access patterns

### For SOC Analyst L3 (Hunting)
- ✅ Raw event data access
- ✅ Custom detection rules
- ✅ Baseline comparison
- ✅ Advanced filtering

---

## 📁 Supported File Formats

| Format | Extension | Notes |
|--------|-----------|-------|
| Process Monitor Log | `.pml` | Native binary format (recommended) |
| CSV Export | `.csv` | Process Monitor CSV export |
| XML Export | `.xml` | Process Monitor XML export |

**Maximum file size:** 500 MB

---

## 🛡️ Detection Capabilities

### Built-in Detection Rules

| Category | Examples |
|----------|----------|
| **LOLBAS** | cmd.exe, powershell.exe, certutil.exe abuse |
| **Suspicious Paths** | Executables in Temp, Downloads, AppData |
| **Parent-Child Anomalies** | Word → PowerShell, Explorer → cmd.exe |
| **Persistence** | Registry Run keys, Scheduled Tasks |
| **Credential Access** | LSASS memory access, SAM registry |

### Custom Rules

Create your own detection rules in YAML:

```yaml
rules:
  - id: my_custom_rule
    name: "Detect MyApp Abuse"
    severity: HIGH
    conditions:
      parent_process: "myapp.exe"
      child_process: "powershell.exe"
    tags: ["custom", "myapp"]
```

---

## 🤖 AI Integration

ProcBench uses AI to provide:
- **Legitimacy Assessment** - Is this process legitimate or suspicious?
- **Risk Scoring** - 0-100 based on behavior analysis
- **Reasoning** - Explanation of why the AI flagged a process
- **Behavioral Tags** - Automatic categorization

### Supported AI Providers

| Provider | Status |
|----------|--------|
| OpenAI-compatible APIs | ✅ Supported |
| Azure OpenAI | ✅ Supported |
| Custom endpoints | ✅ Supported |

Configure via environment variables:

```env
AI_PROVIDER=openai
AI_BASE_URL=https://api.openai.com/v1
AI_API_KEY=sk-xxx
AI_MODEL=gpt-4
```

---

## ⚙️ Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `PORT` | Server port | `8000` |
| `MAX_FILE_SIZE_MB` | Maximum upload size | `500` |
| `AI_PROVIDER` | AI provider type | `openai` |
| `AI_BASE_URL` | AI API endpoint | - |
| `AI_API_KEY` | AI API key | - |
| `AI_MODEL` | Model to use | `gpt-4` |
| `AI_RATE_LIMIT_REQUESTS` | Requests per minute | `10` |

See [`.env.example`](.env.example) for full configuration.

---

## 📊 Architecture

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   Svelte 5 UI   │────▶│ Python Backend  │────▶│    AI API       │
│   (Browser)     │     │    (FastAPI)    │     │   (External)    │
└─────────────────┘     └─────────────────┘     └─────────────────┘
        │                       │
        │                ┌──────┴──────┐
   Glass Design          │             │
   System (CSS)    ┌─────────┐   ┌─────────┐
                   │ Parser  │   │Detection│
                   │PML/CSV  │   │ Engine  │
                   └─────────┘   └─────────┘
```

### Frontend Structure
```
frontend/src/
├── lib/
│   ├── styles/
│   │   ├── design-tokens.ts   # Centralized design values
│   │   └── glass.css          # Glass morphism utilities
│   ├── components/
│   │   ├── ui/                # Reusable UI components
│   │   ├── findings/          # Finding cards and lists
│   │   ├── navigation/        # Sidebar, TopNav
│   │   ├── upload/            # File upload dropzone
│   │   └── visualization/     # RiskGauge, charts
│   ├── stores/                # Svelte stores
│   └── api/                   # API client
└── routes/                    # SvelteKit pages
```

---

## 🧪 Testing

```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm run test

# E2E tests
npm run test:e2e
```

---

## 📖 Documentation

- [Project Specification](docs/PROJECT_SPECIFICATION.md) - Full technical specification
- [Project Structure](docs/PROJECT_STRUCTURE.md) - Repository organization
- [API Documentation](docs/API.md) - REST API reference
- [Detection Rules Guide](docs/DETECTION_RULES.md) - How to write custom rules
- [Deployment Guide](docs/DEPLOYMENT.md) - Production deployment

---

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](docs/CONTRIBUTING.md) for guidelines.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- [Sysinternals](https://learn.microsoft.com/en-us/sysinternals/) - Process Monitor
- [LOLBAS Project](https://lolbas-project.github.io/) - Living Off The Land Binaries
- [MITRE ATT&CK](https://attack.mitre.org/) - Adversary tactics and techniques
- [Sigma](https://github.com/SigmaHQ/sigma) - Generic signature format

---

## 📞 Support

- 📧 Email: support@procbench.io
- 🐛 Issues: [GitHub Issues](https://github.com/yourusername/procbench/issues)
- 💬 Discussions: [GitHub Discussions](https://github.com/yourusername/procbench/discussions)

---

<p align="center">
  <strong>ProcBench</strong> - Turn Process Noise into Threat Signal
</p>
