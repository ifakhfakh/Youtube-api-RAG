import pprint
from youtube_transcript_api import YouTubeTranscriptApi
import chromadb
from chromadb.utils import embedding_functions
import os
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


def format_timestamp( seconds: float) -> str:
    """Convert seconds to HH:MM:SS format"""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    
    if hours > 0:
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"
    return f"{minutes:02d}:{secs:02d}"


# Try to fetch transcript with Docker proxy support
def fetch_transcript_with_proxy(video_id):
    """
    Fetch transcript using Docker-based Squid proxy to bypass YouTube IP blocking
    
    Make sure to run: docker-compose up -d proxy
    The proxy automatically uses environment variables set before import
    """
    try:
        print(f"Fetching transcript for video: {video_id}")
        print(f"Using proxy: http://127.0.0.1:8888")
        
        # Create API instance
        ytt_api = YouTubeTranscriptApi()
        
        # Fetch the transcript
        fetched_transcript = ytt_api.fetch(video_id)
        
        print("✅ Successfully fetched transcript!")
        return fetched_transcript
    except Exception as e:
        error_str = str(e)
        if "RequestBlocked" in str(type(e)) or "blocking" in error_str.lower():
            print(f"\n❌ YouTube blocked the request")
            print("\n💡 Make sure Docker proxy is running:")
            print("   docker-compose up -d proxy")
            print("   docker-compose ps")
        else:
            print(f"\n❌ Error: {e}")
        raise

# Try to fetch real transcript, fallback to demo data if blocked
try:
    fetched_transcript = fetch_transcript_with_proxy("POf5mCs5YgI")
    raw_data = fetched_transcript.to_raw_data()
except Exception as e:
    print("\n⚠️  Using demo data instead (real YouTube blocked from cloud)")
    # Demo data for testing the RAG pipeline
    raw_data = [
        {"text": "Welcome to the Ubuntu installation tutorial", "start": 0.0, "duration": 5.0},
        {"text": "First you need to download Ubuntu from the official website", "start": 5.0, "duration": 5.0},
        {"text": "You can use a USB drive or DVD to boot the installer", "start": 10.0, "duration": 5.0},
        {"text": "Let me show you how to create a bootable USB with the Ubuntu image", "start": 15.0, "duration": 5.0},
        {"text": "You will need to partition your hard drive during installation", "start": 20.0, "duration": 5.0},
        {"text": "Set up your environment by installing essential packages", "start": 25.0, "duration": 5.0},
    ]
    print("✅ Proceeding with demo data for testing")
""" pprint.pprint(raw_data)
 """
""" input_text = ""
for seg in raw_data:
   input_text = input_text.__add__( seg['text'] + " " )

print(input_text) """

chunks = []
chunk_size: int = 3
overlap  = 1
step = chunk_size - overlap
    
for i in range(0, len(raw_data), step):
    group = raw_data[i:i + chunk_size]
    if len(group) < 2:  # Skip very small final chunks
        continue
            
    chunks.append({
        'text': ' '.join([t['text'] for t in group]),
        'start': group[0]['start'],
        'end': group[-1]['start'] + group[-1]['duration'],
        'duration': (group[-1]['start'] + group[-1]['duration']) - group[0]['start'],
        'segment_indices': list(range(i, i + len(group)))
        })
    
documents=[c['text'] for c in chunks]

pprint.pprint(documents)

client = chromadb.Client()  # Use PersistentClient for persistence

""" tokenizer = AutoTokenizer.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")
embedding_fn = AutoModel.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")
 """
embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name="all-MiniLM-L6-v2"
        ) 

collection = client.create_collection(
            name='youtube',
            embedding_function=embedding_fn
        )

collection.add(
            documents=[c['text'] for c in chunks],
            metadatas=[{
                'start': c['start'],
                'end': c['end'],
                'duration': c['duration']
            } for c in chunks],
            ids=[f"chunk_{i}" for i in range(len(chunks))]
        )
n_results = 2
test_queries = [
    "How to setup environment?",      # Your original query
    "How to install Ubuntu?",         # More specific to video
    "step by step tutorial",
    "download and install",
    "USB boot",
    "partition",
    "Who is Raj?",
]

print("\n\n🔍 QUERY COMPARISON:")
print("=" * 60)

for query in test_queries:
    results = collection.query(query_texts=[query], n_results=1)
    
    distance = results['distances'][0][0]
    meta = results['metadatas'][0][0]
    text = results['documents'][0][0][:100]
    
    print(f"\n❓ Query: '{query}'")
    print(f"   📏 Distance: {distance:.4f} {'✅' if distance < 0.5 else '⚠️' if distance < 0.7 else '❌'}")
    print(f"   ⏱️  Timestamp: {format_timestamp(meta['start'])}")
    print(f"   📝 Match: {text}...")

    """Try to figure out what the video is about"""

""" sample_queries = [
    "main topic of this video",
    "what is this tutorial about",
    "introduction",
]

results = collection.query(query_texts=sample_queries, n_results=1)

# Get the intro/overview chunk
intro_text = results['documents'][0][0]



print("📺 This video is about:")
print(    intro_text[:200]) """

n_results = 4
query = "How to install Ubuntu?"
results = collection.query(
    query_texts=[query],
    n_results=n_results
)

# Debug: See the actual structure
print("\n📦 Raw results structure:")
pprint.pprint(results)


# ============================================
# DISPLAY RESULTS (FIXED!)
# ============================================
print(f"\n🔍 Search Results for: '{query}'")
print("-" * 50)

# Method 1: Using range
for i in range(len(results['documents'][0])):
    doc = results['documents'][0][i]
    meta = results['metadatas'][0][i]
    distance = results['distances'][0][i] if results.get('distances') else None
    
    print(f"\nResult {i + 1}:")
    print(f"  ⏱️  Timestamp: {format_timestamp(meta['start'])}")
    print(f"  📝 Text: {doc}...")  # First 100 chars
    print(f"  📏 Distance: {distance}")
    print(f"  🔗 Video URL: youtube.com/watch?v=POf5mCs5YgI&t={int(meta['start'])}s")
