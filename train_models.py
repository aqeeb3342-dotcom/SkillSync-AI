import pandas as pd
import joblib
import os

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import Pipeline

from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier

from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score


# ==========================================
# 1. LOAD DATASET
# ==========================================

df = pd.read_csv("data/placement_data.csv")

print("Dataset loaded successfully!")
print("Shape:", df.shape)


# ==========================================
# 2. REMOVE UNNECESSARY COLUMNS
# ==========================================

df = df.drop(columns=["sl_no", "salary"])


# ==========================================
# 3. SEPARATE FEATURES AND TARGET
# ==========================================

X = df.drop(columns=["status"])

y = df["status"].map({
    "Placed": 1,
    "Not Placed": 0
})


# ==========================================
# 4. IDENTIFY COLUMN TYPES
# ==========================================

categorical_columns = X.select_dtypes(
    include=["object"]
).columns.tolist()

numeric_columns = X.select_dtypes(
    exclude=["object"]
).columns.tolist()


print("\nCategorical columns:")
print(categorical_columns)

print("\nNumerical columns:")
print(numeric_columns)


# ==========================================
# 5. PREPROCESSING
# ==========================================

preprocessor = ColumnTransformer(
    transformers=[
        (
            "num",
            StandardScaler(),
            numeric_columns
        ),
        (
            "cat",
            OneHotEncoder(handle_unknown="ignore"),
            categorical_columns
        )
    ]
)


# ==========================================
# 6. TRAIN-TEST SPLIT
# ==========================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

print("\nTraining samples:", len(X_train))
print("Testing samples:", len(X_test))


# ==========================================
# 7. DEFINE MODELS
# ==========================================

models = {

    "Logistic Regression": LogisticRegression(
        max_iter=1000
    ),

    "Decision Tree": DecisionTreeClassifier(
        random_state=42
    ),

    "Random Forest": RandomForestClassifier(
        n_estimators=100,
        random_state=42
    ),

    "XGBoost": XGBClassifier(
        n_estimators=100,
        max_depth=3,
        learning_rate=0.1,
        random_state=42,
        eval_metric="logloss"
    )
}


# ==========================================
# 8. TRAIN AND EVALUATE
# ==========================================

results = {}
pipelines = {}

print("\n======================================")
print("MODEL RESULTS")
print("======================================")


for name, model in models.items():

    pipeline = Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            ("model", model)
        ]
    )

    pipeline.fit(X_train, y_train)

    y_pred = pipeline.predict(X_test)

    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)

    results[name] = {
        "Accuracy": accuracy,
        "Precision": precision,
        "Recall": recall,
        "F1 Score": f1
    }

    pipelines[name] = pipeline

    print("\n" + name)
    print("-----------------------------")
    print("Accuracy :", round(accuracy, 4))
    print("Precision:", round(precision, 4))
    print("Recall   :", round(recall, 4))
    print("F1 Score :", round(f1, 4))


# ==========================================
# 9. FIND BEST MODEL
# ==========================================

best_model = max(
    results,
    key=lambda x: results[x]["F1 Score"]
)

best_pipeline = pipelines[best_model]


print("\n======================================")
print("BEST MODEL")
print("======================================")

print("Model:", best_model)
print(
    "F1 Score:",
    round(results[best_model]["F1 Score"], 4)
)


# ==========================================
# 10. CREATE MODELS FOLDER
# ==========================================

os.makedirs("models", exist_ok=True)


# ==========================================
# 11. SAVE BEST MODEL
# ==========================================

joblib.dump(
    best_pipeline,
    "models/placement_model.pkl"
)

print("\n======================================")
print("MODEL SAVED")
print("======================================")

print("Saved as: models/placement_model.pkl")