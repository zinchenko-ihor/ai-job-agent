from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.job_skill import JobSkill
from app.models.skill import Skill
from app.models.user_skill import UserSkill
from app.repositories.skill import SkillRepository


class SkillService:
    def __init__(self, session: Session):
        self.session = session
        self.repository = SkillRepository(session)

    def get_or_create_skill(
        self,
        name: str,
        category: str | None = None,
    ) -> Skill:

        #normalized_name = name.strip()
        normalized_name = name.strip().lower()
        normalized_name = normalized_name.title()

        skill = self.repository.get_by_name(
            normalized_name
        )

        if skill:
            return skill

        skill = Skill(
            name=normalized_name,
            category=category,
        )

        return self.repository.add(skill)

    def add_skill_to_user(
        self,
        user_profile_id: int,
        skill_id: int,
        experience_years: float | None = None,
        proficiency: str | None = None,
    ) -> UserSkill:

        statement = select(UserSkill).where(
            UserSkill.user_profile_id == user_profile_id,
            UserSkill.skill_id == skill_id,
        )

        existing = self.session.scalar(statement)

        if existing:
            return existing

        user_skill = UserSkill(
            user_profile_id=user_profile_id,
            skill_id=skill_id,
            experience_years=experience_years,
            proficiency=proficiency,
        )

        self.session.add(user_skill)
        self.session.flush()

        return user_skill

    def add_skill_to_job(
        self,
        job_id: int,
        skill_id: int,
        importance: str | None = None,
    ) -> JobSkill:

        statement = select(JobSkill).where(
            JobSkill.job_id == job_id,
            JobSkill.skill_id == skill_id,
        )

        existing = self.session.scalar(statement)

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
