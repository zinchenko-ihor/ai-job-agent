from concurrent.futures import ThreadPoolExecutor, as_completed

from app.db.session import SessionLocal
from app.models.job import Job
from app.models.job_skill import JobSkill
from app.services.job_processor import JobProcessor


def process_job(job_id: int):

    db = SessionLocal()

    try:
        existing = (
            db.query(JobSkill)
            .filter(JobSkill.job_id == job_id)
            .count()
        )

        if existing:
            return job_id, "skipped"

        processor = JobProcessor(db)
        processor.process(job_id)

        return job_id, "processed"

    except Exception as e:
        db.rollback()
        return job_id, f"error: {e}"

    finally:
        db.close()


db = SessionLocal()

job_ids = [
    job.id
    for job in db.query(Job).all()
]

db.close()


print(f"Total jobs: {len(job_ids)}")
print("Starting parallel processing...")


processed = 0
skipped = 0
errors = 0


with ThreadPoolExecutor(max_workers=2) as executor:

    futures = [
        executor.submit(process_job, job_id)
        for job_id in job_ids
    ]

    for future in as_completed(futures):

        job_id, status = future.result()

        print(
            f"Job {job_id}: {status}"
        )

        if status == "processed":
            processed += 1

        elif status == "skipped":
            skipped += 1

        else:
            errors += 1


print()
print("=== RESULT ===")
print("Processed:", processed)
print("Skipped:", skipped)
print("Errors:", errors)
