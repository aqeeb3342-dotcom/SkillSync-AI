import pandas as pd
import joblib

# ==========================================
# 1. LOAD TRAINED MODEL
# ==========================================

model = joblib.load("models/placement_model.pkl")

print("======================================")
print("       SKILLSYNC AI")
print("   PLACEMENT PREDICTION SYSTEM")
print("======================================")

# ==========================================
# 2. GET STUDENT INPUT
# ==========================================

gender = input("Gender (M/F): ")
ssc_p = float(input("SSC Percentage: "))
ssc_b = input("SSC Board (Central/Others): ")

hsc_p = float(input("HSC Percentage: "))
hsc_b = input("HSC Board (Central/Others): ")
hsc_s = input("HSC Stream (Commerce/Science/Arts): ")

degree_p = float(input("Degree Percentage: "))
degree_t = input("Degree Type (Sci&Tech/Comm&Mgmt/Others): ")

workex = input("Work Experience (Yes/No): ")

etest_p = float(input("Employability Test Percentage: "))

specialisation = input(
    "Specialisation (Mkt&HR/Mkt&Fin): "
)

mba_p = float(input("MBA Percentage: "))


# ==========================================
# 3. CREATE STUDENT DATA
# ==========================================

student = pd.DataFrame([{

    "gender": gender,
    "ssc_p": ssc_p,
    "ssc_b": ssc_b,
    "hsc_p": hsc_p,
    "hsc_b": hsc_b,
    "hsc_s": hsc_s,
    "degree_p": degree_p,
    "degree_t": degree_t,
    "workex": workex,
    "etest_p": etest_p,
    "specialisation": specialisation,
    "mba_p": mba_p

}])


# ==========================================
# 4. MAKE PREDICTION
# ==========================================

prediction = model.predict(student)[0]


# ==========================================
# 5. GET PROBABILITY
# ==========================================

probability = model.predict_proba(student)[0][1]

readiness = round(probability * 100, 2)


# ==========================================
# 6. DISPLAY RESULT
# ==========================================

print("\n======================================")
print("          PREDICTION RESULT")
print("======================================")

if prediction == 1:
    print("Placement Prediction : PLACED")
else:
    print("Placement Prediction : NOT PLACED")

print("Placement Readiness  :", readiness, "%")

print("======================================")