import re


# ============================================================
# SKILL DATABASE
# ============================================================
# This is our initial deterministic skill dictionary.
# We will expand this substantially later.
# ============================================================

SKILL_ALIASES = {

    # Programming
    "Python": [
        "python",
        "python programming"
    ],

    "Java": [
        "java"
    ],

    "JavaScript": [
        "javascript",
        "js"
    ],

    "TypeScript": [
        "typescript",
        "ts"
    ],

    "C++": [
        "c++"
    ],

    "C#": [
        "c#",
        "c sharp"
    ],

    # Data
    "SQL": [
        "sql",
        "structured query language"
    ],

    "Excel": [
        "excel",
        "microsoft excel",
        "ms excel"
    ],

    "Power BI": [
        "power bi",
        "powerbi"
    ],

    "Tableau": [
        "tableau"
    ],

    "R": [
        "r programming",
        "r language"
    ],

    "Pandas": [
        "pandas"
    ],

    "NumPy": [
        "numpy"
    ],

    # Databases
    "MySQL": [
        "mysql"
    ],

    "PostgreSQL": [
        "postgresql",
        "postgres"
    ],

    "MongoDB": [
        "mongodb",
        "mongo db"
    ],

    "Oracle": [
        "oracle database",
        "oracle"
    ],

    # Cloud
    "AWS": [
        "aws",
        "amazon web services"
    ],

    "Azure": [
        "azure",
        "microsoft azure"
    ],

    "Google Cloud": [
        "google cloud",
        "gcp",
        "google cloud platform"
    ],

    # Web
    "HTML": [
        "html"
    ],

    "CSS": [
        "css"
    ],

    "React": [
        "react",
        "react.js",
        "reactjs"
    ],

    "Angular": [
        "angular"
    ],

    "Vue.js": [
        "vue",
        "vue.js",
        "vuejs"
    ],

    "Node.js": [
        "node",
        "node.js",
        "nodejs"
    ],

    # DevOps
    "Docker": [
        "docker"
    ],

    "Kubernetes": [
        "kubernetes",
        "k8s"
    ],

    "Git": [
        "git"
    ],

    "GitHub": [
        "github"
    ],

    "Jenkins": [
        "jenkins"
    ],

    # Cybersecurity
    "Cybersecurity": [
        "cybersecurity",
        "cyber security",
        "information security",
        "infosec"
    ],

    "Network Security": [
        "network security"
    ],

    "SIEM": [
        "siem"
    ],

    "Splunk": [
        "splunk"
    ],

    "Wireshark": [
        "wireshark"
    ],

    "Incident Response": [
        "incident response"
    ],

    "Penetration Testing": [
        "penetration testing",
        "penetration test",
        "pentesting",
        "pen testing"
    ],

    # Business / Management
    "Project Management": [
        "project management"
    ],

    "Agile": [
        "agile"
    ],

    "Scrum": [
        "scrum"
    ],

    "Communication": [
        "communication skills",
        "communication"
    ],

    "Leadership": [
        "leadership",
        "leadership skills"
    ],

    "Problem Solving": [
        "problem solving",
        "problem-solving"
    ],

    "Analytical Skills": [
        "analytical skills",
        "analytical thinking",
        "analytical"
    ],

    # Marketing
    "Digital Marketing": [
        "digital marketing"
    ],

    "SEO": [
        "seo",
        "search engine optimization"
    ],

    "Social Media Marketing": [
        "social media marketing"
    ],

    "Content Marketing": [
        "content marketing"
    ],

    # Finance
    "Financial Analysis": [
        "financial analysis"
    ],

    "Financial Modeling": [
        "financial modeling",
        "financial modelling"
    ],

    "Accounting": [
        "accounting"
    ],

    "Financial Reporting": [
        "financial reporting"
    ]
}


# ============================================================
# TEXT NORMALIZATION
# ============================================================

def normalize_text(text):
    """
    Normalize text for reliable skill matching.
    """

    if not text:
        return ""

    text = str(text).lower()

    # Normalize common punctuation
    text = text.replace("–", "-")
    text = text.replace("—", "-")

    # Normalize multiple spaces
    text = re.sub(r"\s+", " ", text)

    return text.strip()


# ============================================================
# SKILL MATCHING
# ============================================================

def skill_exists(text, alias):
    """
    Check whether a skill alias exists in the text.

    Word-boundary matching prevents false positives such as:
    'r' matching every letter r.
    """

    alias = alias.lower().strip()

    # Special handling for very short aliases
    if len(alias) <= 2:

        pattern = r"(?<![a-zA-Z0-9])" + re.escape(alias) + r"(?![a-zA-Z0-9])"

    else:

        pattern = r"(?<![a-zA-Z0-9])" + re.escape(alias) + r"(?![a-zA-Z0-9])"

    return re.search(pattern, text, re.IGNORECASE) is not None


# ============================================================
# EXTRACT SKILLS
# ============================================================

def extract_skills(text):
    """
    Extract recognized skills from a piece of text.

    Returns canonical skill names.
    """

    text = normalize_text(text)

    if not text:
        return []

    found_skills = []

    for canonical_skill, aliases in SKILL_ALIASES.items():

        for alias in aliases:

            if skill_exists(text, alias):

                found_skills.append(canonical_skill)

                # Once one alias matches, stop checking
                # other aliases for this skill.
                break

    return sorted(set(found_skills))


# ============================================================
# COMPARE SKILLS
# ============================================================

def compare_skills(job_description, resume):
    """
    Compare skills found in the job description
    against skills found in the resume.

    Returns a structured dictionary that the Flask
    API can send directly to the frontend.
    """

    jd_skills = set(
        extract_skills(job_description)
    )

    resume_skills = set(
        extract_skills(resume)
    )


    # --------------------------------------------------------
    # MATCHED SKILLS
    # --------------------------------------------------------

    matched_skills = sorted(
        jd_skills.intersection(resume_skills)
    )


    # --------------------------------------------------------
    # MISSING SKILLS
    # --------------------------------------------------------

    missing_skills = sorted(
        jd_skills.difference(resume_skills)
    )


    # --------------------------------------------------------
    # BASELINE SKILL SCORE
    # --------------------------------------------------------

    total_jd_skills = len(jd_skills)

    matched_skill_count = len(matched_skills)


    if total_jd_skills == 0:

        skill_score = None

    else:

        skill_score = round(
            (
                matched_skill_count
                / total_jd_skills
            ) * 100
        )


    # --------------------------------------------------------
    # RETURN RESULT
    # --------------------------------------------------------

    return {

        "job_description_skills":
            sorted(jd_skills),

        "resume_skills":
            sorted(resume_skills),

        "matched_skills":
            matched_skills,

        "missing_skills":
            missing_skills,

        "skill_score":
            skill_score,

        "matched_count":
            matched_skill_count,

        "job_description_skill_count":
            total_jd_skills,

        "resume_skill_count":
            len(resume_skills)

    }