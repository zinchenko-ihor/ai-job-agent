from app.db.session import SessionLocal
from app.models.job_match import JobMatch


db = SessionLocal()

db.query(JobMatch).delete()

db.commit()

print("Matches cleared")
