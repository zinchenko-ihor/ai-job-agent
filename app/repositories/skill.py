from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.skill import Skill


class SkillRepository:

    def __init__(self, session: Session):
        self.session = session


    def get_by_name(
        self,
        name: str,
    ) -> Skill | None:

        return self.session.scalar(
            select(Skill).where(
                Skill.name == name
            )
        )

    def add(
        self,
        skill: Skill,
    ) -> Skill:

        self.session.add(skill)
        self.session.flush()

        return skill


    def get_or_create(
        self,
        name: str,
        category: str | None = None,
    ) -> Skill:

        skill = self.get_by_name(name)

        if skill:
            return skill


        skill = Skill(
            name=name,
            category=category,
        )

        self.session.add(skill)
        self.session.flush()

        return skill
