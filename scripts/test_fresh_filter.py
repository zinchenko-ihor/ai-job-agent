from datetime import datetime, timedelta, timezone

from app.jobs.fresh_filter import FreshJobFilter


def main():
    fresh_filter = FreshJobFilter(
        max_age_days=2
    )

    now = datetime.now(timezone.utc)

    tests = [
        (
            "Today",
            now,
            True,
        ),
        (
            "Yesterday",
            now - timedelta(days=1),
            True,
        ),
        (
            "Two days ago",
            now - timedelta(days=2),
            True,
        ),
        (
            "Three days ago",
            now - timedelta(days=3),
            False,
        ),
        (
            "One week ago",
            now - timedelta(days=7),
            False,
        ),
        (
            "No publication date",
            None,
            False,
        ),
    ]

    print("=== FRESH JOB FILTER TEST ===")

    passed = 0

    for name, published_at, expected in tests:

        result = fresh_filter.is_fresh(
            published_at
        )

        status = (
            "PASS"
            if result == expected
            else "FAIL"
        )

        print(
            f"{status} | "
            f"{name:25} -> {result}"
        )

        if result == expected:
            passed += 1

    print()

    print(
        f"Result: "
        f"{passed}/{len(tests)} tests passed"
    )


if __name__ == "__main__":
    main()
