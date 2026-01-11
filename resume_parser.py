import pdfplumber
from skills_list import SKILLS

# -------- PDF TEXT EXTRACTION --------
def extract_text_from_pdf(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text.lower()

# -------- SKILL EXTRACTION --------
def extract_skills(text):
    found_skills = set()
    for skill in SKILLS:
        if skill in text:
            found_skills.add(skill)
    return list(found_skills)

# -------- JOB MATCHING --------
def calculate_match(resume_skills, job_skills):
    resume_set = set(resume_skills)
    job_set = set(job_skills)

    matched = resume_set.intersection(job_set)
    missing = job_set - resume_set

    if len(job_set) == 0:
        score = 0
    else:
        score = round((len(matched) / len(job_set)) * 100, 2)

    return score, matched, missing

# -------- RESUME IMPROVEMENT SUGGESTIONS --------
def generate_suggestions(missing_skills):
    suggestions = []

    if not missing_skills:
        suggestions.append(
            "Your resume is well aligned with the job description. No major improvements needed."
        )
        return suggestions

    suggestions.append(
        "To improve your resume match score, consider adding or highlighting the following skills:"
    )

    for skill in missing_skills:
        suggestions.append(f"Add experience or projects related to {skill.capitalize()}")

    suggestions.append(
        "You can include these skills through projects, internships, certifications, or coursework."
    )

    return suggestions





