import os
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional, List
from fastapi.middleware.cors import CORSMiddleware
import google.generativeai as genai
import json

app = FastAPI(title="TechU Research Labs - AI Enrollment Agent (Gemini Powered)")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure Gemini
# The user should set this in Render Environment Variables
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
genai.configure(api_key=GEMINI_API_KEY)

# Define the Course Catalog
COURSES_CATALOG = """
1. Data Science with AI/ML: Focuses on Python, Statistics, Machine Learning, Deep Learning, and Data Analysis. Ideal for aspiring Data Scientists or AI Engineers.
2. Full Stack Development: Covers HTML, CSS, JavaScript, React, Node.js, and Databases. Best for Software Engineers and Web Developers.
3. UI/UX Design: Focuses on Figma, User Research, Prototyping, and Visual Design. Perfect for Creative Designers.
"""

class StudentProfile(BaseModel):
    name: str
    email: str
    education: str
    skills: str
    career_goal: str
    gpa: float
    programming_exp: Optional[str] = ""
    time_commitment: Optional[str] = ""
    course_expectations: Optional[str] = ""

@app.post("/recommend")
async def recommend_course(profile: StudentProfile):
    if not GEMINI_API_KEY:
        return {"error": "Gemini API Key not configured"}

    # Initialize the model
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    prompt = f"""
    You are an Elite Career Counselor for TechU Research Labs. 
    Analyze the following student profile and perform two tasks:
    1. Match them to exactly 3 courses from our INTERNAL CATALOG.
    2. Suggest exactly 2 EXTERNAL COURSES (not from our catalog) if their skills or goals would benefit from specialized learning elsewhere (e.g., Coursera, Udemy, or industry certifications).

    INTERNAL COURSES CATALOG:
    {COURSES_CATALOG}
    
    STUDENT PROFILE:
    - Name: {profile.name}
    - Education Level: {profile.education}
    - Skills: {profile.skills}
    - Career Goal: {profile.career_goal}
    - GPA: {profile.gpa}/10.0
    - Programming Experience: {profile.programming_exp}
    - Weekly Time Commitment: {profile.time_commitment}
    - Expectations: {profile.course_expectations}
    
    SCORING REQUIREMENTS (for Internal Catalog):
    - SKILLS MATCH (40% weight): Match curriculum to {profile.skills}.
    - PROFESSIONAL CONTEXT (30% weight): Tailor for {profile.education} background.
    - GOAL ALIGNMENT (20% weight): Align with {profile.career_goal}.
    - FEASIBILITY (10% weight): Consider GPA/Time.

    EXTERNAL SUGGESTIONS CRITERIA:
    - Identify advanced or niche skills in {profile.skills} or {profile.career_goal} not covered by internal courses.
    - Suggest specific external paths (e.g. "Google Cloud Architect Professional" or "AWS Certified Developer").

    OUTPUT FORMAT (Strict JSON):
    {{
      "recommendations": [
        {{
          "course_name": "Full Name of Course",
          "fit_score": 95,
          "fit_level": "High",
          "match_reason": "Personalized explanation here."
        }}
      ],
      "external_suggestions": [
        {{
          "course_name": "External Course/Cert Name",
          "platform": "e.g., Coursera / Certification Board",
          "reason": "Why this matches their specialized skills/goals."
        }}
      ]
    }}
    
    Sort internal recommendations by fit_score descending. Return ONLY the JSON.
    """

    try:
        response = model.generate_content(prompt)
        # Clean up the response to extract JSON
        content = response.text.strip()
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0].strip()
        elif "```" in content:
            content = content.split("```")[1].split("```")[0].strip()
            
        data = json.loads(content)
        return data
    except Exception as e:
        print(f"Gemini Error: {e}")
        # Fallback to simple matching if AI fails
        return {
            "recommendations": [
                {
                    "course_name": "Full Stack Development",
                    "fit_score": 85,
                    "fit_level": "High",
                    "match_reason": "Our AI is currently optimizing. This course is a strong foundational match for your tech journey."
                }
            ]
        }

@app.get("/")
async def health_check():
    return {"status": "online", "engine": "Gemini 1.5 Flash"}
