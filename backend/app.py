from flask import Flask, jsonify, request
from flask_cors import CORS

from analyzers.basic_analyzer import compare_skills
from analyzers.experience_analyzer import analyze_experience
from analyzers.education_analyzer import analyze_education
from analyzers.scoring_engine import calculate_ats_score
from analyzers.openai_analyzer import analyze_with_openai


# =========================================================
# FLASK APPLICATION
# =========================================================

app = Flask(__name__)

# Allow frontend to communicate with backend
CORS(app)


# =========================================================
# HEALTH CHECK
# =========================================================

@app.route("/api/health", methods=["GET"])
def health_check():

    return jsonify({
        "status": "success",
        "message": "Resume Score Checker backend is running"
    })


# =========================================================
# RESUME ANALYSIS
# =========================================================

@app.route("/api/analyze", methods=["POST"])
def analyze_resume():

    # -----------------------------------------------------
    # GET REQUEST DATA
    # -----------------------------------------------------

    data = request.get_json(silent=True)

    if not data:

        return jsonify({
            "status": "error",
            "message": "No JSON data received"
        }), 400


    # -----------------------------------------------------
    # GET JOB DESCRIPTION AND RESUME
    # -----------------------------------------------------

    job_description = data.get(
        "job_description",
        ""
    ).strip()

    resume = data.get(
        "resume",
        ""
    ).strip()


    # -----------------------------------------------------
    # VALIDATION
    # -----------------------------------------------------

    if not job_description:

        return jsonify({
            "status": "error",
            "message": "Job description is required"
        }), 400


    if not resume:

        return jsonify({
            "status": "error",
            "message": "Resume is required"
        }), 400


    try:

        # =================================================
        # 1. DETERMINISTIC SKILL ANALYSIS
        # =================================================

        skill_analysis = compare_skills(
            job_description,
            resume
        )


        # =================================================
        # 2. EXPERIENCE ANALYSIS
        # =================================================

        experience_analysis = analyze_experience(
            job_description,
            resume
        )


        # =================================================
        # 3. EDUCATION ANALYSIS
        # =================================================

        education_analysis = analyze_education(
            job_description,
            resume
        )


        # =================================================
        # 4. OPENAI INTELLIGENCE ANALYSIS
        # =================================================
        #
        # OpenAI is currently used as an intelligence layer.
        #
        # It can identify:
        # - Skills not present in our dictionary
        # - Synonyms
        # - Equivalent technologies
        # - Related technologies
        # - Skill importance
        # - Resume evidence
        # - Contextual matches
        #
        # IMPORTANT:
        # AI results are NOT used to calculate the ATS
        # score yet.
        #
        # We will first test the AI results against different
        # job descriptions and resumes.
        #

        ai_analysis = analyze_with_openai(
            job_description,
            resume
        )


        # =================================================
        # 5. EXISTING ATS SCORE
        # =================================================
        #
        # The existing deterministic scoring engine remains
        # unchanged at this stage.
        #
        # This allows us to compare:
        #
        # Deterministic analysis
        #          VS
        # OpenAI intelligence
        #
        # before changing the scoring system.
        #

        ats_score = calculate_ats_score(
            skill_analysis,
            experience_analysis,
            education_analysis
        )


        # =================================================
        # RETURN COMPLETE ANALYSIS
        # =================================================

        return jsonify({

            "status": "success",

            "message": "Resume analyzed successfully",

            "data": {

                # -----------------------------------------
                # CHARACTER COUNTS
                # -----------------------------------------

                "job_description_characters":
                    len(job_description),

                "resume_characters":
                    len(resume),


                # -----------------------------------------
                # DETERMINISTIC SKILLS
                # -----------------------------------------

                "skills":
                    skill_analysis,


                # -----------------------------------------
                # EXPERIENCE
                # -----------------------------------------

                "experience":
                    experience_analysis,


                # -----------------------------------------
                # EDUCATION
                # -----------------------------------------

                "education":
                    education_analysis,


                # -----------------------------------------
                # CURRENT ATS SCORE
                # -----------------------------------------

                "score":
                    ats_score,


                # -----------------------------------------
                # OPENAI INTELLIGENCE
                # -----------------------------------------

                "ai_analysis":
                    ai_analysis

            }

        })


    except Exception as error:

        # -------------------------------------------------
        # LOG ERROR IN TERMINAL
        # -------------------------------------------------

        print("Analysis error:", error)


        # -------------------------------------------------
        # RETURN ERROR TO FRONTEND
        # -------------------------------------------------

        return jsonify({

            "status": "error",

            "message":
                "An error occurred while analyzing the resume.",

            "details":
                str(error)

        }), 500


# =========================================================
# START SERVER
# =========================================================

if __name__ == "__main__":

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )