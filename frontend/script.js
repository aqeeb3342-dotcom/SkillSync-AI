// ======================================================
// SKILLSYNC AI - COMPLETE FRONTEND JAVASCRIPT
// ======================================================

const API_URL = "http://127.0.0.1:5000";
// 1. PLACEMENT PREDICTION
// ======================================================

const predictionForm =
    document.getElementById("predictionForm");

if (predictionForm) {

    predictionForm.addEventListener(
        "submit",
        async function (event) {

            event.preventDefault();

            try {

                const student = {

                    gender:
                        document.getElementById("gender").value,

                    ssc_p:
                        parseFloat(
                            document.getElementById("ssc_p").value
                        ),

                    ssc_b:
                        document.getElementById("ssc_b").value,

                    hsc_p:
                        parseFloat(
                            document.getElementById("hsc_p").value
                        ),

                    hsc_b:
                        document.getElementById("hsc_b").value,

                    hsc_s:
                        document.getElementById("hsc_s").value,

                    degree_p:
                        parseFloat(
                            document.getElementById("degree_p").value
                        ),

                    degree_t:
                        document.getElementById("degree_t").value,

                    workex:
                        document.getElementById("workex").value,

                    etest_p:
                        parseFloat(
                            document.getElementById("etest_p").value
                        ),

                    specialisation:
                        document.getElementById(
                            "specialisation"
                        ).value,

                    mba_p:
                        parseFloat(
                            document.getElementById("mba_p").value
                        )
                };


                const response = await fetch(
                    `${API_URL}/api/predict`,
                    {
                        method: "POST",

                        headers: {
                            "Content-Type":
                                "application/json"
                        },

                        body:
                            JSON.stringify(student)
                    }
                );


                const result =
                    await response.json();


                if (!response.ok) {

                    alert(
                        result.error ||
                        "Prediction failed."
                    );

                    return;
                }


                // Display prediction

                const resultCard =
                    document.getElementById(
                        "resultCard"
                    );

                const predictionResult =
                    document.getElementById(
                        "predictionResult"
                    );

                const readinessResult =
                    document.getElementById(
                        "readinessResult"
                    );


                if (predictionResult) {

                    predictionResult.textContent =
                        result.prediction;

                }


                if (readinessResult) {

                    readinessResult.textContent =
                        result.readiness + "%";

                }


                if (resultCard) {

                    resultCard.classList.remove(
                        "hidden"
                    );

                }


                // Save placement data

                localStorage.setItem(
                    "placementPrediction",
                    result.prediction
                );


                localStorage.setItem(
                    "placementReadiness",
                    String(result.readiness)
                );


                // Update dashboard immediately

                loadDashboard();


                console.log(
                    "Placement Prediction:",
                    result
                );

            }

            catch (error) {

                console.error(
                    "Prediction error:",
                    error
                );

                alert(
                    "Unable to connect to backend."
                );

            }

        }
    );

}


// ======================================================
// 2. RESUME ANALYZER
// ======================================================

const analyzeResumeBtn =
    document.getElementById(
        "analyzeResumeBtn"
    );


