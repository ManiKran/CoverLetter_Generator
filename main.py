# main.py

import os
import pdfplumber
from dotenv import load_dotenv
from extract_skills import extract_skills_from_text
from generate_cover_letter import generate_cover_letter, match_skills
from docx_writer import save_cover_letter_to_docx

def read_pdf_text(path):
    try:
        with pdfplumber.open(path) as pdf:
            return "\n".join(page.extract_text() or "" for page in pdf.pages).strip()
    except Exception as e:
        raise RuntimeError(f"❌ Error reading resume PDF: {e}")

def read_txt(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read().strip()
    except Exception as e:
        raise RuntimeError(f"❌ Error reading job description: {e}")

def main():
    load_dotenv()

    print("\n📄 GPT-4o Cover Letter Generator (via GitHub-hosted LLM)\n")

    role = input("Enter the job role you're applying for: ").strip()
    company = input("Enter the company name: ").strip()
    resume_path = input("Path to your resume PDF: ").strip()
    jd_path = input("Path to job description TXT file: ").strip()

    try:
        resume_text = read_pdf_text(resume_path)
        jd_text = read_txt(jd_path)
    except Exception as e:
        print(e)
        return

    print("\n🔍 Extracting skills...")
    resume_skills = extract_skills_from_text(resume_text, "resume")
    jd_skills = extract_skills_from_text(jd_text, "job_description")
    matched = match_skills(resume_skills, jd_skills)
    print(f"✅ Matched Skills: {matched}\n")

    print("✍️ Generating cover letter...")
    letter = generate_cover_letter(resume_text, jd_text, matched, role, company)

    if not letter.strip():
        print("❌ No cover letter generated.")
        return

    print("\n💾 Saving cover letter to DOCX...")
    save_cover_letter_to_docx(letter, role, company)

if __name__ == "__main__":
    main()