from app.db.session import SessionLocal
from app.repositories import (
    JobRepository,
    JobMatchRepository,
    JobSourceRepository,
    SkillRepository,
    UserProfileRepository,
)


def main():
    session = SessionLocal()

    try:
        user_repo = UserProfileRepository(session)
        job_repo = JobRepository(session)
        source_repo = JobSourceRepository(session)
        skill_repo = SkillRepository(session)
        match_repo = JobMatchRepository(session)

        print("=== Repository tests ===")

        print(
            "Users:",
            len(user_repo.get_all()),
        )

        print(
            "Jobs:",
            len(job_repo.get_all()),
        )

        print(
            "Job sources:",
            len(source_repo.get_all()),
        )

        print(
            "Skills:",
            len(skill_repo.get_all()),
        )

        print(
            "Job matches:",
            len(match_repo.get_all()),
        )

        print("\n✓ All repositories initialized successfully")

    finally:
        session.close()


if __name__ == "__main__":
    main()
