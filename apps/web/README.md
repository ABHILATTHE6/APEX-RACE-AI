# APEX-RACE AI Web Experience

The web application is the browser-native digital-twin layer for APEX-RACE AI.

## Purpose

This application is intentionally separate from the existing Streamlit Pit Wall. The Python stack remains responsible for motorsport ingestion, validation and analytics, while apps/web becomes the premium 3D interaction surface.

Current foundation:

- Next.js App Router
- React + TypeScript
- React Three Fiber
- Drei
- Three.js
- Responsive white-first UI
- Procedural circuit geometry
- Procedural prototype car
- Replay timeline
- Telemetry-synchronized vehicle motion
- Clearly labeled simulated data

## Run locally

From apps/web:

    npm install
    npm run dev

Production build:

    npm run build
    npm run start

## Data boundary

The current demo uses deterministic simulated telemetry so the digital twin works without external API access.

The intended production flow is:

provider adapter → normalized APEX telemetry contract → API/WebSocket → digital twin

The browser must never treat simulated fields as proprietary Formula 1 team telemetry.