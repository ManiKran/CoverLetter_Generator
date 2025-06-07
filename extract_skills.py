# extract_skills.py

import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.environ["GITHUB_TOKEN"],
    base_url="https://models.github.ai/inference"
)

model_name = "openai/gpt-4o"

def extract_skills_from_text(text, source="resume"):
    prompt = f"""
Extract a list of technical and soft skills from the following {source} text. 
Return the skills as a Python list of strings. Do not include duplicates.

Text:
{text}
"""

    try:
        response = client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "system", "content": "You are an expert resume/job description parser."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=300
        )
        raw = response.choices[0].message.content.strip()

        # Try to safely evaluate it as a list
        skills = eval(raw) if raw.startswith("[") else []
        return [s.strip() for s in skills if isinstance(s, str)]

    except Exception as e:
        print(f"❌ Error extracting skills: {e}")
        return []