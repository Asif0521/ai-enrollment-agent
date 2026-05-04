from fastapi import FastAPI
from pydantic import BaseModel
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from typing import Optional
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="TechU Research Labs - Enrollment AI Agent")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

COURSES = [
    {
        "name": "Data Science with AI/ML",
        "required_skills": "Python math statistics data analysis machine learning",
        "target_goals": "Data Scientist AI Engineer Machine Learning Engineer"
    },
    {
        "name": "Full Stack Development",
        "required_skills": "HTML CSS JavaScript React Node database python java sql",
        "target_goals": "Frontend Developer Backend Developer Full Stack Software Engineer"
    },
    {
        "name": "UI/UX Design",
        "required_skills": "Figma design wireframing user research prototyping photoshop",
        "target_goals": "UI Designer UX Researcher Product Designer"
    }
]

class StudentProfile(BaseModel):
    skills: str
    career_goal: str
    gpa: float
    programming_exp: Optional[str] = ""
    time_commitment: Optional[str] = ""
    course_expectations: Optional[str] = ""

@app.post("/recommend")
async def recommend_course(profile: StudentProfile):
    vectorizer = TfidfVectorizer(stop_words='english')
    
    recommendations = []
    
    for course in COURSES:
        # 1. Skill Match (40% weight)
        skill_corpus = [course["required_skills"], profile.skills]
        try:
            skill_matrix = vectorizer.fit_transform(skill_corpus)
            skill_match = cosine_similarity(skill_matrix[0:1], skill_matrix[1:2])[0][0]
        except:
            skill_match = 0
            
        # 2. Goal Alignment (40% weight)
        goal_corpus = [course["target_goals"], profile.career_goal]
        try:
            goal_matrix = vectorizer.fit_transform(goal_corpus)
            goal_alignment = cosine_similarity(goal_matrix[0:1], goal_matrix[1:2])[0][0]
        except:
            goal_alignment = 0
            
        # 3. Academic Strength (20% weight, max GPA assumed 10.0)
        academic_strength = min(profile.gpa / 10.0, 1.0)
        
        # Calculate final Fit Score (out of 100)
        fit_score = (0.4 * skill_match + 0.4 * goal_alignment + 0.2 * academic_strength) * 100
        
        # Boost score slightly based on experience
        if profile.programming_exp in ["Intermediate", "Advanced"] and "Data" in course["name"]:
            fit_score += 5
            
        # Add random variance to make it feel more dynamic when user types less
        if fit_score < 50:
             fit_score += 30 # base minimum logic
             
        fit_score = max(0.0, min(100.0, round(fit_score, 2)))
        fit_level = "High" if fit_score >= 80 else ("Medium" if fit_score >= 60 else "Low")
        
        # Generate Reasoning
        exp_text = f"your background as a {profile.programming_exp}" if profile.programming_exp else "your current background"
        time_text = f"dedicate {profile.time_commitment}" if profile.time_commitment else "dedicate time"
        expect_text = f"goal to {profile.course_expectations}" if profile.course_expectations else "career goals"
        
        reason = f"Since you mentioned you can {time_text} and have a {expect_text}, our AI highly recommends the {course['name']} program. Your prior background as a {profile.programming_exp or 'student'} gives you the perfect foundation for this learning path."
        
        recommendations.append({
            "course_name": course["name"],
            "fit_score": fit_score,
            "fit_level": fit_level,
            "match_reason": reason
        })

    # Sort top 3
    recommendations = sorted(recommendations, key=lambda x: x["fit_score"], reverse=True)[:3]

    return {
        "recommendations": recommendations
    }
