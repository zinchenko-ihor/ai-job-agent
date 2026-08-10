from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.job import Job
from app.models.job_skill import JobSkill

from app.repositories.skill import SkillRepository
from app.repositories.job_skill import JobSkillRepository

from app.services.ai import AIService
from app.services.skill_normalizer import normalize_skill


class JobSkillService:

    def __init__(
        self,
        session: Session,
    ):
        self.session = session

        self.ai = AIService()

        self.skill_repository = SkillRepository(
            session
        )

        self.job_skill_repository = JobSkillRepository(
            session
        )

    def process_job(
        self,
        job: Job,
    ) -> list[str]:

        if not job.description:
            return []

        # Skip AI processing if job already has skills
        existing_skill = self.session.scalar(
            select(JobSkill.id)
            .where(JobSkill.job_id == job.id)
            .limit(1)
        )

        if existing_skill:
            return []

        skills = self.ai.extract_skills(
            job.description
        )

        normalized_skills = []

        for skill_name in skills:

            normalized_skill = normalize_skill(
                skill_name
            )

            if not normalized_skill:
                continue

            # Avoid duplicate skills returned by AI
            if normalized_skill in normalized_skills:
                continue

            normalized_skills.append(
                normalized_skill
            )

            skill = self.skill_repository.get_or_create(
                name=normalized_skill
            )

            self.job_skill_repository.create(
                job_id=job.id,
                skill_id=skill.id,
                importance="required",
            )

        self.session.commit()

        return normalized_skills
