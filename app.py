from flask import Flask, render_template, request
import os
import uuid

from resume_parser import (
    extract_text_from_pdf,
    extract_skills,
    calculate_match,
    generate_suggestions
)

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "uploads"

# Create uploads folder if not exists
if not os.path.exists("uploads"):
    os.makedirs("uploads")

@app.route("/", methods=["GET", "POST"])
def index():
    score = None
    matched = []
    missing = []
    suggestions = []

    if request.method == "POST":
        resume_file = request.files["resume"]
        job_desc = request.form["job_desc"]

        # Save resume with unique name
        filename = f"{uuid.uuid4()}.pdf"
        resume_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        resume_file.save(resume_path)

        # Resume analysis
        resume_text = extract_text_from_pdf(resume_path)
        resume_skills = extract_skills(resume_text)

        job_skills = extract_skills(job_desc.lower())

        score, matched, missing = calculate_match(resume_skills, job_skills)

        suggestions = generate_suggestions(missing)

    return render_template(
        "index.html",
        score=score,
        matched=matched,
        missing=missing,
        suggestions=suggestions
    )

if __name__ == "__main__":
    app.run(debug=True)

