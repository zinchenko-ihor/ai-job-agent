from app.db.session import SessionLocal

from app.models.job import Job

from app.services.job_skill import JobSkillService


def main():

    session = SessionLocal()

    try:

        job = session.query(Job).first()


        print("=== JOB ===")
        print(job.id)
        print(job.title)


        service = JobSkillService(
            session
        )


        skills = service.process_job(
            job
        )


        print("\n=== AI SKILLS ===")

        for skill in skills:
            print("-", skill)


    finally:
        session.close()



if __name__ == "__main__":
    main()
