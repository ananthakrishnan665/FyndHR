const jobDescription = document.getElementById("jobDescription");
const resume = document.getElementById("resume");

const jdCounter = document.getElementById("jdCounter");
const resumeCounter = document.getElementById("resumeCounter");

const analyzeButton = document.getElementById("analyzeButton");
const results = document.getElementById("results");


// =========================================================
// CHARACTER COUNTERS
// =========================================================

function updateCounter(textarea, counter) {

    const length = textarea.value.length;

    counter.textContent =
        `${length.toLocaleString()} characters`;
}


jobDescription.addEventListener("input", function () {

    updateCounter(
        jobDescription,
        jdCounter
    );

});


resume.addEventListener("input", function () {

    updateCounter(
        resume,
        resumeCounter
    );

});


// =========================================================
// ANALYZE RESUME
// =========================================================

analyzeButton.addEventListener("click", async function () {

    const jd = jobDescription.value.trim();
    const resumeText = resume.value.trim();


    // =====================================================
    // VALIDATION
    // =====================================================

    if (!jd) {

        alert(
            "Please paste the job description."
        );

        jobDescription.focus();

        return;
    }


    if (!resumeText) {

        alert(
            "Please paste your resume."
        );

        resume.focus();

        return;
    }


    // =====================================================
    // BUTTON STATE
    // =====================================================

    analyzeButton.disabled = true;

    analyzeButton.textContent =
        "Analyzing...";


    try {

        // =================================================
        // SEND REQUEST TO FLASK
        // =================================================

        const response = await fetch(
            "http://127.0.0.1:5000/api/analyze",
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({

                    job_description: jd,

                    resume: resumeText

                })
            }
        );


        // =================================================
        // READ BACKEND RESPONSE
        // =================================================

        const data = await response.json();


        console.log(
            "Backend response:",
            data
        );


        // =================================================
        // HTTP ERROR
        // =================================================

        if (!response.ok) {

            throw new Error(
                data.message ||
                "Server returned an error."
            );
        }


        // =================================================
        // CHECK DATA
        // =================================================

        if (!data.data) {

            throw new Error(
                "Backend returned no analysis data."
            );
        }


        // =================================================
        // GET ANALYSIS DATA
        // =================================================

        const skills =
            data.data.skills || {};

        const experience =
            data.data.experience || {};

        const education =
            data.data.education || {};

        const score =
            data.data.score || {};

        const aiAnalysis =
            data.data.ai_analysis || null;


        // =================================================
        // DEBUG AI RESPONSE
        // =================================================

        console.log(
            "========== AI ANALYSIS =========="
        );

        console.log(
            aiAnalysis
        );

        console.log(
            "================================="
        );


        // =================================================
        // SCORE DATA
        // =================================================

        const overallScore =
            score.overall_score !== undefined &&
            score.overall_score !== null
                ? Number(score.overall_score)
                : null;


        const category =
            score.category ||
            "Not available";


        const scoreMessage =
            score.message ||
            "No additional score analysis available.";


        const componentScores =
            score.component_scores || {};


        const skillsScore =
            componentScores.skills !== undefined
                ? Number(componentScores.skills)
                : null;


        const experienceScore =
            componentScores.experience !== undefined
                ? Number(componentScores.experience)
                : null;


        const educationScore =
            componentScores.education !== undefined
                ? Number(componentScores.education)
                : null;


        // =================================================
        // FORMAT SCORES
        // =================================================

        const formattedOverallScore =
            overallScore !== null
                ? overallScore.toFixed(2)
                : "N/A";


        const formattedSkillsScore =
            skillsScore !== null
                ? skillsScore.toFixed(2)
                : "N/A";


        const formattedExperienceScore =
            experienceScore !== null
                ? experienceScore.toFixed(2)
                : "N/A";


        const formattedEducationScore =
            educationScore !== null
                ? educationScore.toFixed(2)
                : "N/A";


        // =================================================
        // DETERMINISTIC SKILLS
        // =================================================

        const jobDescriptionSkills =
            Array.isArray(
                skills.job_description_skills
            )
                ? skills.job_description_skills
                : [];


        const resumeSkills =
            Array.isArray(
                skills.resume_skills
            )
                ? skills.resume_skills
                : [];


        const matchedSkills =
            Array.isArray(
                skills.matched_skills
            )
                ? skills.matched_skills
                : [];


        const missingSkills =
            Array.isArray(
                skills.missing_skills
            )
                ? skills.missing_skills
                : [];


        // =================================================
        // EDUCATION ARRAYS
        // =================================================

        const requiredEducation =
            Array.isArray(
                education.required_education
            )
                ? education.required_education
                : [];


        const candidateEducation =
            Array.isArray(
                education.candidate_education
            )
                ? education.candidate_education
                : [];


        // =================================================
        // AI INTELLIGENCE ARRAYS
        // =================================================

        const aiJobSkills =
            aiAnalysis &&
            Array.isArray(
                aiAnalysis.job_skills
            )
                ? aiAnalysis.job_skills
                : [];


        const aiResumeSkills =
            aiAnalysis &&
            Array.isArray(
                aiAnalysis.resume_skills
            )
                ? aiAnalysis.resume_skills
                : [];


        const aiMatchedSkills =
            aiAnalysis &&
            Array.isArray(
                aiAnalysis.matched_skills
            )
                ? aiAnalysis.matched_skills
                : [];


        const aiMissingSkills =
            aiAnalysis &&
            Array.isArray(
                aiAnalysis.missing_skills
            )
                ? aiAnalysis.missing_skills
                : [];


        const aiRelatedSkills =
            aiAnalysis &&
            Array.isArray(
                aiAnalysis.related_skills
            )
                ? aiAnalysis.related_skills
                : [];


        // =================================================
        // AI JOB SKILLS HTML
        // =================================================

        const aiJobSkillsHTML =
            aiJobSkills.length > 0

                ? aiJobSkills.map(
                    skill => `

                    <div style="margin-bottom: 14px;">

                        <strong>
                            ${skill.name || "Unknown skill"}
                        </strong>

                        ${
                            skill.category
                                ? `
                                    <br>
                                    <small>
                                        Category:
                                        ${skill.category}
                                    </small>
                                  `
                                : ""
                        }

                        ${
                            skill.importance
                                ? `
                                    <br>
                                    <small>
                                        Importance:
                                        ${skill.importance}
                                    </small>
                                  `
                                : ""
                        }

                    </div>

                `
                ).join("")

                : `
                    <p>
                        Job requirements identified
                    </p>
                `;


        // =================================================
        // AI RESUME SKILLS HTML
        // =================================================

        const aiResumeSkillsHTML =
            aiResumeSkills.length > 0

                ? aiResumeSkills.map(
                    skill => `

                    <div style="margin-bottom: 14px;">

                        <strong>
                            ${skill.name || "Unknown skill"}
                        </strong>

                        ${
                            skill.category
                                ? `
                                    <br>
                                    <small>
                                        Category:
                                        ${skill.category}
                                    </small>
                                  `
                                : ""
                        }

                        ${
                            skill.evidence
                                ? `
                                    <br>
                                    <small>
                                        Evidence:
                                        ${skill.evidence}
                                    </small>
                                  `
                                : ""
                        }

                    </div>

                `
                ).join("")

                : `
                    <p>
                        No AI-identified resume skills found.
                    </p>
                `;


        // =================================================
        // AI MATCHED SKILLS HTML
        // =================================================

        const aiMatchedSkillsHTML =
            aiMatchedSkills.length > 0

                ? aiMatchedSkills.map(
                    match => `

                    <div style="
                        margin-bottom: 16px;
                        padding-bottom: 12px;
                        border-bottom: 1px solid #e5e7eb;
                    ">

                        <strong>
                            ${match.job_skill || "Unknown JD skill"}
                        </strong>

                        →

                        <strong>
                            ${match.resume_skill || "No resume skill"}
                        </strong>

                        <br>

                        <small>
                            Match type:
                            ${match.match_type || "unknown"}
                        </small>

                        <br>

                        <small>
                            Confidence:
                            ${
                                match.confidence !== undefined
                                    ? match.confidence + "%"
                                    : "N/A"
                            }
                        </small>

                    </div>

                `
                ).join("")

                : `
                    <p>
                        No intelligent skill matches found.
                    </p>
                `;


        // =================================================
        // AI MISSING SKILLS HTML
        // =================================================

        const aiMissingSkillsHTML =
            aiMissingSkills.length > 0

                ? aiMissingSkills.map(
                    skill => `

                    <div style="
                        margin-bottom: 14px;
                        padding-bottom: 10px;
                        border-bottom: 1px solid #e5e7eb;
                    ">

                        <strong>
                            ${skill.name || "Unknown skill"}
                        </strong>

                        ${
                            skill.importance
                                ? `
                                    <br>
                                    <small>
                                        Importance:
                                        ${skill.importance}
                                    </small>
                                  `
                                : ""
                        }

                        ${
                            skill.confidence !== undefined
                                ? `
                                    <br>
                                    <small>
                                        Confidence:
                                        ${skill.confidence}%
                                    </small>
                                  `
                                : ""
                        }

                    </div>

                `
                ).join("")

                : `
                    <p>
                        No important missing skills identified by AI.
                    </p>
                `;


        // =================================================
        // AI RELATED SKILLS HTML
        // =================================================

        const aiRelatedSkillsHTML =
            aiRelatedSkills.length > 0

                ? aiRelatedSkills.map(
                    skill => {

                        return `

                            <div style="
                                margin-bottom: 16px;
                                padding-bottom: 12px;
                                border-bottom: 1px solid #e5e7eb;
                            ">

                                <strong>
                                    ${skill.job_skill || "JD skill"}
                                </strong>

                                →

                                <strong>
                                    ${
                                        skill.candidate_skill ||
                                        "Candidate skill"
                                    }
                                </strong>

                                ${
                                    skill.explanation
                                        ? `
                                            <br>
                                            <small>
                                                ${
                                                    skill.explanation
                                                }
                                            </small>
                                          `
                                        : ""
                                }

                                ${
                                    skill.confidence !== undefined
                                        ? `
                                            <br>
                                            <small>
                                                Confidence:
                                                ${skill.confidence}%
                                            </small>
                                          `
                                        : ""
                                }

                            </div>

                        `;
                    }
                ).join("")

                : `
                    <p>
                        No additional related skills identified.
                    </p>
                `;


        // =================================================
        // AI ANALYSIS SECTION
        // =================================================

        const aiAnalysisHTML = aiAnalysis

            ? `

                <br>

                <h2>
                    Intelligent Skill Analysis
                </h2>

                <div class="score-placeholder">

                    <h3>
                        Job Requirements Identified
                    </h3>

                    <div>
                        ${aiJobSkillsHTML}
                    </div>


                    <br>


                    <h3>
                        Skills Identified in Resume
                    </h3>

                    <div>
                        ${aiResumeSkillsHTML}
                    </div>


                    <br>


                    <h3>
                         Skill Matches
                    </h3>

                    <div>
                        ${aiMatchedSkillsHTML}
                    </div>


                    <br>


                    <h3>
                        Potentially Missing Skills
                    </h3>

                    <div>
                        ${aiMissingSkillsHTML}
                    </div>


                    <br>


                    <h3>
                        Related Skills
                    </h3>

                    <div>
                        ${aiRelatedSkillsHTML}
                    </div>

                </div>

            `

            : `

                <br>

                <h2>
                    Intelligent Skill Analysis
                </h2>

                <div class="score-placeholder">

                    <p>
                        Intelligent analysis is not available.
                    </p>

                </div>

            `;


        // =================================================
        // SHOW RESULTS
        // =================================================

        results.classList.remove(
            "hidden"
        );


        results.innerHTML = `

            <!-- =================================================
                 ATS SCORE
                 ================================================= -->

            <h2>
                Resume ATS Score
            </h2>

            <div class="score-placeholder">

                <h1>

                    ${formattedOverallScore}

                    <span>
                        /100
                    </span>

                </h1>

                <h3>
                    ${category} Match
                </h3>

                <p>
                    ${scoreMessage}
                </p>

            </div>


            <br>


            <!-- =================================================
                 COMPONENT SCORES
                 ================================================= -->

            <h2>
                Score Breakdown
            </h2>

            <div class="score-placeholder">

                <h3>
                    Skills Score
                </h3>

                <p>
                    ${formattedSkillsScore}/100
                </p>


                <br>


                <h3>
                    Experience Score
                </h3>

                <p>
                    ${formattedExperienceScore}/100
                </p>


                <br>


                <h3>
                    Education Score
                </h3>

                <p>
                    ${formattedEducationScore}/100
                </p>

            </div>


            <br>


            <!-- =================================================
                 DETERMINISTIC SKILL ANALYSIS
                 ================================================= -->

            <h2>
                Skill Analysis
            </h2>

            <div class="score-placeholder">

                <h3>
                    Skills Found in Job Description
                </h3>

                <p>

                    ${
                        jobDescriptionSkills.length > 0

                            ? jobDescriptionSkills.join(", ")

                            : "No recognized skills found"
                    }

                </p>


                <br>


                <h3>
                    Skills Found in Resume
                </h3>

                <p>

                    ${
                        resumeSkills.length > 0

                            ? resumeSkills.join(", ")

                            : "No recognized skills found"
                    }

                </p>


                <br>


                <h3>
                    Matched Skills
                </h3>

                <p>

                    ${
                        matchedSkills.length > 0

                            ? "✓ " +
                              matchedSkills.join(", ")

                            : "No direct matches found"
                    }

                </p>


                <br>


                <h3>
                    Missing Skills
                </h3>

                <p>

                    ${
                        missingSkills.length > 0

                            ? "⚠ " +
                              missingSkills.join(", ")

                            : "No missing recognized skills"
                    }

                </p>

            </div>


            <br>


            <!-- =================================================
                 AI INTELLIGENCE
                 ================================================= -->

            ${aiAnalysisHTML}


            <br>


            <!-- =================================================
                 EXPERIENCE ANALYSIS
                 ================================================= -->

            <h2>
                Experience Analysis
            </h2>

            <div class="score-placeholder">

                <h3>
                    Required Experience
                </h3>

                <p>

                    ${
                        experience.required_years !== null &&
                        experience.required_years !== undefined

                            ? experience.required_years +
                              " years"

                            : "No specific experience requirement found"
                    }

                </p>


                <br>


                <h3>
                    Candidate Experience
                </h3>

                <p>

                    ${
                        experience.candidate_years !== null &&
                        experience.candidate_years !== undefined

                            ? experience.candidate_years +
                              " years"

                            : "Experience could not be determined"
                    }

                </p>


                <br>


                <h3>
                    Experience Score
                </h3>

                <p>

                    ${
                        experience.score !== null &&
                        experience.score !== undefined

                            ? experience.score +
                              "/100"

                            : "Not available"
                    }

                </p>


                <br>


                <h3>
                    Status
                </h3>

                <p>

                    ${
                        experience.status ===
                        "meets_requirement"

                            ? "✓ Meets the experience requirement"

                            : experience.status ===
                              "below_requirement"

                                ? "⚠ Below the required experience"

                                : "ℹ No specific experience requirement found"
                    }

                </p>


                <br>


                <h3>
                    Analysis
                </h3>

                <p>

                    ${
                        experience.message

                            ? experience.message

                            : "No additional experience analysis available."
                    }

                </p>

            </div>


            <br>


            <!-- =================================================
                 EDUCATION ANALYSIS
                 ================================================= -->

            <h2>
                Education Analysis
            </h2>

            <div class="score-placeholder">

                <h3>
                    Required Education
                </h3>

                <p>

                    ${
                        requiredEducation.length > 0

                            ? requiredEducation.join(", ")

                            : "No specific education requirement found"
                    }

                </p>


                <br>


                <h3>
                    Candidate Education
                </h3>

                <p>

                    ${
                        candidateEducation.length > 0

                            ? candidateEducation.join(", ")

                            : "No recognized education found"
                    }

                </p>


                <br>


                <h3>
                    Required Level
                </h3>

                <p>

                    ${
                        education.required_level !== null &&
                        education.required_level !== undefined

                            ? education.required_level

                            : "Not available"
                    }

                </p>


                <br>


                <h3>
                    Candidate Level
                </h3>

                <p>

                    ${
                        education.candidate_level !== null &&
                        education.candidate_level !== undefined

                            ? education.candidate_level

                            : "Not available"
                    }

                </p>


                <br>


                <h3>
                    Education Score
                </h3>

                <p>

                    ${
                        education.score !== null &&
                        education.score !== undefined

                            ? education.score +
                              "/100"

                            : "Not available"
                    }

                </p>


                <br>


                <h3>
                    Status
                </h3>

                <p>

                    ${
                        education.status ===
                        "meets_requirement"

                            ? "✓ Meets the education requirement"

                            : education.status ===
                              "below_requirement"

                                ? "⚠ Below the required education"

                                : education.status ===
                                  "education_not_found"

                                    ? "⚠ Required education not found"

                                    : "ℹ No specific education requirement found"
                    }

                </p>


                <br>


                <h3>
                    Analysis
                </h3>

                <p>

                    ${
                        education.message

                            ? education.message

                            : "No additional education analysis available."
                    }

                </p>

            </div>

        `;


        // =================================================
        // SCROLL TO RESULTS
        // =================================================

        results.scrollIntoView({
            behavior: "smooth"
        });


    } catch (error) {

        console.error(
            "Analysis error:",
            error
        );


        alert(
            "Analysis error:\n\n" +
            error.message
        );


    } finally {

        analyzeButton.disabled = false;

        analyzeButton.textContent =
            "Analyze Resume";

    }

});