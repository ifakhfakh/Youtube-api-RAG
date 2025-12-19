# 📋 CV Gap Analyzer - Streamlit App

An intelligent CV analyzer that compares your resume against job requirements and provides personalized learning recommendations to fill skill gaps.

## Features

✨ **AI-Powered Analysis**
- Uses LangChain + Groq for intelligent skill extraction and comparison
- Normalizes and matches skills (e.g., "HTML", "html", "HTML5" are treated as the same)
- Identifies exact skill gaps

📊 **Visual Dashboard**
- Match score percentage
- Skills breakdown (matched vs missing)
- Skill comparison charts
- Interactive tabs for detailed analysis

🎓 **Learning Recommendations**
- Automatic course discovery for missing skills
- Direct links to free learning resources
- Personalized recommendations based on your gaps

📱 **User-Friendly Interface**
- Clean, intuitive design
- Step-by-step workflow
- Real-time analysis with spinner indicators

## Setup

### 1. Prerequisites

Make sure you have:
- Python 3.12+
- A Groq API key (get free at https://console.groq.com/)
- A Tavily API key for course recommendations (optional, get at https://tavily.com/)

### 2. Set Environment Variables

```bash
export GROQ_API_KEY=your_groq_api_key_here
export TAVILY_API_KEY=your_tavily_api_key_here
```

### 3. Install Dependencies

If running fresh, install required packages:

```bash
pip install streamlit langchain langchain-groq langchain-community langchain-huggingface pdf2image pypdf
```

### 4. Run the App

From the `Agent-CV-gap` directory:

```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`

## How to Use

### Step 1: Upload Your Resume
- Click on the sidebar file uploader
- Select your resume in PDF format

### Step 2: Paste Job Description
- Copy the job posting from the job site
- Paste it into the text area
- Include job title, responsibilities, and required skills

### Step 3: Analyze
- Click the "🔍 Analyze CV Gap" button
- Wait for the AI to process your data

### Step 4: View Results
The app shows three tabs:

**📊 Analysis Tab:**
- Overall match score (percentage)
- Count of skills you have
- Count of skill gaps
- Color-coded skill lists (green for matched, red for missing)

**🎯 Recommendations Tab:**
- Personalized learning resources
- Direct links to courses
- Alternative platforms if API isn't available

**📋 Details Tab:**
- Raw data from analysis
- Full skill lists
- JSON output for debugging

## File Structure

```
Agent-CV-gap/
├── app.py              # Streamlit UI (frontend only)
├── agent.py            # All logic functions
├── sample.pdf          # Example resume
└── README.md          # This file
```

## Code Architecture

### Separation of Concerns

**agent.py** (All Logic)
```python
def extract_text_from_pdf(pdf_path)          # Extract resume text
def analyze_cv_gap(job_desc, resume_text)    # AI analysis
def find_courses_for_skills(skills)          # Course recommendations
```

**app.py** (UI Only)
```python
# Just imports and calls functions from agent.py
# No business logic, just display logic
```

This design makes it easy to:
- Test functions independently
- Reuse logic in other apps (CLI, API, etc.)
- Update business logic without touching UI

## Example Workflow

1. **Upload resume.pdf** (your CV)
2. **Paste job description:**
   ```
   Looking for a Senior Frontend Engineer
   
   Required Skills:
   - React
   - TypeScript
   - Jest
   - Docker
   ```
3. **Click Analyze**
4. **View Results:**
   - Match Score: 75%
   - You Have: React, Jest
   - Missing: TypeScript, Docker
5. **Get Courses:**
   - TypeScript course link
   - Docker course link

## API Keys

### Required: Groq API Key
- Free tier available: https://console.groq.com/
- Gives you access to LLM models for CV analysis
- ~1000 requests/day on free tier

### Optional: Tavily API Key
- Free tier available: https://tavily.com/
- Enables automatic course recommendations
- Without it, app suggests manual alternatives

## Troubleshooting

**"GROQ_API_KEY not set"**
```bash
export GROQ_API_KEY=sk_...
```

**"Could not find courses"**
- This happens without TAVILY_API_KEY
- Manually search Udemy, Coursera, freeCodeCamp
- The analysis still shows your skill gaps clearly

**"PDF upload fails"**
- Make sure file is a valid PDF
- Try re-saving the PDF if corrupted
- Max size: 200MB

**"Skills not matching correctly"**
- Try more detailed job descriptions
- Include specific skill names from job posting
- The AI is strict about matching - be explicit

## Performance

- **First run:** ~15 seconds (downloading models)
- **Subsequent runs:** ~3-5 seconds (cached models)
- **With Tavily:** Add 2-5 seconds for course search

## Limitations

- Requires PDF resume (not DOCX, images, etc.)
- Job description text must be pasted (no URL parsing)
- Skill matching is case-insensitive but needs exact phrases
- No resume parsing - uses full text extraction

## Future Enhancements

- [ ] Support for DOCX/DOC resumes
- [ ] Direct URL input for job postings
- [ ] Resume improvement suggestions
- [ ] Salary prediction based on skill match
- [ ] Interview preparation resources
- [ ] Timeline to upskill calculation

## Support

For issues or questions:
1. Check environment variables are set
2. Verify PDF file format
3. Check Groq API status
4. Review example job description

## Technologies Used

- **Streamlit** - Web UI framework
- **LangChain** - AI orchestration
- **Groq API** - LLM inference (fast & cheap)
- **Tavily** - Web search for courses
- **ChromaDB** - Vector storage (if used)
- **Hugging Face** - Embeddings

## License

MIT

Enjoy analyzing your CV gaps! 🚀