if (analyzeResumeBtn) {

    analyzeResumeBtn.addEventListener(
        "click",
        async function () {

            const resumeFile =
                document.getElementById(
                    "resumeFile"
                );


            if (
                !resumeFile ||
                !resumeFile.files ||
                resumeFile.files.length === 0
            ) {

                alert(
                    "Please select a PDF resume first."
                );

                return;
            }


            const file =
                resumeFile.files[0];


            const formData =
                new FormData();


            formData.append(
                "resume",
                file
            );


            try {

                const response =
                    await fetch(
                        `${API_URL}/api/analyze-resume`,
                        {
                            method: "POST",
                            body: formData
                        }
                    );


                const result =
                    await response.json();


                if (!response.ok) {

                    alert(
                        result.error ||
                        "Resume analysis failed."
                    );

                    return;
                }


                console.log(
                    "Resume Analysis:",
                    result
                );


                // ------------------------------------------
                // Filename
                // ------------------------------------------

                const resumeFilename =
                    document.getElementById(
                        "resumeFilename"
                    );


                if (resumeFilename) {

                    resumeFilename.textContent =
                        result.filename;

                }


                // ------------------------------------------
                // Skill count
                // ------------------------------------------

                const skillCount =
                    document.getElementById(
                        "skillCount"
                    );


                if (skillCount) {

                    skillCount.textContent =
                        result.total_skills;

                }


                // ------------------------------------------
                // Skills list
                // ------------------------------------------

                const skillsList =
                    document.getElementById(
                        "skillsList"
                    );


                if (skillsList) {

                    skillsList.innerHTML = "";


                    result.skills.forEach(
                        function (skill) {

                            const item =
                                document.createElement(
                                    "span"
                                );


                            item.className =
                                "skill-tag";


                            item.textContent =
                                skill;


                            skillsList.appendChild(
                                item
                            );

                        }
                    );

                }


                // ------------------------------------------
                // Show resume result
                // ------------------------------------------

                const resumeResult =
                    document.getElementById(
                        "resumeResult"
                    );


                if (resumeResult) {

                    resumeResult.classList.remove(
                        "hidden"
                    );

                }


                // ------------------------------------------
                // Save resume data
                // ------------------------------------------

                localStorage.setItem(
                    "resumeSkills",
                    JSON.stringify(
                        result.skills
                    )
                );


                localStorage.setItem(
                    "resumeSkillCount",
                    String(
                        result.total_skills
                    )
                );


                // ------------------------------------------
                // Automatically perform skill gap
                // ------------------------------------------

                await performSkillGap(
                    result.skills
                );

            }

            catch (error) {

                console.error(
                    "Resume analysis error:",
                    error
                );

                alert(
                    "Unable to analyze resume."
                );

            }

        }
    );

}


// ======================================================
// 3. SKILL GAP ANALYSIS
// ======================================================

async function performSkillGap(
    skills
) {

    try {

        const careerSelect =
            document.getElementById(
                "careerSelect"
            );


        const career =
            careerSelect
                ? careerSelect.value
                : "Data Analyst";


        const response =
            await fetch(
                `${API_URL}/api/skill-gap`,
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body:
                        JSON.stringify({

                            skills:
                                skills,

                            career:
                                career

                        })
                }
            );


        const result =
            await response.json();


        if (!response.ok) {

            console.error(
                "Skill gap error:",
                result
            );

            return;
        }


        console.log(
            "Skill Gap:",
            result
        );


        // ------------------------------------------
        // SAVE COMPLETE SKILL GAP DATA
        // ------------------------------------------

        localStorage.setItem(
            "skillGapData",
            JSON.stringify(result)
        );


        localStorage.setItem(
            "skillMatch",
            String(
                result.match_percentage
            )
        );


        localStorage.setItem(
            "missingSkills",
            JSON.stringify(
                result.missing_skills || []
            )
        );


        // ------------------------------------------
        // DISPLAY SKILL GAP
        // ------------------------------------------

        displaySkillGap(
            result
        );


        // ------------------------------------------
        // CAREER RECOMMENDATION
        // ------------------------------------------

        await performCareerRecommendation(
            skills
        );


        // ------------------------------------------
        // UPDATE DASHBOARD
        // ------------------------------------------

        loadDashboard();

    }

    catch (error) {

        console.error(
            "Skill gap error:",
            error
        );

    }

}


// ======================================================
// 4. MANUAL SKILL GAP BUTTON
// ======================================================

const skillGapBtn =
    document.getElementById(
        "skillGapBtn"
    );


if (skillGapBtn) {

    skillGapBtn.addEventListener(
        "click",
        async function () {

            const skills =
                JSON.parse(
                    localStorage.getItem(
                        "resumeSkills"
                    ) || "[]"
                );


            if (skills.length === 0) {

                alert(
                    "Please analyze your resume first."
                );

                return;
            }


            await performSkillGap(
                skills
            );

        }
    );

}


// ======================================================
// 5. DISPLAY SKILL GAP
// ======================================================

