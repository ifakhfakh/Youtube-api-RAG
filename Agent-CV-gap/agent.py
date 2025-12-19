import os
from typing import TypedDict
from langchain_community.document_loaders import PyPDFLoader
import pprint
from groq import Groq

# LangChain imports
from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_core.output_parsers import JsonOutputParser
from langchain_community.tools.tavily_search import TavilySearchResults


parser = JsonOutputParser()


def extract_text_from_pdf(pdf_path):
    """Extract text from a PDF file"""
    loader = PyPDFLoader(pdf_path)
    pages = loader.load()
    full_text = " ".join([page.page_content for page in pages])
    return full_text


def analyze_cv_gap(job_description, resume_text):
    """
    Analyze CV gap between resume and job description
    Returns JSON with resume_skills_found, job_skills_required, and missing_skills
    """
    prompt_template = ChatPromptTemplate.from_messages([
        ("system", """
        You are a strict Technical Recruiter. 
        
        TASK:
        1. Scan the Resume and extract ALL technical skills found (normalize to lowercase).
        2. Scan the Job Description and extract required skills (normalize to lowercase).
        3. Compare the two lists.
        
        CRITICAL RULES:
        - **Normalization:** Treat "HTML", "html", "Html5" as the SAME thing.
        - **Partial Matches:** If JD requires "CI/CD" and Resume has "Jenkins", that is a MATCH (not missing).
        - **Output:** JSON ONLY.
        
        JSON STRUCTURE (You must fill all fields):
        {{
            "resume_skills_found": ["list", "of", "all", "skills", "found", "in", "resume"],
            "job_skills_required": ["list", "of", "skills", "from", "jd"],
            "missing_skills": ["final", "list", "of", "gaps"]
        }}
        """),
        ("human", """
        JOB DESCRIPTION: {job_description}
        RESUME: {resume_text}
        """),
    ])
    
    llm = ChatGroq(
        model="llama-3.1-8b-instant",
        temperature=0,
        model_kwargs={"response_format": {"type": "json_object"}}
    )
    
    rag_chain = (
        prompt_template
        | llm
        | parser
    )
    
    result = rag_chain.invoke({
        "job_description": job_description, 
        "resume_text": resume_text
    })
    
    return result


def find_courses_for_skills(skills, max_results=2):
    """
    Find courses to learn missing skills
    Returns list of recommendations with skill, course_name, and url
    """
    if "TAVILY_API_KEY" not in os.environ:
        return []
    
    tool = TavilySearchResults()
    recommendations = []
    
    for skill in skills[:max_results]:
        query = f"free interactive course to learn {skill} for beginners 2024"
        
        try:
            results = tool.invoke(query)
            
            if results and len(results) > 0:
                top_hit = results[0]
                recommendations.append({
                    "skill": skill,
                    "course_name": top_hit.get('content', 'Course')[:100] + "...",
                    "url": top_hit.get('url', '#')
                })
        except Exception as e:
            print(f"Search failed for {skill}: {e}")
    
    return recommendations


# ============================================
# MAIN EXECUTION (for testing)
# ============================================

if __name__ == "__main__":
    pdf_text = extract_text_from_pdf("sample.pdf")
    # pprint.pprint(pdf_text)

    
    job_description = """
    JOB TITLE: Senior Frontend Engineer
    COMPANY: NexusStream Analytics

    ABOUT THE ROLE:
    We are looking for an experienced developer to lead our dashboard migration team. You will be responsible for building high-performance web applications used by thousands of enterprise clients.

    RESPONSIBILITIES:
    - Architect and develop scalable UI components.
    - Collaborate with the backend team to integrate APIs.
    - Optimize application speed and render performance.
    - Mentor junior developers and conduct code reviews.

    REQUIRED TECHNICAL SKILLS:
    - Proficient in Html is a MUST.
    - Strong experience with **TypeScript** and static typing.
    - State management experience using **Redux Toolkit** or **Zustand**.
    - Experience writing unit tests with **Jest** and **React Testing Library**.
    - Understanding of CI/CD pipelines (GitHub Actions).
    - Basic knowledge of Docker for containerization.

    NICE TO HAVE:
    - Experience with Next.js.
    - Knowledge of GraphQL.

    SOFT SKILLS :
    - Excellent verbal and written communication skills.
    - Ability to work in an Agile/Scrum environment.
    - Strong problem-solving attitude and leadership qualities.
    """
    
    answer = analyze_cv_gap(job_description, pdf_text)
    pprint.pprint(answer)
    
    recommendations = find_courses_for_skills(answer["missing_skills"])
    
    # ---------------------------------------------------------
    # FINAL OUTPUT (What the user sees)
    # ---------------------------------------------------------
    print("\n" + "="*50)
    print("🎓 CAREER DEVELOPMENT PLAN")
    print("="*50)

    if not recommendations:
        print("Good news! You match the job perfectly (or I couldn't find courses).")
    else:
        print(f"Here are {len(recommendations)} resources to close your skill gaps:\n")
        for item in recommendations:
            print(f"🔹 GAP: {item['skill'].upper()}")
            print(f"   📖 Course: {item['course_name']}")
            print(f"   🔗 Link:   {item['url']}")
            print("-" * 30)