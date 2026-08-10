from sqlalchemy import select, func

from app.db.session import SessionLocal
from app.models.job import Job
from app.models.job_source import JobSource


def main():

    session = SessionLocal()

    try:

        print("=== SOURCES ===")

        sources = session.scalars(
            select(JobSource)
        ).all()

        for source in sources:
            print(
                source.id,
                source.name,
                source.base_url
            )


        print("\n=== JOB COUNT ===")

        count = session.scalar(
            select(func.count(Job.id))
        )

        print(
            f"Total jobs: {count}"
        )


        print("\n=== LAST JOBS ===")

        jobs = session.scalars(
            select(Job)
            .order_by(Job.id.desc())
            .limit(5)
        ).all()


        for job in jobs:
            print("----------------")
            print("ID:", job.id)
            print("Title:", job.title)
            print("Company:", job.company)
            print("Location:", job.location)
            print("URL:", job.url)


    finally:
        session.close()


if __name__ == "__main__":
    main()
