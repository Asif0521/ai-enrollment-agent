CREATE TABLE recommendations (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    skills TEXT,
    career_goal TEXT,
    gpa NUMERIC(4,2),
    recommended_course VARCHAR(255),
    fit_score NUMERIC(5,2),
    fit_level VARCHAR(50),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Example Insert Query (used dynamically by n8n)
-- INSERT INTO recommendations (name, email, skills, career_goal, gpa, recommended_course, fit_score, fit_level)
-- VALUES ('Rahul Sharma', 'rahul@example.com', 'Python, SQL', 'Data Scientist', 8.5, 'Data Science & AI', 88.5, 'High');
