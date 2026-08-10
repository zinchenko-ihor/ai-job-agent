from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.job_source import JobSource


class JobSourceRepository:

    def __init__(self, session: Session):
        self.session = session

    def get_or_create(
        self,
        name: str,
        base_url: str | None = None,
    ) -> JobSource:

        source = self.session.scalar(
            select(JobSource).where(
                JobSource.name == name
            )
        )

        if source:
            return source

        source = JobSource(
            name=name,
            base_url=base_url,
        )

        self.session.add(source)
        self.session.flush()

        return source
