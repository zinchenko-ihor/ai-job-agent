from app.db.session import SessionLocal
from app.repositories.job import JobRepository


def main():

    session = SessionLocal()

    try:
        repository = JobRepository(session)

        jobs = repository.get_recent_jobs_by_source(
            source_name="DOU",
            max_age_days=2,
        )

        print("=== RECENT DOU JOBS ===")
        print(f"Total: {len(jobs)}")

        for job in jobs:
            print(
                f"{job.id} | "
                f"{job.title} | "
                f"{job.published_at}"
            )

    finally:
        session.close()


if __name__ == "__main__":
    main()
