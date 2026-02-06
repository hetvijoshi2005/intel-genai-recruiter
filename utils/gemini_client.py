import google.generativeai as genai
import os
import json
from dotenv import load_dotenv

load_dotenv()

# Configure API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Configuration to force JSON output (Crucial for the App)
generation_config = {
    "temperature": 0.1,
    "response_mime_type": "application/json"
}

model = genai.GenerativeModel('gemini-2.5-flash', generation_config=generation_config)

def analyze_candidate(resume_text, job_description):
    """
    Analyzes the candidate against the JD and returns structured JSON.
    """
    prompt = f"""
    You are an expert Technical Recruiter and Bias Auditor.
    
    ### JOB DESCRIPTION:
    {job_description}
    
    ### CANDIDATE RESUME (Compressed):
    {resume_text}
    
    ### INSTRUCTIONS:
    Analyze the candidate and return a JSON object with EXACTLY these fields:
    1. "candidate_name": Extract from resume (or "Unknown").
    2. "match_score": Integer (0-100).
    3. "technical_skills_match": List of matching skills.
    4. "missing_skills": List of critical missing skills.
    5. "bias_audit": {{ 
         "flagged": Boolean (True if sensitive info like age/gender/marital status is prominent),
         "details": "String explaining potential bias triggers found"
       }}
    6. "interview_questions": List of 3 technical questions targeting their missing skills.
    7. "summary": A 2-sentence professional summary.

    Return ONLY valid JSON.
    """
    
    try:
        response = model.generate_content(prompt)
        # Parse the text to ensure it's valid JSON objects
        return json.loads(response.text)
    except Exception as e:
        # Fallback in case of error
        return {
            "candidate_name": "Error Parsing",
            "match_score": 0,
            "summary": f"AI Error: {str(e)}",
            "bias_audit": {"flagged": False, "details": "N/A"},
            "interview_questions": [],
            "technical_skills_match": [],
            "missing_skills": []
        }
    
    
def generate_bias_report(candidates_data):
    """
    Generates a simple Markdown report of all candidates and bias flags.
    """
    report = "# 🛡️ Recruitment Bias Audit Report\n\n"
    report += "| Candidate | Score | Bias Flagged | Notes |\n"
    report += "|-----------|-------|--------------|-------|\n"
    
    for c in candidates_data:
        flag = "🔴 YES" if c['bias_audit']['flagged'] else "🟢 NO"
        report += f"| {c['candidate_name']} | {c['match_score']} | {flag} | {c['bias_audit']['details']} |\n"
    
    return report