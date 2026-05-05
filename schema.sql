-- Recommendations Table (AI Assessment Results)
CREATE TABLE recommendations (
    id SERIAL PRIMARY KEY,
    lead_id VARCHAR(50),
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    education VARCHAR(255),
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

-- Enrollments Table (Modal Form Submissions)
CREATE TABLE enrollments (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    phone VARCHAR(20) NOT NULL,
    selected_course VARCHAR(255) NOT NULL,
    work_experience VARCHAR(50),
    batch VARCHAR(100) DEFAULT 'Not Selected',
    mode VARCHAR(100) DEFAULT 'Not Selected',
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Example Insert Queries (used dynamically by n8n)
-- INSERT INTO recommendations (lead_id, name, email, education, skills, career_goal, gpa, programming_exp, time_commitment, course_expectations, recommended_course, fit_score, fit_level)
-- VALUES ('LID-123456', 'Rahul Sharma', 'rahul@example.com', 'Working Professional', 'Python, SQL', 'Data Scientist', 8.5, 'Beginner', '10-20 hours', 'Build portfolio', 'Data Science & AI', 88.5, 'High');

-- INSERT INTO enrollments (name, email, phone, selected_course, work_experience, batch, mode)
-- VALUES ('Rahul Sharma', 'rahul@example.com', '+91 9876543210', 'Data Science & AI', '2', '12 May', 'Online Live');
