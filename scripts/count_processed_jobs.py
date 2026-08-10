from app.db.session import SessionLocal
from app.models.job import Job
from app.models.job_skill import JobSkill
from sqlalchemy import func


db = SessionLocal()


total = db.query(Job).count()


processed = (
    db.query(JobSkill.job_id)
    .distinct()
    .count()
)


print("Total jobs:", total)
print("Processed:", processed)
print("Remaining:", total - processed)


db.close()
