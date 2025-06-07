import os
from datetime import datetime
from openai import OpenAI
from dotenv import load_dotenv
from prompts.prompt_templates import get_system_prompt

load_dotenv()

# ✅ Official OpenAI API (make sure OPENAI_API_KEY is in your environment on Render)
client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

model_name = "gpt-4o"  # You can also use "gpt-3.5-turbo" to reduce cost

def match_skills(resume_skills, jd_skills):
    return list(set(resume_skills) & set(jd_skills))

def generate_cover_letter(resume_text, jd_text, matched_skills, role, company):
    system_prompt = get_system_prompt()
    today = datetime.today().strftime("%B %d, %Y")  # e.g., June 7, 2025

    user_prompt = f"""
Generate a personalized and concise cover letter for the role of "{role}" at "{company}".

Today's Date: {today}

Resume:
{resume_text}

Job Description:
{jd_text}

Matched Skills:
{matched_skills}

Only use the information provided. Do not invent details.
Use a professional tone and follow the format in the system prompt.
"""

    try:
        response = client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.7,
            max_tokens=600
        )
        return response.choices[0].message.content.strip()

    except Exception as e:
        print(f"❌ Error generating cover letter: {e}")
        return ""