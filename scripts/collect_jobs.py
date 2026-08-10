from app.db.session import SessionLocal
from app.services.job_collection import JobCollectionService


def main():

    session = SessionLocal()

    try:

        service = JobCollectionService(
            session
        )

        result = service.collect_dou(
            category="devops"
        )

        print("=== JOB COLLECTION ===")
        print("Source: DOU")
        print(f"Fetched:  {result['fetched']}")
        print(f"Fresh:    {result['fresh']}")
        print(f"Stale:    {result['stale']}")
        print(f"Created:  {result['created']}")
        print(f"Existing: {result['existing']}")

    except Exception as e:

        print(
            f"ERROR: {e}"
        )

        raise

    finally:

        session.close()


if __name__ == "__main__":
    main()
