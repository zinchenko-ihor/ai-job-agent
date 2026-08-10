from app.jobs.matcher import JobMatcher


def test_job_match_by_skills():
    matcher = JobMatcher()

    profile = {
        "target_roles": [
            "DevOps Engineer",
        ],
        "seniority": "Mid",
        "english_level": "B1",
        "skills": [
            "Python",
            "Docker",
            "AWS",
        ],
        "devops": [
            "Docker",
        ],
        "cloud": [
            "AWS",
        ],
        "monitoring": [],
        "databases": [],
        "operating_systems": [
            "Ubuntu Server",
        ],
        "networking": [],
    }

    job = {
        "title": "DevOps Engineer",
        "description": """
        We are looking for a DevOps Engineer.
        Requirements:
        Docker, AWS, Python and Linux.
        English B1.
        """,
    }

    result = matcher.match(
        profile=profile,
        job=job,
    )

    assert result["matched"] is True
    assert result["score"] > 0

    assert "docker" in result["matched_skills"]
    assert "aws" in result["matched_skills"]
    assert "python" in result["matched_skills"]


def test_job_rejected_for_english_above_b1():
    matcher = JobMatcher()

    profile = {
        "target_roles": [
            "DevOps Engineer",
        ],
        "seniority": "Mid",
        "english_level": "B1",
        "skills": [
            "Docker",
            "AWS",
        ],
        "devops": [
            "Docker",
        ],
        "cloud": [
            "AWS",
        ],
        "monitoring": [],
        "databases": [],
        "operating_systems": [],
        "networking": [],
    }

    job = {
        "title": "DevOps Engineer",
        "description": """
        Requirements:
        Docker, AWS.
        English C1 required.
        """,
    }

    result = matcher.match(
        profile=profile,
        job=job,
    )

    assert result["matched"] is False
    assert result["score"] == 0
    assert result["reason"] == "English level above B1"
