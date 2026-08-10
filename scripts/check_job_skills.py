from sqlalchemy import select

from app.db.session import SessionLocal
from app.models.job import Job
from app.models.skill import Skill
from app.models.job_skill import JobSkill


def main():

    session = SessionLocal()

    try:

        print("=== SKILLS ===")

        skills = session.scalars(
            select(Skill)
        ).all()


        for skill in skills:
            print(
                skill.id,
                skill.name
            )


        print("\n=== JOB SKILLS ===")


        relations = session.scalars(
            select(JobSkill)
        ).all()


        for relation in relations:

            print(
                f"Job {relation.job_id} -> Skill {relation.skill_id}"
            )


    finally:
        session.close()


if __name__ == "__main__":
    main()
