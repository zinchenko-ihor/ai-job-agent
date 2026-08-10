import json

from ollama import Client

from app.core.config import settings


class OllamaClient:

    def __init__(
        self,
        host: str | None = None,
        model: str | None = None,
    ):
        self.host = host or settings.ollama_host
        self.model = model or settings.ollama_model

        self.client = Client(
            host=self.host
        )

    def generate(
        self,
        prompt: str,
    ) -> str:

        response = self.client.chat(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
        )

        return response["message"]["content"]

    def extract_skills(
        self,
        text: str,
    ) -> list[str]:

        prompt = f"""
You are a technical recruitment assistant.

Extract technical skills from the job description below.

Return ONLY valid JSON in exactly this format:

{{
    "skills": ["skill1", "skill2", "skill3"]
}}

Rules:

- Include programming languages, frameworks, databases,
  cloud platforms, DevOps tools and infrastructure technologies.
- Do not include soft skills.
- Do not include job titles.
- Do not include explanations.
- Return an empty list if no technical skills are found.

Job description:

{text}
"""

        response = self.client.chat(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            format="json",
        )

        content = response["message"]["content"]

        data = json.loads(content)

        skills = data.get(
            "skills",
            [],
        )

        if not isinstance(skills, list):
            return []

        return [
            str(skill).strip()
            for skill in skills
            if str(skill).strip()
        ]
