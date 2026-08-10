from app.db.session import SessionLocal
from app.models.user_profile import UserProfile


db = SessionLocal()


user = UserProfile(
    name="Ihor",
    desired_position="DevOps Engineer",
)


db.add(user)
db.commit()

print(user.id)

db.close()
