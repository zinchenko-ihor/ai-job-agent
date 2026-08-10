from app.db.session import SessionLocal
from app.services.ai_skill import AISkillService


def main():

    session = SessionLocal()

    try:
        service = AISkillService(session)

        description = """
        We are looking for a Middle DevOps Engineer to join our team.

        Requirements:
        - 2+ years of experience with Linux administration
        - AWS cloud experience
        - Docker and Kubernetes
        - Terraform for infrastructure as code
        - Jenkins and GitHub Actions for CI/CD
        - Prometheus and Grafana for monitoring
        - PostgreSQL database experience
        - Bash and Python scripting

        Responsibilities:
        - Maintain Linux servers
        - Build CI/CD pipelines
        - Deploy applications to Kubernetes
        - Manage AWS infrastructure
        - Monitor production systems
        """

        skills = service.ai.extract_skills(description)

        print("=== AI DETECTED SKILLS ===")

        for skill in skills:
            print(f"- {skill}")

    finally:
        session.close()


if __name__ == "__main__":
    main()
