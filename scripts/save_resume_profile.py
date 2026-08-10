from app.resume.parser import extract_text
from app.resume.analyzer import ResumeAnalyzer
from app.resume.profile import ResumeProfileRepository


USER_ID = 723138866


def main():
    resume_path = (
        f"storage/resumes/{USER_ID}/resume.pdf"
    )

    print("=== RESUME PROFILE CREATION ===")
    print()
    print("Reading resume...")

    resume_text = extract_text(
        resume_path
    )

    print(
        f"Extracted characters: "
        f"{len(resume_text)}"
    )

    print()
    print(
        "Analyzing resume with Ollama..."
    )
    print(
        "This may take some time..."
    )

    analyzer = ResumeAnalyzer()

    profile = analyzer.analyze(
        resume_text
    )

    repository = ResumeProfileRepository()

    path = repository.save(
        USER_ID,
        profile,
    )

    print()
    print("=== PROFILE SAVED ===")
    print(f"File: {path}")
    print()
    print(
        f"Name: "
        f"{profile.get('name')}"
    )
    print(
        f"English: "
        f"{profile.get('english_level')}"
    )
    print(
        f"Seniority: "
        f"{profile.get('seniority')}"
    )
    print()
    print("Target roles:")

    for role in profile.get(
        "target_roles",
        [],
    ):
        print(f"  - {role}")

    print()
    print("Skills:")

    for skill in profile.get(
        "skills",
        [],
    ):
        print(f"  - {skill}")


if __name__ == "__main__":
    main()
