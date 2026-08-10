from app.services.ai import AIService


def main():

    ai = AIService()


    skills = ai.extract_skills(
        """
        We need DevOps engineer.

        Requirements:
        AWS,
        Kubernetes,
        Docker,
        Terraform,
        Linux administration.
        """
    )


    print("=== AI SKILLS ===")

    for skill in skills:
        print("-", skill)



if __name__ == "__main__":
    main()
