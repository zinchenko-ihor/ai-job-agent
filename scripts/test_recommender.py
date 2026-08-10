from app.jobs.recommender import JobRecommender


CANDIDATE_PROFILE = {
    "name": "Ihor Zinchenko",
    "location": "Kyiv, Ukraine, 02000",
    "english_level": "B1",

    "target_roles": [
        "IT Operations Engineer",
        "Technical Support Engineer",
        "System Administrator",
    ],

    "seniority": "Mid",

    "skills": [
        "ADDS",
        "DNS",
        "DHCP",
        "VPN",
        "VMWare ESXi",
        "VMware Workstation",
        "Windows Server 2008 - 2019",
        "Ubuntu Server 18.04 - 24.04",
        "Oracle Linux 9",
        "Prometheus",
        "Grafana",
        "Kibana",
        "Zabbix",
        "Git",
        "GitHub",
        "Jira",
        "Confluence",
        "Docker",
        "AWS EC2",
        "IAM",
        "S3",
        "CloudWatch",
        "SG",
        "RDS",
        "MySQL",
        "MariaDB",
        "PostgreSQL",
        "MSSQL",
        "Python",
        "Bash",
        "PowerShell",
        "Jenkins",
        "Ansible",
        "GitHub Actions",
        "Nginx",
    ],
}


JOBS = [
    {
        "title": "Middle DevOps Engineer",
        "description": """
        We are looking for a Middle DevOps Engineer.

        Requirements:
        AWS, Docker, Jenkins, Ansible,
        GitHub Actions, Linux, Terraform
        and Kubernetes.

        English level: B1.
        """,
    },
    {
        "title": "Technical Support Engineer",
        "description": """
        Technical Support Engineer position.

        Experience with Linux, Windows Server,
        Docker, Nginx and AWS is required.

        English level: B1.
        """,
    },
    {
        "title": "Cloud Operations Engineer",
        "description": """
        Cloud Operations Engineer.

        Work with AWS, CloudWatch, Docker,
        Kubernetes, Linux and Terraform.

        English level: B1.
        """,
    },
    {
        "title": "Senior Backend Python Developer",
        "description": """
        Senior Backend Python Developer.

        Python, FastAPI, PostgreSQL and REST APIs.

        English level: B2.
        """,
    },
    {
        "title": "Frontend Developer",
        "description": """
        Frontend Developer.

        React, TypeScript, JavaScript and CSS.

        English level: B2.
        """,
    },
    {
        "title": "Data Engineer",
        "description": """
        Data Engineer.

        Python, Spark, Airflow, SQL and data pipelines.

        English level: B2.
        """,
    },
]


def main() -> None:

    recommender = JobRecommender()

    recommendations = recommender.recommend(
        profile=CANDIDATE_PROFILE,
        jobs=JOBS,
        limit=10,
    )

    print("=== JOB RECOMMENDER TEST ===")
    print()

    print(
        f"Candidate: {CANDIDATE_PROFILE['name']}"
    )

    print(
        f"English: {CANDIDATE_PROFILE['english_level']}"
    )

    print()

    print(
        f"Recommendations: {len(recommendations)}"
    )

    print()

    for index, recommendation in enumerate(
        recommendations,
        start=1,
    ):

        job = recommendation["job"]

        print("=" * 60)

        print(
            f"{index}. {job['title']}"
        )

        print(
            f"MATCH: {recommendation['score']}%"
        )

        print(
            f"REASON: {recommendation['reason']}"
        )

        matched = recommendation[
            "matched_skills"
        ]

        missing = recommendation[
            "missing_skills"
        ]

        print(
            "MATCHED:",
            ", ".join(matched)
            if matched
            else "none",
        )

        print(
            "MISSING:",
            ", ".join(missing)
            if missing
            else "none",
        )

    print("=" * 60)


if __name__ == "__main__":
    main()
