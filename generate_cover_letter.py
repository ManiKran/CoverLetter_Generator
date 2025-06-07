import os
from datetime import datetime
import httpx
from dotenv import load_dotenv
from prompts.prompt_templates import get_system_prompt

load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
BASE_URL = "https://models.github.ai/inference"

HEADERS = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Content-Type": "application/json"
}

def generate_cover_letter(resume_text, jd_text, full_name, email, phone, linkedin):
    today = datetime.today().strftime("%B %d, %Y")
    system_prompt = get_system_prompt()

    user_prompt = f"""
Generate a personalized and concise cover letter for the role of "{jd_text[:40]}..." at the company.

Today's Date: {today}

Candidate Info:
Full Name: {full_name}
Email: {email}
Phone: {phone}
LinkedIn: {linkedin if linkedin else 'N/A'}

Resume:
{resume_text}

Job Description:
{jd_text}

Only use the information provided. Do not invent details.
Use a professional tone and follow the format in the system prompt.
"""

    payload = {
        "model": "openai/gpt-4o",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "temperature": 0.7,
        "max_tokens": 700
    }

    try:
        response = httpx.post(BASE_URL, json=payload, headers=HEADERS, timeout=60)
        response.raise_for_status()
        result = response.json()
        content = result["choices"][0]["message"]["content"].strip()

        # Save as DOCX file
        from docx_writer import write_docx
        output_path = "outputs/latest_cover_letter.docx"
        write_docx(content, output_path)

        return output_path, content

    except Exception as e:
        print(f"❌ Error generating cover letter: {e}")
        raise e