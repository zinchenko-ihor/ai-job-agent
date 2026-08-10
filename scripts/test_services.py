from app.db.session import SessionLocal
from app.services import (
    JobService,
    MatchingService,
    SkillService,
    UserProfileService,
)


def main():
    session = SessionLocal()

    try:
        user_service = UserProfileService(session)
        job_service = JobService(session)
        skill_service = SkillService(session)
        matching_service = MatchingService(session)

        print("=== Creating test user ===")

        user = user_service.create_profile(
            name="Test User",
            telegram_chat_id="test_123456",
            desired_position="DevOps Engineer",
            location="Remote",
        )

        print(
            f"User: {user.id} - {user.name}"
        )

        print("\n=== Creating skills ===")

        linux = skill_service.get_or_create_skill(
            "Linux",
            "System",
        )

        aws = skill_service.get_or_create_skill(
            "AWS",
            "Cloud",
        )

        terraform = skill_service.get_or_create_skill(
            "Terraform",
            "DevOps",
        )

        kubernetes = skill_service.get_or_create_skill(
            "Kubernetes",
            "DevOps",
        )

        print(
            f"Skills: {linux.name}, "
            f"{aws.name}, "
            f"{terraform.name}, "
            f"{kubernetes.name}"
        )

        print("\n=== Adding user skills ===")

        skill_service.add_skill_to_user(
            user.id,
            linux.id,
            5,
            "advanced",
        )

        skill_service.add_skill_to_user(
            user.id,
            aws.id,
            2,
            "intermediate",
        )

        skill_service.add_skill_to_user(
            user.id,
            terraform.id,
            1,
            "intermediate",
        )

        print("✓ User skills added")

        print("\n=== Creating job source ===")

        source = job_service.get_or_create_source(
            "test_source",
            "https://example.com",
        )

        print(
            f"Source: {source.id} - {source.name}"
        )

        print("\n=== Creating test job ===")

        job = job_service.save_job_if_new(
            source_id=source.id,
            external_id="test-job-001",
            title="Middle DevOps Engineer",
            company="Test Company",
            location="Remote",
            description="DevOps engineer position",
            url="https://example.com/jobs/test-job-001",
        )

        print(
            f"Job: {job.id} - {job.title}"
        )

        print("\n=== Adding job skills ===")

        skill_service.add_skill_to_job(
            job.id,
            linux.id,
            "required",
        )

        skill_service.add_skill_to_job(
            job.id,
            aws.id,
            "required",
        )

        skill_service.add_skill_to_job(
            job.id,
            terraform.id,
            "required",
        )

        skill_service.add_skill_to_job(
            job.id,
            kubernetes.id,
            "preferred",
        )

        print("✓ Job skills added")

        print("\n=== Calculating match ===")

        match = matching_service.create_match(
            user_profile_id=user.id,
            job_id=job.id,
        )

        print(
            f"Match score: {match.match_score}%"
        )

        print(
            f"Recommended: {match.is_recommended}"
        )

        session.commit()

        print("\n✓ Integration test completed")

    except Exception:
        session.rollback()
        raise

    finally:
        session.close()


if __name__ == "__main__":
    main()
