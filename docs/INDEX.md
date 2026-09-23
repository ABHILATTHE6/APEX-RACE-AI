# 📚 APEX-RACE-AI Documentation Index

Welcome to the documentation hub for APEX-RACE-AI — Real-Time Motorsport Data & AI Engineering Platform.

## 01 — Start here

| Document | Purpose |
|---|---|
| Project README | Product summary, features, stack, architecture, setup and roadmap |
| Pit Wall Dashboard | Dashboard behavior, UI design and launch instructions |
| Project Overview | Detailed project definition, objectives, scope and engineering responsibilities |
| System Architecture | End-to-end architecture and component boundaries |
| Data Dictionary | Normalized telemetry fields, units, ranges and semantics |
| Roadmap | Delivery phases and planned engineering modules |
| Contributing | Branching, coding and pull-request workflow |

Links:
- [Project README](../README.md)
- [Pit Wall Dashboard](../dashboard/README.md)
- [Project Overview](project-overview.md)
- [System Architecture](architecture/system-architecture.md)
- [Data Dictionary](data-dictionary.md)
- [Roadmap](roadmap.md)
- [Contributing](../CONTRIBUTING.md)

## 02 — Platform map

    DATA SOURCES
       │
       ├── FastF1 historical sessions
       ├── OpenF1 REST
       └── Future UDP / live streams
       │
       ▼
    INGESTION
       │
       ▼
    RAW DATA ZONE
       │
       ▼
    VALIDATION / DATA CONTRACT
       │
       ▼
    PROCESSING / FEATURES
       │
       ├──────────────┐
       ▼              ▼
    PIT WALL        AI / ML
    DASHBOARD       SERVICES
       │              │
       └──────┬───────┘
              ▼
       ENGINEERING INSIGHT

## 03 — Source code map

### Dashboard
- dashboard/app.py — Streamlit application shell and telemetry cockpit.
- dashboard/assets/apex-mark.svg — visual identity mark.

### Ingestion
- ingestion/fastf1/telemetry_ingestion.py — historical FastF1 session loading and fastest-lap telemetry extraction.
- ingestion/openf1/telemetry_ingestion.py — OpenF1 REST adapters.

### Processing
- processing/telemetry_metrics.py — telemetry KPI, driver delta and sector analytics.
- processing/validation/telemetry_validator.py — telemetry quality checks.

### Data
- data/schemas/telemetry_schema.json — normalized telemetry contract.
- data/samples/ — safe-to-commit sample datasets.
- data/raw/ — local downloads and generated data.

## 04 — Operational entry points

Launch the UI:

    pip install -r requirements.txt
    streamlit run dashboard/app.py

Run syntax checks:

    python -m compileall dashboard ingestion processing

## 05 — Engineering contract

The normalized downstream contract currently centers on:

- Distance
- Speed
- Throttle
- Brake
- RPM
- Gear
- DRS

Optional context fields:

- Driver
- X
- Y

## 06 — Future documentation

As the platform grows, this index will also host:

- live-stream protocol documentation
- database and warehouse schema
- ETL/ELT job specifications
- feature engineering definitions
- ML experiment reports
- model cards
- strategy simulator design
- deployment/runbooks