function displaySkillGap(
    result
) {

    const skillGapResult =
        document.getElementById(
            "skillGapResult"
        );


    const skillGapCareer =
        document.getElementById(
            "skillGapCareer"
        );


    const skillMatch =
        document.getElementById(
            "skillMatch"
        );


    const matchedSkills =
        document.getElementById(
            "matchedSkills"
        );


    const missingSkills =
        document.getElementById(
            "missingSkills"
        );


    // Career

    if (skillGapCareer) {

        skillGapCareer.textContent =
            result.career;

    }


    // Match percentage

    if (skillMatch) {

        skillMatch.textContent =
            result.match_percentage + "%";

    }


    // Matched skills

    if (matchedSkills) {

        matchedSkills.innerHTML = "";


        if (
            result.matched_skills &&
            result.matched_skills.length > 0
        ) {

            result.matched_skills.forEach(
                function (skill) {

                    const item =
                        document.createElement(
                            "span"
                        );


                    item.className =
                        "skill-tag";


                    item.textContent =
                        skill;


                    matchedSkills.appendChild(
                        item
                    );

                }
            );

        }

        else {

            matchedSkills.textContent =
                "No matched skills.";

        }

    }


    // Missing skills

    if (missingSkills) {

        missingSkills.innerHTML = "";


        if (
            result.missing_skills &&
            result.missing_skills.length > 0
        ) {

            result.missing_skills.forEach(
                function (skill) {

                    const item =
                        document.createElement(
                            "span"
                        );


                    item.className =
                        "missing-skill";


                    item.textContent =
                        skill;


                    missingSkills.appendChild(
                        item
                    );

                }
            );

        }

        else {

            missingSkills.textContent =
                "No skill gaps found.";

        }

    }


    // Show skill gap section

    if (skillGapResult) {

        skillGapResult.classList.remove(
            "hidden"
        );

    }


    // Save again for safety

    localStorage.setItem(
        "skillGapData",
        JSON.stringify(result)
    );

    localStorage.setItem(
        "skillMatch",
        String(
            result.match_percentage
        )
    );

    localStorage.setItem(
        "missingSkills",
        JSON.stringify(
            result.missing_skills || []
        )
    );

}


// ======================================================
// 6. CAREER RECOMMENDATION
// ======================================================

async function performCareerRecommendation(
    skills
) {

    try {

        const response =
            await fetch(
                `${API_URL}/api/career-recommendation`,
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body:
                        JSON.stringify({
                            skills:
                                skills
                        })
                }
            );


        const result =
            await response.json();


        if (!response.ok) {

            console.error(
                "Career recommendation error:",
                result
            );

            return;
        }


        console.log(
            "Career Recommendation:",
            result
        );


        // Display career recommendations

        displayCareerRecommendations(
            result
        );


        // ------------------------------------------
        // Get skill gap data
        // ------------------------------------------

        const skillGapData =
            JSON.parse(
                localStorage.getItem(
                    "skillGapData"
                ) || "{}"
            );


        const missingSkills =
            skillGapData.missing_skills || [];


        // ------------------------------------------
        // Learning recommendations
        // ------------------------------------------

        if (
            missingSkills.length > 0
        ) {

            await performLearningRecommendation(
                missingSkills
            );

        }


        // Update dashboard

        loadDashboard();

    }

    catch (error) {

        console.error(
            "Career recommendation error:",
            error
        );

    }

}


// ======================================================
// 7. DISPLAY CAREER RECOMMENDATIONS
// ======================================================

