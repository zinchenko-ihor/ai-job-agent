from datetime import datetime
from typing import Any


class RemoteOKJobParser:

    SOURCE_NAME = "remoteok"

    def parse(self, raw_job: dict[str, Any]) -> dict[str, Any]:

        published_at = None

        raw_date = raw_job.get("date")

        if raw_date:
            try:
                published_at = datetime.fromisoformat(
                    raw_date.replace("Z", "+00:00")
                )
            except ValueError:
                published_at = None

        return {
            "external_id": str(
                raw_job.get("id")
            ),
            "title": raw_job.get("position")
            or "Unknown position",
            "company": raw_job.get("company"),
            "location": raw_job.get("location"),
            "description": raw_job.get("description"),
            "url": raw_job.get("url"),
            "published_at": published_at,
        }
