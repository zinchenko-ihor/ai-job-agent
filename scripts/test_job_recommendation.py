from app.db.session import SessionLocal
from app.services.job_recommendation import JobRecommendationService


USER_ID = 723138866
TOP_N = 5


def main():
    session = SessionLocal()

    try:
        service = JobRecommendationService(
            session
        )

        print("=== JOB RECOMMENDATION TEST ===")
        print()
        print(
            f"User ID: {USER_ID}"
        )
        print(
            f"Limit:   {TOP_N}"
        )
        print()

        recommendations = (
            service.recommend_for_user(
                user_id=USER_ID,
                limit=TOP_N,
            )
        )

        print(
            f"Found: {len(recommendations)} "
            f"recommendation(s)"
        )
        print()

        if not recommendations:
            print(
                "No suitable fresh DOU jobs found."
            )
            return

        for index, item in enumerate(
            recommendations,
            start=1,
        ):
            job = item["job"]

            print("=" * 60)
            print(f"#{index}")

            print(
                f"Title:    "
                f"{job.get('title', 'N/A')}"
            )

            print(
                f"Company:  "
                f"{job.get('company', 'N/A')}"
            )

            print(
                f"Location: "
                f"{job.get('location', 'N/A')}"
            )

            print(
                f"Score:    "
                f"{item.get('score', 0)}%"
            )

            print(
                f"Reason:   "
                f"{item.get('reason', 'N/A')}"
            )

            matched = item.get(
                "matched_skills",
                [],
            )

            missing = item.get(
                "missing_skills",
                [],
            )

            print(
                "Matched:  "
                + (
                    ", ".join(matched)
                    if matched
                    else "none"
                )
            )

            print(
                "Missing:  "
                + (
                    ", ".join(missing)
                    if missing
                    else "none"
                )
            )

            print(
                f"URL:      "
                f"{job.get('url', 'N/A')}"
            )

            print()

        print("=" * 60)
        print(
            "Recommendation test completed."
        )

    except Exception as exc:
        print(
            f"ERROR: {exc}"
        )
        raise

    finally:
        session.close()


if __name__ == "__main__":
    main()
