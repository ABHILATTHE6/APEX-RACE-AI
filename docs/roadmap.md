# 🗺️ APEX-RACE-AI Engineering Roadmap

The roadmap increases system realism in stages: historical analysis first, live operations second, predictive AI third.

## Phase 1 — Data Foundation ✅

Delivered:
- [x] FastF1 historical ingestion
- [x] FastF1 caching
- [x] OpenF1 REST adapter
- [x] Normalized telemetry schema
- [x] Data-quality validator
- [x] Raw data convention
- [x] Processing module separation

Next hardening:
- [ ] Formal unit tests
- [ ] Structured logging
- [ ] Retry/backoff helpers
- [ ] Schema-version metadata
- [ ] Sample fixture datasets

## Phase 2 — Pit Wall Experience ✅

Delivered:
- [x] Dark motorsport visual system
- [x] APEX-RACE identity mark
- [x] Mission Control sidebar
- [x] Telemetry KPI wall
- [x] Speed, throttle, brake, RPM and gear charts
- [x] Track trace
- [x] Driver delta analysis
- [x] Data-quality panel
- [x] Raw telemetry export
- [x] Offline demo mode

Next enhancements:
- [ ] Real circuit map rendering
- [ ] Lap-over-lap comparison
- [ ] Sector timing table
- [ ] DRS zone visualization
- [ ] Corner event detection
- [ ] Driver selector from session metadata

## Phase 3 — Live Race Operations 🔜

### Data
- [ ] Live OpenF1 integration
- [ ] UDP telemetry gateway abstraction
- [ ] Message-broker interface
- [ ] Event-time processing
- [ ] Replayable raw event store

### Pit Wall
- [ ] Live timing tower
- [ ] Live track position
- [ ] Sector gaps
- [ ] Race-control timeline
- [ ] Session status banner
- [ ] Engineer alert queue

## Phase 4 — Strategy & Performance 🔜

- [ ] Tire/stint model
- [ ] Pace degradation curves
- [ ] Fuel-adjusted lap pace
- [ ] Pit-window calculator
- [ ] Undercut/overcut scenarios
- [ ] Strategy comparison
- [ ] Driver performance fingerprints

## Phase 5 — AI / ML 🔜

### Models
- [ ] Lap-time prediction
- [ ] Tire degradation forecasting
- [ ] Telemetry anomaly detection
- [ ] Driver clustering
- [ ] Pace classification
- [ ] Strategy scoring

### MLOps
- [ ] Feature dataset versioning
- [ ] Experiment tracking
- [ ] Model registry
- [ ] Offline evaluation reports
- [ ] Model monitoring
- [ ] Prediction lineage

## Phase 6 — Production Platform 🔜

- [ ] PostgreSQL or analytical warehouse
- [ ] Object storage for raw telemetry
- [ ] Containerized services
- [ ] API layer
- [ ] Authentication and authorization where needed
- [ ] Cloud deployment
- [ ] Observability
- [ ] End-to-end integration tests

## Definition of done

A major module should have:

1. A clear purpose.
2. A stable input/output contract.
3. Error handling.
4. A reproducible test path.
5. Documentation.
6. CI coverage where practical.
7. A clear location in the architecture.
