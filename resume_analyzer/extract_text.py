from pypdf import PdfReader

# Path to resume
pdf_path = "resume_analyzer/resumes/resume.pdf"

# Read PDF
reader = PdfReader(pdf_path)

# Extract text
text = ""

for page in reader.pages:
    page_text = page.extract_text()

    if page_text:
        text += page_text + "\n"


print("======================================")
print("       SKILLSYNC AI")
print("        RESUME ANALYZER")
print("======================================")

print("\nExtracted Resume Text:")
print("--------------------------------------")

print(text)

print("--------------------------------------")
print("Resume analysis completed!")