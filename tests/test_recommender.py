from app.jobs.recommender import JobRecommender


class FakeMatcher:
    def __init__(self, scores):
        self.scores = scores

    def match(self, profile, job):
        score = self.scores.get(job["title"], 0)

        return {
            "score": score,
            "reason": f"score {score}",
            "matched_skills": [],
            "missing_skills": [],
        }


def test_recommender_filters_low_score_jobs():
    jobs = [
        {
            "title": "DevOps Engineer",
            "description": "Docker AWS Linux",
        },
        {
            "title": "Java Developer",
            "description": "Java Spring",
        },
    ]

    matcher = FakeMatcher(
        {
            "DevOps Engineer": 80,
            "Java Developer": 20,
        }
    )

    recommender = JobRecommender(
        matcher=matcher
    )

    result = recommender.recommend(
        candidate_profile={},
        jobs=jobs,
    )

    assert len(result) == 1
    assert result[0]["job"]["title"] == "DevOps Engineer"
    assert result[0]["score"] == 80


def test_recommender_sorts_by_score_descending():
    jobs = [
        {
            "title": "Job A",
            "description": "Docker",
        },
        {
            "title": "Job B",
            "description": "AWS",
        },
        {
            "title": "Job C",
            "description": "Kubernetes",
        },
    ]

    matcher = FakeMatcher(
        {
            "Job A": 40,
            "Job B": 90,
            "Job C": 60,
        }
    )

    recommender = JobRecommender(
        matcher=matcher
    )

    result = recommender.recommend(
        candidate_profile={},
        jobs=jobs,
    )

    assert [
        item["job"]["title"]
        for item in result
    ] == [
        "Job B",
        "Job C",
        "Job A",
    ]


def test_recommender_respects_limit():
    jobs = [
        {
            "title": "Job A",
            "description": "Docker",
        },
        {
            "title": "Job B",
            "description": "AWS",
        },
        {
            "title": "Job C",
            "description": "Kubernetes",
        },
    ]

    matcher = FakeMatcher(
        {
            "Job A": 50,
            "Job B": 90,
            "Job C": 70,
        }
    )

    recommender = JobRecommender(
        matcher=matcher
    )

    result = recommender.recommend(
        candidate_profile={},
        jobs=jobs,
        limit=2,
    )

    assert len(result) == 2

    assert [
        item["job"]["title"]
        for item in result
    ] == [
        "Job B",
        "Job C",
    ]
