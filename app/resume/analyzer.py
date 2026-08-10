import json
import re

from app.ai.ollama_client import OllamaClient


class ResumeAnalyzer:

    def __init__(self):
        self.ai = OllamaClient()

    def analyze(
        self,
        resume_text: str,
    ) -> dict:

        if not resume_text.strip():
            return {}

        prompt = f"""
You are an experienced technical recruiter.

Analyze the candidate's CV and build a structured professional profile.

Return ONLY valid JSON.
Do not use markdown.
Do not add explanations.

Use exactly this structure:

{{
    "name": "",
    "location": "",
    "english_level": "",
    "target_roles": [],
    "seniority": "",
    "skills": [],
    "cloud": [],
    "operating_systems": [],
    "devops": [],
    "monitoring": [],
    "databases": [],
    "programming": [],
    "networking": [],
    "experience": [],
    "education": [],
    "courses": []
}}

Rules:

1. Extract information only from the CV.
2. Do not invent skills, technologies or experience.
3. Normalize obvious spelling mistakes.

Examples:

"Phyton" -> "Python"
"Git Hub" -> "GitHub"
"GitHub Action" -> "GitHub Actions"
"Conuence" -> "Confluence"
"cloude platforms" -> "cloud platforms"

4. Keep technical skills as separate items.
5. Do not include soft skills as technical skills.
6. Do not include job titles in the skills list.
7. target_roles must contain realistic roles based on the candidate's actual experience.
8. DevOps, Operations Engineer, System Administrator and Technical Support Engineer
   are valid target roles when supported by the CV.
9. Do not suggest unrelated roles only because the candidate knows a programming language.
10. seniority should be estimated from the candidate's actual professional experience.
11. If English level is specified, preserve it.
12. If the CV says "Intermediate (B1)", return "B1".
13. experience should contain the candidate's relevant work experience.
14. education should contain education entries.
15. courses should contain professional courses and certifications.
16. Return empty arrays when information is not available.

Candidate CV:

{resume_text}
"""

        response = self.ai.generate(prompt)

        return self._parse_response(response)

    @staticmethod
    def _parse_response(
        response: str,
    ) -> dict:

        content = response.strip()

        # Remove markdown code fences if Ollama
        # accidentally returns them.
        content = re.sub(
            r"^```json\s*",
            "",
            content,
            flags=re.IGNORECASE,
        )

        content = re.sub(
            r"\s*```$",
            "",
            content,
        )

        try:
            data = json.loads(content)

        except json.JSONDecodeError as exc:
            raise ValueError(
                "Ollama returned invalid JSON:\n"
                f"{content}"
            ) from exc

        if not isinstance(data, dict):
            raise ValueError(
                "Resume analysis must return a JSON object."
            )

        return data
