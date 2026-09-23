# APEX-RACE-AI System Architecture

## Purpose

APEX-RACE-AI separates acquisition, validation, analytics, presentation and future ML services so each layer can evolve independently.

## Logical flow

    ┌─────────────────────────┐
    │   Motorsport sources    │
    │ FastF1 • OpenF1 • UDP   │
    └────────────┬────────────┘
                 │
                 ▼
    ┌─────────────────────────┐
    │       INGESTION         │
    │  adapters + caching     │
    └────────────┬────────────┘
                 │
                 ▼
    ┌─────────────────────────┐
    │      RAW DATA ZONE      │
    │  CSV / Parquet / cache  │
    └────────────┬────────────┘
                 │
                 ▼
    ┌─────────────────────────┐
    │      VALIDATION         │
    │ schema + range checks   │
    └────────────┬────────────┘
                 │
                 ▼
    ┌─────────────────────────┐
    │ PROCESSING / ANALYTICS  │
    │ KPIs • delta • sectors  │
    └───────┬────────┬────────┘
            │        │
            ▼        ▼
      ┌──────────┐ ┌──────────────┐
      │ PIT WALL │ │ AI / ML      │
      │ Streamlit│ │ predictions  │
      │ cockpit  │ │ anomalies    │
      └────┬─────┘ └──────┬───────┘
           │              │
           └──────┬───────┘
                  ▼
        ┌─────────────────────┐
        │ ENGINEERING INSIGHT │
        │ pace / strategy /   │
        │ race operations     │
        └─────────────────────┘

## Component responsibilities

### Ingestion

- ingestion/fastf1/telemetry_ingestion.py handles historical FastF1 session loading and fastest-lap extraction.
- ingestion/openf1/telemetry_ingestion.py exposes lightweight DataFrame-oriented OpenF1 adapters.

### Data contract

data/schemas/telemetry_schema.json defines the normalized fields shared by downstream consumers.

### Validation

processing/validation/telemetry_validator.py checks required fields, numeric coercion, expected value ranges, nulls and duplicate distance samples.

### Processing

processing/telemetry_metrics.py contains pure analytics functions for dashboard KPIs, driver comparison and sector summaries.

### Presentation

dashboard/app.py provides the human-facing pit-wall cockpit. The offline demo path keeps product demos and UI work independent of external API availability.

## Live-runtime evolution

For live operations:

1. UDP/OpenF1 events enter a queue or streaming broker.
2. A streaming consumer writes raw immutable events.
3. Validation converts events to the normalized contract.
4. Feature jobs build lap, sector, tire and strategy features.
5. Model services score anomalies, pace and strategy states.
6. The dashboard reads low-latency aggregates while raw events remain replayable.

## Non-functional goals

- Reproducible ingestion
- Explicit data contracts
- Graceful failure when external APIs are unavailable
- Cached historical loads
- Source-independent visualization contracts
- Optional live and ML components
- CI checks on every push and pull request
