"""
APEX-RACE-AI
OpenF1 REST ingestion.

Historical OpenF1 data (2023+) can be queried without authentication.
The client returns plain pandas DataFrames so downstream processing stays
independent of source-specific response models.
"""

from __future__ import annotations

import json
from typing import Any
from urllib.parse import urlencode
from urllib.request import Request, urlopen

import pandas as pd


class OpenF1TelemetryIngestion:
    """Small OpenF1 HTTP client with DataFrame adapters."""

    def __init__(
        self,
        base_url: str = "https://api.openf1.org/v1",
        timeout: int = 30,
    ):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    def _get(self, endpoint: str, **params: Any) -> list[dict[str, Any]]:
        query = {key: value for key, value in params.items() if value is not None}
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        if query:
            url = f"{url}?{urlencode(query)}"

        request = Request(
            url,
            headers={"User-Agent": "APEX-RACE-AI/1.0"},
            method="GET",
        )

        with urlopen(request, timeout=self.timeout) as response:
            payload = json.loads(response.read().decode("utf-8"))

        if not isinstance(payload, list):
            raise ValueError(f"OpenF1 returned an unexpected payload for {endpoint!r}.")
        return payload

    def sessions(
        self,
        year: int | None = None,
        country_name: str | None = None,
        session_name: str | None = None,
    ) -> pd.DataFrame:
        """Return sessions matching optional filters."""
        return pd.DataFrame(
            self._get(
                "sessions",
                year=year,
                country_name=country_name,
                session_name=session_name,
            )
        )

    def drivers(self, session_key: int) -> pd.DataFrame:
        """Return driver metadata for a session."""
        return pd.DataFrame(self._get("drivers", session_key=session_key))

    def car_data(
        self,
        session_key: int,
        driver_number: int | None = None,
    ) -> pd.DataFrame:
        """Return car telemetry samples."""
        return pd.DataFrame(
            self._get(
                "car_data",
                session_key=session_key,
                driver_number=driver_number,
            )
        )

    def position(
        self,
        session_key: int,
        driver_number: int | None = None,
    ) -> pd.DataFrame:
        """Return track position/timing samples."""
        return pd.DataFrame(
            self._get(
                "position",
                session_key=session_key,
                driver_number=driver_number,
            )
        )

    def location(
        self,
        session_key: int,
        driver_number: int | None = None,
    ) -> pd.DataFrame:
        """Return car location samples."""
        return pd.DataFrame(
            self._get(
                "location",
                session_key=session_key,
                driver_number=driver_number,
            )
        )


if __name__ == "__main__":
    client = OpenF1TelemetryIngestion()
    sample = client.sessions(year=2024)
    print(sample.tail(5).to_string(index=False))
