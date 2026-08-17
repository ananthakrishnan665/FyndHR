import os
import json
from openai import OpenAI


# ============================================================
# OPENAI CLIENT
# ============================================================

def get_client():
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        raise RuntimeError(
            "OPENAI_API_KEY environment variable is not set."
        )

    return OpenAI(api_key=api_key)


# ============================================================
# AI RESUME / JD ANALYSIS
# ============================================================

def analyze_with_openai(job_description, resume):
    """
    Use OpenAI to understand skills and terminology that
    cannot reliably be detected by our fixed skill dictionary.

    The deterministic analyzers remain the foundation.
    This function provides the intelligence layer.
    """

    if not job_description or not resume:
        raise ValueError(
            "Both job description and resume are required."
        )

    client = get_client()

    prompt = f"""
You are an expert ATS resume analyzer.

Your task is to compare a JOB DESCRIPTION against a CANDIDATE RESUME.

IMPORTANT RULES:

1. Do NOT assume that a skill is missing merely because it is
   unfamiliar or not present in a fixed dictionary.

2. Identify skills, technologies, tools, methodologies,
   professional competencies, domain knowledge, and platforms.

3. Understand synonyms and equivalent terminology.

   Examples:
   - Microsoft Excel = Excel
   - PostgreSQL = Postgres
   - Amazon Web Services = AWS
   - Customer Relationship Management = CRM
   - Search Engine Optimization = SEO

4. Distinguish between:
   - exact matches
   - equivalent/synonymous matches
   - related but not equivalent skills
   - genuinely missing skills

5. Do NOT treat every word in the job description as a skill.

6. Do NOT invent skills that are not supported by the text.

7. If the evidence is ambiguous, mark it as uncertain rather
   than claiming a definite match.

8. Consider context.

   Example:
   "Built dashboards using Power BI"
   means the candidate has Power BI experience.

9. Return ONLY valid JSON.
10. Do not include markdown or explanations outside the JSON.

Return this exact structure:

{{
    "job_skills": [
        {{
            "name": "skill name",
            "category": "category",
            "importance": "required|preferred|mentioned"
        }}
    ],

    "resume_skills": [
        {{
            "name": "skill name",
            "category": "category",
            "evidence": "short evidence from resume"
        }}
    ],

    "matched_skills": [
        {{
            "job_skill": "skill from JD",
            "resume_skill": "corresponding skill from resume",
            "match_type": "exact|synonym|equivalent",
            "confidence": 0
        }}
    ],

    "missing_skills": [
        {{
            "name": "skill",
            "importance": "required|preferred|mentioned",
            "confidence": 0
        }}
    ],

    "related_skills": [
        {{
            "job_skill": "skill",
            "candidate_skill": "related skill",
            "explanation": "why they are related but not equivalent",
            "confidence": 0
        }}
    ]
}}

Confidence must be an integer from 0 to 100.

JOB DESCRIPTION:
----------------
{job_description}

CANDIDATE RESUME:
-----------------
{resume}
"""

    response = client.responses.create(
        model="gpt-5-mini",
        input=prompt,
        
    )

    output = response.output_text.strip()

    try:
        result = json.loads(output)

    except json.JSONDecodeError as error:
        raise RuntimeError(
            f"OpenAI returned invalid JSON: {error}\n\n"
            f"Raw response:\n{output}"
        )

    return result


# ============================================================
# SIMPLE DIRECT TEST
# ============================================================

if __name__ == "__main__":

    print("=" * 70)
    print("OPENAI INTELLIGENCE ANALYZER TEST")
    print("=" * 70)

    test_jd = """
    We are looking for a Data Analyst with experience in
    SQL, Python, Power BI and customer relationship management.
    Experience with cloud platforms is preferred.
    """

    test_resume = """
    John Doe
    Data Analyst

    Experience:
    2 years working with PostgreSQL and Python.
    Created dashboards using Microsoft Power BI.
    Worked with Salesforce CRM.

    Skills:
    Python, PostgreSQL, Power BI, Salesforce.
    """

    try:

        result = analyze_with_openai(
            test_jd,
            test_resume
        )

        print("\nAI ANALYSIS:")
        print(json.dumps(
            result,
            indent=4,
            ensure_ascii=False
        ))

        print("\n")
        print("=" * 70)
        print("TEST COMPLETED")
        print("=" * 70)

    except Exception as error:

        print("\n")
        print("=" * 70)
        print("TEST FAILED")
        print("=" * 70)

        print(error)

        print("=" * 70)