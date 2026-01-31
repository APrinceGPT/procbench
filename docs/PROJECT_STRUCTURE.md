# ProcBench - Project Structure

> **"Turn Process Noise into Threat Signal"**

---

## Repository Structure

```
procbench/
├── .github/
│   ├── workflows/
│   │   ├── ci.yml                 # CI pipeline
│   │   ├── release.yml            # Release automation
│   │   └── security.yml           # Security scanning
│   ├── ISSUE_TEMPLATE/
│   │   ├── bug_report.md
│   │   ├── feature_request.md
│   │   └── detection_rule.md
│   └── PULL_REQUEST_TEMPLATE.md
│
├── backend/                        # Python backend (FastAPI)
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                # Application entry point
│   │   ├── config.py              # Configuration management
│   │   │
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   ├── routes.py          # API route definitions
│   │   │   ├── dependencies.py    # Dependency injection
│   │   │   └── middleware.py      # CORS, logging, etc.
│   │   │
│   │   ├── parsers/
│   │   │   ├── __init__.py
│   │   │   ├── base.py            # Base parser interface
│   │   │   ├── pml_parser.py      # PML binary parser
│   │   │   ├── csv_parser.py      # CSV parser
│   │   │   └── xml_parser.py      # XML parser
│   │   │
│   │   ├── detection/
│   │   │   ├── __init__.py
│   │   │   ├── engine.py          # Detection engine
│   │   │   ├── rules.py           # Rule loading/matching
│   │   │   ├── lolbas.py          # LOLBAS detection
│   │   │   ├── suspicious.py      # Suspicious path detection
│   │   │   └── parent_child.py    # Parent-child anomalies
│   │   │
│   │   ├── ai/
│   │   │   ├── __init__.py
│   │   │   ├── client.py          # AI API client
│   │   │   ├── prompts.py         # Prompt templates
│   │   │   └── rate_limiter.py    # Rate limiting
│   │   │
│   │   ├── analysis/
│   │   │   ├── __init__.py
│   │   │   ├── analyzer.py        # Main analysis orchestrator
│   │   │   ├── process_tree.py    # Process tree builder
│   │   │   ├── timeline.py        # Timeline generator
│   │   │   └── comparison.py      # Baseline comparison
│   │   │
│   │   ├── report/
│   │   │   ├── __init__.py
│   │   │   ├── pdf_generator.py   # PDF generator
│   │   │   └── templates.py       # Report templates
│   │   │
│   │   └── models/
│   │       ├── __init__.py
│   │       ├── event.py           # Event structures
│   │       ├── process.py         # Process structures
│   │       ├── finding.py         # Finding structures
│   │       └── rule.py            # Rule structures
│   │
│   ├── rules/
│   │   ├── lolbas.yaml            # LOLBAS rules
│   │   ├── suspicious_paths.yaml
│   │   ├── parent_child.yaml
│   │   ├── persistence.yaml
│   │   └── credential_access.yaml
│   │
│   ├── tests/
│   │   ├── __init__.py
│   │   ├── test_parsers.py
│   │   ├── test_detection.py
│   │   ├── test_ai.py
│   │   └── test_api.py
│   │
│   ├── requirements.txt
│   └── pytest.ini
│
├── frontend/                       # Svelte frontend
│   ├── src/
│   │   ├── lib/
│   │   │   ├── components/
│   │   │   │   ├── common/
│   │   │   │   │   ├── Button.svelte
│   │   │   │   │   ├── Card.svelte
│   │   │   │   │   ├── Modal.svelte
│   │   │   │   │   ├── Tooltip.svelte
│   │   │   │   │   └── Badge.svelte
│   │   │   │   │
│   │   │   │   ├── upload/
│   │   │   │   │   ├── FileUpload.svelte
│   │   │   │   │   ├── DragDrop.svelte
│   │   │   │   │   └── ProgressBar.svelte
│   │   │   │   │
│   │   │   │   ├── visualization/
│   │   │   │   │   ├── ProcessTree.svelte
│   │   │   │   │   ├── Timeline.svelte
│   │   │   │   │   ├── Treemap.svelte
│   │   │   │   │   ├── RiskGauge.svelte
│   │   │   │   │   └── OperationChart.svelte
│   │   │   │   │
│   │   │   │   ├── findings/
│   │   │   │   │   ├── FindingCard.svelte
│   │   │   │   │   ├── FindingList.svelte
│   │   │   │   │   ├── ProcessDetail.svelte
│   │   │   │   │   └── BehaviorTag.svelte
│   │   │   │   │
│   │   │   │   ├── navigation/
│   │   │   │   │   ├── TopNav.svelte
│   │   │   │   │   ├── Sidebar.svelte
│   │   │   │   │   └── Breadcrumb.svelte
│   │   │   │   │
│   │   │   │   ├── guided/
│   │   │   │   │   ├── GuidedWizard.svelte
│   │   │   │   │   ├── StepIndicator.svelte
│   │   │   │   │   └── TipBox.svelte
│   │   │   │   │
│   │   │   │   ├── onboarding/
│   │   │   │   │   ├── WelcomeModal.svelte
│   │   │   │   │   ├── Tutorial.svelte
│   │   │   │   │   └── HelpTooltip.svelte
│   │   │   │   │
│   │   │   │   └── export/
│   │   │   │       ├── ExportButton.svelte
│   │   │   │       └── ExportPreview.svelte
│   │   │   │
│   │   │   ├── stores/
│   │   │   │   ├── analysis.ts    # Analysis state
│   │   │   │   ├── ui.ts          # UI state (theme, view mode)
│   │   │   │   ├── filters.ts     # Filter state
│   │   │   │   └── guided.ts      # Guided mode state
│   │   │   │
│   │   │   ├── api/
│   │   │   │   ├── client.ts      # API client
│   │   │   │   └── types.ts       # TypeScript types
│   │   │   │
│   │   │   └── utils/
│   │   │       ├── formatters.ts  # Data formatters
│   │   │       ├── colors.ts      # Color utilities
│   │   │       └── helpers.ts     # General helpers
│   │   │
│   │   ├── routes/
│   │   │   ├── +layout.svelte     # Root layout
│   │   │   ├── +page.svelte       # Home/Upload page
│   │   │   ├── dashboard/
│   │   │   │   └── +page.svelte   # Dashboard view
│   │   │   ├── investigate/
│   │   │   │   ├── +page.svelte   # Investigation view
│   │   │   │   ├── tree/
│   │   │   │   │   └── +page.svelte
│   │   │   │   ├── timeline/
│   │   │   │   │   └── +page.svelte
│   │   │   │   └── heatmap/
│   │   │   │       └── +page.svelte
│   │   │   ├── compare/
│   │   │   │   └── +page.svelte   # Comparison view
│   │   │   ├── rules/
│   │   │   │   └── +page.svelte   # Custom rules
│   │   │   └── help/
│   │   │       └── +page.svelte   # Help/documentation
│   │   │
│   │   ├── app.html
│   │   ├── app.css                # Global styles
│   │   └── app.d.ts
│   │
│   ├── static/
│   │   ├── favicon.ico
│   │   └── sample/
│   │       └── sample.pml         # Sample file for demo
│   │
│   ├── tests/
│   │   ├── unit/
│   │   └── e2e/
│   │
│   ├── package.json
│   ├── svelte.config.js
│   ├── tailwind.config.js
│   ├── vite.config.js
│   └── tsconfig.json
│
├── docs/
│   ├── PROJECT_SPECIFICATION.md   # This document
│   ├── PROJECT_STRUCTURE.md       # Project structure
│   ├── API.md                     # API documentation
│   ├── DETECTION_RULES.md         # Rule writing guide
│   ├── DEPLOYMENT.md              # Deployment guide
│   └── CONTRIBUTING.md            # Contribution guidelines
│
├── deploy/
│   ├── docker/
│   │   ├── Dockerfile             # Multi-stage build
│   │   └── docker-compose.yml     # Local development
│   ├── kubernetes/
│   │   ├── deployment.yaml
│   │   ├── service.yaml
│   │   └── ingress.yaml
│   └── terraform/                 # Infrastructure as code
│       └── main.tf
│
├── scripts/
│   ├── build.sh                   # Build script
│   ├── dev.sh                     # Development script
│   └── test.sh                    # Test runner
│
├── .env.example                   # Environment template
├── .gitignore
├── LICENSE                        # MIT License
├── README.md                      # Project README
└── CHANGELOG.md                   # Version history
```

