import os
import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def screen_candidate(job_description: str, resume_text: str) -> dict:
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": """You are an expert recruiter. 
                Analyze the candidate resume against the job description.
                Return ONLY a JSON object with exactly these fields:
                {
                    "match_score": <number between 0 and 100>,
                    "reasoning": "<one paragraph explanation>",
                    "recommendation": "<exactly one of: hire, maybe, reject>"
                }
                No extra text. No markdown. Just the JSON object."""
            },
            {
                "role": "user",
                "content": f"Job Description: {job_description}\n\nResume: {resume_text}"
            }
        ]
    )
    
    raw = response.choices[0].message.content
    return json.loads(raw)