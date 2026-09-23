# 🏎️ APEX-RACE-AI Project Overview

## 1. Project identity

Project name: APEX-RACE-AI

Expansion: Real-Time Motorsport Data & AI Engineering Platform

Primary domain: Motorsport and Formula 1 data engineering

Primary engineering focus: Data ingestion, data quality, analytics, visualization and future AI/ML services.

Product surface: A dark motorsport-inspired engineering cockpit called the APEX Pit Wall.

## 2. Problem statement

Motorsport telemetry is valuable only when raw measurements can be converted into reliable and interpretable engineering information.

APEX-RACE-AI demonstrates that complete flow:

collect data → standardize it → validate it → calculate features → visualize it → generate engineering insight

The dashboard is therefore a consumer of a reusable data platform rather than the platform itself.

## 3. Objectives

### Engineering objectives

1. Build a reproducible telemetry ingestion layer.
2. Create a normalized telemetry contract independent of source.
3. Validate telemetry before analytics consume it.
4. Provide reusable analytics primitives.
5. Expose capabilities through an engineering dashboard.
6. Keep the platform extensible toward live streaming, databases and ML.

### Portfolio objectives

The repository demonstrates:

- Python engineering
- source integration
- pandas and numpy processing
- API integration
- caching
- data validation
- dashboard development
- Git and GitHub workflow
- CI automation
- architecture documentation
- ML readiness

## 4. Current functional scope

### FastF1 ingestion
- Load a historical session.
- Select a driver.
- Extract the driver's fastest lap.
- Add distance information.
- Persist telemetry as CSV.

### OpenF1 ingestion
- Query sessions.
- Query drivers.
- Query car telemetry.
- Query position data.
- Query location data.

### Validation
- Required field checks.
- Numeric checks.
- Range checks.
- Null detection.
- Duplicate-distance detection.
- File and in-memory validation.

### Processing
- Top speed.
- Average speed.
- Peak RPM.
- Peak braking.
- Average throttle.
- Distance-aligned driver speed delta.
- Equal-distance sector summary.

### Pit Wall
- Offline synthetic telemetry.
- Historical FastF1 mode.
- KPI wall.
- Telemetry charts.
- Track trace.
- Driver delta view.
- Data-quality panel.
- Raw table.
- CSV export.

### Engineering operations
- GitHub Actions syntax checks.
- Analytics smoke tests.
- Runtime configuration example.
- Local data protection rules.

## 5. Non-functional requirements

### Reproducibility
A new developer should be able to clone the repository, install dependencies and launch the dashboard without hidden project state.

### Observability
Important pipeline state should be visible: source, session, driver, row count, validation status and findings.

### Fault tolerance
External data-source failures should be handled gracefully. The offline demo path should remain usable.

### Modularity
Ingestion, validation, processing and presentation should remain separate modules.

### Extensibility
A new source or model should be addable without rewriting existing downstream consumers.

## 6. Target architecture

    ┌───────────────────────────────────────────┐
    │              DATA SOURCES                 │
    │ FastF1 • OpenF1 • UDP • future telemetry  │
    └─────────────────────┬─────────────────────┘
                          ▼
    ┌───────────────────────────────────────────┐
    │                 INGESTION                 │
    │ adapters • retries • caching • metadata  │
    └─────────────────────┬─────────────────────┘
                          ▼
    ┌───────────────────────────────────────────┐
    │                RAW DATA ZONE              │
    │ immutable events • CSV • Parquet • cache │
    └─────────────────────┬─────────────────────┘
                          ▼
    ┌───────────────────────────────────────────┐
    │              DATA CONTRACT                │
    │ schema • normalization • validation       │
    └─────────────────────┬─────────────────────┘
                          ▼
    ┌───────────────────────────────────────────┐
    │           PROCESSING / FEATURES           │
    │ KPI • sectors • deltas • stint features  │
    └───────────────┬──────────────────┬────────┘
                    ▼                  ▼
          ┌─────────────────┐  ┌─────────────────┐
          │   PIT WALL UI   │  │    AI / ML      │
          │   monitoring    │  │ predictions     │
          │   exploration   │  │ anomalies       │
          └────────┬────────┘  └────────┬────────┘
                   └────────────┬───────┘
                                ▼
                    ENGINEERING INSIGHT

## 7. Future modules

### Race Monitor
- current session state
- running order
- gaps
- sector times
- lap count
- flag/safety-car context
- race-control events

### Telemetry Lab
- multi-driver comparison
- synchronized traces
- lap overlays
- corner-by-corner analysis
- delta trace
- sector decomposition

### Strategy Simulator
- pit-window exploration
- tire-stint comparison
- safety-car scenarios
- undercut/overcut analysis
- fuel-adjusted pace
- projected race completion

### AI Layer
- anomaly detection
- lap-time prediction
- tire degradation forecasting
- driver clustering
- pace classification
- strategy scenario scoring

## 8. Data lifecycle

1. Source data arrives.
2. Adapter converts the source into records or DataFrames.
3. Raw data is preserved for replay and debugging.
4. Normalization maps source fields to the contract.
5. Validation identifies malformed or suspicious records.
6. Analytics computes engineering features.
7. Dashboard exposes human-readable insight.
8. Feature datasets become model inputs when ML modules are enabled.

## 9. Success criteria

A new contributor should be able to:

- understand the system from the README
- identify the telemetry contract
- launch the UI locally
- run an offline demo
- ingest historical telemetry
- inspect validation output
- add a processing metric
- understand where live and ML modules belong
- review changes through CI and pull requests
