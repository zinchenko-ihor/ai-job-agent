from app.resume.parser import extract_text


PDF_PATH = "storage/resumes/723138866/resume.pdf"


def main():
    text = extract_text(PDF_PATH)

    print("=== RESUME TEXT ===")
    print(text)


if __name__ == "__main__":
    main()
