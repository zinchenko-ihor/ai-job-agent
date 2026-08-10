class SkillNormalizer:

    ALIASES = {
        "amazon web services": "AWS",
        "aws cloud": "AWS",

        "k8s": "Kubernetes",
        "kubernetes cluster": "Kubernetes",

        "postgres": "PostgreSQL",
        "postgres db": "PostgreSQL",

        "python3": "Python",

        "docker compose": "Docker",

        "gitlab": "Git",
        "github": "Git",

        "google cloud platform": "GCP",
        "google cloud": "GCP",

        "microsoft azure": "Azure",

        "cicd": "CI/CD",
        "ci cd": "CI/CD",
    }

    def normalize(self, skill: str) -> str:

        normalized = skill.strip()

        key = normalized.lower()

        return self.ALIASES.get(
            key,
            normalized,
        )

    def normalize_many(
        self,
        skills: list[str],
    ) -> list[str]:

        normalized = {
            self.normalize(skill)
            for skill in skills
            if skill.strip()
        }

        return sorted(normalized)
