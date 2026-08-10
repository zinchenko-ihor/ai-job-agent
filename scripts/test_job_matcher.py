from app.jobs.matcher import JobMatcher


PROFILE = {
    "name": "Ihor Zinchenko",
    "location": "Kyiv, Ukraine",
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


TEST_JOBS = [
    {
        "title": "Middle DevOps Engineer",
        "description": """
        AWS, Linux, Docker, Jenkins, Ansible,
        GitHub Actions, Terraform, Kubernetes.
        English B1 required.
        """,
    },
    {
        "title": "Technical Support Engineer",
        "description": """
        Linux, Windows Server, AWS, Docker,
        PostgreSQL, Nginx, monitoring.
        English B1 required.
        """,
    },
    {
        "title": "Cloud Operations Engineer",
        "description": """
        AWS, Linux, Terraform, Kubernetes,
        Docker and CloudWatch.
        English B1.
        """,
    },
    {
        "title": "Senior Backend Python Developer",
        "description": """
        Python, PostgreSQL, Django and REST APIs.
        English B2 required.
        """,
    },
    {
        "title": "Frontend Developer",
        "description": """
        JavaScript, React, TypeScript and CSS.
        English B2 required.
        """,
    },
    {
        "title": "Data Engineer",
        "description": """
        Python, SQL, Spark, Airflow and BigQuery.
        English B2 required.
        """,
    },
]


def main():

    matcher = JobMatcher()

    print("=== JOB MATCHER TEST ===")

    for job in TEST_JOBS:

        result = matcher.match(
            profile=PROFILE,
            job=job,
        )

        print()
        print("=" * 60)
        print(f"JOB: {job['title']}")
        print(f"MATCH: {result['matched']}")
        print(f"SCORE: {result['score']}%")
        print(f"REASON: {result['reason']}")

        print(
            "MATCHED SKILLS:",
            ", ".join(
                result["matched_skills"]
            )
            or "none",
        )

        print(
            "MISSING SKILLS:",
            ", ".join(
                result["missing_skills"]
            )
            or "none",
        )


if __name__ == "__main__":
    main()
