from app.collectors.remotive import RemotiveCollector
from app.parsers.remotive import RemotiveJobParser


def main():

    collector = RemotiveCollector()

    try:

        jobs = collector.fetch_jobs(
            category="software-dev",
            limit=1,
        )

        if not jobs:
            print("No jobs found")
            return

        raw_job = jobs[0]

        parsed_job = RemotiveJobParser.parse(
            raw_job
        )

        print("=== PARSED JOB ===")

        for key, value in parsed_job.items():
            print(f"{key}: {value}")

    finally:
        collector.close()


if __name__ == "__main__":
    main()
