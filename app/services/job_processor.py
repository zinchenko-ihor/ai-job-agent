from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.job import Job
from app.models.job_skill import JobSkill
from app.services.ai import AIService
from app.services.skill import SkillService
from app.services.skill_normalizer import normalize_skill


class JobProcessor:

    def __init__(
        self,
        session: Session,
    ):
        self.session = session
        self.ai = AIService()
        self.skill_service = SkillService(session)

    def process(
        self,
        job_id: int,
    ):

        job = self.session.get(
            Job,
            job_id
        )

        if not job:
            return None

        # Skip AI processing if job already has skills
        existing_skill = self.session.scalar(
            select(JobSkill.id)
            .where(JobSkill.job_id == job.id)
            .limit(1)
        )

        if existing_skill:
            return []

        skills = self.ai.extract_skills(
            job.description or ""
        )

        for skill_name in skills:

            normalized_skill = normalize_skill(
                skill_name
            )

            if not normalized_skill:
                continue

            skill = self.skill_service.get_or_create_skill(
                normalized_skill
            )

            self.skill_service.add_skill_to_job(
                job_id=job.id,
                skill_id=skill.id,
                importance="required",
            )

        self.session.commit()

        return skills
