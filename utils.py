import fitz  # PyMuPDF
import spacy
from collections import Counter

nlp = spacy.load("en_core_web_sm")

# Words to ignore when extracting keywords from job descriptions
IGNORE_WORDS = {
    "looking", "look", "must", "should", "ability", "familiarity",
    "knowledge", "requirements", "responsibility", "etc", "like"
}

def extract_text_from_pdf(path):
    text = ""
    with fitz.open(path) as doc:
        for page in doc:
            text += page.get_text()
    return text

def extract_keywords(text):
    doc = nlp(text.lower())
    return [
        token.lemma_
        for token in doc
        if (
            (token.pos_ in {"NOUN", "VERB", "PROPN"} or token.text.isupper())
            and not token.is_stop
            and token.is_alpha
        )
    ]

def get_common_keywords(resume_text, jd_text):
    resume_words = extract_keywords(resume_text)
    jd_words = extract_keywords(jd_text)

    # Clean JD words by removing irrelevant noise
    jd_words = [w for w in jd_words if w not in IGNORE_WORDS]

    resume_counts = Counter(resume_words)
    jd_counts = Counter(jd_words)

    jd_unique = set(jd_counts.keys())
    resume_unique = set(resume_counts.keys())

    matched = sorted(jd_unique & resume_unique)
    missing = sorted(jd_unique - resume_unique)

    # Dynamically extract top verbs from JD
    jd_verbs = [
        token.lemma_ for token in nlp(jd_text.lower())
        if token.pos_ == "VERB" and not token.is_stop
    ]
    top_verbs = [v for v, _ in Counter(jd_verbs).most_common(10) if v not in IGNORE_WORDS]

    verbs_found = [v for v in top_verbs if v in resume_unique]
    verbs_missing = [v for v in top_verbs if v not in resume_unique]

    return {
        "matched_keywords": matched,
        "missing_keywords": missing,
        "power_verbs_found": verbs_found,
        "power_verbs_suggested": verbs_missing
    }
