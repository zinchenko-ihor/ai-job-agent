from app.services.job_filter import JobFilter


def main():

    job_filter = JobFilter()

    tests = [
        # ---------------------------------------------------------
        # DEVOPS
        # ---------------------------------------------------------

        (
            "Middle DevOps Engineer",
            "Manage AWS, Kubernetes and Terraform infrastructure.",
            True,
        ),
        (
            "Senior DevOps Engineer",
            "AWS, Terraform, Docker and Kubernetes.",
            True,
        ),
        (
            "Senior Site Reliability Engineer",
            "Kubernetes, Linux, AWS.",
            True,
        ),
        (
            "Cloud Engineer",
            "AWS and Terraform infrastructure.",
            True,
        ),
        (
            "Platform Engineer",
            "Kubernetes and AWS platform.",
            True,
        ),
        (
            "Infrastructure Engineer",
            "Linux infrastructure and automation.",
            True,
        ),
        (
            "DevSecOps Engineer",
            "AWS, Kubernetes and security automation.",
            True,
        ),
        (
            "Systems Administrator",
            "Linux servers and infrastructure.",
            True,
        ),
        (
            "Cloud Operations Engineer",
            "AWS cloud infrastructure and monitoring.",
            True,
        ),

        # ---------------------------------------------------------
        # TECHNICAL SUPPORT + DEVOPS STACK
        # ---------------------------------------------------------

        (
            "Technical Support Engineer",
            "Linux, AWS, Docker and Kubernetes.",
            True,
        ),
        (
            "IT Support Engineer",
            "Linux administration, networking and monitoring.",
            True,
        ),
        (
            "Cloud Support Engineer",
            "AWS, Terraform and Kubernetes.",
            True,
        ),
        (
            "Production Support Engineer",
            "Linux, Docker, Jenkins and monitoring.",
            True,
        ),
        (
            "Application Support Engineer",
            "Kubernetes, Linux and CI/CD pipelines.",
            True,
        ),
        (
            "Technical Support Engineer",
            "Windows, Office 365 and Active Directory.",
            False,
        ),
        (
            "Customer Support Engineer",
            "CRM, Salesforce and customer service.",
            False,
        ),

        # ---------------------------------------------------------
        # UNRELATED
        # ---------------------------------------------------------

        (
            "Barista",
            "Prepare coffee and serve customers.",
            False,
        ),
        (
            "Sales Manager",
            "B2B sales and customer acquisition.",
            False,
        ),
        (
            "Backend Python Developer",
            "Develop APIs using Python and PostgreSQL.",
            False,
        ),
        (
            "Senior Backend Engineer",
            "Python, PostgreSQL, Docker and AWS.",
            False,
        ),
        (
            "Frontend Developer",
            "React, JavaScript and TypeScript.",
            False,
        ),
        (
            "Full Stack Developer",
            "React, Node.js, PostgreSQL and AWS.",
            False,
        ),
        (
            "Data Engineer",
            "Python, Spark, AWS and Kubernetes.",
            False,
        ),
        (
            "Machine Learning Engineer",
            "Python, AWS and Docker.",
            False,
        ),
        (
            "QA Automation Engineer",
            "Python, Selenium and Jenkins.",
            False,
        ),
        (
            "Software Engineer",
            "Python, Docker, Kubernetes and AWS.",
            False,
        ),
    ]

    passed = 0

    print("=== JOB FILTER TEST ===")

    for title, description, expected in tests:

        result = job_filter.is_relevant(
            title=title,
            description=description,
        )

        status = "PASS" if result == expected else "FAIL"

        if result == expected:
            passed += 1

        print(
            f"{status:4} | "
            f"{title:40} -> {result}"
        )

    print()
    print(
        f"Result: {passed}/{len(tests)} tests passed"
    )


if __name__ == "__main__":
    main()
