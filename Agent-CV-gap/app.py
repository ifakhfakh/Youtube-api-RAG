import streamlit as st
import tempfile
import os
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from agent import extract_text_from_pdf, analyze_cv_gap, find_courses_for_skills

# ==========================================
# PAGE CONFIG
# ==========================================
st.set_page_config(
    page_title="CV Gap Analyzer",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# STYLING
# ==========================================
st.markdown("""
    <style>
    .skill-match {
        background-color: #d4edda;
        padding: 10px;
        border-radius: 5px;
        margin: 5px 0;
        border-left: 4px solid #28a745;
    }
    .skill-missing {
        background-color: #f8d7da;
        padding: 10px;
        border-radius: 5px;
        margin: 5px 0;
        border-left: 4px solid #dc3545;
    }
    .course-card {
        background-color: #e7f3ff;
        padding: 15px;
        border-radius: 8px;
        margin: 10px 0;
        border-left: 4px solid #0066cc;
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# TITLE & INTRO
# ==========================================
st.title("📋 CV Gap Analyzer")
st.markdown("""
Analyze the gap between your CV and job requirements. Upload your resume (PDF), paste a job description, 
and get an AI-powered analysis with personalized learning recommendations.
""")

# ==========================================
# SIDEBAR - INPUT SECTION
# ==========================================
with st.sidebar:
    st.header("📝 Input Your Data")
    
    # PDF Upload
    st.subheader("1. Your Resume")
    pdf_file = st.file_uploader(
        "Upload your resume (PDF)",
        type=['pdf'],
        help="Upload your resume in PDF format"
    )
    
    # Job Description
    st.subheader("2. Job Description")
    job_description = st.text_area(
        "Paste the job description",
        height=300,
        placeholder="Paste the complete job description here...",
        help="Include job title, responsibilities, required skills, etc."
    )
    
    # Analyze Button
    st.markdown("---")
    analyze_button = st.button("🔍 Analyze CV Gap", use_container_width=True, type="primary")

# ==========================================
# MAIN CONTENT
# ==========================================

if analyze_button:
    # Validation
    if not pdf_file:
        st.error("❌ Please upload your resume (PDF)")
    elif not job_description.strip():
        st.error("❌ Please paste a job description")
    else:
        # Process Resume
        with st.spinner("📖 Reading your resume..."):
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                tmp_file.write(pdf_file.getbuffer())
                tmp_path = tmp_file.name
            
            try:
                resume_text = extract_text_from_pdf(tmp_path)
            finally:
                os.unlink(tmp_path)
        
        # Analyze CV Gap
        with st.spinner("🤖 Analyzing your skills vs job requirements..."):
            analysis = analyze_cv_gap(job_description, resume_text)
        
        # ==========================================
        # DISPLAY RESULTS
        # ==========================================
        
        # Create tabs
        tab1, tab2, tab3 = st.tabs(["📊 Analysis", "🎯 Recommendations", "📋 Details"])
        
        with tab1:
            st.subheader("Skills Analysis")
            
            # Overall Score
            resume_skills = set(analysis.get('resume_skills_found', []))
            required_skills = set(analysis.get('job_skills_required', []))
            missing_skills = analysis.get('missing_skills', [])
            
            matched_count = len(set(required_skills) & set(resume_skills))
            total_required = len(required_skills)
            match_percentage = (matched_count / total_required * 100) if total_required > 0 else 0
            
            # Score Display
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric(
                    "Match Score",
                    f"{match_percentage:.0f}%",
                    delta=f"{matched_count}/{total_required} skills"
                )
            
            with col2:
                st.metric(
                    "Skills You Have",
                    len(resume_skills),
                    help="Total technical skills found in your resume"
                )
            
            with col3:
                st.metric(
                    "Skill Gaps",
                    len(missing_skills),
                    help="Skills you need to develop"
                )
            
            # Progress Bar
            st.progress(match_percentage / 100)
            
            # Matched Skills
            st.subheader("✅ Your Matching Skills")
            matched_skills = set(required_skills) & set(resume_skills)
            if matched_skills:
                for skill in sorted(matched_skills):
                    st.markdown(
                        f'<div class="skill-match">✓ {skill.capitalize()}</div>',
                        unsafe_allow_html=True
                    )
            else:
                st.info("No matching skills found yet")
            
            # Missing Skills
            st.subheader("❌ Missing Skills")
            if missing_skills:
                for skill in missing_skills:
                    st.markdown(
                        f'<div class="skill-missing">✗ {skill.capitalize()}</div>',
                        unsafe_allow_html=True
                    )
            else:
                st.success("🎉 You have all required skills!")
        
        # Recommendations Tab
        with tab2:
            st.subheader("🎓 Learning Resources")
            
            if missing_skills:
                with st.spinner("🔎 Finding courses for your skill gaps..."):
                    recommendations = find_courses_for_skills(missing_skills)
                
                if recommendations:
                    st.success(f"Found {len(recommendations)} learning resources!")
                    
                    for i, rec in enumerate(recommendations, 1):
                        col1, col2 = st.columns([2, 1])
                        
                        with col1:
                            st.markdown(f"""
                            <div class="course-card">
                                <h4>📖 {rec['skill'].capitalize()}</h4>
                                <p>{rec['course_name']}</p>
                                <a href="{rec['url']}" target="_blank" style="color: #0066cc; text-decoration: none;">
                                    🔗 View Course →
                                </a>
                            </div>
                            """, unsafe_allow_html=True)
                else:
                    st.warning("⚠️ Could not find courses. Please set TAVILY_API_KEY to enable course recommendations.")
                    st.info("You can still learn these skills through online platforms like:")
                    st.markdown("""
                    - **Udemy** - https://www.udemy.com
                    - **Coursera** - https://www.coursera.org
                    - **freeCodeCamp** - https://www.freecodecamp.org
                    - **Codecademy** - https://www.codecademy.com
                    """)
            else:
                st.success("🎉 No skill gaps to fill! You're ready to apply!")
        
        # Details Tab
        with tab3:
            st.subheader("📋 Detailed Analysis")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**Your Skills Found:**")
                if analysis.get('resume_skills_found'):
                    st.write(", ".join([f"`{s}`" for s in sorted(analysis['resume_skills_found'])]))
                else:
                    st.write("No skills found")
            
            with col2:
                st.write("**Job Required Skills:**")
                if analysis.get('job_skills_required'):
                    st.write(", ".join([f"`{s}`" for s in sorted(analysis['job_skills_required'])]))
                else:
                    st.write("No skills specified")
            
            st.write("**Raw Analysis:**")
            st.json(analysis)

else:
    # Welcome State
    st.markdown("---")
    st.markdown("""
    ### How to use:
    
    1. **Upload Your Resume** - Upload your CV in PDF format from the sidebar
    2. **Paste Job Description** - Copy and paste the job description from the job posting
    3. **Click Analyze** - Let AI analyze the gap between your skills and job requirements
    4. **Get Recommendations** - Receive personalized learning resources to fill your skill gaps
    
    ### Benefits:
    
    ✨ **Instant Analysis** - Get AI-powered skill gap analysis in seconds
    
    🎯 **Personalized Recommendations** - Receive targeted learning resources for your gaps
    
    📊 **Visual Insights** - See your match score and skill comparison at a glance
    
    🚀 **Career Development** - Close skill gaps and prepare for your target role
    """)
    
    # Example Job Description
    with st.expander("📝 Example Job Description (for testing)"):
        st.text("""JOB TITLE: Senior Frontend Engineer
COMPANY: NexusStream Analytics

REQUIRED TECHNICAL SKILLS:
- Proficient in HTML/CSS
- Strong experience with TypeScript and static typing
- State management experience using Redux Toolkit or Zustand
- Experience writing unit tests with Jest and React Testing Library
- Understanding of CI/CD pipelines (GitHub Actions)
- Basic knowledge of Docker for containerization
- Experience with Next.js
- Knowledge of GraphQL

SOFT SKILLS:
- Excellent communication skills
- Ability to work in Agile/Scrum environment
- Strong problem-solving attitude""")

# ==========================================
# FOOTER
# ==========================================
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #888; font-size: 12px;'>
    Powered by LangChain + Groq + Streamlit | CV Gap Analyzer
</div>
""", unsafe_allow_html=True)
