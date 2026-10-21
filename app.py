import streamlit as st
import os
from dotenv import load_dotenv
from pathlib import Path
import sys

# Add utils to path
sys.path.append(str(Path(__file__).parent))

from utils.resume_parser import ResumeParser
from utils.skill_extractor import SkillExtractor
from utils.matcher import JobMatcher
from utils.report_generator import ReportGenerator

# Load environment variables (local .env file)
load_dotenv()


def get_api_key():
    """Read the Groq key from Streamlit secrets (cloud) or .env / environment (local)."""
    try:
        if "GROQ_API_KEY" in st.secrets:
            return st.secrets["GROQ_API_KEY"]
    except Exception:
        pass
    return os.getenv("GROQ_API_KEY")

def get_model():
    """Groq model name. Override with GROQ_MODEL in secrets/.env if Groq retires this one."""
    try:
        if "GROQ_MODEL" in st.secrets:
            return st.secrets["GROQ_MODEL"]
    except Exception:
        pass
    return os.getenv("GROQ_MODEL", "openai/gpt-oss-120b")

# Page config
st.set_page_config(
    page_title="ResumeIQ - AI Resume Analyzer",
    page_icon="📄",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
        padding: 30px;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 30px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
    }
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 12px 24px;
        border-radius: 8px;
        font-weight: bold;
        font-size: 16px;
        transition: all 0.3s;
    }
    .stButton>button:hover {
        transform: translateY(-3px);
        box-shadow: 0 6px 20px rgba(102,126,234,0.4);
    }
    .score-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        color: white;
        margin: 10px 0;
        box-shadow: 0 5px 15px rgba(102,126,234,0.3);
    }
    .metric-card h2, .metric-card p { color: #1a1a2e !important; }
    .analysis-box {
        background: #f8f9fa;
        border-left: 4px solid #667eea;
        padding: 20px;
        border-radius: 5px;
        margin: 10px 0;
    }
    .metric-card {
        background: white;
        padding: 15px;
        border-radius: 10px;
        text-align: center;
        color: #1a1a2e;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# Main Header
st.markdown("""
<div class="main-header">
    <h1>📄 ResumeIQ</h1>
    <h3>AI-Powered Resume Analyzer & Job Matcher</h3>
    <p>Upload your resume, paste a job description, and get instant insights!</p>
</div>
""", unsafe_allow_html=True)

# Initialize session state
if "analysis_result" not in st.session_state:
    st.session_state.analysis_result = None
if "resume_text" not in st.session_state:
    st.session_state.resume_text = None
if "skills" not in st.session_state:
    st.session_state.skills = None

# Initialize components
@st.cache_resource
def init_components():
    groq_api_key = get_api_key()
    if not groq_api_key:
        st.error("⚠️ GROQ_API_KEY not found! Add it to .env (local) or Streamlit Secrets (cloud).")
        return None, None, None, None
    
    parser = ResumeParser()
    skill_extractor = SkillExtractor(groq_api_key, get_model())
    matcher = JobMatcher(groq_api_key, get_model())
    report_gen = ReportGenerator()
    
    return parser, skill_extractor, matcher, report_gen

parser, skill_extractor, matcher, report_gen = init_components()
if parser is None:
    st.stop()

# Main Layout
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📤 Upload Resume")
    resume_file = st.file_uploader(
        "Upload your resume (PDF or DOCX)",
        type=["pdf", "docx"],
        key="resume"
    )
    
    if resume_file:
        with st.spinner("Parsing resume..."):
            resume_text = parser.parse_resume(resume_file)
            if resume_text:
                st.session_state.resume_text = resume_text
                st.success(f"✅ Resume parsed successfully! ({len(resume_text)} characters)")
                
                # Show preview
                with st.expander("📄 Resume Preview"):
                    st.text(resume_text[:2000])

with col2:
    st.subheader("💼 Job Description")
    job_description = st.text_area(
        "Paste the job description here",
        height=200,
        placeholder="Paste the job description you want to match against..."
    )

# Analyze Button
if st.button("🎯 Analyze Match", use_container_width=True):
    if not resume_file:
        st.error("⚠️ Please upload your resume first!")
    elif not job_description.strip():
        st.error("⚠️ Please paste a job description!")
    else:
        with st.spinner("Analyzing resume and job match..."):
            try:
                # Extract skills from resume
                skills = skill_extractor.extract_skills(st.session_state.resume_text)
                st.session_state.skills = skills
                
                # Analyze match
                analysis = matcher.analyze_match(
                    st.session_state.resume_text,
                    job_description
                )
                if analysis.get("error"):
                    st.session_state.analysis_result = None
                    st.error(f"❌ AI analysis failed: {analysis['error']}")
                else:
                    st.session_state.analysis_result = analysis
                    st.success("✅ Analysis complete!")
                
            except Exception as e:
                st.error(f"❌ Error during analysis: {str(e)}")

# Display Results
if st.session_state.analysis_result:
    result = st.session_state.analysis_result
    
    # Score Section
    st.markdown("---")
    st.subheader("📊 Analysis Results")
    
    # Score Card
    score = result.get('match_score', 0)
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div class="score-card">
            <h1>{score}%</h1>
            <p>Match Score</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        # Skills extracted
        if st.session_state.skills:
            tech_count = len(st.session_state.skills.get('technical_skills', []))
            soft_count = len(st.session_state.skills.get('soft_skills', []))
            st.markdown(f"""
            <div class="metric-card">
                <h2>{tech_count}</h2>
                <p>Technical Skills</p>
            </div>
            """, unsafe_allow_html=True)
    
    with col3:
        missing_count = len(result.get('missing_skills', []))
        st.markdown(f"""
        <div class="metric-card">
            <h2>{missing_count}</h2>
            <p>Missing Skills</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Summary
    st.markdown("---")
    st.subheader("📝 Summary")
    summary = result.get('summary', 'No summary available')
    st.info(summary)
    
    # Skills Extracted
    if st.session_state.skills:
        st.subheader("🛠️ Extracted Skills")
        
        tabs = st.tabs(["Technical", "Soft Skills", "Domain", "Certifications"])
        
        with tabs[0]:
            tech_skills = st.session_state.skills.get('technical_skills', [])
            if tech_skills:
                for skill in tech_skills:
                    st.write(f"• {skill}")
            else:
                st.write("No technical skills found")
        
        with tabs[1]:
            soft_skills = st.session_state.skills.get('soft_skills', [])
            if soft_skills:
                for skill in soft_skills:
                    st.write(f"• {skill}")
            else:
                st.write("No soft skills found")
        
        with tabs[2]:
            domain_skills = st.session_state.skills.get('domain_skills', [])
            if domain_skills:
                for skill in domain_skills:
                    st.write(f"• {skill}")
            else:
                st.write("No domain skills found")
        
        with tabs[3]:
            certifications = st.session_state.skills.get('certifications', [])
            if certifications:
                for cert in certifications:
                    st.write(f"• {cert}")
            else:
                st.write("No certifications found")
    
    # Missing Skills
    st.markdown("---")
    st.subheader("❌ Missing Skills")
    missing_skills = result.get('missing_skills', [])
    if missing_skills:
        for skill in missing_skills:
            st.warning(f"• {skill}")
    else:
        st.success("Great! No missing skills detected.")
    
    # Strengths
    st.markdown("---")
    st.subheader("💪 Strengths")
    strengths = result.get('strengths', [])
    if strengths:
        for strength in strengths:
            st.success(f"• {strength}")
    
    # Recommendations
    st.markdown("---")
    st.subheader("📈 Recommendations")
    recommendations = result.get('recommendations', [])
    if recommendations:
        for rec in recommendations:
            st.info(f"• {rec}")
    
    # Download Report
    st.markdown("---")
    st.subheader("📥 Download Report")
    
    report_buffer = report_gen.generate_report(
        result,
        st.session_state.resume_text,
        job_description
    )
    st.download_button(
        label="📄 Download PDF Report",
        data=report_buffer,
        file_name="resume_analysis_report.pdf",
        mime="application/pdf"
    )

# Footer
st.markdown("""
---
<div style="text-align: center; color: #666; padding: 20px;">
    <p>Built with ❤️ using LangChain, Groq, Streamlit</p>
    <p>© 2026 ResumeIQ With Naveed. All rights reserved.</p>
</div>
""", unsafe_allow_html=True)