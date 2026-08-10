from app.collectors.remoteok import RemoteOKCollector


def main():
    collector = RemoteOKCollector()

    jobs = collector.fetch_jobs()

    print(f"✓ Received {len(jobs)} jobs")

    for job in jobs[:5]:
        print()
        print("ID:", job.get("id"))
        print("Title:", job.get("position"))
        print("Company:", job.get("company"))
        print("Location:", job.get("location"))
        print("URL:", job.get("url"))


if __name__ == "__main__":
    main()
