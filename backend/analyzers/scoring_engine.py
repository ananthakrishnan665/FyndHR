# =========================================================
# ATS SCORING ENGINE
# =========================================================
#
# Combines:
#   - Skills Analysis
#   - Experience Analysis
#   - Education Analysis
#
# Overall weighting:
#   Skills     = 50%
#   Experience = 30%
#   Education  = 20%
#
# =========================================================


def calculate_ats_score(
    skill_analysis,
    experience_analysis,
    education_analysis
):
    """
    Calculate the overall ATS score from the individual
    analyzer results.
    """

    # -----------------------------------------------------
    # SAFETY CHECKS
    # -----------------------------------------------------

    if not isinstance(skill_analysis, dict):
        skill_analysis = {}

    if not isinstance(experience_analysis, dict):
        experience_analysis = {}

    if not isinstance(education_analysis, dict):
        education_analysis = {}


    # -----------------------------------------------------
    # SKILLS SCORE
    # -----------------------------------------------------

    matched_skills = skill_analysis.get(
        "matched_skills",
        []
    )

    job_description_skills = skill_analysis.get(
        "job_description_skills",
        []
    )

    if not isinstance(matched_skills, list):
        matched_skills = []

    if not isinstance(job_description_skills, list):
        job_description_skills = []


    if len(job_description_skills) > 0:

        skill_score = (
            len(matched_skills)
            / len(job_description_skills)
        ) * 100

    else:

        # No recognized skills in JD.
        # Do not penalize candidate.
        skill_score = 100


    skill_score = max(
        0,
        min(skill_score, 100)
    )


    # -----------------------------------------------------
    # EXPERIENCE SCORE
    # -----------------------------------------------------

    experience_score = experience_analysis.get(
        "score"
    )

    experience_status = experience_analysis.get(
        "status"
    )


    if experience_score is None:

        # No explicit experience requirement.
        experience_score = 100

    else:

        try:
            experience_score = float(
                experience_score
            )
        except (TypeError, ValueError):
            experience_score = 100


    experience_score = max(
        0,
        min(experience_score, 100)
    )


    # -----------------------------------------------------
    # EDUCATION SCORE
    # -----------------------------------------------------

    education_score = education_analysis.get(
        "score"
    )

    education_status = education_analysis.get(
        "status"
    )


    if education_score is None:

        # No explicit education requirement.
        education_score = 100

    else:

        try:
            education_score = float(
                education_score
            )
        except (TypeError, ValueError):
            education_score = 100


    education_score = max(
        0,
        min(education_score, 100)
    )


    # -----------------------------------------------------
    # WEIGHTED SCORE
    # -----------------------------------------------------

    weighted_score = (

        (skill_score * 0.50)

        + (experience_score * 0.30)

        + (education_score * 0.20)

    )


    # Round to two decimal places
    overall_score = round(
        weighted_score,
        2
    )


    # -----------------------------------------------------
    # SCORE CATEGORY
    # -----------------------------------------------------

    if overall_score >= 90:

        category = "Excellent"

        message = (
            "Your resume is a very strong match "
            "for this job description."
        )

    elif overall_score >= 75:

        category = "Strong"

        message = (
            "Your resume is a strong match, "
            "but there are some areas that could "
            "be improved."
        )

    elif overall_score >= 60:

        category = "Moderate"

        message = (
            "Your resume has a moderate match "
            "with the job description. "
            "Several areas could be improved."
        )

    elif overall_score >= 40:

        category = "Weak"

        message = (
            "Your resume has a relatively weak "
            "match with the job description."
        )

    else:

        category = "Poor"

        message = (
            "Your resume currently has a low match "
            "with the job description."
        )


    # -----------------------------------------------------
    # RETURN RESULT
    # -----------------------------------------------------

    return {

        "overall_score":
            overall_score,

        "category":
            category,

        "message":
            message,

        "component_scores": {

            "skills":
                round(skill_score, 2),

            "experience":
                round(experience_score, 2),

            "education":
                round(education_score, 2)

        },

        "weights": {

            "skills":
                50,

            "experience":
                30,

            "education":
                20

        }

    }