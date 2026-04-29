from fastapi import FastAPI
from pydantic import BaseModel
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

app = FastAPI(title="Enrollment AI Agent")

# Sample Course Dataset
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

class StudentProfile(BaseModel):
    skills: str
    career_goal: str
    gpa: float

@app.post("/recommend")
async def recommend_course(profile: StudentProfile):
    vectorizer = TfidfVectorizer(stop_words='english')
    
    best_course = "General Technical Program"
    highest_score = 0
    
    for course in COURSES:
        # 1. Skill Match (50% weight)
        skill_corpus = [course["required_skills"], profile.skills]
        skill_matrix = vectorizer.fit_transform(skill_corpus)
        skill_match = cosine_similarity(skill_matrix[0:1], skill_matrix[1:2])[0][0]
        
        # 2. Goal Alignment (30% weight)
        goal_corpus = [course["target_goals"], profile.career_goal]
        goal_matrix = vectorizer.fit_transform(goal_corpus)
        goal_alignment = cosine_similarity(goal_matrix[0:1], goal_matrix[1:2])[0][0]
        
        # 3. Academic Strength (20% weight, max GPA assumed 10.0)
        academic_strength = min(profile.gpa / 10.0, 1.0)
        
        # Calculate final Fit Score (out of 100)
        fit_score = (0.5 * skill_match + 0.3 * goal_alignment + 0.2 * academic_strength) * 100
        
        if fit_score > highest_score:
            highest_score = fit_score
            best_course = course["name"]

    # Floor at 0, cap at 100
    highest_score = max(0.0, min(100.0, round(highest_score, 2)))

    return {
        "recommended_course": best_course,
        "fit_score": highest_score
    }
