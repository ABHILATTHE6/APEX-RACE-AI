# 🤝 Contributing to APEX-RACE-AI

## Development philosophy

Keep the project modular, reproducible and engineering-focused.

Prefer small, composable modules over large scripts.

## Workflow

### 1. Update your branch

    git checkout main
    git pull

### 2. Create a feature branch

Examples:

    feature/live-openf1
    feature/sector-analysis
    fix/telemetry-validation
    docs/architecture-update

### 3. Make focused changes

A pull request should solve one coherent problem.

Examples:

- one ingestion adapter
- one processing capability
- one dashboard area
- one CI improvement
- one documentation section

### 4. Run local checks

    python -m compileall dashboard ingestion processing
    streamlit run dashboard/app.py

Use Demo telemetry for an offline smoke test.

### 5. Open a pull request

Explain:

- what changed
- why it changed
- affected modules
- how it was tested
- known limitations
- follow-up work

## Code conventions

### Python

- Use clear names.
- Add docstrings to reusable modules.
- Keep source adapters separate from analytics.
- Prefer type hints for public functions.
- Avoid source-specific assumptions in the dashboard.

### Data

- Keep large generated datasets out of Git.
- Use data/samples for small reproducible fixtures.
- Document units, source and semantics for new fields.
- Update the telemetry schema when the contract changes.

### Dashboard

- Keep presentation in dashboard.
- Keep reusable calculations in processing.
- Avoid making the dashboard the only home of an analytical calculation.

## Commit style

Use descriptive conventional-style messages where practical:

    feat: add sector delta analysis
    fix: normalize OpenF1 DRS state
    docs: add live architecture notes
    ci: add telemetry validation workflow

## Pull-request checklist

- [ ] Change is focused and documented.
- [ ] Python modules compile successfully.
- [ ] New logic has a reproducible test path.
- [ ] Telemetry contract is updated when necessary.
- [ ] No secrets are committed.
- [ ] Generated/raw data is not accidentally added.
- [ ] README/docs are updated for user-facing changes.

## Adding a new data source

Use:

    source → ingestion adapter → normalized contract → validation → processing → dashboard

Do not make the dashboard directly responsible for source-specific API logic unless there is a clear architectural reason.

## Adding a new metric

1. Implement the calculation in processing.
2. Make its inputs explicit.
3. Document units and interpretation.
4. Add a smoke or unit test.
5. Expose it in the dashboard after the underlying processing function exists.

## Security

Never commit:

- API keys
- tokens
- .env files
- credentials
- private telemetry dumps

Use .env.example to document configuration names without secret values.
