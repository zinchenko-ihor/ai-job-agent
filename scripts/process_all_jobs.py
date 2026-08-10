from app.db.session import SessionLocal
from app.models.job import Job
from app.models.job_skill import JobSkill
from app.services.job_processor import JobProcessor


db = SessionLocal()

processor = JobProcessor(db)


jobs = db.query(Job).all()


processed = 0
skipped = 0


for job in jobs:

    existing = (
        db.query(JobSkill)
        .filter(
            JobSkill.job_id == job.id
        )
        .count()
    )

    if existing:
        skipped += 1
        continue


    print(
        f"Processing {job.id}: {job.title}"
    )


    processor.process(
        job.id
    )

    processed += 1


print()
print("=== RESULT ===")
print("Processed:", processed)
print("Skipped:", skipped)


db.close()
