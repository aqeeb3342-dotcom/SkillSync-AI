from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import joblib
from pypdf import PdfReader

app = Flask(__name__)
CORS(app)

# ==========================================
# LOAD PLACEMENT MODEL
# ==========================================

model = joblib.load("models/placement_model.pkl")


# ==========================================
# RESUME SKILLS
# ==========================================

SKILLS = [
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
# HOME
# ==========================================

@app.route("/")
def home():

    return jsonify({
        "project": "SkillSync AI",
        "message": "AI-Based Career Guidance & Placement Prediction",
        "status": "Backend is running successfully"
    })


# ==========================================
# HEALTH CHECK
# ==========================================

@app.route("/health")
def health():

    return jsonify({
        "status": "OK"
    })


# ==========================================
# PROJECT MODULES
# ==========================================

@app.route("/api/project")
def project():

    return jsonify({

        "placement_prediction": True,

        "resume_analysis": True,

        "skill_gap_analysis": True,

        "career_recommendation": True,

        "learning_recommendation": True

    })


# ==========================================
# PLACEMENT PREDICTION
# ==========================================

@app.route("/api/predict", methods=["POST"])
def predict():

    data = request.get_json()

    student = pd.DataFrame([{

        "gender": data["gender"],

        "ssc_p": float(data["ssc_p"]),

        "ssc_b": data["ssc_b"],

        "hsc_p": float(data["hsc_p"]),

        "hsc_b": data["hsc_b"],

        "hsc_s": data["hsc_s"],

        "degree_p": float(data["degree_p"]),

        "degree_t": data["degree_t"],

        "workex": data["workex"],

        "etest_p": float(data["etest_p"]),

        "specialisation":
            data["specialisation"],

        "mba_p": float(data["mba_p"])

    }])


    prediction = model.predict(student)[0]

    probability = model.predict_proba(student)[0][1]

    readiness = round(
        probability * 100,
        2
    )


    if prediction == 1:

        result = "PLACED"

    else:

        result = "NOT PLACED"


    return jsonify({

        "prediction": result,

        "readiness": readiness

    })


# ==========================================
# RESUME ANALYZER
# ==========================================

@app.route(
    "/api/analyze-resume",
    methods=["POST"]
)
def analyze_resume():

    if "resume" not in request.files:

        return jsonify({
            "error":
                "No resume file uploaded"
        }), 400


    file = request.files["resume"]


    if file.filename == "":

        return jsonify({
            "error":
                "No file selected"
        }), 400


    if not file.filename.lower().endswith(".pdf"):

        return jsonify({
            "error":
                "Only PDF files are supported"
        }), 400


    # Read PDF directly

    reader = PdfReader(file.stream)

    text = ""


    for page in reader.pages:

        page_text = page.extract_text()

        if page_text:

            text += page_text + "\n"


    text_lower = text.lower()


    # Detect skills

    detected_skills = []


    for skill in SKILLS:

        if skill.lower() in text_lower:

            detected_skills.append(skill)


    return jsonify({

        "filename":
            file.filename,

        "skills":
            detected_skills,

        "total_skills":
            len(detected_skills)

    })


# ==========================================
# SKILL GAP ANALYSIS
# ==========================================

@app.route(
    "/api/skill-gap",
    methods=["POST"]
)
def skill_gap():

    data = request.get_json()

    student_skills = data.get(
        "skills",
        []
    )

    career = data.get(
        "career",
        "Data Analyst"
    )


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


    # Convert student skills to lowercase

    student_skills_lower = [

        skill.lower()

        for skill in student_skills

    ]


    # Find matched skills

    matched_skills = []


    for skill in required_skills:

        if skill.lower() in student_skills_lower:

            matched_skills.append(skill)


    # Find missing skills

    missing_skills = []


    for skill in required_skills:

        if skill.lower() not in student_skills_lower:

            missing_skills.append(skill)


    # Calculate match percentage

    match_percentage = round(

        (
            len(matched_skills)
            /
            len(required_skills)
        )
        * 100,

        2

    )


    return jsonify({

        "career":
            career,

        "required_skills":
            required_skills,

        "matched_skills":
            matched_skills,

        "missing_skills":
            missing_skills,

        "match_percentage":
            match_percentage

    })


# ==========================================
# CAREER RECOMMENDATION
# ==========================================

@app.route(
    "/api/career-recommendation",
    methods=["POST"]
)
def career_recommendation():

    data = request.get_json()

    student_skills = data.get(
        "skills",
        []
    )


    student_skills_lower = [

        skill.lower()

        for skill in student_skills

    ]


    career_skills = {

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


    recommendations = []


    for career, required_skills in career_skills.items():

        matched_skills = []

        missing_skills = []


        for skill in required_skills:

            if skill.lower() in student_skills_lower:

                matched_skills.append(skill)

            else:

                missing_skills.append(skill)


        match_percentage = round(

            (
                len(matched_skills)
                /
                len(required_skills)
            )
            * 100,

            2

        )


        recommendations.append({

            "career":
                career,

            "match_percentage":
                match_percentage,

            "matched_skills":
                matched_skills,

            "missing_skills":
                missing_skills

        })


    # Sort by match percentage

    recommendations.sort(

        key=lambda x:
            x["match_percentage"],

        reverse=True

    )


    return jsonify({

        "recommendations":
            recommendations

    })


# ==========================================
# LEARNING RECOMMENDATION
# ==========================================

@app.route(
    "/api/learning-recommendation",
    methods=["POST"]
)
def learning_recommendation():

    data = request.get_json()

    missing_skills = data.get(
        "missing_skills",
        []
    )


    # Learning resources

    learning_resources = {

        "Python":
            "Learn Python basics, functions, OOP and problem solving.",

        "SQL":
            "Learn SQL queries, joins, subqueries, grouping and databases.",

        "Pandas":
            "Learn Pandas for data cleaning, filtering and data analysis.",

        "NumPy":
            "Learn NumPy arrays, mathematical operations and numerical computing.",

        "Excel":
            "Learn Excel formulas, functions, pivot tables and data analysis.",

        "Power BI":
            "Learn Power BI dashboards, reports and data visualization.",

        "Statistics":
            "Learn descriptive statistics, probability and basic statistical analysis.",

        "Data Visualization":
            "Learn charts, graphs, dashboards and visual storytelling.",

        "Git":
            "Learn Git commands, repositories, branching and version control.",

        "Machine Learning":
            "Learn supervised learning, classification, regression and model evaluation.",

        "Scikit-learn":
            "Learn Scikit-learn preprocessing, model training and evaluation.",

        "XGBoost":
            "Learn gradient boosting, XGBoost training and model tuning.",

        "Flask":
            "Learn Flask APIs, routes, requests and backend development.",

        "Data Structures and Algorithms":
            "Practice arrays, strings, linked lists, stacks, queues, trees and algorithms.",

        "Object-Oriented Programming":
            "Learn classes, objects, inheritance, polymorphism and encapsulation.",

        "HTML":
            "Learn HTML structure, forms, tables and semantic elements.",

        "CSS":
            "Learn CSS layouts, Flexbox, Grid and responsive design.",

        "JavaScript":
            "Learn JavaScript fundamentals, DOM manipulation and APIs.",

        "MySQL":
            "Learn database design, SQL queries, joins and database management.",

        "MongoDB":
            "Learn MongoDB collections, documents, queries and CRUD operations.",

        "Natural Language Processing":
            "Learn text preprocessing, tokenization, TF-IDF and basic NLP techniques.",

        "Deep Learning":
            "Learn neural networks, backpropagation and deep learning frameworks.",

        "TensorFlow":
            "Learn TensorFlow models, neural networks and model training.",

        "PyTorch":
            "Learn PyTorch tensors, neural networks and deep learning workflows."

    }


    recommendations = []


    for skill in missing_skills:

        if skill in learning_resources:

            recommendations.append({

                "skill":
                    skill,

                "recommendation":
                    learning_resources[skill]

            })

        else:

            recommendations.append({

                "skill":
                    skill,

                "recommendation":
                    "Find beginner-level courses and practice projects for this skill."

            })


    return jsonify({

        "missing_skills":
            missing_skills,

        "recommendations":
            recommendations

    })


# ==========================================
# START FLASK SERVER
# ==========================================

if __name__ == "__main__":

    app.run(
        debug=True
    )