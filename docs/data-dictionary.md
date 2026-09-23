# 📐 APEX-RACE-AI Telemetry Data Dictionary

This document defines the normalized telemetry contract used by downstream analytics and the Pit Wall dashboard.

## Core fields

| Field | Type | Unit | Range / rule | Meaning |
|---|---|---|---|---|
| Distance | number | m | ≥ 0 | Distance traveled along the lap trace |
| Speed | number | km/h | 0–450 | Vehicle speed |
| Throttle | number | % | 0–100 | Accelerator/throttle position |
| Brake | number | % | 0–100 | Brake application |
| RPM | number | rpm | 0–20,000 | Engine rotational speed |
| Gear | integer | gear | 0–8 | Selected gear; 0 represents neutral |
| DRS | integer | flag | 0 or 1 | Normalized DRS state |

## Context fields

| Field | Type | Unit | Requirement | Meaning |
|---|---|---|---|---|
| Driver | string | — | optional | Three-letter driver identifier |
| X | number | relative/track unit | optional | Track/circuit x-coordinate |
| Y | number | relative/track unit | optional | Track/circuit y-coordinate |

## Source mapping

### FastF1

The ingestion layer maps source telemetry into the normalized contract. The current mapping includes nGear to Gear plus the common Speed, Throttle, Brake, RPM, DRS and Distance measurements.

### OpenF1

OpenF1 exposes separate endpoints for session metadata, driver metadata, car telemetry, position and location data.

The adapter returns DataFrames so later normalization and feature engineering remain source-independent.

## Validation rules

1. Core fields are present.
2. Core measurements can be interpreted numerically.
3. Distance is non-negative.
4. Speed remains within the configured range.
5. Throttle and brake remain within 0–100 percent.
6. RPM remains within the configured engineering range.
7. Gear remains within 0–8.
8. DRS is binary.
9. Duplicate distance samples are reported.
10. Null or malformed values are reported.

## Data-quality interpretation

PASS means the dataset cleared the configured structural and range checks.

PASS does not claim that telemetry is physically perfect, scientifically complete or free of sensor issues.

Future checks should include:

- timestamp monotonicity
- sampling-rate checks
- telemetry-gap detection
- outlier detection
- cross-field consistency
- session/lap boundary checks
- unit provenance
- source lineage metadata

## Recommended production metadata

Future normalized datasets should carry:

- source
- source_version
- season
- event
- session
- driver
- lap
- ingested_at
- schema_version
- processing_version

This makes datasets reproducible and model inputs traceable.
