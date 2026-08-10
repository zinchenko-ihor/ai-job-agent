from sqlalchemy import select

from app.db.session import SessionLocal
from app.extractors.skills import SkillExtractor
from app.models.job import Job
from app.services.skill import SkillService


def main():
    session = SessionLocal()

    try:
        extractor = SkillExtractor()
        skill_service = SkillService(session)

        jobs = session.scalars(
            select(Job)
        ).all()

        processed = 0

        for job in jobs:

            skills = extractor.extract(
                title=job.title,
                description=job.description,
            )

            for skill_name in skills:

                skill = skill_service.get_or_create_skill(
                    name=skill_name,
                    category="technology",
                )

                skill_service.add_skill_to_job(
                    job_id=job.id,
                    skill_id=skill.id,
                    importance="detected",
                )

            processed += 1

        session.commit()

        print(
            f"✓ Processed {processed} jobs"
        )

    except Exception:
        session.rollback()
        raise

    finally:
        session.close()


if __name__ == "__main__":
    main()
