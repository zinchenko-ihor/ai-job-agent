from pathlib import Path

from app.resume.parser import extract_text
from app.resume.analyzer import ResumeAnalyzer


RESUME_PATH = Path(
    "storage/resumes/723138866/resume.pdf"
)


def main():

    print("=== RESUME ANALYSIS ===")

    if not RESUME_PATH.exists():
        raise FileNotFoundError(
            f"Resume not found: {RESUME_PATH}"
        )

    # Step 1. Extract text from PDF.
    resume_text = extract_text(
        RESUME_PATH
    )

    print(
        f"Extracted characters: {len(resume_text)}"
    )

    # Step 2. Analyze resume using Ollama.
    analyzer = ResumeAnalyzer()

    profile = analyzer.analyze(
        resume_text
    )

    # Step 3. Display structured profile.
    print("\n=== CANDIDATE PROFILE ===")

    for key, value in profile.items():

        print(f"\n{key}:")

        if isinstance(value, list):

            for item in value:
                print(f"  - {item}")

        else:

            print(f"  {value}")


if __name__ == "__main__":
    main()
