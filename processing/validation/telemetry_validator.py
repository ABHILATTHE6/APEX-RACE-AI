"""
APEX-RACE-AI
Telemetry Data Quality Validator

Purpose:
    Validate raw motorsport telemetry before it
    enters the downstream processing pipeline.
"""

from pathlib import Path

import pandas as pd


REQUIRED_COLUMNS = [
    "Date",
    "RPM",
    "Speed",
    "nGear",
    "Throttle",
    "Brake",
    "DRS",
    "Source",
    "Time",
    "SessionTime",
    "Distance",
    "Driver",
]


def validate_schema(df: pd.DataFrame) -> list[str]:
    """Check whether all required columns are present."""

    errors = []

    missing_columns = [
        column
        for column in REQUIRED_COLUMNS
        if column not in df.columns
    ]

    if missing_columns:
        errors.append(
            f"Missing columns: {missing_columns}"
        )

    return errors


def validate_nulls(df: pd.DataFrame) -> list[str]:
    """Check for null values in required columns."""

    errors = []

    for column in REQUIRED_COLUMNS:
        if column in df.columns:
            null_count = int(df[column].isna().sum())

            if null_count > 0:
                errors.append(
                    f"{column}: {null_count} null values"
                )

    return errors


def validate_duplicates(df: pd.DataFrame) -> list[str]:
    """Check for duplicate telemetry records."""

    duplicate_count = int(df.duplicated().sum())

    if duplicate_count > 0:
        return [
            f"Duplicate rows: {duplicate_count}"
        ]

    return []


def validate_numeric_columns(df: pd.DataFrame) -> list[str]:
    """Check that telemetry measurements are numeric."""

    errors = []

    numeric_columns = [
        "RPM",
        "Speed",
        "nGear",
        "Throttle",
        "Distance",
    ]

    for column in numeric_columns:
        if column not in df.columns:
            continue

        if not pd.api.types.is_numeric_dtype(df[column]):
            errors.append(
                f"{column}: expected numeric data type"
            )

    return errors


def validate_ranges(df: pd.DataFrame) -> list[str]:
    """Validate physically meaningful telemetry ranges."""

    errors = []

    if "Speed" in df.columns:
        invalid_speed = (df["Speed"] < 0).sum()

        if invalid_speed:
            errors.append(
                f"Speed: {invalid_speed} negative values"
            )

    if "RPM" in df.columns:
        invalid_rpm = (df["RPM"] < 0).sum()

        if invalid_rpm:
            errors.append(
                f"RPM: {invalid_rpm} negative values"
            )

    if "nGear" in df.columns:
        invalid_gear = (
            (df["nGear"] < 0) |
            (df["nGear"] > 8)
        ).sum()

        if invalid_gear:
            errors.append(
                f"nGear: {invalid_gear} invalid values"
            )

    if "Throttle" in df.columns:
        invalid_throttle = (
            (df["Throttle"] < 0) |
            (df["Throttle"] > 100)
        ).sum()

        if invalid_throttle:
            errors.append(
                f"Throttle: {invalid_throttle} values outside 0-100"
            )

    if "Distance" in df.columns:
        invalid_distance = (
            df["Distance"] < 0
        ).sum()

        if invalid_distance:
            errors.append(
                f"Distance: {invalid_distance} negative values"
            )

    return errors


def validate_driver(df: pd.DataFrame) -> list[str]:
    """Validate driver identifiers."""

    errors = []

    if "Driver" in df.columns:
        empty_driver = (
            df["Driver"]
            .astype(str)
            .str.strip()
            .eq("")
            .sum()
        )

        if empty_driver:
            errors.append(
                f"Driver: {empty_driver} empty values"
            )

    return errors


def validate_telemetry(file_path: str) -> bool:
    """
    Run all telemetry quality checks.

    Returns True when the dataset passes all checks.
    """

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(
            f"Telemetry file not found: {path}"
        )

    df = pd.read_csv(path)

    errors = []

    errors.extend(validate_schema(df))
    errors.extend(validate_nulls(df))
    errors.extend(validate_duplicates(df))
    errors.extend(validate_numeric_columns(df))
    errors.extend(validate_ranges(df))
    errors.extend(validate_driver(df))

    print("=" * 60)
    print("APEX-RACE-AI DATA QUALITY REPORT")
    print("=" * 60)

    print(f"File: {path}")
    print(f"Rows: {len(df)}")
    print(f"Columns: {len(df.columns)}")

    if errors:
        print("\nSTATUS: FAILED")
        print("\nIssues found:")

        for error in errors:
            print(f"  - {error}")

        return False

    print("\nSTATUS: PASSED")
    print("All telemetry quality checks passed.")

    return True


if __name__ == "__main__":

    telemetry_file = (
        "data/raw/fastf1/2024/"
        "italian_gp/LEC_fastest_lap.csv"
    )

    validate_telemetry(telemetry_file)