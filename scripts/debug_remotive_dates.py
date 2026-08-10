from datetime import datetime, timezone

from app.collectors.remotive import RemotiveCollector


def main():
    collector = RemotiveCollector()

    try:
        jobs = collector.fetch_jobs(
            category="software-dev",
            limit=10,
        )

        now = datetime.now(timezone.utc)

        print("=== REMOTIVE PUBLICATION DATES ===")
        print(f"NOW: {now.isoformat()}")
        print()

        for job in jobs:
            print(
                f"ID: {job.get('id')}"
            )

            print(
                f"TITLE: {job.get('title')}"
            )

            print(
                f"PUBLICATION DATE: "
                f"{job.get('publication_date')}"
            )

            print()

    finally:
        collector.close()


if __name__ == "__main__":
    main()