---

## Directory Descriptions

### `/backend`

Python (FastAPI) backend application handling:
- PML/CSV/XML file parsing (using procmon-parser)
- Detection engine with YAML rule matching
- AI integration with rate limiting
- PDF report generation
- REST API

### `/frontend`

Svelte-based single-page application providing:
- File upload interface
- Interactive visualizations (D3.js powered)
- Guided investigation workflow
- Multi-skill level views (L1/L2/L3)

### `/docs`

Project documentation:
- Technical specifications
- API reference
- User guides
- Contribution guidelines

### `/deploy`

Deployment configurations:
- Docker containerization
- Kubernetes manifests
- Infrastructure as code (Terraform)

---

## Key Files

| File | Purpose |
|------|---------|
| `backend/app/main.py` | Application entry point |
| `backend/app/parsers/pml_parser.py` | Core PML parsing logic |
| `backend/app/detection/engine.py` | Rule-based detection |
| `backend/app/ai/client.py` | AI API integration |
| `frontend/src/routes/+page.svelte` | Main upload page |
| `frontend/src/lib/components/visualization/ProcessTree.svelte` | Process tree visualization |

---

## Development Commands

```bash
# Backend
cd backend
python -m venv venv         # Create virtual environment
source venv/bin/activate    # Activate (Linux/Mac)
venv\Scripts\activate       # Activate (Windows)
pip install -r requirements.txt  # Install dependencies
uvicorn app.main:app --reload    # Run development server
pytest                      # Run tests

# Frontend
cd frontend
npm install         # Install dependencies
npm run dev         # Development server
npm run build       # Production build
npm run test        # Run tests

# Docker
docker-compose up   # Run full stack locally
docker build -t procbench .  # Build container
```

---

## Environment Variables

See `.env.example` for full list:

```env
# Server
PORT=8000
ENVIRONMENT=development

# AI Configuration (OpenAI-compatible)
OPENAI_BASE_URL=https://api.rdsec.trendmicro.com/prod/aiendpoint/v1/
OPENAI_API_KEY=your-api-key
OPENAI_MODEL=claude-4-sonnet

# Rate Limiting
AI_RATE_LIMIT_REQUESTS=10
AI_BATCH_SIZE=15

# Limits
MAX_FILE_SIZE_MB=500
```
