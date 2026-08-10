from sqlalchemy import select

from app.db.session import SessionLocal
from app.models.job import Job


def main():
    session = SessionLocal()

    try:
        job = session.scalar(
            select(Job).where(Job.id == 1)
        )

        if not job:
            print("Job not found")
            return

        print("=== JOB ===")
        print(f"ID: {job.id}")
        print(f"Title: {job.title}")
        print(f"Company: {job.company}")
        print(f"Location: {job.location}")

        print("\n=== DESCRIPTION ===")
        print(job.description)

        print("\n=== URL ===")
        print(job.url)

    finally:
        session.close()


if __name__ == "__main__":
    main()
