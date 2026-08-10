from typing import Any

import httpx

from app.collectors.base import BaseJobCollector


class RemoteOKCollector(BaseJobCollector):

    API_URL = "https://remoteok.com/api"

    def fetch_jobs(self) -> list[dict[str, Any]]:
        headers = {
            "User-Agent": "AI-Job-Agent/1.0"
        }

        response = httpx.get(
            self.API_URL,
            headers=headers,
            timeout=30,
        )

        response.raise_for_status()

        data = response.json()

        if not isinstance(data, list):
            raise ValueError(
                "Unexpected Remote OK API response"
            )

        # First item contains API metadata.
        jobs = [
            item
            for item in data
            if isinstance(item, dict)
            and item.get("id")
        ]

        return jobs
