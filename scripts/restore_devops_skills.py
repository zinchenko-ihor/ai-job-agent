from sqlalchemy import select

from app.db.session import SessionLocal
from app.models.skill import Skill


DEVOPS_SKILLS = [
    "GCP",
    "Jenkins",
    "GitLab",
    "Ansible",
    "MongoDB",
    "Windows",
    "Virtual Private Cloud",
    "Networking",
    "SDN",
    "CI/CD",
    "Monitoring",
    "Logging",
    "Security",
    "Database Management",
    "DevOps Automation",
]


def main():
    session = SessionLocal()

    try:
        created = 0
        existing = 0

        for skill_name in DEVOPS_SKILLS:

            skill = session.scalar(
                select(Skill).where(
                    Skill.name == skill_name
                )
            )

            if skill:
                existing += 1
                continue

            skill = Skill(
                name=skill_name,
                category="technology",
            )

            session.add(skill)
            created += 1

        session.commit()

        print("=== RESTORE DEVOPS SKILLS ===")
        print(f"Created:  {created}")
        print(f"Existing: {existing}")
        print(f"Total:    {len(DEVOPS_SKILLS)}")

    except Exception:
        session.rollback()
        raise

    finally:
        session.close()


if __name__ == "__main__":
    main()
