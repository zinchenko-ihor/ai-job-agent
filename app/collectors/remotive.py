import httpx


class RemotiveCollector:

    BASE_URL = "https://remotive.com/api/remote-jobs"

    def __init__(self):
        self.client = httpx.Client(
            timeout=30.0
        )

    def fetch_jobs(
        self,
        category: str = "software-dev",
        limit: int = 20,
    ) -> list[dict]:

        response = self.client.get(
            self.BASE_URL,
            params={
                "category": category,
                "limit": limit,
            },
        )

        response.raise_for_status()

        data = response.json()

        return data.get("jobs", [])

    def close(self):
        self.client.close()
