from app.collectors.remotive import RemotiveCollector


def main():

    collector = RemotiveCollector()

    try:

        jobs = collector.fetch_jobs(
            category="software-dev",
            limit=5,
        )

        print(f"Found {len(jobs)} jobs\n")

        for job in jobs:

            print("=" * 60)

            print(f"ID: {job.get('id')}")
            print(f"Title: {job.get('title')}")
            print(f"Company: {job.get('company_name')}")
            print(f"Location: {job.get('candidate_required_location')}")
            print(f"URL: {job.get('url')}")

    finally:
        collector.close()


if __name__ == "__main__":
    main()
