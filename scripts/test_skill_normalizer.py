from app.ai.skill_normalizer import SkillNormalizer


def main():

    normalizer = SkillNormalizer()

    skills = [
        "AWS",
        "Amazon Web Services",
        "K8s",
        "Kubernetes",
        "Postgres",
        "PostgreSQL",
        "Python3",
        "Docker Compose",
        "GitHub",
        "CI/CD",
    ]

    result = normalizer.normalize_many(skills)

    print("=== NORMALIZED SKILLS ===")

    for skill in result:
        print(f"- {skill}")


if __name__ == "__main__":
    main()
