import pandas as pd
import random
from datetime import datetime, timedelta

# 1. GENERATE RAW TEST DATA
def generate_raw_data(num_records=150):
    first_names = ["Rahul", "Priya", "Amit", "Neha", "Vikram", "Sneha", "Karan", "Pooja", "Arjun", "Anjali", "Rohan", "Riya"]
    last_names = ["Sharma", "Verma", "Patel", "Singh", "Kumar", "Gupta", "Reddy", "Nair", "Iyer", "Joshi"]
    
    courses = ["Data Science & AI", "Full Stack Web Development", "Cloud DevOps Engineering", "Cybersecurity Specialist"]
    
    skills_pool = [
        "Python, SQL, Machine Learning", "HTML, CSS, React, Node.js", 
        "AWS, Docker, Kubernetes, Linux", "Network Security, Wireshark, Ethical Hacking",
        "Java, Spring Boot, MySQL", "Excel, Power BI, Tableau", 
        "Python, Django, PostgreSQL", "C++, Embedded Systems, IoT"
    ]
    
    goals_pool = [
        "Data Scientist", "Frontend Developer", "Cloud Architect", 
        "Security Analyst", "Backend Engineer", "Data Analyst",
        "Full Stack Developer", "IoT Engineer"
    ]
    
    cities = ["Bangalore", "Hyderabad", "Pune", "Mumbai", "Delhi", "Chennai"]
    
    data = []
    
    for i in range(num_records):
        name = f"{random.choice(first_names)} {random.choice(last_names)}"
        email = f"{name.lower().replace(' ', '.')}@example.com"
        
        # Random date within the last 6 months
        days_ago = random.randint(0, 180)
        app_date = datetime.now() - timedelta(days=days_ago)
        
        gpa = round(random.uniform(5.5, 9.8), 1)
        skills = random.choice(skills_pool)
        goal = random.choice(goals_pool)
        course = random.choice(courses)
        
        # Correlate score slightly with GPA for realistic look
        base_score = random.randint(40, 85)
        fit_score = min(100, int(base_score + (gpa * 1.5)))
        
        status = random.choices(["Enrolled", "Pending", "Dropped"], weights=[60, 30, 10])[0]
        city = random.choice(cities)
        
        data.append({
            "Application_ID": f"APP-{1000 + i}",
            "Date": app_date.strftime("%Y-%m-%d"),
            "Name": name,
            "Email": email,
            "City": city,
            "GPA": gpa,
            "Skills": skills,
            "Career_Goal": goal,
            "Recommended_Course": course,
            "Fit_Score": fit_score,
            "Status": status
        })
        
    df = pd.DataFrame(data)
    df.to_csv("raw_enrollment_data.csv", index=False)
    print("Created raw_enrollment_data.csv (150 records)")
    return df

# 2. TRANSFORM DATA FOR POWER BI
def transform_data(df):
    print("Transforming data for Power BI...")
    
    # Create 'Fit Level' Dimension for easy slicers in Power BI
    def get_fit_level(score):
        if score >= 85: return "High Fit"
        elif score >= 65: return "Medium Fit"
        else: return "Low Fit"
        
    df["Fit_Level"] = df["Fit_Score"].apply(get_fit_level)
    
    # Extract primary skill (first skill in the comma separated list) for Skill Distribution Charts
    df["Primary_Skill"] = df["Skills"].apply(lambda x: x.split(',')[0].strip())
    
    # Add an Application Month column for Time Series tracking
    df['Date'] = pd.to_datetime(df['Date'])
    df['Month_Year'] = df['Date'].dt.to_period('M')
    
    # Create an "Is_Enrolled" integer column (1 or 0) for easy DAX measure summing
    df['Is_Enrolled'] = df['Status'].apply(lambda x: 1 if x == 'Enrolled' else 0)
    
    # Save the transformed dataset
    df.to_csv("powerbi_transformed_data.csv", index=False)
    print("Created powerbi_transformed_data.csv!")
    print("\nTop 5 rows of Transformed Data:")
    print(df.head())

if __name__ == "__main__":
    raw_df = generate_raw_data(150)
    transform_data(raw_df)
    print("\nTransformation Complete! Import 'powerbi_transformed_data.csv' into Power BI.")
