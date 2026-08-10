import httpx


class DOUCollector:

    BASE_URL = "https://jobs.dou.ua/vacancies/"

    def __init__(self):
        self.client = httpx.Client(
            timeout=30.0,
            headers={
                "User-Agent": (
                    "Mozilla/5.0 "
                    "(X11; Linux x86_64) "
                    "AppleWebKit/537.36 "
                    "(KHTML, like Gecko) "
                    "Chrome/131.0 Safari/537.36"
                )
            },
        )

    def fetch_jobs(
        self,
        category: str = "devops",
    ) -> list[dict]:

        response = self.client.get(
            self.BASE_URL,
            params={
                "category": category,
            },
        )

        response.raise_for_status()

        return [
            {
                "html": item
            }
            for item in [response.text]
        ]

    def close(self):
        self.client.close()
