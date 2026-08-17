import re


# ============================================================
# EXPERIENCE ANALYZER
# ============================================================


def extract_year_requirements(text):
    """
    Extract explicit years-of-experience requirements
    from a job description or resume.
    """

    if not text:
        return []

    text = str(text).lower()

    patterns = [
        r'(\d+)\s*\+?\s*years?',
        r'(\d+)\s*-\s*(\d+)\s*years?',
        r'minimum\s+of\s+(\d+)\s*years?',
        r'at\s+least\s+(\d+)\s*years?',
    ]

    results = []

    for pattern in patterns:

        matches = re.findall(pattern, text)

        for match in matches:

            if isinstance(match, tuple):

                for value in match:

                    if value:
                        try:
                            results.append(float(value))
                        except ValueError:
                            pass

            else:

                try:
                    results.append(float(match))
                except ValueError:
                    pass

    return results


def extract_max_experience(text):
    """
    Detect phrases such as:

    'less than 3 years'
    'up to 2 years'
    'maximum 5 years'
    """

    if not text:
        return None

    text = str(text).lower()

    patterns = [
        r'less\s+than\s+(\d+)\s*years?',
        r'up\s+to\s+(\d+)\s*years?',
        r'maximum\s+of\s+(\d+)\s*years?',
        r'maximum\s+(\d+)\s*years?',
    ]

    for pattern in patterns:

        match = re.search(pattern, text)

        if match:

            try:
                return float(match.group(1))
            except ValueError:
                return None

    return None


def estimate_candidate_experience(resume):
    """
    Estimate total experience from explicit statements
    in the resume.

    This is intentionally conservative.

    We only use explicit year statements for now.
    Later we can add date-range calculation.
    """

    years = extract_year_requirements(resume)

    if not years:
        return None

    return max(years)


def analyze_experience(job_description, resume):
    """
    Compare required experience with candidate experience.
    """

    jd_years = extract_year_requirements(job_description)

    candidate_years = estimate_candidate_experience(resume)

    max_allowed = extract_max_experience(job_description)


    # --------------------------------------------------------
    # No explicit experience requirement
    # --------------------------------------------------------

    if not jd_years:

        return {
            "status": "not_specified",
            "required_years": None,
            "candidate_years": candidate_years,
            "score": None,
            "message": (
                "The job description does not specify "
                "a clear years-of-experience requirement."
            )
        }


    # --------------------------------------------------------
    # Required experience
    # --------------------------------------------------------

    required_years = max(jd_years)


    # --------------------------------------------------------
    # Candidate experience unavailable
    # --------------------------------------------------------

    if candidate_years is None:

        return {
            "status": "unknown",
            "required_years": required_years,
            "candidate_years": None,
            "score": None,
            "message": (
                "The resume does not contain a clear "
                "numeric years-of-experience statement."
            )
        }


    # --------------------------------------------------------
    # Candidate meets requirement
    # --------------------------------------------------------

    if candidate_years >= required_years:

        return {
            "status": "meets_requirement",
            "required_years": required_years,
            "candidate_years": candidate_years,
            "score": 100,
            "message": (
                "The candidate meets or exceeds "
                "the stated experience requirement."
            )
        }


    # --------------------------------------------------------
    # Candidate has partial experience
    # --------------------------------------------------------

    score = round(
        (candidate_years / required_years) * 100
    )

    score = max(0, min(score, 100))


    return {
        "status": "below_requirement",
        "required_years": required_years,
        "candidate_years": candidate_years,
        "score": score,
        "message": (
            f"The candidate has approximately "
            f"{candidate_years:g} years of experience, "
            f"while the job description requests "
            f"{required_years:g} years."
        )
    }