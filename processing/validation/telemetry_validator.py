"""Validation layer for the normalized APEX-RACE-AI telemetry contract."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pandas as pd


REQUIRED_FIELDS = {
    "Distance": "non-negative numeric distance",
    "Speed": "0..450 km/h",
    "Throttle": "0..100 percentage",
    "Brake": "0..100 percentage",
    "RPM": "0..20000 rpm",
    "Gear": "1..8 gear",
    "DRS": "binary flag",
}


def validate_telemetry(df: pd.DataFrame) -> dict[str, Any]:
    """Validate an in-memory telemetry DataFrame for dashboard use."""
    fields = {field: field in df.columns for field in REQUIRED_FIELDS}
    issues: list[str] = []

    for field, present in fields.items():
        if not present:
            issues.append(f"Missing required field: {field}")

    for field in REQUIRED_FIELDS:
        if field not in df.columns:
            continue
        numeric = pd.to_numeric(df[field], errors="coerce")
        if numeric.isna().any():
            issues.append(f"{field} contains non-numeric or null values.")

    ranges = {
        "Distance": (0, None),
        "Speed": (0, 450),
        "Throttle": (0, 100),
        "Brake": (0, 100),
        "RPM": (0, 20000),
        "Gear": (1, 8),
        "DRS": (0, 1),
    }

    for field, (lower, upper) in ranges.items():
        if field not in df.columns:
            continue
        values = pd.to_numeric(df[field], errors="coerce").dropna()
        if lower is not None and (values < lower).any():
            issues.append(f"{field} contains values below {lower}.")
        if upper is not None and (values > upper).any():
            issues.append(f"{field} contains values above {upper}.")

    duplicate_distance = int(df["Distance"].duplicated().sum()) if "Distance" in df.columns else 0

    return {
        "valid": len(issues) == 0,
        "rows": int(len(df)),
        "missing_cells": int(df.isna().sum().sum()),
        "duplicate_distance": duplicate_distance,
        "fields": fields,
        "issues": issues,
    }


def validate_telemetry_file(file_path: str | Path) -> dict[str, Any]:
    """Validate a CSV file using the same telemetry contract."""
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"Telemetry file not found: {path}")
    return validate_telemetry(pd.read_csv(path))


def print_quality_report(report: dict[str, Any], file_path: str | Path | None = None) -> None:
    """Render a compact quality report for CLI usage."""
    print("=" * 60)
    print("APEX-RACE-AI DATA QUALITY REPORT")
    print("=" * 60)
    if file_path:
        print(f"File: {file_path}")
    print(f"Rows: {report['rows']}")
    print(f"Missing cells: {report['missing_cells']}")
    print(f"Duplicate distance samples: {report['duplicate_distance']}")
    print(f"Status: {'PASSED' if report['valid'] else 'FAILED'}")
    for issue in report["issues"]:
        print(f"  - {issue}")


if __name__ == "__main__":
    telemetry_file = "data/raw/fastf1/2024/italian_gp/LEC_fastest_lap.csv"
    result = validate_telemetry_file(telemetry_file)
    print_quality_report(result, telemetry_file)
