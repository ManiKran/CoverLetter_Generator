# main.py

import os
import pdfplumber
from dotenv import load_dotenv
from extract_skills import extract_skills_from_text
from generate_cover_letter import generate_cover_letter, match_skills
from docx_writer import save_cover_letter

load_dotenv()

def extract_text_from_pdf(pdf_path):
    try:
        with pdfplumber.open(pdf_path) as pdf:
            text = "\n".join(page.extract_text() or "" for page in pdf.pages)
        return text
    except Exception as e:
        print(f"❌ Error reading PDF: {e}")
        return ""

def read_txt_file(file_path):
    try:
        with open(file_path, "r") as file:
            return file.read()
    except Exception as e:
        print(f"❌ Error reading TXT file: {e}")
        return ""

def main():
    print("\n📄 GPT-4o Cover Letter Generator (via GitHub-hosted LLM)\n")

    role = input("Enter the job role you're applying for: ").strip()
    company = input("Enter the company name: ").strip()
    resume_path = input("Path to your resume PDF: ").strip()
    jd_path = input("Path to job description TXT file: ").strip()

    full_name = input("Your full name: ").strip()
    email = input("Your email: ").strip()
    phone = input("Your phone number: ").strip()
    linkedin = input("Your LinkedIn URL: ").strip()

    print("\n🔍 Extracting skills...")

    resume_text = extract_text_from_pdf(resume_path)
    jd_text = read_txt_file(jd_path)

    resume_skills = extract_skills_from_text(resume_text, source="resume")
    jd_skills = extract_skills_from_text(jd_text, source="job description")
    matched = match_skills(resume_skills, jd_skills)

    print(f"\n✅ Matched Skills: {matched}\n")

    print("✍️ Generating cover letter...\n")
    cover_letter = generate_cover_letter(resume_text, jd_text, matched, role, company)

    if cover_letter:
        filename = f"outputs/cover_letter_{role.replace(' ', '_')}_{company.replace(' ', '_')}.docx"
        os.makedirs("outputs", exist_ok=True)
        save_cover_letter(cover_letter, filename, full_name, email, phone, linkedin)
        print(f"✅ Cover letter saved to: {filename}")
    else:
        print("❌ No cover letter generated.")

if __name__ == "__main__":
    main()