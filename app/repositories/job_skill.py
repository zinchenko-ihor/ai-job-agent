from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.job_skill import JobSkill


class JobSkillRepository:

    def __init__(
        self,
        session: Session,
    ):
        self.session = session


    def exists(
        self,
        job_id: int,
        skill_id: int,
    ) -> bool:

        result = self.session.scalar(
            select(JobSkill).where(
                JobSkill.job_id == job_id,
                JobSkill.skill_id == skill_id,
            )
        )

        return result is not None


    def create(
        self,
        job_id: int,
        skill_id: int,
        importance: str = "required",
    ) -> JobSkill:

        existing = self.session.scalar(
            select(JobSkill).where(
                JobSkill.job_id == job_id,
                JobSkill.skill_id == skill_id,
            )
        )

        if existing:
            return existing


        job_skill = JobSkill(
            job_id=job_id,
            skill_id=skill_id,
            importance=importance,
        )

        self.session.add(job_skill)
        self.session.flush()

        return job_skill
