# 🏁 APEX-RACE-AI

### Real-Time Motorsport Data & AI Engineering Platform

[![APEX-RACE-AI CI](https://github.com/ABHILATTHE6/APEX-RACE-AI/actions/workflows/ci.yml/badge.svg)](https://github.com/ABHILATTHE6/APEX-RACE-AI/actions/workflows/ci.yml)
![Python](https://img.shields.io/badge/Python-3.14-3776AB?logo=python&logoColor=white)
![FastF1](https://img.shields.io/badge/FastF1-3.8.3-111827)
![Streamlit](https://img.shields.io/badge/Streamlit-1.64.0-FF4B4B?logo=streamlit&logoColor=white)
![License](https://img.shields.io/badge/license-TBD-lightgrey)

APEX-RACE-AI is a modular motorsport data platform that turns telemetry into an engineering workflow:

**ingest → normalize → validate → process → visualize → model → act**

The project combines historical motorsport data engineering, an interactive Pit Wall dashboard, data-quality controls and an architecture ready for live streaming and AI/ML services.

---

## 🧭 Project Index

| Area | Link | What you will find |
|---|---|---|
| 🚀 Start | [Quick project overview](docs/project-overview.md) | Purpose, objectives, scope, lifecycle and success criteria |
| 📚 Docs | [Documentation index](docs/INDEX.md) | Central map of the repository documentation |
| 🏎️ UI | [Pit Wall dashboard](dashboard/README.md) | Dashboard features and launch guide |
| 🧱 Architecture | [System architecture](docs/architecture/system-architecture.md) | Components, data flow and future runtime |
| 📐 Data | [Telemetry data dictionary](docs/data-dictionary.md) | Fields, units, ranges and validation semantics |
| 🗺️ Plan | [Engineering roadmap](docs/roadmap.md) | Delivered work and future phases |
| 🤝 Development | [Contributing guide](CONTRIBUTING.md) | Branching, coding, testing and PR workflow |

---

## ⚡ At a glance

**Current state:** historical telemetry engineering platform + interactive Pit Wall cockpit

**Primary sources:** FastF1 and OpenF1

**Primary language:** Python

**Processing:** pandas + numpy

**Visualization:** Streamlit

**Quality:** normalized schema + telemetry validator

**Automation:** GitHub Actions

**Future target:** live race operations + strategy analytics + AI/ML

---

## 🎯 What problem does APEX-RACE-AI solve?

Motorsport telemetry can contain thousands of measurements per lap, but raw numbers are only useful when they are reliable, structured and converted into interpretable engineering signals.

APEX-RACE-AI is built to demonstrate that entire path.

### Input

Historical telemetry, session metadata and future live event streams.

### Engineering layer

Ingestion, source adaptation, caching, normalization, validation and reusable feature calculations.

### Output

A visual Pit Wall with KPIs, telemetry traces, driver deltas and data-quality state.

### Future output

Live timing, race-control events, strategy simulations, anomaly alerts and predictive models.

---

## 🏎️ Core capabilities

### 1. FastF1 historical ingestion

The FastF1 adapter currently supports:

- historical session loading
- driver selection
- fastest-lap extraction
- car telemetry extraction
- distance enrichment
- CSV persistence
- local FastF1 caching

### 2. OpenF1 ingestion

The OpenF1 adapter provides DataFrame-oriented access to:

- sessions
- driver metadata
- car telemetry
- position data
- location data

### 3. Telemetry data contract

The normalized contract currently centers on:

| Field | Meaning | Unit |
|---|---|---|
| Distance | Position along lap trace | metres |
| Speed | Vehicle speed | km/h |
| Throttle | Throttle position | % |
| Brake | Brake application | % |
| RPM | Engine speed | rpm |
| Gear | Selected gear | 0–8 |
| DRS | Normalized DRS state | binary |

Optional context includes Driver, X and Y.

Full definitions are in [docs/data-dictionary.md](docs/data-dictionary.md).

### 4. Data quality

Telemetry can be checked for:

- missing required fields
- malformed numeric values
- invalid ranges
- null/missing values
- duplicate distance samples
- file-based quality reporting

### 5. Processing

Current reusable analytics include:

- top speed
- average speed
- peak RPM
- peak braking
- average throttle
- distance-aligned driver speed delta
- equal-distance sector summary

### 6. APEX Pit Wall

The UI includes:

- Mission Control sidebar
- offline demonstration telemetry
- FastF1 session mode
- telemetry KPI wall
- speed chart
- throttle chart
- brake chart
- RPM chart
- gear chart
- track trace
- driver delta view
- data-quality panel
- raw telemetry table
- CSV export

---

## 🎨 Visual identity

The Pit Wall is intentionally designed as an engineering cockpit rather than a generic analytics dashboard.

### Design language

- deep graphite background
- red signal accents
- compact information hierarchy
- large numerical KPIs
- small source/status chips
- engineering terminology
- low-noise layout
- clear separation between data, analysis and operations

The visual identity is represented by the custom APEX-RACE mark in dashboard/assets/apex-mark.svg.

---

## 🧠 System architecture

    ┌────────────────────────────────────────────┐
    │                 DATA SOURCES               │
    │ FastF1 • OpenF1 • future UDP/live streams │
    └──────────────────────┬─────────────────────┘
                           ▼
    ┌────────────────────────────────────────────┐
    │                  INGESTION                 │
    │ adapters • caching • metadata • retries   │
    └──────────────────────┬─────────────────────┘
                           ▼
    ┌────────────────────────────────────────────┐
    │                 RAW DATA                   │
    │ CSV / Parquet / immutable future events   │
    └──────────────────────┬─────────────────────┘
                           ▼
    ┌────────────────────────────────────────────┐
    │              NORMALIZATION                 │
    │ source fields → common telemetry contract │
    └──────────────────────┬─────────────────────┘
                           ▼
    ┌────────────────────────────────────────────┐
    │               VALIDATION                   │
    │ schema • ranges • nulls • duplicates      │
    └──────────────────────┬─────────────────────┘
                           ▼
    ┌────────────────────────────────────────────┐
    │            PROCESSING / FEATURES           │
    │ KPI • delta • sectors • future stints     │
    └───────────────┬───────────────────┬────────┘
                    ▼                   ▼
             ┌──────────────┐    ┌──────────────┐
             │  APEX        │    │   AI / ML    │
             │  PIT WALL    │    │   SERVICES   │
             └──────┬───────┘    └──────┬───────┘
                    └──────────┬─────────┘
                               ▼
                    ENGINEERING INSIGHT

Detailed architecture: [docs/architecture/system-architecture.md](docs/architecture/system-architecture.md)

---

## 📂 Repository structure

    APEX-RACE-AI/
    │
    ├── .github/
    │   └── workflows/
    │       └── ci.yml                  # CI checks
    │
    ├── .streamlit/
    │   └── config.toml                # Pit Wall theme configuration
    │
    ├── dashboard/
    │   ├── app.py                     # Main Streamlit application
    │   ├── README.md                  # Dashboard guide
    │   └── assets/
    │       └── apex-mark.svg          # Project visual identity
    │
    ├── data/
    │   ├── raw/                       # Local/generated telemetry
    │   ├── samples/                   # Small reproducible fixtures
    │   └── schemas/
    │       └── telemetry_schema.json  # Normalized data contract
    │
    ├── docs/
    │   ├── INDEX.md
    │   ├── project-overview.md
    │   ├── data-dictionary.md
    │   ├── roadmap.md
    │   └── architecture/
    │       └── system-architecture.md
    │
    ├── ingestion/
    │   ├── fastf1/
    │   │   └── telemetry_ingestion.py
    │   └── openf1/
    │       └── telemetry_ingestion.py
    │
    ├── processing/
    │   ├── telemetry_metrics.py
    │   └── validation/
    │       └── telemetry_validator.py
    │
    ├── .env.example                  # Runtime configuration template
    ├── .gitignore                    # Local/generated data exclusions
    ├── CONTRIBUTING.md               # Development workflow
    ├── README.md                     # Project entry point
    └── requirements.txt              # Python dependencies

---

## 🛠️ Technology stack

| Technology | Role |
|---|---|
| Python 3.14 | Primary implementation language |
| FastF1 3.8.3 | Historical F1 session and telemetry access |
| OpenF1 | Session and telemetry API integration |
| pandas 2.3.3 | Tabular telemetry processing |
| numpy 2.5.3 | Numerical processing and demo signal generation |
| Streamlit 1.64.0 | Interactive Pit Wall |
| Matplotlib | Supporting visualization ecosystem |
| GitHub Actions | CI automation |
| Git | Source control |

---

## 🚀 Quick start

### Windows

Create and activate a virtual environment:

    python -m venv .venv
    .venv\Scripts\activate
    python -m pip install --upgrade pip
    pip install -r requirements.txt

Launch:

    streamlit run dashboard/app.py

Then select:

**Demo telemetry → choose driver → explore the Pit Wall**

Demo mode is designed to work without an external telemetry service.

### FastF1 mode

Switch the sidebar to:

**FastF1 session**

Then select:

- season
- Grand Prix
- session
- driver code

The adapter loads the requested historical session and prepares normalized telemetry for the dashboard.

---

## 🧪 Validation and CI

Run the same basic Python syntax check used by CI:

    python -m compileall dashboard ingestion processing

GitHub Actions currently checks:

1. Python module compilation.
2. Analytics/validation smoke behavior.

The repository uses CI so data-processing changes can be checked before being merged.

---

## 🔐 Data and secrets

Never commit:

- .env files
- API tokens
- passwords
- private credentials
- large generated telemetry dumps
- private datasets

Use .env.example for non-secret configuration names.

Generated raw CSV and Parquet telemetry is intentionally excluded from version control.

---

## 🧩 Design principles

### Separation of concerns

Source adapters, processing logic, validation and presentation are independent layers.

### Contract first

Downstream code should rely on the normalized telemetry contract rather than source-specific field names.

### Reproducible demos

An offline synthetic telemetry path makes the interface demonstrable even when APIs are unavailable.

### Data lineage

Future production datasets should retain source, event, session, driver, lap, schema-version and processing-version metadata.

### Incremental complexity

The project grows in controlled phases instead of introducing live streaming, databases and ML as hard dependencies on day one.

---

## 🗺️ Delivery roadmap

### Phase 1 — Data foundation ✅

- [x] FastF1 ingestion
- [x] FastF1 caching
- [x] OpenF1 client
- [x] Telemetry schema
- [x] Validation layer
- [x] Processing layer

### Phase 2 — Pit Wall ✅

- [x] Dark engineering UI
- [x] APEX-RACE identity
- [x] KPI wall
- [x] Telemetry views
- [x] Driver delta
- [x] Data-quality view
- [x] Raw telemetry export
- [x] Offline demo mode

### Phase 3 — Live race operations 🔜

- [ ] Live OpenF1 integration
- [ ] UDP telemetry gateway
- [ ] live timing tower
- [ ] live track visualization
- [ ] sector gaps
- [ ] race-control events
- [ ] engineer alert queue

### Phase 4 — Strategy 🔜

- [ ] tire/stint analytics
- [ ] degradation curves
- [ ] fuel-adjusted pace
- [ ] pit-window calculator
- [ ] undercut/overcut scenarios
- [ ] strategy comparison

### Phase 5 — AI/ML 🔜

- [ ] anomaly detection
- [ ] lap-time prediction
- [ ] tire degradation forecasting
- [ ] driver clustering
- [ ] pace classification
- [ ] strategy scoring
- [ ] experiment tracking
- [ ] model registry

### Phase 6 — Production platform 🔜

- [ ] PostgreSQL / analytical warehouse
- [ ] object storage
- [ ] containerized services
- [ ] API layer
- [ ] cloud deployment
- [ ] observability
- [ ] end-to-end integration tests

Full roadmap: [docs/roadmap.md](docs/roadmap.md)

---

## 📊 Example engineering workflow

    01  SELECT SESSION
          ↓
    02  LOAD TELEMETRY
          ↓
    03  NORMALIZE FIELDS
          ↓
    04  RUN QUALITY GATE
          ↓
    05  CALCULATE FEATURES
          ↓
    06  VISUALIZE TRACE
          ↓
    07  COMPARE DRIVERS
          ↓
    08  GENERATE ENGINEERING INSIGHT
          ↓
    09  FEED FUTURE AI / STRATEGY LAYERS

---

## 📡 Data-source notes

FastF1 is used for historical session loading and telemetry extraction.

OpenF1 provides motorsport timing and telemetry API access. Consult the official documentation for endpoint behavior, availability, limits and subscription requirements:

https://openf1.org/docs/

---

## 🧑‍💻 Development workflow

The recommended workflow is:

    main
      │
      ├── feature/*
      ├── fix/*
      └── docs/*
            │
            ▼
       Pull Request
            │
            ▼
        GitHub CI
            │
            ▼
       Review / merge

See [CONTRIBUTING.md](CONTRIBUTING.md) for the repository workflow.

---

## 📌 Project status

**Current milestone:** Pit Wall foundation

**Repository direction:** historical telemetry → live race engineering platform

**Documentation maturity:** project hub + architecture + data contract + roadmap

**Current CI:** GitHub Actions syntax and smoke validation

**Next engineering focus:** live race operations, real circuit visualization, sector analytics and strategy features

---

## 🏁 End-state vision

APEX-RACE-AI is intended to become a complete motorsport data-engineering platform where:

**raw telemetry** becomes **trusted data**, trusted data becomes **features**, features become **models**, and models become **engineering insight**.

The long-term system should be capable of supporting historical analysis, live race monitoring, telemetry intelligence, strategy simulation and AI-assisted motorsport analytics while keeping the underlying data pipeline observable and reproducible.

---

## 📚 Documentation

Start with the [Documentation Index](docs/INDEX.md) or go directly to the [Project Overview](docs/project-overview.md).
