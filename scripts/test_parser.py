from app.collectors.remoteok import RemoteOKCollector
from app.parsers.job import RemoteOKJobParser


def main():
    collector = RemoteOKCollector()
    parser = RemoteOKJobParser()

    jobs = collector.fetch_jobs()

    if not jobs:
        print("No jobs received")
        return

    parsed = parser.parse(jobs[0])

    print("=== Parsed job ===")

    for key, value in parsed.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    main()