function displayCareerRecommendations(
    result
) {

    const container =
        document.getElementById(
            "careerRecommendations"
        );


    const careerResult =
        document.getElementById(
            "careerRecommendationResult"
        );


    const dashboardCareer =
        document.getElementById(
            "dashboardCareer"
        );


    if (
        !result ||
        !result.recommendations ||
        result.recommendations.length === 0
    ) {

        if (container) {

            container.innerHTML =
                "<p>No career recommendations available.</p>";

        }


        if (dashboardCareer) {

            dashboardCareer.textContent =
                "---";

        }


        return;
    }


    // ------------------------------------------
    // TOP RECOMMENDED CAREER
    // ------------------------------------------

    const topCareer =
        result.recommendations[0];


    console.log(
        "TOP CAREER:",
        topCareer
    );


    // ------------------------------------------
    // Dashboard Career
    // ------------------------------------------

    if (dashboardCareer) {

        dashboardCareer.textContent =
            topCareer.career;

    }


    // ------------------------------------------
    // Career recommendation section
    // ------------------------------------------

    if (container) {

        container.innerHTML = "";


        result.recommendations.forEach(
            function (item, index) {

                const card =
                    document.createElement(
                        "div"
                    );


                card.className =
                    "career-card";


                card.innerHTML = `

                    <h3>
                        ${index + 1}.
                        ${item.career}
                    </h3>

                    <p>
                        <strong>
                            ${item.match_percentage}%
                            Match
                        </strong>
                    </p>

                    <p>
                        <strong>
                            Matched Skills:
                        </strong>
                        ${
                            item.matched_skills &&
                            item.matched_skills.length > 0
                            ? item.matched_skills.join(", ")
                            : "None"
                        }
                    </p>

                    <p>
                        <strong>
                            Missing Skills:
                        </strong>
                        ${
                            item.missing_skills &&
                            item.missing_skills.length > 0
                            ? item.missing_skills.join(", ")
                            : "None"
                        }
                    </p>

                `;


                container.appendChild(
                    card
                );

            }
        );

    }


    // Show section

    if (careerResult) {

        careerResult.classList.remove(
            "hidden"
        );

    }


    // ------------------------------------------
    // Save career recommendation
    // ------------------------------------------

    localStorage.setItem(
        "recommendedCareer",
        topCareer.career
    );


    localStorage.setItem(
        "recommendedCareerMatch",
        String(
            topCareer.match_percentage
        )
    );


    localStorage.setItem(
        "careerRecommendations",
        JSON.stringify(
            result.recommendations
        )
    );


    console.log(
        "Recommended Career Saved:",
        topCareer.career
    );

}


// ======================================================
// 8. LEARNING RECOMMENDATION
// ======================================================

async function performLearningRecommendation(
    missingSkills
) {

    try {

        const response =
            await fetch(
                `${API_URL}/api/learning-recommendation`,
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body:
                        JSON.stringify({

                            missing_skills:
                                missingSkills

                        })
                }
            );


        const result =
            await response.json();


        if (!response.ok) {

            console.error(
                "Learning recommendation error:",
                result
            );

            return;
        }


        console.log(
            "Learning Recommendations:",
            result
        );


        displayLearningRecommendations(
            result
        );


        // Save

        localStorage.setItem(
            "learningRecommendations",
            JSON.stringify(
                result.recommendations || []
            )
        );


        loadDashboard();

    }

    catch (error) {

        console.error(
            "Learning recommendation error:",
            error
        );

    }

}


// ======================================================
// 9. DISPLAY LEARNING RECOMMENDATIONS
// ======================================================

function displayLearningRecommendations(
    result
) {

    const container =
        document.getElementById(
            "learningRecommendations"
        );


    const learningResult =
        document.getElementById(
            "learningRecommendationResult"
        );


    if (
        !result ||
        !result.recommendations ||
        result.recommendations.length === 0
    ) {

        if (container) {

            container.innerHTML =
                "<p>No learning recommendations available.</p>";

        }

        return;
    }


    if (container) {

        container.innerHTML = "";


        result.recommendations.forEach(
            function (item) {

                const card =
                    document.createElement(
                        "div"
                    );


                card.className =
                    "learning-card";


                card.innerHTML = `

                    <h3>
                        ${item.skill}
                    </h3>

                    <p>
                        ${item.recommendation}
                    </p>

                `;


                container.appendChild(
                    card
                );

            }
        );

    }


    if (learningResult) {

        learningResult.classList.remove(
            "hidden"
        );

    }


    // Save learning data

    localStorage.setItem(
        "learningRecommendations",
        JSON.stringify(
            result.recommendations
        )
    );

}


// ======================================================
// 10. DASHBOARD
// ======================================================

