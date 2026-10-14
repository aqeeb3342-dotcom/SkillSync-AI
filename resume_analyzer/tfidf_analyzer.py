from pypdf import PdfReader
from sklearn.feature_extraction.text import TfidfVectorizer


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


# ==========================================
# 2. TF-IDF PROCESSING
# ==========================================

vectorizer = TfidfVectorizer(
    stop_words="english"
)

tfidf_matrix = vectorizer.fit_transform([text])


# ==========================================
# 3. GET WORDS AND SCORES
# ==========================================

words = vectorizer.get_feature_names_out()

scores = tfidf_matrix.toarray()[0]


# Combine words and scores
word_scores = list(zip(words, scores))


# Sort by TF-IDF score
word_scores = sorted(
    word_scores,
    key=lambda x: x[1],
    reverse=True
)


# ==========================================
# 4. DISPLAY RESULTS
# ==========================================

print("======================================")
print("       SKILLSYNC AI")
print("         TF-IDF ANALYZER")
print("======================================")

print("\nImportant Resume Terms:")
print("--------------------------------------")

for word, score in word_scores[:20]:
    print(f"{word:25} {score:.4f}")

print("--------------------------------------")
print("TF-IDF analysis completed!")