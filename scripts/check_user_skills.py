from app.db.session import SessionLocal
from app.models.user_skill import UserSkill


db = SessionLocal()

skills = db.query(UserSkill).filter(
    UserSkill.user_profile_id == 1
).all()


for s in skills:
    print(
        s.user_profile_id,
        s.skill_id,
        s.proficiency
    )

db.close()
