import re


class SkillExtractor:

    SKILLS = {
        "Python": ["python", "python3"],
        "Linux": ["linux", "ubuntu", "centos", "debian"],
        "AWS": ["aws", "amazon web services"],
        "Azure": ["azure", "microsoft azure"],
        "GCP": ["gcp", "google cloud", "google cloud platform"],
        "Docker": ["docker", "docker compose"],
        "Kubernetes": ["kubernetes", "k8s"],
        "Terraform": ["terraform"],
        "Ansible": ["ansible"],
        "Jenkins": ["jenkins"],
        "Git": ["git", "github", "gitlab"],
        "PostgreSQL": ["postgresql", "postgres"],
        "MySQL": ["mysql"],
        "MongoDB": ["mongodb", "mongo"],
        "Prometheus": ["prometheus"],
        "Grafana": ["grafana"],
        "ELK": ["elk", "elasticsearch", "logstash", "kibana"],
        "Helm": ["helm"],
        "Nginx": ["nginx"],
        "Apache2": ["apache2", "httpd"],
        "Bash": ["bash", "shell scripting", "shell script"],
        "CI/CD": ["ci/cd", "cicd", "continuous integration"],
    }

    def extract(
        self,
        title: str | None,
        description: str | None,
        tags: list[str] | None = None,
    ) -> list[str]:

        parts = [
            title or "",
            description or "",
            " ".join(tags or []),
        ]

        text = " ".join(parts).lower()

        found = []

        for skill, keywords in self.SKILLS.items():

            for keyword in keywords:

                pattern = r"\b" + re.escape(
                    keyword.lower()
                ) + r"\b"

                if re.search(pattern, text):
                    found.append(skill)
                    break

        return sorted(found)
