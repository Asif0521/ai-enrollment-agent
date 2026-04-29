import streamlit as st
import requests

# Set n8n Webhook URL (Make sure your n8n workflow is active)
N8N_WEBHOOK_URL = "http://localhost:5678/webhook/student-enroll"

st.set_page_config(page_title="Course Enrollment Agent", page_icon="🎓", layout="centered")

st.title("🎓 AI Course Enrollment Assistant")
st.write("Fill out your details and our AI will recommend the perfect learning path for you.")

with st.form("enrollment_form"):
    name = st.text_input("Full Name", placeholder="e.g., Rahul Sharma")
    email = st.text_input("Email Address", placeholder="e.g., rahul@example.com")
    skills = st.text_area("Current Skills", placeholder="e.g., Python, SQL, Communication")
    career_goal = st.text_input("Career Goal", placeholder="e.g., Data Scientist")
    gpa = st.number_input("GPA (out of 10.0)", min_value=0.0, max_value=10.0, value=7.5, step=0.1)
    
    submitted = st.form_submit_button("Get AI Recommendation")
    
    if submitted:
        if not name or not email or not skills or not career_goal:
            st.error("Please fill in all required fields.")
        else:
            payload = {
                "name": name,
                "email": email,
                "skills": skills,
                "career_goal": career_goal,
                "gpa": float(gpa)
            }
            
            with st.spinner("AI is analyzing your profile..."):
                try:
                    response = requests.post(N8N_WEBHOOK_URL, json=payload)
                    if response.status_code == 200:
                        st.success(f"Success! Your application has been submitted. Check your email for recommendations!")
                    else:
                        st.error(f"Failed to submit. Status code: {response.status_code}")
                except Exception as e:
                    st.error(f"Error connecting to n8n: {str(e)}")
