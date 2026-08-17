import os
from pathlib import Path

from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS

from analyzers.basic_analyzer import compare_skills
from analyzers.experience_analyzer import analyze_experience
from analyzers.education_analyzer import analyze_education
from analyzers.scoring_engine import calculate_ats_score
from analyzers.openai_analyzer import analyze_with_openai


# =========================================================
# PATH CONFIGURATION
# =========================================================

BASE_DIR = Path(__file__).resolve().parent
FRONTEND_DIR = BASE_DIR.parent / "frontend"


# =========================================================
# FLASK APPLICATION
# =========================================================

app = Flask(__name__)

CORS(app)


# =========================================================
# FRONTEND
# =========================================================

@app.route("/", methods=["GET"])
def serve_index():

    return send_from_directory(
        FRONTEND_DIR,
        "index.html"
    )


@app.route("/<path:filename>", methods=["GET"])
def serve_frontend_file(filename):

    return send_from_directory(
        FRONTEND_DIR,
        filename
    )


# =========================================================
# HEALTH CHECK
# =========================================================

@app.route("/api/health", methods=["GET"])
def health_check():

    return jsonify({
        "status": "success",
        "message": "FyndHR backend is running"
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
    # GET JOB DESCRIPTION
    # -----------------------------------------------------

    job_description = data.get(
        "job_description",
        ""
    ).strip()


    # -----------------------------------------------------
    # GET RESUME
    # -----------------------------------------------------

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

        ai_analysis = analyze_with_openai(
            job_description,
            resume
        )


        # =================================================
        # 5. ATS SCORE
        # =================================================

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
                # SKILLS
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
                # ATS SCORE
                # -----------------------------------------

                "score":
                    ats_score,


                # -----------------------------------------
                # AI ANALYSIS
                # -----------------------------------------

                "ai_analysis":
                    ai_analysis

            }

        })


    except Exception as error:

        print(
            "Analysis error:",
            error
        )


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

    port = int(
        os.environ.get(
            "PORT",
            5000
        )
    )

    app.run(
        host="0.0.0.0",
        port=port,
        debug=False
    )