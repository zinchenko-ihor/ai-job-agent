from app.ai.ollama_client import OllamaClient


def main():

    client = OllamaClient()

    prompt = """
You are a job recruitment assistant.

Extract technical skills from the following job description.

Return only a comma-separated list of skills.

Job description:

We are looking for a DevOps Engineer with experience
in AWS, Kubernetes, Docker, Terraform and Linux.
Experience with Jenkins and Prometheus is also required.
"""

    result = client.generate(prompt)

    print("=== AI RESPONSE ===")
    print(result)


if __name__ == "__main__":
    main()
