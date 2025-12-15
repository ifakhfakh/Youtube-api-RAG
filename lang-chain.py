import pprint
import chromadb
from chromadb.utils import embedding_functions
import os
from groq import Groq

# LangChain imports
from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser



def format_timestamp(seconds: float) -> str:
    """Convert seconds to HH:MM:SS format"""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    
    if hours > 0:
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"
    return f"{minutes:02d}:{secs:02d}"


def analyze_with_groq(query, search_results):
    """
    Use Groq to analyze search results and provide a comprehensible step-by-step breakdown
    """
    api_key = os.getenv("GROQ_API_KEY")
    
    if not api_key:
        print("\n⚠️  GROQ_API_KEY environment variable not set")
        print("   Set it with: export GROQ_API_KEY=your_api_key")
        return None
    
    client = Groq(api_key=api_key)
    
    # Prepare the context from search results
    context = "\n".join([
        f"Result {i+1}:\n{doc}"
        for i, doc in enumerate(search_results['documents'][0])
    ])
    
    # Create a prompt to analyze the results
    prompt = f"""Based on the following search results related to the query "{query}", 
please provide a clear, step-by-step breakdown of the process or information.

Search Results:
{context}

Please format your response as:
1. Provide a brief summary of what the query is asking for
2. List the key steps or information in a clear, numbered format
3. Add any important notes or tips
4. Keep the explanation concise and easy to understand"""
    
    try:
        # 1. Change 'messages.create' to 'chat.completions.create'
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            max_tokens=1024,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        # 2. Change how you access the text
        return completion.choices[0].message.content

    except Exception as e:
        print(f"Error: {e}")
        return None


# Demo data for testing the RAG pipeline
raw_data = [
  {
    "text": "hi friends my name is Raj and you are watching Tech white so in this video I will show you a step-by-step tutorial how to install Ubuntu",
    "start": 0.0,
    "duration": 9.0
  },
  {
    "text": "so let's start so first I will show you how to download Ubuntu and how to create a bootable pen drive open your browser and type Ubuntu download and this is the official website of Ubuntu click on it",
    "start": 9.0,
    "duration": 13.0
  },
  {
    "text": "now go to this download option then click on Ubuntu desktop now scroll down and you can see this is the version of Ubuntu",
    "start": 22.0,
    "duration": 10.0
  },
  {
    "text": "simply click on download and you can see the download process has been started",
    "start": 32.0,
    "duration": 6.0
  },
  {
    "text": "so the file size is 4.6 GB so I already have the image so I will cancel this process",
    "start": 38.0,
    "duration": 8.0
  },
  {
    "text": "this is my Ubuntu ISO image now your next step will be download rufo software which help you to create a bootable pen drive",
    "start": 46.0,
    "duration": 9.0
  },
  {
    "text": "so again open your browser and type rufos click on roof Force",
    "start": 55.0,
    "duration": 7.0
  },
  {
    "text": "so this is the official website of rufos Simply click on it scroll down and this is a download link download simply click on this URL to download Rufus so these are the two softwares which you need now insert your pen drive",
    "start": 62.0,
    "duration": 17.0
  },
  {
    "text": "so this is my USB pen drive now after plug in your pen drive simply run this software roof Force",
    "start": 79.0,
    "duration": 9.0
  },
  {
    "text": "so this is the interface of roof force and it will automatically detect your pen drive so this is my pen drive of 8 GB then click on select option now select your Ubuntu ISO image",
    "start": 88.0,
    "duration": 14.0
  },
  {
    "text": "then click on open that's it now click on start then click on OK and click on OK",
    "start": 102.0,
    "duration": 8.0
  },
  {
    "text": "and you can see the process has been started so the process has been completed simply click on close remove your pen drive",
    "start": 110.0,
    "duration": 10.0
  },
  {
    "text": "so I will insert my pen drive and I will show you how to boot from your pen drive so I am using Dell laptop in Dell laptop you have to press F12 key",
    "start": 120.0,
    "duration": 12.0
  },
  {
    "text": "this key to open your boot menu so I will show you how to open your boot menu and boot from your pen drive turn on your laptop",
    "start": 132.0,
    "duration": 10.0
  },
  {
    "text": "and then continuously press F12 key and you can see this is the boot menu now boot from your USB storage press enter",
    "start": 142.0,
    "duration": 14.0
  },
  {
    "text": "now select the first option try or install Ubuntu on the left side you can see the language select your language then click on install Ubuntu",
    "start": 156.0,
    "duration": 13.0
  },
  {
    "text": "this is the keyboard layout select your keyboard layout then click on continue don't do anything just click on continue",
    "start": 169.0,
    "duration": 9.0
  },
  {
    "text": "so I'm doing a fresh installation so I will select the first option then click on install now",
    "start": 178.0,
    "duration": 8.0
  },
  {
    "text": "click on continue now select your country region now enter your detail your name your computer name your pick name or your password",
    "start": 186.0,
    "duration": 10.0
  },
  {
    "text": "fill all the details then click on continue so the process has been started and it will take some time so I will fast forward this video or simply click on restart now",
    "start": 196.0,
    "duration": 12.0
  },
  {
    "text": "remove your pen drive then press enter",
    "start": 208.0,
    "duration": 4.0
  },
  {
    "text": "so this is my login name simply click on",
    "start": 212.0,
    "duration": 3.0
  },
  {
    "text": "it now enter your password press enter",
    "start": 215.0,
    "duration": 3.0
  },
  {
    "text": "to login so this is the interface of",
    "start": 218.0,
    "duration": 3.0
  },
  {
    "text": "Ubuntu as you can see these are the",
    "start": 221.0,
    "duration": 2.0
  },
  {
    "text": "options okay these are the pre-loaded",
    "start": 223.0,
    "duration": 3.0
  },
  {
    "text": "apps preloaded applications",
    "start": 226.0,
    "duration": 3.0
  },
  {
    "text": "and if you want to create a another",
    "start": 229.0,
    "duration": 2.0
  },
  {
    "text": "username simply click on this option",
    "start": 231.0,
    "duration": 3.0
  },
  {
    "text": "then go to settings option",
    "start": 234.0,
    "duration": 2.0
  },
  {
    "text": "so these are the options you can use",
    "start": 236.0,
    "duration": 3.0
  },
  {
    "text": "and if you want to download any software",
    "start": 239.0,
    "duration": 4.0
  },
  {
    "text": "click on this option Ubuntu software",
    "start": 243.0,
    "duration": 3.0
  },
  {
    "text": "Ubuntu has its own store of applications",
    "start": 246.0,
    "duration": 5.0
  }
]

