from pypdf import PdfReader

# ==========================================
# 1. RESUME PATH
# ==========================================

pdf_path = "resume_analyzer/resumes/resume.pdf"


# ==========================================
# 2. EXTRACT TEXT FROM PDF
# ==========================================

reader = PdfReader(pdf_path)

text = ""

for page in reader.pages:
    page_text = page.extract_text()

    if page_text:
        text += page_text + "\n"


# Convert text to lowercase for matching
text_lower = text.lower()


# ==========================================
# 3. SKILL DATABASE
# ==========================================

skills = [
    "Python",
    "Java",
    "SQL",
    "Machine Learning",
    "Scikit-learn",
    "Logistic Regression",
    "Decision Tree",
    "Random Forest",
    "XGBoost",
    "Pandas",
    "NumPy",
    "Matplotlib",
    "HTML",
    "CSS",
    "JavaScript",
    "Flask",
    "MySQL",
    "MongoDB",
    "Data Structures and Algorithms",
    "Object-Oriented Programming",
    "Natural Language Processing",
    "Deep Learning",
    "TensorFlow",
    "PyTorch",
    "C++",
    "Git",
    "GitHub"
]


# ==========================================
# 4. FIND SKILLS
# ==========================================

detected_skills = []

for skill in skills:

    if skill.lower() in text_lower:
        detected_skills.append(skill)


# ==========================================
# 5. DISPLAY RESULTS
# ==========================================

print("======================================")
print("       SKILLSYNC AI")
print("       RESUME ANALYZER")
print("======================================")

print("\nDetected Skills:")
print("--------------------------------------")

if detected_skills:

    for skill in detected_skills:
        print("✓", skill)

else:
    print("No skills detected.")


print("--------------------------------------")
print("Total Skills Detected:", len(detected_skills))
print("Resume analysis completed!")