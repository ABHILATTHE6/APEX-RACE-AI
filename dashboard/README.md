# APEX-RACE-AI Pit Wall Dashboard

The dashboard is the visual cockpit for the APEX-RACE-AI engineering platform.

## What it provides

- Offline demo telemetry for product demos and UI development.
- Historical FastF1 session loading on demand.
- KPI cards for top speed, average speed, RPM, braking and throttle.
- Speed, throttle, brake, RPM and gear telemetry views.
- Relative track trace.
- Distance-aligned driver delta analysis.
- Structural and range validation using the telemetry data contract.
- Raw telemetry inspection and CSV export.

## Launch

    pip install -r requirements.txt
    streamlit run dashboard/app.py

Start in Demo telemetry for an instant offline experience, then switch to FastF1 session when you want historical data.

## UI direction

The interface follows a modern motorsport engineering-pit-wall visual language:

- deep graphite background
- red signal accents
- compact information density
- oversized telemetry KPIs
- small status chips
- clean section hierarchy
- extensible tabbed views

Future modules can plug into the same shell:

1. Live OpenF1 stream
2. UDP telemetry gateway
3. Race strategy panel
4. Tire degradation view
5. AI anomaly and incident feed
6. Race-control timeline
