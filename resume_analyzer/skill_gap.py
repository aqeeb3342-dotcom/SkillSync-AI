from pypdf import PdfReader


# ==========================================
# 1. READ RESUME
# ==========================================

pdf_path = "resume_analyzer/resumes/resume.pdf"

reader = PdfReader(pdf_path)

text = ""

for page in reader.pages:
    page_text = page.extract_text()

    if page_text:
        text += page_text + "\n"


text = text.lower()


# ==========================================
# 2. DETECTED STUDENT SKILLS
# ==========================================

skills = [
    "Python",
    "Java",
    "SQL",
    "Machine Learning",
    "Scikit-learn",
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
    "XGBoost",
    "TensorFlow",
    "PyTorch",
    "Git",
    "GitHub"
]


detected_skills = []

for skill in skills:

    if skill.lower() in text:
        detected_skills.append(skill)


# ==========================================
# 3. CAREER ROLE
# ==========================================

role = "Data Analyst"


# ==========================================
# 4. REQUIRED SKILLS FOR DATA ANALYST
# ==========================================

required_skills = [
    "Python",
    "SQL",
    "Pandas",
    "NumPy",
    "Excel",
    "Power BI",
    "Statistics",
    "Data Visualization"
]


# ==========================================
# 5. FIND SKILL GAP
# ==========================================

skill_gap = []

for skill in required_skills:

    if skill.lower() not in text:
        skill_gap.append(skill)


# ==========================================
# 6. DISPLAY RESULTS
# ==========================================

print("======================================")
print("       SKILLSYNC AI")
print("       SKILL GAP ANALYSIS")
print("======================================")

print("\nTarget Career:", role)

print("\nStudent Skills:")
print("--------------------------------------")

for skill in detected_skills:
    print("✓", skill)


print("\nRequired Skills:")
print("--------------------------------------")

for skill in required_skills:
    print("✓", skill)


print("\nSkill Gap:")
print("--------------------------------------")

if skill_gap:

    for skill in skill_gap:
        print("✗", skill)

else:
    print("No skill gap found!")


print("--------------------------------------")
print("Skills Missing:", len(skill_gap))

print("\nSkill gap analysis completed!")