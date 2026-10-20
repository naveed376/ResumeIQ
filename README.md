# 📄 ResumeIQ - AI Resume Analyzer & Job Matcher

ResumeIQ takes your resume (PDF/DOCX) and a job description, then uses an LLM (Groq - Llama 3.3 70B via LangChain) to give you:

- 🎯 Match score (0-100)
- 🛠️ Extracted skills (technical, soft, domain, certifications)
- ❌ Missing skills for the job
- 💪 Strengths and 📈 recommendations
- 📥 Downloadable PDF report

## Tech Stack
Streamlit · LangChain · Groq · pypdf · python-docx · ReportLab

## Run Locally
```bash
git clone https://github.com/naveed376/ResumeIQ.git
cd ResumeIQ
python -m venv venv
venv\Scripts\activate        # Windows  (Mac/Linux: source venv/bin/activate)
pip install -r requirements.txt
copy .env.example .env       # Mac/Linux: cp .env.example .env
# open .env and put your real GROQ_API_KEY
streamlit run app.py
```
Get a free Groq key at https://console.groq.com/keys

## Deploy on Streamlit Community Cloud
1. Push this repo to GitHub.
2. Go to https://share.streamlit.io -> **Create app** -> select this repo, branch `main`, main file `app.py`.
3. Open **Advanced settings -> Secrets** and add:
   ```toml
   GROQ_API_KEY = "your_groq_api_key_here"
   ```
4. Click **Deploy**.

## Project Structure
```
ResumeIQ/
├── app.py
├── requirements.txt
├── utils/
│   ├── resume_parser.py
│   ├── skill_extractor.py
│   ├── matcher.py
│   └── report_generator.py
└── .streamlit/secrets.toml.example
```

Built by Naveed Ahmad.
