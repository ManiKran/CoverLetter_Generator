# extract_skills.py

import os
import openai
from dotenv import load_dotenv

load_dotenv()

# Your working GitHub-hosted config
openai.api_key = os.environ["GITHUB_TOKEN"]
openai.api_base = "https://models.github.ai/inference"
model_name = "openai/gpt-4o"

def extract_skills_from_text(input_text: str, content_type: str = "resume") -> list:
    user_prompt = (
        f"Here is a {content_type.replace('_', ' ')}:\n\n{input_text}\n\n"
        "Extract all relevant technical and soft skills as a Python list."
    )

    try:
        response = openai.ChatCompletion.create(
            model=model_name,
            messages=[
                {"role": "system", "content": "You are a helpful assistant that extracts skills from resumes and job descriptions."},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.2,
            max_tokens=300
        )

        result = response.choices[0].message.content.strip()
        return eval(result) if result.startswith("[") else []

    except Exception as e:
        print(f"❌ Error extracting skills: {e}")
        return []