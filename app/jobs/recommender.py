from __future__ import annotations

from typing import Any

from app.jobs.matcher import JobMatcher


class JobRecommender:
    """
    Selects best jobs for candidate profile.

    Flow:
    - Run deterministic matcher
    - Calculate score
    - Keep all jobs with meaningful score
    - Sort descending
    - Return TOP N

    Designed for Telegram recommendations.
    """

    MIN_SCORE = 25


    def __init__(
        self,
        matcher: JobMatcher | None = None,
    ):
        self.matcher = matcher or JobMatcher()



    def recommend(
        self,
        candidate_profile: dict[str, Any],
        jobs: list[dict[str, Any]],
        limit: int = 5,
    ) -> list[dict[str, Any]]:


        recommendations = []


        for job in jobs:

            try:

                result = self.matcher.match(
                    profile=candidate_profile,
                    job=job,
                )


            except Exception as e:

                print(
                    f"MATCH ERROR "
                    f"{job.get('title')}: {e}"
                )

                continue



            score = result.get(
                "score",
                0
            )


            #
            # Do not drop everything.
            # Keep reasonable matches.
            #
            if score < self.MIN_SCORE:
                continue



            recommendations.append(
                {
                    "job": job,

                    "score": score,

                    "reason": result.get(
                        "reason",
                        "Matched by profile",
                    ),

                    "matched_skills": result.get(
                        "matched_skills",
                        [],
                    ),

                    "missing_skills": result.get(
                        "missing_skills",
                        [],
                    ),

                }
            )



        recommendations.sort(
            key=lambda item: item["score"],
            reverse=True,
        )


        return recommendations[:limit]
