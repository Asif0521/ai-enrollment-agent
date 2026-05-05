from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from fastapi.middleware.cors import CORSMiddleware
import numpy as np

app = FastAPI(title="TechU Research Labs - Enrollment AI Agent")

# Enable CORS for the Vercel frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Course Dataset
COURSES = [
    {
        "name": "Data Science & AI",
        "required_skills": "Python math statistics data analysis machine learning",
        "target_goals": "Data Scientist AI Engineer Machine Learning Engineer"
    },
    {
        "name": "Full Stack Web Development",
        "required_skills": "HTML CSS JavaScript React Node database",
        "target_goals": "Frontend Developer Backend Developer Full Stack Software Engineer"
    },
    {
        "name": "Cloud DevOps Engineering",
        "required_skills": "Linux networking scripting AWS Azure Docker",
        "target_goals": "DevOps Engineer Cloud Architect SRE"
    },
    {
        "name": "Cybersecurity Specialist",
        "required_skills": "Networking security Linux hacking protocols",
        "target_goals": "Security Analyst Penetration Tester Information Security"
    }
]

# External suggestions mapping by career goal keywords
EXTERNAL_MAP = {
    "cloud": [
        {"course_name": "Google Cloud Professional Architect", "platform": "Google Cloud", "reason": "Industry-standard certification for cloud architecture roles."},
        {"course_name": "AWS Certified Solutions Architect", "platform": "Amazon AWS", "reason": "Most in-demand cloud certification globally."}
    ],
    "data": [
        {"course_name": "IBM Data Science Professional Certificate", "platform": "Coursera", "reason": "Comprehensive data science track from IBM covering Python, SQL, and ML."},
        {"course_name": "TensorFlow Developer Certificate", "platform": "Google / Coursera", "reason": "Validates deep learning expertise with TensorFlow."}
    ],
    "security": [
        {"course_name": "CompTIA Security+", "platform": "CompTIA", "reason": "Globally recognized entry-level cybersecurity certification."},
        {"course_name": "Certified Ethical Hacker (CEH)", "platform": "EC-Council", "reason": "Essential for penetration testing and security analyst roles."}
    ],
    "devops": [
        {"course_name": "Docker & Kubernetes: The Complete Guide", "platform": "Udemy", "reason": "Hands-on container orchestration skills for DevOps pipelines."},
        {"course_name": "HashiCorp Terraform Associate", "platform": "HashiCorp", "reason": "Infrastructure-as-code certification for modern DevOps."}
    ],
    "default": [
        {"course_name": "Google Project Management Certificate", "platform": "Coursera", "reason": "Enhances project management and leadership skills for any tech role."},
        {"course_name": "Meta Front-End Developer Certificate", "platform": "Coursera", "reason": "Solid front-end foundation from Meta for career flexibility."}
    ]
}

class StudentProfile(BaseModel):
    name: str
    email: str
    skills: str
    career_goal: str
    education: str
    gpa: float
    programming_exp: str = ""
    time_commitment: str = ""
    course_expectations: str = ""

class EnrollmentRequest(BaseModel):
    name: str
    email: str
    phone: str
    selected_course: str
    work_experience: str
    batch: Optional[str] = "Not Selected"
    mode: Optional[str] = "Not Selected"

@app.post("/enroll")
async def enroll_student(enrollment: EnrollmentRequest):
    print(f"New Enrollment Received: {enrollment.name} for {enrollment.selected_course}")
    return {
        "status": "success",
        "message": f"Successfully enrolled {enrollment.name} in {enrollment.selected_course}",
        "received_data": enrollment
    }

@app.post("/recommend")
async def recommend_course(profile: StudentProfile):
    vectorizer = TfidfVectorizer(stop_words='english')
    results = []
    
    # Calculate Professional/Experience Multiplier
    exp_multiplier = 1.0
    if "Professional" in profile.education or "Advanced" in profile.programming_exp:
        exp_multiplier = 1.25
    elif "Intermediate" in profile.programming_exp:
        exp_multiplier = 1.1

    for course in COURSES:
        # 1. Skill Match (40% weight)
        skill_corpus = [course["required_skills"], profile.skills]
        skill_matrix = vectorizer.fit_transform(skill_corpus)
        skill_match = cosine_similarity(skill_matrix[0:1], skill_matrix[1:2])[0][0]
        
        # 2. Goal Alignment (20% weight)
        goal_corpus = [course["target_goals"], profile.career_goal]
        goal_matrix = vectorizer.fit_transform(goal_corpus)
        goal_alignment = cosine_similarity(goal_matrix[0:1], goal_matrix[1:2])[0][0]
        
        # 3. Academic & Commitment (10% weight)
        academic_strength = min(profile.gpa / 10.0, 1.0)
        
        # 4. Professional Context (30% weight)
        professional_weight = 0.3 if exp_multiplier > 1.0 and goal_alignment > 0.3 else 0.1
        
        # Calculate final Fit Score (out of 100)
        raw_score = (0.4 * skill_match + 0.2 * goal_alignment + 0.1 * academic_strength + professional_weight) * 100
        fit_score = max(50.0, min(98.0, round(raw_score * exp_multiplier, 2)))
        
        # Determine Fit Level
        if fit_score >= 85:
            fit_level = "High"
        elif fit_score >= 70:
            fit_level = "Medium"
        else:
            fit_level = "Low"
            
        match_reason = f"Based on your {profile.skills} skills and goal as a {profile.career_goal}, this course is a solid match."
        if exp_multiplier > 1.1:
            match_reason = f"As a {profile.education}, your background in {profile.skills} makes this program an elite choice for your career pivot."

        results.append({
            "course_name": course["name"],
            "fit_score": fit_score,
            "fit_level": fit_level,
            "match_reason": match_reason
        })

    # Sort by fit_score descending and take Top 3
    results.sort(key=lambda x: x["fit_score"], reverse=True)
    top_3 = results[:3]

    # Determine external suggestions based on career goal
    goal_lower = profile.career_goal.lower()
    external = EXTERNAL_MAP.get("default")
    for key in EXTERNAL_MAP:
        if key in goal_lower or key in profile.skills.lower():
            external = EXTERNAL_MAP[key]
            break

    return {
        "recommendations": top_3,
        "external_suggestions": external
    }

@app.get("/")
async def health_check():
    return {"status": "online", "engine": "TF-IDF Fallback + Gemini Primary"}