function loadDashboard() {

    console.log(
        "Loading dashboard..."
    );


    // ==================================================
    // PLACEMENT PREDICTION
    // ==================================================

    const prediction =
        localStorage.getItem(
            "placementPrediction"
        );


    const readiness =
        localStorage.getItem(
            "placementReadiness"
        );


    const dashboardPrediction =
        document.getElementById(
            "dashboardPrediction"
        );


    const dashboardReadiness =
        document.getElementById(
            "dashboardReadiness"
        );


    if (dashboardPrediction) {

        dashboardPrediction.textContent =
            prediction || "---";

    }


    if (dashboardReadiness) {

        dashboardReadiness.textContent =
            readiness
                ? readiness + "%"
                : "--%";

    }


    // ==================================================
    // RESUME SKILLS
    // ==================================================

    const skillCount =
        localStorage.getItem(
            "resumeSkillCount"
        );


    const dashboardSkillCount =
        document.getElementById(
            "dashboardSkillCount"
        );


    if (dashboardSkillCount) {

        dashboardSkillCount.textContent =
            skillCount || "0";

    }


    // ==================================================
    // SKILL GAP
    // ==================================================

    const skillGapData =
        JSON.parse(
            localStorage.getItem(
                "skillGapData"
            ) || "{}"
        );


    const skillMatch =
        skillGapData.match_percentage;


    const missingSkills =
        skillGapData.missing_skills || [];


    const dashboardSkillMatch =
        document.getElementById(
            "dashboardSkillMatch"
        );


    if (dashboardSkillMatch) {

        if (
            skillMatch !== undefined &&
            skillMatch !== null
        ) {

            dashboardSkillMatch.textContent =
                skillMatch + "%";

        }

        else {

            dashboardSkillMatch.textContent =
                "--%";

        }

    }


    // ==================================================
    // MISSING SKILLS
    // ==================================================

    const dashboardMissingSkills =
        document.getElementById(
            "dashboardMissingSkills"
        );


    if (dashboardMissingSkills) {

        if (
            missingSkills.length > 0
        ) {

            dashboardMissingSkills.textContent =
                missingSkills.join(
                    " • "
                );

        }

        else {

            dashboardMissingSkills.textContent =
                "No skill-gap data available yet.";

        }

    }


    // ==================================================
    // CAREER RECOMMENDATION
    // ==================================================

    const recommendedCareer =
        localStorage.getItem(
            "recommendedCareer"
        );


    const dashboardCareer =
        document.getElementById(
            "dashboardCareer"
        );


    if (dashboardCareer) {

        dashboardCareer.textContent =
            recommendedCareer || "---";

    }


    // ==================================================
    // LEARNING RECOMMENDATIONS
    // ==================================================

    const learningRecommendations =
        JSON.parse(
            localStorage.getItem(
                "learningRecommendations"
            ) || "[]"
        );


    const dashboardLearning =
        document.getElementById(
            "dashboardLearning"
        );


    if (dashboardLearning) {

        dashboardLearning.innerHTML = "";


        if (
            learningRecommendations.length > 0
        ) {

            learningRecommendations.forEach(
                function (item) {

                    const div =
                        document.createElement(
                            "div"
                        );


                    div.className =
                        "dashboard-learning-item";


                    div.innerHTML = `

                        <p>
                            <strong>
                                ${item.skill}
                            </strong>
                        </p>

                        <p>
                            ${item.recommendation}
                        </p>

                    `;


                    dashboardLearning.appendChild(
                        div
                    );

                }
            );

        }

        else {

            dashboardLearning.textContent =
                "No learning recommendations available yet.";

        }

    }


    console.log(
        "Dashboard data:",
        {
            prediction:
                prediction,

            readiness:
                readiness,

            skillCount:
                skillCount,

            skillMatch:
                skillMatch,

            missingSkills:
                missingSkills,

            recommendedCareer:
                recommendedCareer,

            learningRecommendations:
                learningRecommendations
        }
    );

}


// ======================================================
// 11. REFRESH DASHBOARD BUTTON
// ======================================================

const refreshDashboard =
    document.getElementById(
        "refreshDashboard"
    );


if (refreshDashboard) {
    refreshDashboard.addEventListener("click", function () {
        const confirmed = window.confirm(
            "Start fresh? This clears saved browser data for this frontend."
        );

        if (!confirmed) return;

        localStorage.clear();
        sessionStorage.clear();
        window.location.reload();
    });
}


// ======================================================
// // 12. PAGE LOAD
// ======================================================

document.addEventListener(
    "DOMContentLoaded",
    function () {

        loadDashboard();

        console.log(
            "SkillSync AI frontend loaded successfully."
        );

    }
);
