from app.db.session import SessionLocal
from app.services.collector import JobCollectionService


def main():
    session = SessionLocal()

    try:
        service = JobCollectionService(session)

        created = service.collect_remoteok()

        print()
        print(
            f"✓ Collection completed"
        )
        print(
            f"✓ New jobs: {created}"
        )

    except Exception:
        session.rollback()
        raise

    finally:
        session.close()


if __name__ == "__main__":
    main()
