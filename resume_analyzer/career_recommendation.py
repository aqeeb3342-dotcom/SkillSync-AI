from pypdf import PdfReader

# Load resume
pdf_path = "resume_analyzer/resumes/resume.pdf"
reader = PdfReader(pdf_path)

text = ""

for page in reader.pages:
    page_text = page.extract_text()
    if page_text:
        text += page_text + "\n"

text = text.lower()

# Skills to search
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
    "GitHub",
    "Excel",
    "Power BI",
    "Statistics",
    "Data Visualization"
]

detected_skills = []

for skill in skills:
    if skill.lower() in text:
        detected_skills.append(skill)


# Career roles and required skills
career_roles = {
    "Data Analyst": [
        "Python",
        "SQL",
        "Pandas",
        "NumPy",
        "Excel",
        "Power BI",
        "Statistics",
        "Data Visualization"
    ],

    "Python Developer": [
        "Python",
        "SQL",
        "Flask",
        "Git",
        "Data Structures and Algorithms",
        "Object-Oriented Programming"
    ],

    "Machine Learning Engineer": [
        "Python",
        "Machine Learning",
        "Scikit-learn",
        "Pandas",
        "NumPy",
        "Statistics",
        "XGBoost"
    ],

    "Web Developer": [
        "HTML",
        "CSS",
        "JavaScript",
        "Flask",
        "Git"
    ]
}


# Calculate matching percentage
recommendations = []

for role, required_skills in career_roles.items():

    matched = 0

    for skill in required_skills:
        if skill.lower() in text:
            matched += 1

    percentage = (matched / len(required_skills)) * 100

    recommendations.append(
        (role, matched, len(required_skills), percentage)
    )


# Sort by matching percentage
recommendations.sort(key=lambda x: x[3], reverse=True)


# Display result
print("======================================")
print("       SKILLSYNC AI")
print("   CAREER RECOMMENDATION")
print("======================================")

print("\nDetected Skills:")
print("--------------------------------------")

for skill in detected_skills:
    print("✓", skill)

print("\nCareer Recommendations:")
print("--------------------------------------")

for role, matched, total, percentage in recommendations:
    print(
        f"{role}: {percentage:.2f}% match "
        f"({matched}/{total} skills)"
    )

print("--------------------------------------")

print("\nTop Recommended Career:")
print(recommendations[0][0])

print("\nCareer recommendation completed!")