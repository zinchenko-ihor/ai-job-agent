SKILL_ALIASES = {
    # DevOps
    "devops": "DevOps",
    "devops engineer": "DevOps",
    "devops engineering": "DevOps",

    # Linux
    "linux": "Linux",
    "linux administration": "Linux",
    "linux administrator": "Linux",
    "linux administration skills": "Linux",

    # CI/CD
    "ci/cd": "CI/CD",
    "ci/cd pipelines": "CI/CD",
    "ci_cd": "CI/CD",
    "ci-cd": "CI/CD",
    "ci cd": "CI/CD",

    # Cloud
    "amazon web services": "AWS",
    "aws cloud": "AWS",

    # Kubernetes
    "k8s": "Kubernetes",

    # Docker
    "docker containerization": "Docker",
    "containerization (docker)": "Docker",

    # PostgreSQL
    "postgres": "PostgreSQL",
    "postgresql database": "PostgreSQL",

    # MongoDB
    "mongodb database": "MongoDB",

    # MySQL
    "mysql database": "MySQL",

    # JavaScript
    "javascript": "JavaScript",
    "js": "JavaScript",

    # Node.js
    "nodejs": "Node.js",
    "node.js": "Node.js",

    # Shell
    "shell scripting": "Shell",
    "shell_scripting": "Shell",
    "bash scripting": "Bash",
}


def normalize_skill(name: str) -> str:
    """
    Normalize AI-generated skill names to canonical names.
    """

    if not name:
        return ""

    key = " ".join(
        name.strip().lower().split()
    )

    return SKILL_ALIASES.get(
        key,
        name.strip(),
    )
