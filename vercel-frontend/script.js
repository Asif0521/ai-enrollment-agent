// Production n8n Webhook URL
const WEBHOOK_URL = "https://n8nds.duckdns.org/webhook/student-enroll";

document.addEventListener('DOMContentLoaded', () => {
    const gpaInput = document.getElementById('gpa');
    const gpaValue = document.getElementById('gpa-value');
    const form = document.getElementById('enrollmentForm');
    const submitBtn = document.getElementById('submitBtn');
    const btnText = submitBtn.querySelector('span');
    const loader = document.getElementById('loader');
    const resultCard = document.getElementById('resultCard');

    // Update GPA value display dynamically
    gpaInput.addEventListener('input', (e) => {
        gpaValue.textContent = parseFloat(e.target.value).toFixed(1);
    });

    // Handle Form Submission
    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        // Get values
        const payload = {
            name: document.getElementById('name').value,
            email: document.getElementById('email').value,
            skills: document.getElementById('skills').value,
            career_goal: document.getElementById('career_goal').value,
            gpa: parseFloat(gpaInput.value)
        };

        // UI Loading State
        submitBtn.disabled = true;
        btnText.textContent = "Analyzing Profile...";
        loader.style.display = "block";

        try {
            const response = await fetch(WEBHOOK_URL, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(payload)
            });

            if (response.ok) {
                // Success State
                form.classList.add('hidden');
                resultCard.classList.remove('hidden');
            } else {
                alert(`Error: Received status code ${response.status}`);
                resetBtn();
            }
        } catch (error) {
            alert("Network Error: Could not reach the AI Agent. Please ensure n8n is running.");
            console.error(error);
            resetBtn();
        }
    });

    function resetBtn() {
        submitBtn.disabled = false;
        btnText.textContent = "Get AI Recommendation";
        loader.style.display = "none";
    }
});
