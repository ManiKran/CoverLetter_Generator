import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

# ✅ Use OpenAI's official endpoint (Render-friendly)
client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

model_name = "gpt-4o"  # or "gpt-3.5-turbo" if needed

def extract_skills_from_text(text, source="resume"):
    prompt = f"""
Extract a list of technical and soft skills from the following {source} text. 
Return the skills as a valid Python list of strings (e.g., ["Python", "Teamwork", "SQL"]).
Do not include duplicates. Only include individual skill names.

Text:
{text}
"""

    try:
        response = client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "system", "content": "You are an expert in analyzing resumes and job descriptions to extract relevant skills."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=300
        )

        raw = response.choices[0].message.content.strip()
        skills = eval(raw) if raw.startswith("[") else []

        return [s.strip() for s in skills if isinstance(s, str)]

    except Exception as e:
        print(f"❌ Error extracting skills: {e}")
        return []