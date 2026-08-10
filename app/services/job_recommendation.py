from __future__ import annotations

from typing import Any

from sqlalchemy.orm import Session

from app.jobs.recommender import JobRecommender
from app.repositories.job import JobRepository
from app.repositories.job_recommendation import (
    JobRecommendationRepository,
)
from app.resume.profile import ResumeProfileRepository


class JobRecommendationService:

    def __init__(
        self,
        session: Session,
    ):

        self.session = session

        self.job_repository = JobRepository(
            session
        )

        self.recommendation_repository = (
            JobRecommendationRepository(
                session
            )
        )

        self.profile_repository = (
            ResumeProfileRepository()
        )

        self.recommender = JobRecommender()



    # ==================================================
    # Telegram entry point
    # ==================================================

    def get_recommendations(
        self,
        user_id: int,
        limit: int = 5,
        force_refresh: bool = False,
    ) -> list[dict[str, Any]]:


        # -----------------------------
        # Cache
        # -----------------------------

        if not force_refresh:

            cached = (
                self.recommendation_repository
                .get_recent(
                    user_id=user_id,
                    hours=24,
                )
            )


            if cached:

                print(
                    "JOB CACHE USED"
                )


                return [
                    self._serialize_cached(
                        item
                    )
                    for item in cached[:limit]
                ]



        # -----------------------------
        # Generate
        # -----------------------------

        return self.recommend_for_user(
            user_id=user_id,
            limit=limit,
        )



    # ==================================================
    # Recommendation generation
    # ==================================================

    def recommend_for_user(
        self,
        user_id: int,
        limit: int = 5,
    ) -> list[dict[str, Any]]:


        profile = (
            self.profile_repository
            .get(user_id)
        )


        if not profile:

            raise FileNotFoundError(
                "Resume profile not found"
            )



        print(
            "PROFILE LOADED"
        )



        db_jobs = (
            self.job_repository
            .get_recent_jobs_by_source(
                source_name="DOU",
                max_age_days=2,
            )
        )


        print(
            "JOBS:",
            len(db_jobs)
        )



        if not db_jobs:
            return []



        jobs = []


        for job in db_jobs:

            jobs.append(
                {
                    "id": job.id,
                    "title": job.title,
                    "company": job.company,
                    "location": job.location,
                    "description": job.description or "",
                    "url": job.url,
                    "published_at": job.published_at,
                }
            )



        results = (
            self.recommender
            .recommend(
                candidate_profile=profile,
                jobs=jobs,
                limit=limit,
            )
        )



        print(
            "MATCHED:",
            len(results)
        )



        if not results:

            return []



        # remove old cache

        self.recommendation_repository\
            .delete_for_user(
                user_id
            )



        response = []



        for item in results:


            job = item["job"]


            self.recommendation_repository.create(

                user_id=user_id,

                job_id=job["id"],

                score=item["score"],

                reason=item["reason"],

                matched_skills=item[
                    "matched_skills"
                ],

                missing_skills=item[
                    "missing_skills"
                ],
            )



            response.append(
                {
                    "title": job["title"],
                    "company": job["company"],
                    "location": job["location"],
                    "url": job["url"],
                    "score": item["score"],
                    "reason": item["reason"],
                    "matched_skills": item[
                        "matched_skills"
                    ],
                }
            )



        self.session.commit()


        return response



    # ==================================================
    # Cache serializer
    # ==================================================

    @staticmethod
    def _serialize_cached(
        item,
    ) -> dict[str, Any]:

        return {

            "title": item.job.title,

            "company": item.job.company,

            "location": item.job.location,

            "url": item.job.url,

            "score": item.score,

            "reason": item.reason,

            "matched_skills":
                item.matched_skills,

        }
