import requests


class AIService:

    def __init__(
        self,
        model: str = "qwen2.5:3b",
        url: str = "http://localhost:11434/api/chat",
    ):
        self.model = model
        self.url = url

    def _chat(
        self,
        prompt: str,
    ) -> str:

        response = requests.post(
            self.url,
            json={
                "model": self.model,
                "messages": [
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                "stream": False,
            },
            timeout=120,
        )

        response.raise_for_status()

        data = response.json()

        return data["message"]["content"].strip()

    def extract_skills(
        self,
        text: str,
    ) -> list[str]:

        if not text.strip():
            return []

        prompt = f"""
Extract only technical skills from the job description.

Include:
- programming languages
- cloud platforms
- DevOps tools
- infrastructure tools
- databases
- operating systems
- CI/CD tools
- monitoring tools
- networking technologies
- technical frameworks

Do NOT include:
- soft skills
- education
- certifications
- job titles
- company names
- benefits
- salary
- locations
- generic adjectives
- UI/browser text
- navigation words
- duties without a technical technology/skill

Return only skill names.
One skill per line.
No explanations.
No numbering.

Job description:

{text}
"""

        content = self._chat(prompt)

        skills = []

        for line in content.splitlines():

            skill = line.strip()

            if not skill:
                continue

            # Remove common list markers
            skill = skill.lstrip("-*•").strip()

            # Remove accidental numbering: "1. Python"
            if "." in skill[:4]:
                prefix, value = skill.split(".", 1)

                if prefix.strip().isdigit():
                    skill = value.strip()

            if skill:
                skills.append(skill)

        return skills

    def generate_text(
        self,
        prompt: str,
    ) -> str:

        return self._chat(prompt)
