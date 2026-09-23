"""
APEX-RACE-AI • Pit Wall
Interactive motorsport telemetry cockpit.

Run:
    streamlit run dashboard/app.py
"""

from __future__ import annotations

from io import StringIO
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
import streamlit as st

from processing.telemetry_metrics import compare_drivers, telemetry_summary
from processing.validation.telemetry_validator import validate_telemetry


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SESSION_PRESETS = [
    "Monza",
    "Silverstone",
    "Spa-Francorchamps",
    "Suzuka",
    "Bahrain",
    "Spielberg",
    "Imola",
    "Barcelona",
    "Miami",
]
DRIVER_PRESETS = ["LEC", "VER", "NOR", "HAM", "PIA", "RUS", "SAI", "ALO"]


st.set_page_config(
    page_title="APEX-RACE-AI • Pit Wall",
    page_icon="🏁",
    layout="wide",
    initial_sidebar_state="expanded",
)


def inject_styles() -> None:
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Space+Grotesk:wght@500;600;700&display=swap');

        html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
        .block-container { padding-top: 1.1rem; padding-bottom: 3rem; max-width: 1500px; }

        .apex-topbar {
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 18px;
            margin-bottom: 18px;
            padding: 18px 20px;
            border: 1px solid rgba(255,255,255,0.09);
            border-radius: 18px;
            background:
                radial-gradient(circle at 82% 12%, rgba(255, 53, 53, .14), transparent 25%),
                linear-gradient(135deg, rgba(255,255,255,.055), rgba(255,255,255,.015));
            backdrop-filter: blur(14px);
        }
        .apex-brand { font-family: 'Space Grotesk', sans-serif; font-size: 1.55rem; font-weight: 700; letter-spacing: -.03em; }
        .apex-sub { color: #9ca3af; font-size: .78rem; margin-top: 2px; }
        .apex-live { display: inline-flex; align-items: center; gap: 7px; color: #e5e7eb; font-size: .78rem; }
        .apex-dot { width: 8px; height: 8px; border-radius: 50%; background: #ff4545; box-shadow: 0 0 14px rgba(255,69,69,.75); }

        .section-kicker {
            color: #9ca3af;
            text-transform: uppercase;
            letter-spacing: .12em;
            font-size: .67rem;
            font-weight: 700;
            margin: 8px 0 5px;
        }
        .section-title {
            font-family: 'Space Grotesk', sans-serif;
            font-size: 1.15rem;
            font-weight: 700;
            margin-bottom: 12px;
        }
        .status-chip {
            display: inline-flex;
            padding: 5px 9px;
            border-radius: 999px;
            border: 1px solid rgba(255,255,255,.09);
            background: rgba(255,255,255,.03);
            color: #d4d4d8;
            font-size: .68rem;
            font-weight: 600;
        }
        .status-chip.ok { border-color: rgba(34,197,94,.25); color: #86efac; background: rgba(34,197,94,.07); }
        .status-chip.info { border-color: rgba(59,130,246,.25); color: #93c5fd; background: rgba(59,130,246,.07); }

        div[data-testid="stMetric"] {
            background: rgba(255,255,255,.025);
            border: 1px solid rgba(255,255,255,.07);
            padding: 12px 14px;
            border-radius: 14px;
        }
        div[data-testid="stMetricLabel"] { font-size: .72rem; }
        div[data-testid="stMetricValue"] { font-family: 'Space Grotesk', sans-serif; }

        .footer-line {
            border-top: 1px solid rgba(255,255,255,.07);
            padding-top: 14px;
            margin-top: 25px;
            color: #71717a;
            font-size: .72rem;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def header() -> None:
    st.markdown(
        """
        <div class="apex-topbar">
          <div>
            <div class="apex-brand">APEX-RACE-AI <span style="color:#ff4545;">//</span> PIT WALL</div>
            <div class="apex-sub">Motorsport data engineering cockpit • telemetry → validation → insight</div>
          </div>
          <div class="apex-live"><span class="apex-dot"></span> PIPELINE READY</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


@st.cache_data(ttl="1h", show_spinner="Generating demonstration telemetry…")
def generate_demo_telemetry(driver: str, seed: int = 27) -> pd.DataFrame:
    """Create deterministic telemetry so the UI remains explorable offline."""
    rng = np.random.default_rng(seed + sum(ord(c) for c in driver))
    points = 720
    distance = np.linspace(0, 5300, points)

    corner_centres = np.array([820, 1460, 2225, 3010, 3740, 4400, 5025])
    corner_depth = np.array([78, 58, 92, 70, 63, 86, 55])
    corner_width = np.array([95, 140, 105, 120, 115, 105, 150])

    speed = np.full(points, 325.0)
    for centre, depth, width in zip(corner_centres, corner_depth, corner_width):
        speed -= depth * np.exp(-0.5 * ((distance - centre) / width) ** 2)

    speed += 6 * np.sin(distance / 310) + rng.normal(0, 1.7, points)
    speed = np.clip(speed, 82, 340)

    braking = np.clip((170 - speed) / 1.75, 0, 100)
    throttle = np.clip(100 - braking * 1.08 + rng.normal(0, 2.0, points), 0, 100)
    rpm = np.clip(
        11400 + (speed - speed.mean()) * 28 + rng.normal(0, 180, points),
        6200,
        13200,
    )
    gear = np.clip(np.rint((speed - 55) / 38), 2, 8)

    track_x = 1000 * np.cos(distance / 820) + 220 * np.sin(distance / 250)
    track_y = 620 * np.sin(distance / 720) + 110 * np.cos(distance / 340)

    return pd.DataFrame(
        {
            "Distance": distance,
            "Speed": speed,
            "Throttle": throttle,
            "Brake": braking,
            "RPM": rpm,
            "Gear": gear.astype(int),
            "DRS": np.where((speed > 265) & (braking < 1), 1, 0),
            "X": track_x,
            "Y": track_y,
            "Driver": driver,
        }
    )


@st.cache_data(ttl="1h", show_spinner="Loading FastF1 session…")
def load_fastf1_telemetry(
    year: int,
    grand_prix: str,
    session_code: str,
    driver: str,
) -> pd.DataFrame:
    from ingestion.fastf1.telemetry_ingestion import FastF1TelemetryIngestion

    ingestion = FastF1TelemetryIngestion()
    session = ingestion.load_session(year, grand_prix, session_code)
    telemetry = ingestion.get_driver_telemetry(session, driver).copy()

    rename_map = {"nGear": "Gear"}
    telemetry = telemetry.rename(columns=rename_map)

    for field in ("Distance", "Speed", "Throttle", "Brake", "RPM", "Gear", "DRS"):
        if field not in telemetry.columns:
            telemetry[field] = np.nan

    telemetry["Distance"] = pd.to_numeric(telemetry["Distance"], errors="coerce")
    telemetry["Driver"] = driver
    return telemetry.dropna(subset=["Distance"]).reset_index(drop=True)


def sidebar_controls() -> dict[str, Any]:
    st.sidebar.markdown("### 🏎️ Mission Control")
    source = st.sidebar.radio("Data source", ["Demo telemetry", "FastF1 session"], index=0)
    st.sidebar.caption(
        "Demo mode is fully offline. FastF1 mode loads historical session data on demand."
    )

    controls: dict[str, Any] = {"source": source}

    if source == "Demo telemetry":
        controls["driver"] = st.sidebar.selectbox("Driver", DRIVER_PRESETS, index=0)
        controls["compare"] = st.sidebar.toggle("Enable driver comparison", value=True)
        controls["driver_2"] = st.sidebar.selectbox("Compare against", DRIVER_PRESETS, index=1)
    else:
        controls["year"] = st.sidebar.slider("Season", 2018, 2026, 2024)
        controls["grand_prix"] = st.sidebar.selectbox("Grand Prix", SESSION_PRESETS, index=0)
        controls["session_code"] = st.sidebar.selectbox(
            "Session", ["R", "Q", "FP1", "FP2", "FP3", "S", "SQ"], index=0
        )
        controls["driver"] = st.sidebar.text_input("Driver code", "LEC").upper().strip()
        controls["compare"] = False

    st.sidebar.divider()
    st.sidebar.markdown("**Display**")
    controls["show_raw"] = st.sidebar.toggle("Show raw telemetry table", value=False)
    controls["compact"] = st.sidebar.toggle("Compact charts", value=False)
    return controls


def metric_row(summary: dict[str, float]) -> None:
    cols = st.columns(5)
    metrics = [
        ("TOP SPEED", f"{summary['max_speed']:.1f}", "km/h"),
        ("AVG SPEED", f"{summary['avg_speed']:.1f}", "km/h"),
        ("PEAK RPM", f"{summary['max_rpm']:,.0f}", "rpm"),
        ("BRAKE PEAK", f"{summary['max_brake']:.0f}", "%"),
        ("THROTTLE AVG", f"{summary['avg_throttle']:.1f}", "%"),
    ]
    for col, (label, value, suffix) in zip(cols, metrics):
        with col:
            st.metric(label, value, suffix)


def telemetry_chart(df: pd.DataFrame, fields: list[str], height: int) -> None:
    chart_df = df.set_index("Distance")[fields].copy()
    st.line_chart(chart_df, height=height, use_container_width=True)


def main() -> None:
    inject_styles()
    header()
    controls = sidebar_controls()

    driver = controls["driver"]

    if controls["source"] == "Demo telemetry":
        df = generate_demo_telemetry(driver)
        secondary = (
            generate_demo_telemetry(controls["driver_2"], seed=41)
            if controls["compare"]
            else None
        )
        source_badge = "DEMO / OFFLINE"
        source_detail = "Synthetic telemetry lab"
    else:
        try:
            df = load_fastf1_telemetry(
                controls["year"],
                controls["grand_prix"],
                controls["session_code"],
                driver,
            )
            secondary = None
            source_badge = f"FASTF1 / {controls['year']}"
            source_detail = f"{controls['grand_prix']} • {controls['session_code']}"
        except Exception as exc:
            st.error(f"FastF1 session could not be loaded: {exc}")
            st.info("Switch to Demo telemetry to explore the full cockpit without network access.")
            return

    validation = validate_telemetry(df)
    summary = telemetry_summary(df)

    st.markdown('<div class="section-kicker">SESSION</div>', unsafe_allow_html=True)
    session_cols = st.columns([2.1, 1, 1, 1])
    with session_cols[0]:
        st.markdown(f"### {source_detail}")
        st.caption(f"Driver focus: **{driver}**")
    with session_cols[1]:
        st.markdown(f'<span class="status-chip ok">● {source_badge}</span>', unsafe_allow_html=True)
    with session_cols[2]:
        chip = "VALIDATED" if validation["valid"] else "CHECK REQUIRED"
        cls = "ok" if validation["valid"] else "info"
        st.markdown(f'<span class="status-chip {cls}">{chip}</span>', unsafe_allow_html=True)
    with session_cols[3]:
        st.markdown(
            f'<span class="status-chip info">{len(df):,} TELEMETRY ROWS</span>',
            unsafe_allow_html=True,
        )

    metric_row(summary)

    tabs = st.tabs(["Telemetry", "Track Map", "Driver Delta", "Data Quality"])

    with tabs[0]:
        st.markdown('<div class="section-kicker">TELEMETRY STREAM</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Speed / throttle / braking</div>', unsafe_allow_html=True)
        telemetry_chart(df, ["Speed"], 310 if controls["compact"] else 360)

        split1, split2 = st.columns(2)
        with split1:
            st.caption("Throttle (%)")
            telemetry_chart(df, ["Throttle"], 220)
        with split2:
            st.caption("Brake (%)")
            telemetry_chart(df, ["Brake"], 220)

        lower1, lower2 = st.columns(2)
        with lower1:
            st.caption("Engine response — RPM")
            telemetry_chart(df, ["RPM"], 210)
        with lower2:
            st.caption("Gear selection")
            telemetry_chart(df, ["Gear"], 210)

    with tabs[1]:
        st.markdown('<div class="section-kicker">CIRCUIT VISUALIZATION</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Telemetry trace across the circuit</div>', unsafe_allow_html=True)
        track = df.dropna(subset=["X", "Y"]).copy()
        if track.empty:
            st.info("Track coordinates are unavailable for this source.")
        else:
            st.line_chart(track.set_index("X")["Y"], height=480, use_container_width=True)
        st.caption(
            "Demo coordinates are a relative circuit shape. A future track-geometry adapter can map real position telemetry."
        )

    with tabs[2]:
        st.markdown('<div class="section-kicker">RACE ENGINEERING</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Driver-to-driver pace delta</div>', unsafe_allow_html=True)
        if secondary is None:
            st.info("Enable comparison in Demo mode to activate delta analysis.")
        else:
            comparison = compare_drivers(df, secondary)
            st.line_chart(
                comparison.set_index("Distance")["Speed Delta"],
                height=330,
                use_container_width=True,
            )
            delta_cols = st.columns(3)
            delta_cols[0].metric(
                "MAX POSITIVE DELTA", f"{comparison['Speed Delta'].max():.1f} km/h"
            )
            delta_cols[1].metric(
                "MAX NEGATIVE DELTA", f"{comparison['Speed Delta'].min():.1f} km/h"
            )
            delta_cols[2].metric("MEAN DELTA", f"{comparison['Speed Delta'].mean():.1f} km/h")
            st.caption(
                f"Delta = {driver} speed − {controls['driver_2']} speed, aligned on distance."
            )

    with tabs[3]:
        st.markdown('<div class="section-kicker">DATA CONTRACT</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Telemetry quality gate</div>', unsafe_allow_html=True)
        quality_cols = st.columns(4)
        quality_cols[0].metric("SCHEMA", "PASS" if validation["valid"] else "CHECK")
        quality_cols[1].metric("ROWS", f"{validation['rows']:,}")
        quality_cols[2].metric("MISSING CELLS", f"{validation['missing_cells']:,}")
        quality_cols[3].metric("DUPLICATE DISTANCE", f"{validation['duplicate_distance']:,}")

        if validation["issues"]:
            st.warning("Validation findings")
            for issue in validation["issues"]:
                st.write(f"• {issue}")
        else:
            st.success("Telemetry contract passed all configured structural and range checks.")

        quality_table = pd.DataFrame(
            [{"Field": key, "Status": "OK" if value else "MISSING"} for key, value in validation["fields"].items()]
        )
        st.dataframe(quality_table, use_container_width=True, hide_index=True)

    if controls["show_raw"]:
        st.markdown('<div class="section-kicker">RAW VIEW</div>', unsafe_allow_html=True)
        st.dataframe(df, use_container_width=True, height=360, hide_index=True)
        csv_buffer = StringIO()
        df.to_csv(csv_buffer, index=False)
        st.download_button(
            "⬇ Download telemetry CSV",
            data=csv_buffer.getvalue(),
            file_name=f"apex_{driver.lower()}_telemetry.csv",
            mime="text/csv",
        )

    st.markdown(
        '<div class="footer-line">APEX-RACE-AI • data engineering layer for motorsport analytics • extensible into live OpenF1/UDP streams, ML signals, and race strategy services.</div>',
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()
