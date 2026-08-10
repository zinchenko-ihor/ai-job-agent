from app.collectors.dou import DOUCollector
from app.parsers.dou import DOUJobParser


def main():

    print("=== DOU COLLECTOR TEST ===")

    collector = DOUCollector()

    try:

        raw_jobs = collector.fetch_jobs()

        print(
            f"HTML responses: {len(raw_jobs)}"
        )

        if not raw_jobs:
            print(
                "ERROR: no HTML received"
            )
            return

        html = raw_jobs[0]["html"]

        print(
            f"HTML characters: {len(html)}"
        )

        jobs = DOUJobParser.parse(
            html
        )

        print(
            f"Parsed jobs: {len(jobs)}"
        )

        print()

        for job in jobs[:10]:

            print(
                "----------------------------------------"
            )

            print(
                f"ID:          {job['external_id']}"
            )

            print(
                f"Title:       {job['title']}"
            )

            print(
                f"Company:     {job['company']}"
            )

            print(
                f"Location:    {job['location']}"
            )

            print(
                f"Published:   {job['published_at']}"
            )

            print(
                f"URL:         {job['url']}"
            )

    finally:

        collector.close()


if __name__ == "__main__":
    main()
