from sqlalchemy import delete, func, select

from app.db.session import SessionLocal
from app.models.skill import Skill
from app.models.job_skill import JobSkill
from app.models.user_skill import UserSkill


def main():
    session = SessionLocal()

    try:
        skills = session.scalars(
            select(Skill)
            .order_by(Skill.id)
        ).all()

        skills_to_delete = []

        for skill in skills:
            used_in_jobs = session.scalar(
                select(func.count())
                .select_from(JobSkill)
                .where(JobSkill.skill_id == skill.id)
            )

            used_by_users = session.scalar(
                select(func.count())
                .select_from(UserSkill)
                .where(UserSkill.skill_id == skill.id)
            )

            if used_in_jobs == 0 and used_by_users == 0:
                skills_to_delete.append(skill)

        print("=== SKILL CLEANUP ===")
        print(f"Total skills: {len(skills)}")
        print(f"To delete:   {len(skills_to_delete)}")
        print(
            f"To keep:     "
            f"{len(skills) - len(skills_to_delete)}"
        )
        print()

        if not skills_to_delete:
            print("Nothing to delete.")
            return

        print("=== SKILLS TO DELETE ===")

        skill_ids = [skill.id for skill in skills_to_delete]

        for skill in skills_to_delete:
            print(f"{skill.id:4} | {skill.name}")

        print()

        result = session.execute(
            delete(Skill).where(
                Skill.id.in_(skill_ids)
            )
        )

        session.commit()

        print(
            f"Deleted Skill records: "
            f"{result.rowcount}"
        )

        remaining = session.scalar(
            select(func.count()).select_from(Skill)
        )

        print()
        print("=== CLEANUP COMPLETE ===")
        print(f"Remaining skills: {remaining}")

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
