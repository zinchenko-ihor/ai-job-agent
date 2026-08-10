from app.db.session import SessionLocal
from app.models.user_skill import UserSkill
from app.models.skill import Skill
from sqlalchemy import select


db = SessionLocal()

user_id = 1

skills = [
    "Linux",
    "AWS",
    "Terraform",
    "Kubernetes",
    "Python",
]


for skill_name in skills:

    skill = db.scalar(
        select(Skill).where(
            Skill.name == skill_name
        )
    )

    if not skill:
        print(f"Skill not found: {skill_name}")
        continue

    existing = db.scalar(
        select(UserSkill).where(
            UserSkill.user_profile_id == user_id,
            UserSkill.skill_id == skill.id
        )
    )

    if existing:
        print(f"Exists: {skill_name}")
        continue

    user_skill = UserSkill(
        user_profile_id=user_id,
        skill_id=skill.id,
        proficiency="middle",
    )

    db.add(user_skill)
    print(f"Added: {skill_name}")


db.commit()

print("Done")
