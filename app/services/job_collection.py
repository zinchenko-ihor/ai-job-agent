from datetime import datetime, timezone, timedelta

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.collectors.dou import DOUCollector
from app.parsers.dou import DOUJobParser

from app.repositories.job import JobRepository
from app.repositories.job_source import JobSourceRepository

from app.jobs.fresh_filter import FreshJobFilter

from app.models.job import Job


class JobCollectionService:

    SOURCE_NAME = "DOU"
    SOURCE_URL = "https://jobs.dou.ua"


    def __init__(
        self,
        session: Session,
    ):

        self.session = session

        self.job_repository = (
            JobRepository(session)
        )

        self.source_repository = (
            JobSourceRepository(session)
        )

        self.fresh_filter = (
            FreshJobFilter(
                max_age_days=2
            )
        )


    # =====================================================
    # CACHE CHECK
    # =====================================================

    def needs_update(
        self,
        hours: int = 6,
    ) -> bool:
        """
        Check if DOU data should be refreshed.

        Refresh only if:
        - no jobs exist
        - last collection older than X hours
        """


        last_job = self.session.scalar(
            select(Job)
            .order_by(
                Job.collected_at.desc()
            )
            .limit(1)
        )


        if not last_job:
            return True


        if not last_job.collected_at:
            return True


        now = datetime.now(
            timezone.utc
        )


        delta = (
            now
            -
            last_job.collected_at
        )


        return (
            delta
            >
            timedelta(
                hours=hours
            )
        )



    # =====================================================
    # DOU COLLECTION
    # =====================================================


    def collect_dou(
        self,
        category: str = "devops",
    ) -> dict:


        source = (
            self.source_repository
            .get_or_create(
                name=self.SOURCE_NAME,
                base_url=self.SOURCE_URL,
            )
        )


        collector = DOUCollector()


        created = 0
        existing = 0
        fresh = 0
        stale = 0


        try:

            raw_pages = (
                collector.fetch_jobs(
                    category=category,
                )
            )


            parsed_jobs = []


            for raw_page in raw_pages:

                html = raw_page.get(
                    "html"
                )


                if not html:
                    continue


                jobs = (
                    DOUJobParser.parse(
                        html
                    )
                )


                parsed_jobs.extend(
                    jobs
                )



            for parsed_job in parsed_jobs:


                # -----------------------------------------
                # Fresh filter
                # -----------------------------------------


                if not self.fresh_filter.is_fresh(
                    parsed_job["published_at"]
                ):

                    stale += 1
                    continue



                fresh += 1



                # -----------------------------------------
                # Existing check
                # -----------------------------------------


                existing_job = (
                    self.job_repository
                    .get_by_external_id(
                        source_id=source.id,
                        external_id=
                        parsed_job["external_id"],
                    )
                )


                if existing_job:

                    existing += 1

                    continue



                # -----------------------------------------
                # Save job
                # -----------------------------------------


                self.job_repository.create(
                    source_id=source.id,
                    **parsed_job,
                )


                created += 1



            self.session.commit()



            return {

                "source": self.SOURCE_NAME,

                "fetched": len(
                    parsed_jobs
                ),

                "fresh": fresh,

                "stale": stale,

                "created": created,

                "existing": existing,

            }



        except Exception:


            self.session.rollback()

            raise



        finally:

            collector.close()
