from app.ai.ollama_client import OllamaClient


def main():
    client = OllamaClient()

    description = """
    We are looking for a Middle DevOps Engineer.

    Requirements:
    - Linux administration
    - AWS
    - Docker
    - Kubernetes
    - Terraform
    - Jenkins
    - Prometheus
    - Grafana
    - PostgreSQL
    - Python

    Experience with CI/CD pipelines is required.
    """

    skills = client.extract_skills(description)

    print("=== AI SKILLS ===")

    for skill in skills:
        print(f"- {skill}")


if __name__ == "__main__":
    main()
