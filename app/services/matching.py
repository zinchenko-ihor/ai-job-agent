from sqlalchemy.orm import Session

from app.models.job_match import JobMatch
from app.models.job_skill import JobSkill
from app.models.user_skill import UserSkill
from sqlalchemy import select
from app.services.ai import AIService
from app.models.job import Job
from app.models.skill import Skill

class MatchingService:

    def __init__(self, session: Session):
        self.session = session
        self.ai = AIService()


    def calculate_match(
        self,
        user_profile_id: int,
        job_id: int,
    ):

        user_skills = {
            x.skill_id
            for x in self.session.query(UserSkill)
            .filter(
                UserSkill.user_profile_id == user_profile_id
            )
            .all()
        }


        job_skills = {
            x.skill_id
            for x in self.session.query(JobSkill)
            .filter(
                JobSkill.job_id == job_id
            )
            .all()
        }


        if not job_skills:
            score = 0
        else:
            matched = user_skills.intersection(job_skills)
            score = len(matched) / len(job_skills) * 100


        job = self.session.scalar(
            select(Job).where(Job.id == job_id)
        )

        reasoning = None

        if job:
          prompt = f"""
        Analyze this job match.

        Job title:
        {job.title}

        Description:
        {job.description}

        Match score:
        {round(score,2)}%

        Provide a short explanation why this candidate matches.
        """

        reasoning = self.ai.generate_text(prompt)

        match = JobMatch(
           user_profile_id=user_profile_id,
           job_id=job_id,
           match_score=round(score,2),
           is_recommended=score >= 70,
           ai_reasoning=reasoning,
           status="new",
        )

        existing = self.session.scalar(
            select(JobMatch).where(
              JobMatch.user_profile_id == user_profile_id,
              JobMatch.job_id == job_id,
            )
        )

        if existing:
            return existing

        self.session.add(match)
        self.session.commit()

        return match
