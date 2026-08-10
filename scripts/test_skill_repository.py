from app.db.session import SessionLocal

from app.repositories.skill import SkillRepository


def main():

    session = SessionLocal()

    try:
        repo = SkillRepository(session)

        skill = repo.get_or_create(
            name="Python",
            category="programming"
        )

        session.commit()

        print("=== SKILL ===")
        print(skill.id)
        print(skill.name)
        print(skill.category)

    finally:
        session.close()


if __name__ == "__main__":
    main()
