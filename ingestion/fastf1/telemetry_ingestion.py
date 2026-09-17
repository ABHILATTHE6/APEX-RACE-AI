"""
APEX-RACE-AI
FastF1 Telemetry Ingestion

Purpose:
    Load historical F1 session telemetry,
    extract driver telemetry, and persist
    raw telemetry as CSV.
"""

from pathlib import Path

import fastf1
import pandas as pd


class FastF1TelemetryIngestion:
    """Handles historical telemetry ingestion using FastF1."""

    def __init__(self):
        """Initialize FastF1 cache inside the APEX-RACE-AI data directory."""

        project_root = Path(__file__).resolve().parents[2]

        self.cache_dir = project_root / "data" / "raw" / "fastf1_cache"
        self.output_dir = project_root / "data" / "raw" / "fastf1"

        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        fastf1.Cache.enable_cache(str(self.cache_dir))

    def load_session(
        self,
        year: int,
        grand_prix: str,
        session_type: str = "R",
    ):
        """
        Load an F1 session.

        Parameters
        ----------
        year : int
            F1 season year.

        grand_prix : str
            Grand Prix name or supported event identifier.

        session_type : str
            Session type such as FP1, FP2, FP3, Q, SQ, S, R.

        Returns
        -------
        fastf1.core.Session
            Loaded FastF1 session.
        """

        session = fastf1.get_session(
            year,
            grand_prix,
            session_type,
        )

        session.load()

        return session

    def get_driver_telemetry(
        self,
        session,
        driver: str,
    ) -> pd.DataFrame:
        """
        Extract telemetry from a driver's fastest lap.

        Parameters
        ----------
        session :
            Loaded FastF1 session.

        driver : str
            Driver abbreviation, e.g. VER, HAM, LEC.

        Returns
        -------
        pandas.DataFrame
            Driver telemetry data.
        """

        laps = session.laps.pick_drivers(driver)

        if laps.empty:
            raise ValueError(
                f"No laps found for driver: {driver}"
            )

        fastest_lap = laps.pick_fastest()

        if fastest_lap.empty:
            raise ValueError(
                f"No valid fastest lap found for driver: {driver}"
            )

        telemetry = fastest_lap.get_car_data().add_distance()

        telemetry["Driver"] = driver

        return telemetry.reset_index(drop=True)

    def save_telemetry(
        self,
        telemetry: pd.DataFrame,
        year: int,
        grand_prix: str,
        driver: str,
    ) -> Path:
        """
        Save telemetry as a CSV file.

        Returns
        -------
        pathlib.Path
            Path to the generated CSV file.
        """

        event_name = grand_prix.lower().replace(" ", "_")
        event_dir = self.output_dir / str(year) / event_name

        event_dir.mkdir(parents=True, exist_ok=True)

        output_file = event_dir / f"{driver}_fastest_lap.csv"

        telemetry.to_csv(
            output_file,
            index=False,
        )

        return output_file


if __name__ == "__main__":
    ingestion = FastF1TelemetryIngestion()

    session = ingestion.load_session(
        2024,
        "Monza",
        "R",
    )

    telemetry = ingestion.get_driver_telemetry(
        session,
        "LEC",
    )

    output_file = ingestion.save_telemetry(
        telemetry,
        2024,
        "Italian_GP",
        "LEC",
    )

    print("APEX-RACE-AI telemetry ingestion successful.")
    print(f"Rows extracted: {len(telemetry)}")
    print(f"Output file: {output_file}")