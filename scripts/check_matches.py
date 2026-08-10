from app.db.session import SessionLocal
from app.models.job_match import JobMatch


db = SessionLocal()

matches = db.query(JobMatch).all()

for m in matches:
    print("Score:", m.match_score)
    print("Recommended:", m.is_recommended)
    print("Reason:")
    print(m.ai_reasoning)
    print("---")
