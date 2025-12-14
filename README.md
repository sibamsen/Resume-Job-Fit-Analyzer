# 📄 Resume – Job Fit Analyzer (NLP-Based)

A practical NLP-powered web application that analyzes a candidate’s resume and identifies the best-matched job role by comparing it against multiple job descriptions. The system provides explainable insights such as matched skills, missing skills, and fit level to support hiring decisions.

## 🚀 Live Demo
https://customer-churn-lab.streamlit.app/

## 🎯 Problem Statement
Recruiters often need to quickly assess whether a candidate’s resume aligns with a given job role. Manual screening is time-consuming and subjective. This project aims to automate resume screening using explainable NLP techniques rather than black-box models.

## 🧠 Solution Overview
The application uses Natural Language Processing (NLP) to extract and preprocess resume text, convert text into numerical features using TF-IDF, compute semantic similarity with multiple job descriptions, and identify the best-fit role with clear reasoning.

## 🔑 Key Features
- Resume upload (PDF & DOCX)
- Best-matched job role identification
- Match percentage with fit level (Low / Medium / Strong)
- Matched skills and missing skills analysis
- Clear explanation of why a role was selected
- Alternative suitable role suggestion
- Dynamic job role updates via job description files

## 🧩 NLP Techniques Used
- Text extraction from PDF and DOCX files
- Text cleaning and normalization
- Tokenization
- TF-IDF vectorization
- Cosine similarity for semantic matching
- Rule-based skill extraction for explainability
- 
---

## ⚙️ Installation & Run Locally
```bash
git clone https://github.com/<your-username>/<repo-name>.git
cd <repo-name>
pip install -r requirements.txt
streamlit run app/streamlit_app.py ```

---

🔄 Dynamic Job Role Updates

Job roles are dynamically loaded from the data/job_descriptions folder. Adding or updating a job description file automatically reflects in the deployed application without retraining or code changes.

🎤 Interview Talking Points

Used TF-IDF and cosine similarity for resume–job matching

Focused on explainable NLP rather than black-box models

Designed the system for dynamic role updates

Optimized outputs for recruiter clarity and usability

🚧 Limitations & Future Enhancements

Currently uses keyword-based skill extraction

Can be enhanced using sentence embeddings (e.g., SBERT)

Batch resume analysis and recruiter-specific weighting can be added

📌 Disclaimer

This tool supports hiring decisions and should be used alongside human judgment.

👤 Author

Sibam Sen
Aspiring AI/ML Engineer
