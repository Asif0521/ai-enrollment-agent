// Production URLs
const BACKEND_URL = "https://ai-enrollment-agent.onrender.com/recommend";
const WEBHOOK_URL = "https://n8nds.duckdns.org/webhook/student-enroll";
const SELECTION_WEBHOOK_URL = "https://n8nds.duckdns.org/webhook/course-selection";

document.addEventListener('DOMContentLoaded', () => {
    const gpaInput = document.getElementById('gpa');
    const gpaValue = document.getElementById('gpa-value');
    const form = document.getElementById('enrollmentForm');
    const submitBtn = document.getElementById('submitBtn');
    const btnText = submitBtn.querySelector('span');
    const loader = document.getElementById('loader');
    const resultCard = document.getElementById('resultCard');

    // Update GPA value display dynamically
    if (gpaInput) {
        gpaInput.addEventListener('input', (e) => {
            gpaValue.textContent = parseFloat(e.target.value).toFixed(1);
        });
    }

    // Handle Form Submission
    if (form) {
        form.addEventListener('submit', async (e) => {
            e.preventDefault();

            // Get values
            const payload = {
                name: document.getElementById('name').value,
                email: document.getElementById('email').value,
                phone: document.getElementById('phone').value,
                location: document.getElementById('location').value,
                education: document.getElementById('education').value,
                skills: document.getElementById('skills').value,
                career_goal: document.getElementById('career_goal').value,
                gpa: parseFloat(gpaInput.value),
                programming_exp: document.getElementById('programming_exp').value,
                time_commitment: document.getElementById('time_commitment').value,
                course_expectations: document.getElementById('course_expectations').value
            };

            // UI Loading State
            submitBtn.disabled = true;
            submitBtn.style.opacity = "0.7";
            btnText.textContent = "AI is Analyzing Profile...";
            loader.style.display = "inline-block";

            try {
                // 1. Get High-Accuracy Prediction from Render Backend (Direct Gemini Call)
                const response = await fetch(BACKEND_URL, {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify(payload)
                });

                let data;
                if (response.ok) {
                    data = await response.json();
                    
                    // 2. Sync to n8n in background (for Google Sheets/Email)
                    fetch(WEBHOOK_URL, {
                        method: "POST",
                        headers: { "Content-Type": "application/json" },
                        body: JSON.stringify({ ...payload, recommendations: data.recommendations })
                    }).catch(e => console.warn("n8n Logging failed", e));
                    
                } else {
                    console.warn(`Backend failed. Calculating smart local recommendation.`);
                    const goal = payload.career_goal.toLowerCase();
                    const skills = payload.skills.toLowerCase();
                    
                    const localResults = [
                        { name: "Full Stack Development", keywords: ["web", "full stack", "frontend", "backend", "react", "node", "javascript", "html", "css"], score: 40 },
                        { name: "Data Science with AI/ML", keywords: ["data", "science", "ai", "ml", "machine learning", "python", "sql", "analysis", "statistics"], score: 40 },
                        { name: "UI/UX Design", keywords: ["design", "ui", "ux", "figma", "user", "interface", "experience", "branding"], score: 40 }
                    ];

                    localResults.forEach(res => {
                        res.keywords.forEach(kw => {
                            if (goal.includes(kw)) res.score += 20;
                            if (skills.includes(kw)) res.score += 10;
                        });
                        res.score = Math.min(95, res.score);
                    });

                    data = {
                        recommendations: localResults.sort((a,b) => b.score - a.score).map(res => ({
                            course_name: res.name,
                            fit_score: res.score,
                            fit_level: res.score >= 80 ? "High" : (res.score >= 60 ? "Medium" : "Low"),
                            match_reason: `Based on your profile, ${res.name} aligns with your career path.`
                        }))
                    };
                }
                
                // Fallback for different data formats
                let recommendations = [];
                if (data.recommendations) {
                    recommendations = data.recommendations;
                } else if (data.recommended_course) {
                    // Adapt old format to new UI
                    recommendations = [{
                        course_name: data.recommended_course,
                        fit_score: data.fit_score,
                        fit_level: data.fit_level || (data.fit_score >= 80 ? "High" : "Medium")
                    }];
                }
                
                // Hide form and show results
                form.classList.add('hidden');
                resultCard.classList.remove('hidden');

                // Unlock Enrollment across the site
                const confirmBtn = document.getElementById('confirm-enroll-btn');
                const lockBtn = document.getElementById('lock-enroll-btn');
                if (confirmBtn) confirmBtn.classList.remove('hidden');
                if (lockBtn) lockBtn.classList.add('hidden');

                // Render Top 3 Cards
                const recommendationsList = document.getElementById('recommendationsList');
                recommendationsList.innerHTML = '';

                recommendations.forEach((item, index) => {
                    const card = document.createElement('div');
                    card.className = `course-card fit-${item.fit_level.toLowerCase()}`;
                    card.style.animationDelay = `${index * 0.1}s`;
                    
                    card.innerHTML = `
                        <div class="card-badge">${item.fit_level} Match</div>
                        <h4>${item.course_name}</h4>
                        <div class="fit-score-container">
                            <div class="score-bar">
                                <div class="score-fill" style="width: ${item.fit_score}%"></div>
                            </div>
                            <span class="score-text">${item.fit_score}% Fit</span>
                        </div>
                        <p class="match-reason" style="font-size: 0.9rem; color: var(--text-secondary); margin-bottom: 1rem; line-height: 1.4;">
                            ${item.match_reason || "Based on your profile, this course is a strong match."}
                        </p>
                        <button class="enroll-btn" onclick="enrollInCourse('${item.course_name}', ${item.fit_score})">
                            View Course Details
                        </button>
                    `;
                    recommendationsList.appendChild(card);
                });

            } catch (error) {
                console.error("Network Error:", error);
                alert("Could not reach the AI Agent (Server offline). Displaying offline preview.");
                // Execute fallback logic if completely unreachable
                form.classList.add('hidden');
                resultCard.classList.remove('hidden');
                const recommendationsList = document.getElementById('recommendationsList');
                recommendationsList.innerHTML = `
                    <div class="course-card fit-high">
                        <div class="card-badge">High Match</div>
                        <h4>Full Stack Development</h4>
                        <div class="fit-score-container">
                            <div class="score-bar"><div class="score-fill" style="width: 95%"></div></div>
                            <span class="score-text">95% Fit</span>
                        </div>
                        <p class="match-reason" style="font-size: 0.9rem; color: var(--text-secondary); margin-bottom: 1rem; line-height: 1.4;">
                            Perfect match for your technical background.
                        </p>
                        <button class="enroll-btn" onclick="enrollInCourse('Full Stack Development', 95)">View Course Details</button>
                    </div>`;
            } finally {
                resetBtn();
            }
        });
    }

    window.enrollInCourse = async (courseName, score) => {
        const email = document.getElementById('email').value;
        const name = document.getElementById('name').value;

        // Visual feedback
        const btn = event.target;
        const originalText = btn.textContent;
        btn.disabled = true;
        btn.textContent = "Finalizing...";

        try {
            // Send webhook (don't block UI if it fails)
            fetch(SELECTION_WEBHOOK_URL, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    name, email,
                    selected_course: courseName,
                    fit_score: score,
                    skills: document.getElementById('skills').value,
                    gpa: document.getElementById('gpa').value,
                    phone: document.getElementById('phone').value,
                    location: document.getElementById('location').value,
                    education: document.getElementById('education').value,
                    programming_exp: document.getElementById('programming_exp').value,
                    time_commitment: document.getElementById('time_commitment').value,
                    course_expectations: document.getElementById('course_expectations').value,
                    fit_level: btn.closest('.course-card').querySelector('.card-badge').textContent.split(' ')[0]
                })
            }).catch(e => console.warn("Background sync failed", e));
            
            // Assuming price maps based on course name
            let price = "99,000";
            let oldPrice = "1,40,000";
            let save = "41,000";
            if (courseName.includes("Data Science")) {
                price = "85,000"; oldPrice = "1,20,000"; save = "35,000";
            } else if (courseName.includes("UI/UX")) {
                price = "65,000"; oldPrice = "95,000"; save = "30,000";
            }
            
            // Show the course details section (Amount Page) directly
            if (typeof window.showCourseDetails === 'function') {
                window.showCourseDetails(courseName, price, oldPrice, save);
                // Alert the user about the email
                console.log("Enrollment email triggered via background sync.");
            } else {
                // Fallback if the function isn't ready
                alert(`Redirecting to details for ${courseName}...`);
            }

        } catch (error) {
            console.error("Selection Error:", error);
            btn.disabled = false;
            btn.textContent = originalText;
        }
    };

    function resetBtn() {
        submitBtn.disabled = false;
        submitBtn.style.opacity = "1";
        btnText.textContent = "Initialize AI Assessment";
        loader.style.display = "none";
    }
});
