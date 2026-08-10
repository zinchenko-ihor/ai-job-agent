from datetime import datetime

from bs4 import BeautifulSoup


class RemotiveJobParser:

    @staticmethod
    def clean_html(html: str | None) -> str | None:
        if not html:
            return None

        soup = BeautifulSoup(html, "html.parser")

        return soup.get_text(
            separator="\n",
            strip=True,
        )

    @staticmethod
    def parse(job: dict) -> dict:

        published_at = None

        publication_date = job.get("publication_date")

        if publication_date:
            try:
                published_at = datetime.fromisoformat(
                    publication_date.replace("Z", "+00:00")
                )
            except ValueError:
                published_at = None

        return {
            "external_id": str(job["id"]),
            "title": job.get("title"),
            "company": job.get("company_name"),
            "location": job.get(
                "candidate_required_location"
            ),
            "employment_type": job.get("job_type"),
            "description": RemotiveJobParser.clean_html(
                job.get("description")
            ),
            "url": job.get("url"),
            "published_at": published_at,
            "salary_min": None,
            "salary_max": None,
            "currency": None,
        }
