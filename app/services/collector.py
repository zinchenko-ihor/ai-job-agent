from sqlalchemy.orm import Session

from app.collectors.remoteok import RemoteOKCollector
from app.extractors.skills import SkillExtractor
from app.parsers.job import RemoteOKJobParser
from app.services.job import JobService
from app.services.job_filter import JobFilter
from app.services.skill import SkillService


class JobCollectionService:

    def __init__(self, session: Session):
        self.session = session

        self.job_service = JobService(session)
        self.skill_service = SkillService(session)

        self.collector = RemoteOKCollector()
        self.parser = RemoteOKJobParser()
        self.skill_extractor = SkillExtractor()
        self.job_filter = JobFilter()

    def collect_remoteok(self) -> int:

        source = self.job_service.get_or_create_source(
            name="remoteok",
            base_url="https://remoteok.com",
        )

        raw_jobs = self.collector.fetch_jobs()

        created = 0
        relevant = 0
        skipped = 0
        existing_count = 0

        for raw_job in raw_jobs:

            try:
                job_data = self.parser.parse(raw_job)

                # -------------------------------------------------
                # 1. Filter job BEFORE saving it to the database
                # -------------------------------------------------

                if not self.job_filter.is_relevant(
                    title=job_data["title"],
                    description=job_data["description"],
                ):
                    skipped += 1
                    continue

                relevant += 1

                # -------------------------------------------------
                # 2. Check whether relevant job already exists
                # -------------------------------------------------

                existing = (
                    self.job_service.job_repository
                    .get_by_external_id(
                        source_id=source.id,
                        external_id=job_data["external_id"],
                    )
                )

                if existing:
                    existing_count += 1
                    continue

                # -------------------------------------------------
                # 3. Save ONLY relevant jobs
                # -------------------------------------------------

                job = self.job_service.save_job_if_new(
                    source_id=source.id,
                    external_id=job_data["external_id"],
                    title=job_data["title"],
                    company=job_data["company"],
                    location=job_data["location"],
                    description=job_data["description"],
                    url=job_data["url"],
                    published_at=job_data["published_at"],
                )

                # -------------------------------------------------
                # 4. Extract skills ONLY for relevant jobs
                # -------------------------------------------------

                skills = self.skill_extractor.extract(
                    title=job.title,
                    description=job.description,
                    tags=raw_job.get("tags", []),
                )

                # -------------------------------------------------
                # 5. Save job skills
                # -------------------------------------------------

                for skill_name in skills:

                    skill = (
                        self.skill_service
                        .get_or_create_skill(
                            name=skill_name,
                            category="technology",
                        )
                    )

                    self.skill_service.add_skill_to_job(
                        job_id=job.id,
                        skill_id=skill.id,
                        importance="detected",
                    )

                created += 1

            except Exception as exc:
                print(
                    f"Failed to process job: {exc}"
                )

        self.session.commit()

        # ---------------------------------------------------------
        # Collection statistics
        # ---------------------------------------------------------

        print("=== JOB COLLECTION ===")
        print("Source: RemoteOK")
        print(f"Fetched: {len(raw_jobs)}")
        print(f"Relevant: {relevant}")
        print(f"Skipped: {skipped}")
        print(f"Created: {created}")
        print(f"Existing: {existing_count}")

        return created
