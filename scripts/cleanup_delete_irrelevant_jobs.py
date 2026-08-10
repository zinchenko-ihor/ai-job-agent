from sqlalchemy import delete, func, select

from app.db.session import SessionLocal
from app.models.job import Job
from app.models.job_match import JobMatch
from app.models.job_skill import JobSkill
from app.services.job_filter import JobFilter


def main():
    session = SessionLocal()
    job_filter = JobFilter()

    try:
        jobs = session.scalars(
            select(Job)
        ).all()

        jobs_to_delete = []

        for job in jobs:
            is_relevant = job_filter.is_relevant(
                title=job.title or "",
                description=job.description or "",
            )

            if not is_relevant:
                jobs_to_delete.append(job)

        total_jobs = len(jobs)
        jobs_to_delete_count = len(jobs_to_delete)
        jobs_to_keep_count = total_jobs - jobs_to_delete_count

        print("=== DELETE IRRELEVANT JOBS ===")
        print(f"Total jobs:   {total_jobs}")
        print(f"To delete:    {jobs_to_delete_count}")
        print(f"To keep:      {jobs_to_keep_count}")
        print()

        if not jobs_to_delete:
            print("Nothing to delete.")
            return

        print("=== JOBS TO DELETE ===")

        job_ids = [job.id for job in jobs_to_delete]

        for job in jobs_to_delete:
            print(f"{job.id:4} | {job.title}")

        print()

        # ---------------------------------------------------------
        # 1. Delete JobMatch records
        # ---------------------------------------------------------

        match_result = session.execute(
            delete(JobMatch).where(
                JobMatch.job_id.in_(job_ids)
            )
        )

        print(
            f"Deleted JobMatch records: "
            f"{match_result.rowcount}"
        )

        # ---------------------------------------------------------
        # 2. Delete JobSkill records
        # ---------------------------------------------------------

        skill_result = session.execute(
            delete(JobSkill).where(
                JobSkill.job_id.in_(job_ids)
            )
        )

        print(
            f"Deleted JobSkill records: "
            f"{skill_result.rowcount}"
        )

        # ---------------------------------------------------------
        # 3. Delete Job records
        # ---------------------------------------------------------

        job_result = session.execute(
            delete(Job).where(
                Job.id.in_(job_ids)
            )
        )

        print(
            f"Deleted Job records: "
            f"{job_result.rowcount}"
        )

        # ---------------------------------------------------------
        # 4. Commit transaction
        # ---------------------------------------------------------

        session.commit()

        # ---------------------------------------------------------
        # 5. Verify remaining jobs
        # ---------------------------------------------------------

        remaining_jobs = session.scalar(
            select(func.count()).select_from(Job)
        )

        print()
        print("=== CLEANUP COMPLETE ===")
        print(f"Remaining jobs: {remaining_jobs}")

    except Exception as exc:
        session.rollback()

        print()
        print("=== CLEANUP FAILED ===")
        print(f"Error: {exc}")

        raise

    finally:
        session.close()


if __name__ == "__main__":
    main()
