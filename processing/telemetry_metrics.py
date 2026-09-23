"""Reusable telemetry analytics for the APEX-RACE-AI pipeline."""

from __future__ import annotations

import numpy as np
import pandas as pd


def _numeric(df: pd.DataFrame, column: str) -> pd.Series:
    if column not in df:
        return pd.Series(dtype=float)
    return pd.to_numeric(df[column], errors="coerce").dropna()


def telemetry_summary(df: pd.DataFrame) -> dict[str, float]:
    """Return dashboard-ready KPI metrics from a normalized telemetry frame."""
    speed = _numeric(df, "Speed")
    rpm = _numeric(df, "RPM")
    brake = _numeric(df, "Brake")
    throttle = _numeric(df, "Throttle")

    return {
        "max_speed": float(speed.max()) if not speed.empty else 0.0,
        "avg_speed": float(speed.mean()) if not speed.empty else 0.0,
        "max_rpm": float(rpm.max()) if not rpm.empty else 0.0,
        "max_brake": float(brake.max()) if not brake.empty else 0.0,
        "avg_throttle": float(throttle.mean()) if not throttle.empty else 0.0,
    }


def compare_drivers(
    primary: pd.DataFrame,
    secondary: pd.DataFrame,
    step_km: float = 0.01,
) -> pd.DataFrame:
    """Align two speed traces on distance and calculate a primary-minus-secondary delta."""
    if "Distance" not in primary or "Distance" not in secondary:
        raise ValueError("Both telemetry frames require a Distance column.")

    left = primary[["Distance", "Speed"]].dropna().sort_values("Distance")
    right = secondary[["Distance", "Speed"]].dropna().sort_values("Distance")

    if left.empty or right.empty:
        return pd.DataFrame(columns=["Distance", "Speed Delta"])

    start = max(float(left["Distance"].min()), float(right["Distance"].min()))
    stop = min(float(left["Distance"].max()), float(right["Distance"].max()))
    if stop <= start:
        return pd.DataFrame(columns=["Distance", "Speed Delta"])

    distance = np.arange(start, stop, max(step_km * 1000.0, 1.0))
    primary_speed = np.interp(distance, left["Distance"], left["Speed"])
    secondary_speed = np.interp(distance, right["Distance"], right["Speed"])

    return pd.DataFrame(
        {"Distance": distance, "Speed Delta": primary_speed - secondary_speed}
    )


def lap_sector_summary(df: pd.DataFrame, sectors: int = 3) -> pd.DataFrame:
    """Create equal-distance sector statistics for a telemetry trace."""
    if "Distance" not in df or df.empty:
        return pd.DataFrame(
            columns=["Sector", "Distance Start", "Distance End", "Avg Speed", "Top Speed"]
        )

    clean = df.dropna(subset=["Distance"]).copy()
    edges = np.linspace(clean["Distance"].min(), clean["Distance"].max(), sectors + 1)
    clean["Sector"] = pd.cut(
        clean["Distance"], bins=edges, labels=False, include_lowest=True
    ) + 1

    return (
        clean.groupby("Sector", dropna=True)
        .agg(
            **{
                "Distance Start": ("Distance", "min"),
                "Distance End": ("Distance", "max"),
                "Avg Speed": ("Speed", "mean"),
                "Top Speed": ("Speed", "max"),
            }
        )
        .reset_index()
    )
