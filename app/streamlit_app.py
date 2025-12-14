import streamlit as st
import os
import re
import nltk
import pdfplumber
import docx
import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.corpus import stopwords

# -----------------------------
# Page config
# -----------------------------
st.set_page_config(
    page_title="Resume – Job Fit Analyzer",
    layout="centered"
)

# -----------------------------
# Custom CSS (UI POLISH)
# -----------------------------
st.markdown("""
<style>
.main-card {
    background-color: #111827;
    padding: 25px;
    border-radius: 14px;
    margin-top: 20px;
}

.section-card {
    background-color: #0f172a;
    padding: 18px;
    border-radius: 12px;
    margin-top: 16px;
}

.hero-score {
    font-size: 44px;
    font-weight: 700;
    color: #22c55e;
}

.role-name {
    font-size: 22px;
    font-weight: 600;
    margin-bottom: 5px;
}

.badge-low {
    color: #ef4444;
    font-weight: 600;
}

.badge-medium {
    color: #facc15;
    font-weight: 600;
}

.badge-high {
    color: #22c55e;
    font-weight: 600;
}

.subtle {
    color: #9ca3af;
    font-size: 14px;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# NLTK setup
# -----------------------------
nltk.download('stopwords')
STOP_WORDS = set(stopwords.words('english'))

# -----------------------------
# Utility functions
# -----------------------------
def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-zA-Z ]', ' ', text)
    words = [w for w in text.split() if w not in STOP_WORDS]
    return ' '.join(words)

def extract_resume_text(uploaded_file):
    if uploaded_file.type == "application/pdf":
        text = ""
        with pdfplumber.open(uploaded_file) as pdf:
            for page in pdf.pages:
                text += page.extract_text() or ""
        return text
    elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        doc = docx.Document(uploaded_file)
        return " ".join(p.text for p in doc.paragraphs)
    return ""

def load_job_descriptions():
    jd_folder = "data/job_descriptions"
    jds = {}
    for file in os.listdir(jd_folder):
        with open(os.path.join(jd_folder, file), "r", encoding="utf-8") as f:
            jds[file] = clean_text(f.read())
    return jds

def rank_roles(clean_resume, clean_jds):
    docs = [clean_resume] + list(clean_jds.values())
    tfidf = TfidfVectorizer().fit_transform(docs)
    scores = cosine_similarity(tfidf[0], tfidf[1:])[0]
    return pd.DataFrame({
        "file": list(clean_jds.keys()),
        "score": scores
    }).sort_values(by="score", ascending=False)

MASTER_SKILLS = [
    "python","sql","pandas","numpy","excel","statistics",
    "machine","learning","deep","deployment","api",
    "java","database","backend",
    "sales","communication","crm","negotiation",
    "recruitment","talent","hr",
    "coordination","planning","documentation"
]

def extract_skills(text):
    return set(text.split()).intersection(MASTER_SKILLS)

# -----------------------------
# UI
# -----------------------------
st.title("📄 Resume – Job Fit Analyzer")
st.write("Upload your resume to find the best-matched role with clear reasoning.")

uploaded_file = st.file_uploader(
    "Upload Resume (PDF or DOCX)",
    type=["pdf", "docx"]
)

if uploaded_file:
    with st.spinner("Analyzing resume..."):
        resume_text = extract_resume_text(uploaded_file)
        clean_resume = clean_text(resume_text)
        clean_jds = load_job_descriptions()
        results = rank_roles(clean_resume, clean_jds)

    best = results.iloc[0]
    second = results.iloc[1]

    best_score = round(best["score"] * 100, 2)
    best_role = best["file"].replace("jd_", "").replace(".txt", "").replace("_", " ").title()

    with open(os.path.join("data/job_descriptions", best["file"]), "r", encoding="utf-8") as f:
        jd_text = clean_text(f.read())

    resume_skills = extract_skills(clean_resume)
    jd_skills = extract_skills(jd_text)

    matched = resume_skills & jd_skills
    missing = jd_skills - resume_skills

    fit_label = (
        "Strong Fit" if best_score >= 65 else
        "Medium Fit" if best_score >= 40 else
        "Low Fit"
    )

    badge_class = (
        "badge-high" if best_score >= 65 else
        "badge-medium" if best_score >= 40 else
        "badge-low"
    )

    st.markdown("<div class='main-card'>", unsafe_allow_html=True)

    st.markdown(f"<div class='role-name'>🏆 {best_role}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='hero-score'>{best_score}%</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='{badge_class}'>Fit Level: {fit_label}</div>", unsafe_allow_html=True)

    st.markdown("<div class='section-card'>", unsafe_allow_html=True)
    st.markdown("### ✅ Matched Skills")
    st.write(f"{len(matched)} / {len(jd_skills)} skills matched")
    st.write(", ".join(sorted(matched)) if matched else "None")
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='section-card'>", unsafe_allow_html=True)
    st.markdown("### ⚠️ Missing Skills")
    st.write(", ".join(sorted(missing)) if missing else "None")
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='section-card'>", unsafe_allow_html=True)
    st.markdown("### 💡 Why this role?")
    st.write(
        "Your resume shows alignment with the core skills and responsibilities defined for this role."
    )
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='section-card'>", unsafe_allow_html=True)
    st.markdown("### 📌 Recommendation")
    st.write(
        "Partial fit. Consider upskilling in the missing areas before applying."
        if best_score < 65 else
        "Strong fit. You are well aligned with this role."
    )
    st.markdown("</div>", unsafe_allow_html=True)

    alt_role = second["file"].replace("jd_", "").replace(".txt", "").replace("_", " ").title()
    alt_score = round(second["score"] * 100, 2)

    st.markdown("<div class='section-card'>", unsafe_allow_html=True)
    st.markdown("### 🔄 Alternative Suitable Role")
    st.write(f"{alt_role} ({alt_score}%)")
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<p class='subtle'>Note: This tool supports hiring decisions and should be used along with human judgment.</p>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)
