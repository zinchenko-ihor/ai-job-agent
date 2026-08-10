from datetime import datetime, timedelta

from sqlalchemy import select, delete
from sqlalchemy.orm import Session, joinedload

from app.models.job_recommendation import JobRecommendation


class JobRecommendationRepository:

    def __init__(
        self,
        session: Session,
    ):
        self.session = session


    def get_recent(
        self,
        user_id: int,
        hours: int = 24,
    ):

        border = (
            datetime.utcnow()
            - timedelta(hours=hours)
        )

        return self.session.scalars(
            select(JobRecommendation)
            .options(
                joinedload(
                    JobRecommendation.job
                )
            )
            .where(
                JobRecommendation.user_id == user_id,
                JobRecommendation.created_at >= border,
            )
            .order_by(
                JobRecommendation.score.desc()
            )
        ).all()


    def delete_for_user(
        self,
        user_id: int,
    ):

        self.session.execute(
            delete(JobRecommendation)
            .where(
                JobRecommendation.user_id == user_id
            )
        )


    def create(
        self,
        **kwargs,
    ):

        recommendation = JobRecommendation(
            **kwargs
        )

        self.session.add(
            recommendation
        )

        return recommendation
