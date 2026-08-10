from sqlalchemy.orm import Session

from app.ai.ollama_client import OllamaClient
from app.ai.skill_normalizer import SkillNormalizer
from app.services.skill import SkillService


class AISkillService:

    def __init__(self, session: Session):
        self.session = session

        self.ai = OllamaClient()
        self.normalizer = SkillNormalizer()
        self.skill_service = SkillService(session)

    def extract_and_save_for_job(
        self,
        job_id: int,
        title: str | None,
        description: str | None,
    ) -> list[str]:

        text = f"""
Job title:
{title or ""}

Job description:
{description or ""}
"""

        # 1. AI extraction
        skills = self.ai.extract_skills(text)

        # 2. Normalize
        skills = self.normalizer.normalize_many(
            skills
        )

        # 3. Save to DB
        for skill_name in skills:

            skill = self.skill_service.get_or_create_skill(
                name=skill_name,
                category="technology",
            )

            self.skill_service.add_skill_to_job(
                job_id=job_id,
                skill_id=skill.id,
                importance="ai_detected",
            )

        self.session.commit()

        return skills
