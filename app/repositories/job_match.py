from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.job_match import JobMatch
from app.repositories.base import BaseRepository


class JobMatchRepository(BaseRepository[JobMatch]):
    def __init__(self, session: Session):
        super().__init__(session, JobMatch)

    def get_match(
        self,
        user_profile_id: int,
        job_id: int,
    ) -> JobMatch | None:

        statement = select(JobMatch).where(
            JobMatch.user_profile_id == user_profile_id,
            JobMatch.job_id == job_id,
        )

        return self.session.scalar(statement)

    def get_recommended_jobs(
        self,
        user_profile_id: int,
        min_score: float = 70,
    ) -> list[JobMatch]:

        statement = (
            select(JobMatch)
            .where(
                JobMatch.user_profile_id == user_profile_id,
                JobMatch.is_recommended.is_(True),
                JobMatch.match_score >= min_score,
            )
            .order_by(JobMatch.match_score.desc())
        )

        return list(
            self.session.scalars(statement).all()
        )
