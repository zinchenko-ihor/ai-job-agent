from datetime import datetime, timedelta, timezone

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.job import Job
from app.models.job_source import JobSource


class JobRepository:

    def __init__(self, session: Session):
        self.session = session

    def get_by_external_id(
        self,
        source_id: int,
        external_id: str,
    ) -> Job | None:

        return self.session.scalar(
            select(Job).where(
                Job.source_id == source_id,
                Job.external_id == external_id,
            )
        )

    def create(
        self,
        source_id: int,
        external_id: str,
        title: str,
        company: str | None,
        location: str | None,
        description: str | None,
        url: str,
        published_at: datetime | None = None,
        employment_type: str | None = None,
        salary_min=None,
        salary_max=None,
        currency: str | None = None,
    ) -> Job:

        job = Job(
            source_id=source_id,
            external_id=external_id,
            title=title,
            company=company,
            location=location,
            description=description,
            url=url,
            published_at=published_at,
            employment_type=employment_type,
            salary_min=salary_min,
            salary_max=salary_max,
            currency=currency,
        )

        self.session.add(job)
        self.session.flush()

        return job

    def get_recent_jobs_by_source(
        self,
        source_name: str,
        max_age_days: int = 2,
    ) -> list[Job]:

        cutoff = (
            datetime.now(timezone.utc)
            - timedelta(days=max_age_days)
        )

        statement = (
            select(Job)
            .join(
                JobSource,
                Job.source_id == JobSource.id,
            )
            .where(
                JobSource.name == source_name,
                Job.published_at.is_not(None),
                Job.published_at >= cutoff,
            )
            .order_by(
                Job.published_at.desc()
            )
        )

        return list(
            self.session.scalars(statement).all()
        )
