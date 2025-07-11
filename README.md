# 📄 Keyword Assistant – Resume vs JD Matcher (Flask)

This is a Flask web app that analyzes how well your resume matches a job description. It extracts keywords and compares them to highlight:

- ✅ Matched Keywords
- ❌ Missing Keywords
- 📢 Power Verbs Present
- 💡 Suggested Power Verbs

## 🔧 Tech Stack

- Python + Flask
- spaCy for NLP
- PyMuPDF for PDF text extraction
- HTML/CSS frontend

## 🚀 How to Run

1. Clone this repo  
2. Install dependencies: 
    pip install flask spacy pymupdf
    python -m spacy download en_core_web_sm
3. Run the app:
    python app.py

4. Go to: `http://127.0.0.1:5000/`

## 💡 Purpose

Helps job seekers optimize resumes for ATS (Applicant Tracking Systems).




