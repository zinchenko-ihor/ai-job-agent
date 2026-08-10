from sqlalchemy.orm import Session

from app.models.job import Job
from app.repositories.job import JobRepository
from app.repositories.job_source import JobSourceRepository


class JobService:
    def __init__(self, session: Session):
        self.job_repository = JobRepository(session)
        self.source_repository = JobSourceRepository(session)

    def get_or_create_source(
        self,
        name: str,
        base_url: str | None = None,
    ):
        source = self.source_repository.get_by_name(name)

        if source:
            return source

        from app.models.job_source import JobSource

        source = JobSource(
            name=name,
            base_url=base_url,
        )

        return self.source_repository.add(source)

    def save_job_if_new(
        self,
        source_id: int,
        external_id: str,
        title: str,
        url: str,
        company: str | None = None,
        location: str | None = None,
        employment_type: str | None = None,
        description: str | None = None,
        salary_min=None,
        salary_max=None,
        currency: str | None = None,
        published_at=None,
    ) -> Job:

        existing = self.job_repository.get_by_external_id(
            source_id=source_id,
            external_id=external_id,
        )

        if existing:
            return existing

        job = Job(
            source_id=source_id,
            external_id=external_id,
            title=title,
            company=company,
            location=location,
            employment_type=employment_type,
            salary_min=salary_min,
            salary_max=salary_max,
            currency=currency,
            description=description,
            url=url,
            published_at=published_at,
        )

        return self.job_repository.add(job)