print("✅ Processing data into LangChain Documents...")

chunks = []
chunk_size = 3
overlap = 1
step = chunk_size - overlap

langchain_docs = []

for i in range(0, len(raw_data), step):
    group = raw_data[i:i + chunk_size]
    if len(group) < 2: continue
    
    # Create the text block
    combined_text = ' '.join([t['text'] for t in group])
    
    # Calculate metadata
    start_time = group[0]['start']
    
    # Create a LangChain Document object
    doc = Document(
        page_content=combined_text,
        metadata={
            "start": start_time,
            "timestamp_str": format_timestamp(start_time),
            "source": "video_transcript"
        }
    )
    langchain_docs.append(doc)

# ==========================================
# 3. INITIALIZE LANGCHAIN COMPONENTS
# ==========================================

# A. Embeddings (Using the same model you used before)
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# B. Vector Store (Chroma)
# This automatically handles embedding generation and storage
vectorstore = Chroma.from_documents(
    documents=langchain_docs,
    embedding=embeddings,
    collection_name="youtube_langchain"
)

# C. Retriever
retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

# D. LLM (Groq)
llm = ChatGroq(
    model="llama-3.1-8b-instant", # Smart model
    temperature=0
)

# ==========================================
# 4. CREATE THE RAG CHAIN (Simplified)
# ==========================================

# Define the Prompt
prompt_template = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant. Use the following context to answer the question.\n\nContext:\n{context}"),
    ("human", "{input}"),
])

# Create simple RAG chain
def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

rag_chain = (
    {"context": retriever | format_docs, "input": RunnablePassthrough()}
    | prompt_template
    | llm
    | StrOutputParser()
)

# ==========================================
# 5. RUN QUERY
# ==========================================

query = "How to install Ubuntu?"

print(f"\n🤖 Asking Groq via LangChain: '{query}'...\n")

answer = rag_chain.invoke(query)

# ==========================================
# 6. DISPLAY RESULTS
# ==========================================

print("📋 ANSWER:")
print(answer)

# Get the source documents
source_docs = retriever.invoke(query)
print("\n🔍 SOURCE DOCUMENTS USED:")
for i, doc in enumerate(source_docs):
    print(f"\n--- Source {i+1} ---")
    print(f"Timestamp: {doc.metadata.get('timestamp_str', 'N/A')}")
    print(f"Content: {doc.page_content[:100]}...")