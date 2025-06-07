# generate_cover_letter.py

import os
import openai
from dotenv import load_dotenv
from prompts.prompt_templates import get_system_prompt

load_dotenv()

# Use your working GitHub-hosted GPT-4o setup
openai.api_key = os.environ["GITHUB_TOKEN"]
openai.api_base = "https://models.github.ai/inference"
model_name = "openai/gpt-4o"

def match_skills(resume_skills, jd_skills):
    return list(set(resume_skills) & set(jd_skills))

def generate_cover_letter(resume_text, jd_text, matched_skills, role, company):
    system_prompt = get_system_prompt()

    user_prompt = f"""
Generate a personalized and concise cover letter for the role of "{role}" at "{company}".

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
        response = openai.ChatCompletion.create(
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