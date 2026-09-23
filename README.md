# 🏁 APEX-RACE-AI

### Real-Time Motorsport Data & AI Engineering Platform

APEX-RACE-AI is a modular motorsport data platform built around:

**ingest → validate → process → visualize → model → act**

The project is designed as a portfolio-grade data engineering system that can grow from historical telemetry analysis into live race operations tooling.

## Current platform

| Layer | Component | Status |
|---|---|---|
| Data source | FastF1 historical telemetry | ✅ |
| Data source | OpenF1 REST ingestion | ✅ |
| Data contract | Normalized telemetry schema | ✅ |
| Quality | Structural + range validation | ✅ |
| Analytics | Telemetry KPI / driver delta | ✅ |
| UI | Streamlit Pit Wall cockpit | ✅ |
| CI | Python compile + analytics smoke test | ✅ |
| Live UDP | Gateway adapter | 🔜 |
| ML | Anomaly / strategy signals | 🔜 |

## Architecture

    Motorsport sources
            │
            ▼
       INGESTION
   FastF1 / OpenF1 / UDP
            │
            ▼
        RAW DATA
       CSV / Parquet
            │
            ▼
        VALIDATION
    schema + range checks
            │
            ▼
    PROCESSING / METRICS
      KPI • delta • sectors
         │          │
         ▼          ▼
     PIT WALL     AI / ML
      Streamlit   services
         │          │
         └────┬─────┘
              ▼
      ENGINEERING INSIGHT

## Repository layout

    APEX-RACE-AI/
    ├── dashboard/                    # Interactive engineering cockpit
    │   ├── app.py
    │   ├── README.md
    │   └── assets/apex-mark.svg
    ├── ingestion/
    │   ├── fastf1/telemetry_ingestion.py
    │   └── openf1/telemetry_ingestion.py
    ├── processing/
    │   ├── telemetry_metrics.py
    │   └── validation/telemetry_validator.py
    ├── data/
    │   ├── raw/                      # Local downloaded telemetry
    │   ├── samples/
    │   └── schemas/telemetry_schema.json
    ├── docs/architecture/system-architecture.md
    ├── .github/workflows/ci.yml
    └── requirements.txt

## Run locally

### 1. Create an environment

    python -m venv .venv
    .venv\Scripts\activate
    pip install -r requirements.txt

### 2. Launch the cockpit

    streamlit run dashboard/app.py

Start with **Demo telemetry** to explore the interface without a network dependency. Switch to **FastF1 session** when you want historical session data.

## What the Pit Wall provides

### Session command
- Data-source state
- Session context
- Driver focus
- Telemetry row count
- Validation status

### Telemetry cockpit
- Speed trace
- Throttle trace
- Brake trace
- RPM response
- Gear selection

### Driver engineering
- Distance-aligned speed delta
- Positive and negative delta extremes
- Mean pace delta

### Data quality
- Required-field contract
- Numeric checks
- Physical range checks
- Null detection
- Duplicate-distance detection
- Raw data inspection
- CSV export

## Engineering principles

- **Source separation:** ingestion code does not own analytics logic.
- **Data contracts:** telemetry is validated before downstream use.
- **Cache first:** historical session loads are cached by the UI.
- **Offline demo path:** product demos do not depend on live services.
- **Observable pipeline:** the dashboard exposes source, row count and validation state.
- **Incremental architecture:** OpenF1, UDP and ML layers can be added without rewriting the dashboard shell.

## Roadmap

### Phase 1 — Data foundation
- [x] FastF1 ingestion
- [x] OpenF1 client
- [x] Normalized telemetry contract
- [x] Data validation

### Phase 2 — Engineering cockpit
- [x] Dark motorsport UI
- [x] KPI wall
- [x] Telemetry charts
- [x] Track trace
- [x] Driver delta
- [x] CSV export

### Phase 3 — Race operations
- [ ] Live OpenF1 refresh
- [ ] UDP telemetry adapter
- [ ] Sector timing board
- [ ] Tire / stint timeline
- [ ] Strategy scenario simulator
- [ ] Engineer alert feed

### Phase 4 — AI engineering
- [ ] Lap-time prediction
- [ ] Tire degradation forecasting
- [ ] Driver performance clustering
- [ ] Anomaly detection
- [ ] Strategy simulation service

## Data-source note

OpenF1 is an unofficial open-source API for Formula 1 timing and telemetry data. Its documentation states that historical data from 2023 onward is available without authentication, while real-time data requires a paid subscription: https://openf1.org/docs/

FastF1 is used for historical session loading and telemetry extraction.

## Portfolio target

The end state is more than a dashboard: a credible end-to-end engineering platform demonstrating **Python, data ingestion, validation, caching, visualization, CI, cloud-ready structure, and ML integration** around a distinctive motorsport use case.
