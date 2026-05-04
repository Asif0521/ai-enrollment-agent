CREATE TABLE recommendations (
    id SERIAL PRIMARY KEY,
    lead_id VARCHAR(50),
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    skills TEXT,
    career_goal TEXT,
    gpa NUMERIC(4,2),
    programming_exp VARCHAR(255),
    time_commitment VARCHAR(255),
    course_expectations TEXT,
    recommended_course VARCHAR(255),
    fit_score NUMERIC(5,2),
    fit_level VARCHAR(50),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Example Insert Query (used dynamically by n8n)
-- INSERT INTO recommendations (lead_id, name, email, skills, career_goal, gpa, programming_exp, time_commitment, course_expectations, recommended_course, fit_score, fit_level)
-- VALUES ('LID-123456', 'Rahul Sharma', 'rahul@example.com', 'Python, SQL', 'Data Scientist', 8.5, 'Beginner', '10-20 hours', 'Build portfolio', 'Data Science & AI', 88.5, 'High');
