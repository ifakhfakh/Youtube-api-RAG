from typing import TypedDict
from langgraph.graph import StateGraph, END
from agent import extract_text_from_pdf, analyze_cv_gap, find_courses_for_skills

import pprint

class AgentState(TypedDict):
    resume_text: str
    job_description: str
    missing_skills: list
    courses: list

pdf_text = extract_text_from_pdf("sample.pdf")
state = AgentState()
state['resume_text'] = pdf_text
state['job_description'] = """

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

def scanner_node(state: AgentState):
    # 1. READ from the folder
    resume = state['resume_text'] 
    
    # 2. DO work (Your LLM logic)
    found_gaps = analyze_cv_gap(state['job_description'], resume) # e.g., ['docker', 'react']
    
    # 3. WRITE back to the folder (Update)
    # We only return the key we want to update.
    return {"missing_skills": found_gaps['missing_skills']} 

def searcher_node(state: AgentState):
    missing_skills = state['missing_skills']
    
    recommendations = find_courses_for_skills(missing_skills)
    
    return {"courses": recommendations}

# 2. Define the Graph
workflow = StateGraph(AgentState)
workflow.add_node("scanner", scanner_node)
workflow.add_node("searcher", searcher_node)

workflow.add_conditional_edges(
    "scanner",
    lambda state: "searcher" if state['missing_skills'] else END
)

workflow.set_entry_point("scanner")
workflow.add_edge("searcher", END)

# 5. Compile
app = workflow.compile()

print("🚀 Starting LangGraph Workflow...")
result = app.invoke(state)

print("\n✅ FINAL RESULT:")

pprint.pprint(result['courses'])