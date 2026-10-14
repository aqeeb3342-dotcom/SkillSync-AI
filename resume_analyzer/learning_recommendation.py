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


# Required skills for Data Analyst
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


# Find missing skills
missing_skills = []

for skill in required_skills:
    if skill.lower() not in text:
        missing_skills.append(skill)


# Learning recommendations
learning_resources = {
    "Excel": "Learn Excel fundamentals, formulas, functions and data analysis.",
    "Power BI": "Learn Power BI dashboards, reports and data visualization.",
    "Statistics": "Learn descriptive statistics, probability and basic statistical analysis.",
    "Data Visualization": "Learn charts, graphs, dashboards and visual storytelling.",
    "Python": "Learn Python programming, functions, libraries and problem solving.",
    "SQL": "Learn SQL queries, joins, filtering, grouping and database operations.",
    "Pandas": "Learn Pandas for data cleaning, manipulation and analysis.",
    "NumPy": "Learn NumPy arrays, mathematical operations and numerical computing."
}


# Display result
print("======================================")
print("       SKILLSYNC AI")
print("  LEARNING RECOMMENDATION")
print("======================================")

print("\nMissing Skills:")
print("--------------------------------------")

if missing_skills:

    for skill in missing_skills:
        print("✗", skill)

    print("\nRecommended Learning:")
    print("--------------------------------------")

    for skill in missing_skills:
        print("\n", skill)
        print("→", learning_resources[skill])

else:
    print("No missing skills found!")
    print("Student has all required skills.")

print("--------------------------------------")
print("Learning recommendation completed!")