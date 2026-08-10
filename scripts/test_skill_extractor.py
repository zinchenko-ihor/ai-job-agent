from app.extractors.skills import SkillExtractor


def main():
    extractor = SkillExtractor()

    title = "Middle DevOps Engineer"

    description = """
    We are looking for a DevOps Engineer with experience
    in AWS, Kubernetes, Docker and Terraform.

    Experience with Linux, Jenkins and Prometheus
    would be a plus.
    """

    skills = extractor.extract(
        title=title,
        description=description,
    )

    print("Detected skills:")

    for skill in skills:
        print(f"- {skill}")


if __name__ == "__main__":
    main()
