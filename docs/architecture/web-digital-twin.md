# Web Digital Twin Architecture

## Role

The Next.js web experience is the presentation and interaction layer for APEX-RACE AI's digital twin.

The existing Python/Streamlit application remains useful as the historical telemetry engineering and validation workspace. The web layer is the path toward the target premium 3D platform.

## Current flow

    simulated telemetry
            ↓
      normalized demo state
            ↓
       replay timeline
            ↓
    React state / timeline
            ↓
      React Three Fiber
            ↓
       3D circuit + car

## Target production flow

    FastF1 / OpenF1 / Jolpica / circuit adapters
                    ↓
            normalization
                    ↓
              validation
                    ↓
       processing / derived metrics
                    ↓
          FastAPI REST + WebSocket
                    ↓
             Next.js web app
              ┌─────┴─────┐
              ↓           ↓
        telemetry UI   3D digital twin
              ↓           ↓
             synchronized replay

## Architectural rules

1. Provider-specific response formats do not reach the React UI.
2. Real, derived, interpolated and simulated data remain explicitly distinguishable.
3. Replay state is the single timeline used by charts, markers and 3D motion.
4. Circuit geometry is reusable and independent of any one session.
5. 3D assets should be optimized for browser delivery.
6. Data provenance must be visible in the final user interface.

## Current limitation

The current web foundation uses a procedural prototype car and a procedural circuit path. It does not claim to reproduce a proprietary F1 chassis, private sensor system or survey-grade circuit geometry.