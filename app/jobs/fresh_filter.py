from datetime import datetime, timedelta, timezone


class FreshJobFilter:
    """
    Keeps jobs published within the last N calendar days.

    max_age_days=2 means:
        today
        yesterday
        two days ago
    """

    def __init__(self, max_age_days: int = 2):
        self.max_age_days = max_age_days

    def is_fresh(
        self,
        published_at: datetime | None,
    ) -> bool:

        if published_at is None:
            return False

        if published_at.tzinfo is None:
            published_at = published_at.replace(
                tzinfo=timezone.utc
            )

        today = datetime.now(
            timezone.utc
        ).date()

        oldest_allowed_date = (
            today
            - timedelta(
                days=self.max_age_days
            )
        )

        return (
            published_at.date()
            >= oldest_allowed_date
        )
