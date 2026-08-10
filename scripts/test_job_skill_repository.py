from app.db.session import SessionLocal

from app.repositories.skill import SkillRepository
from app.repositories.job_skill import JobSkillRepository


def main():

    session = SessionLocal()

    try:

        skill_repo = SkillRepository(session)
        job_skill_repo = JobSkillRepository(session)


        skill = skill_repo.get_or_create(
            name="Docker",
            category="DevOps"
        )


        relation = job_skill_repo.create(
            job_id=1,
            skill_id=skill.id,
            importance="required"
        )


        session.commit()


        print("=== JOB SKILL ===")
        print("ID:", relation.id)
        print("JOB:", relation.job_id)
        print("SKILL:", relation.skill_id)
        print("IMPORTANCE:", relation.importance)


    finally:
        session.close()


if __name__ == "__main__":
    main()
