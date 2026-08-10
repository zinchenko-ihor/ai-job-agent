from app.db.session import SessionLocal

from app.models.job import Job
from app.services.job_filter import JobFilter


def main():

    db = SessionLocal()
    job_filter = JobFilter()

    try:
        jobs = (
            db.query(Job)
            .order_by(Job.id)
            .all()
        )

        relevant = []
        irrelevant = []

        for job in jobs:

            is_relevant = job_filter.is_relevant(
                title=job.title or "",
                description=job.description or "",
            )

            if is_relevant:
                relevant.append(job)
            else:
                irrelevant.append(job)

        print("=== DATABASE CLEANUP PREVIEW ===")
        print()
        print(f"Total jobs:     {len(jobs)}")
        print(f"Relevant jobs:  {len(relevant)}")
        print(f"To delete:      {len(irrelevant)}")
        print()

        print("=== JOBS TO KEEP ===")

        for job in relevant:
            print(
                f"{job.id:4} | "
                f"{job.title}"
            )

        print()
        print("=== JOBS TO DELETE ===")

        for job in irrelevant:
            print(
                f"{job.id:4} | "
                f"{job.title}"
            )

    finally:
        db.close()


if __name__ == "__main__":
    main()
