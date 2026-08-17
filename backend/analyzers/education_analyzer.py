import re


# =========================================================
# EDUCATION ANALYZER
# =========================================================

def normalize_text(text):
    """
    Convert text to lowercase and normalize whitespace.
    """

    if not text:
        return ""

    return re.sub(
        r"\s+",
        " ",
        str(text).lower()
    ).strip()


# =========================================================
# EXTRACT EDUCATION REQUIREMENTS
# =========================================================

def extract_education_requirements(text):
    """
    Detect common education requirements from a job description.
    """

    text = normalize_text(text)

    if not text:
        return []

    requirements = []

    education_patterns = [

        # -------------------------------------------------
        # PhD / Doctorate
        # -------------------------------------------------

        (
            r"\b(ph\.?d\.?|doctorate|doctoral degree)\b",
            "PhD"
        ),

        # -------------------------------------------------
        # Master's
        # -------------------------------------------------

        (
            r"\b("
            r"master'?s degree|"
            r"master'?s|"
            r"masters degree|"
            r"master of [a-z]+(?: [a-z]+){0,5}|"
            r"mba|"
            r"m\.?s\.?|"
            r"m\.?tech|"
            r"m\.?sc\.?"
            r")\b",
            "Master's"
        ),

        # -------------------------------------------------
        # Bachelor's
        # -------------------------------------------------

        (
            r"\b("
            r"bachelor'?s degree|"
            r"bachelor'?s|"
            r"bachelors degree|"
            r"bachelor of [a-z]+(?: [a-z]+){0,6}|"
            r"b\.?a\.?|"
            r"b\.?sc\.?|"
            r"b\.?tech|"
            r"bba|"
            r"b\.?com"
            r")\b",
            "Bachelor's"
        ),

        # -------------------------------------------------
        # Associate
        # -------------------------------------------------

        (
            r"\b("
            r"associate'?s degree|"
            r"associate degree|"
            r"associate of [a-z]+(?: [a-z]+){0,5}"
            r")\b",
            "Associate"
        ),

        # -------------------------------------------------
        # Diploma
        # -------------------------------------------------

        (
            r"\b("
            r"diploma|"
            r"diploma qualification"
            r")\b",
            "Diploma"
        )
    ]

    for pattern, education in education_patterns:

        if re.search(
            pattern,
            text,
            re.IGNORECASE
        ):

            if education not in requirements:

                requirements.append(education)

    return requirements


# =========================================================
# EXTRACT CANDIDATE EDUCATION
# =========================================================

def extract_candidate_education(text):
    """
    Detect education information present in a resume.
    """

    text = normalize_text(text)

    if not text:
        return []

    education = []

    education_patterns = [

        # -------------------------------------------------
        # PhD / Doctorate
        # -------------------------------------------------

        (
            r"\b(ph\.?d\.?|doctorate|doctoral degree)\b",
            "PhD"
        ),

        # -------------------------------------------------
        # Master's
        # -------------------------------------------------

        (
            r"\b("
            r"master'?s degree|"
            r"master'?s|"
            r"masters degree|"
            r"master of [a-z]+(?: [a-z]+){0,6}|"
            r"mba|"
            r"m\.?s\.?|"
            r"m\.?tech|"
            r"m\.?sc\.?"
            r")\b",
            "Master's"
        ),

        # -------------------------------------------------
        # Bachelor's
        # -------------------------------------------------

        (
            r"\b("
            r"bachelor'?s degree|"
            r"bachelor'?s|"
            r"bachelors degree|"
            r"bachelor of [a-z]+(?: [a-z]+){0,8}|"
            r"b\.?a\.?|"
            r"b\.?sc\.?|"
            r"b\.?tech|"
            r"bba|"
            r"b\.?com"
            r")\b",
            "Bachelor's"
        ),

        # -------------------------------------------------
        # Associate
        # -------------------------------------------------

        (
            r"\b("
            r"associate'?s degree|"
            r"associate degree|"
            r"associate of [a-z]+(?: [a-z]+){0,6}"
            r")\b",
            "Associate"
        ),

        # -------------------------------------------------
        # Diploma
        # -------------------------------------------------

        (
            r"\b("
            r"diploma|"
            r"diploma qualification"
            r")\b",
            "Diploma"
        )
    ]

    for pattern, education_name in education_patterns:

        if re.search(
            pattern,
            text,
            re.IGNORECASE
        ):

            if education_name not in education:

                education.append(
                    education_name
                )

    return education


# =========================================================
# EDUCATION LEVEL
# =========================================================

def get_education_level(education):
    """
    Convert education into a numerical level.

    Higher number = higher education level.
    """

    levels = {

        "Diploma": 1,

        "Associate": 2,

        "Bachelor's": 3,

        "Master's": 4,

        "PhD": 5
    }

    highest_level = 0
    highest_name = None

    for item in education:

        level = levels.get(
            item,
            0
        )

        if level > highest_level:

            highest_level = level
            highest_name = item

    return highest_level, highest_name


# =========================================================
# EDUCATION ANALYSIS
# =========================================================

def analyze_education(
    job_description,
    resume
):
    """
    Compare the education requirement in the job
    description against the candidate's education.
    """

    required_education = extract_education_requirements(
        job_description
    )

    candidate_education = extract_candidate_education(
        resume
    )

    # -----------------------------------------------------
    # NO EDUCATION REQUIREMENT
    # -----------------------------------------------------

    if not required_education:

        return {

            "status":
                "no_requirement",

            "required_education":
                [],

            "candidate_education":
                candidate_education,

            "required_level":
                0,

            "candidate_level":
                get_education_level(
                    candidate_education
                )[0],

            "score":
                100,

            "message":
                "No specific education requirement "
                "was found in the job description."
        }

    # -----------------------------------------------------
    # EDUCATION NOT FOUND IN RESUME
    # -----------------------------------------------------

    if not candidate_education:

        return {

            "status":
                "education_not_found",

            "required_education":
                required_education,

            "candidate_education":
                [],

            "required_level":
                get_education_level(
                    required_education
                )[0],

            "candidate_level":
                0,

            "score":
                0,

            "message":
                "The job description specifies an "
                "education requirement, but no "
                "recognized education qualification "
                "was found in the resume."
        }

    # -----------------------------------------------------
    # GET EDUCATION LEVELS
    # -----------------------------------------------------

    required_level, required_name = get_education_level(
        required_education
    )

    candidate_level, candidate_name = get_education_level(
        candidate_education
    )

    # -----------------------------------------------------
    # MEETS OR EXCEEDS REQUIREMENT
    # -----------------------------------------------------

    if candidate_level >= required_level:

        score = 100

        status = "meets_requirement"

        message = (
            f"The candidate's {candidate_name} "
            f"qualification meets or exceeds the "
            f"required {required_name} education level."
        )

    # -----------------------------------------------------
    # BELOW REQUIREMENT
    # -----------------------------------------------------

    else:

        score = int(
            (
                candidate_level /
                required_level
            ) * 100
        )

        score = max(
            0,
            min(
                score,
                100
            )
        )

        status = "below_requirement"

        message = (
            f"The candidate has {candidate_name} "
            f"education, while the job description "
            f"requests {required_name}."
        )

    # -----------------------------------------------------
    # RETURN RESULT
    # -----------------------------------------------------

    return {

        "status":
            status,

        "required_education":
            required_education,

        "candidate_education":
            candidate_education,

        "required_level":
            required_level,

        "candidate_level":
            candidate_level,

        "score":
            score,

        "message":
            message
    }