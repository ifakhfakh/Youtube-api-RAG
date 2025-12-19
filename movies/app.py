import streamlit as st
import pandas as pd
import chromadb
from chromadb.utils import embedding_functions
from PIL import Image
import requests
from io import BytesIO
import os

# Set page config
st.set_page_config(
    page_title="🎬 Movie Recommendation Engine",
    page_icon="🎬",
    layout="wide"
)

# Add title and description
st.title("🎬 Movie Recommendation Engine")
st.markdown("Search for movies based on your description and find the best matches!")

# ==========================================
# Initialize ChromaDB with Movies Data
# ==========================================
@st.cache_resource
def load_movies_db():
    """Load and initialize the movies database"""
    # Read CSV
    df = pd.read_csv("movies-1000.csv")
    
    # Create raw data
    raw_data = []
    for index, row in df.iterrows():
        raw_data.append({
            'title': row['title'],
            'overview': row['overview'] if pd.notna(row['overview']) else '',
            'poster_url': row.get('poster_url', '') if 'poster_url' in row.index else ''
        })
    
    # Initialize ChromaDB
    client = chromadb.Client()
    
    embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name="all-MiniLM-L6-v2"
    )
    
    collection = client.create_collection(
        name='movies',
        embedding_function=embedding_fn
    )
    
    # Add documents
    collection.add(
        documents=[c['overview'] for c in raw_data],
        metadatas=[{
            'title': c['title'],
            'poster_url': c.get('poster_url', '')
        } for c in raw_data],
        ids=[f"movie_{i}" for i in range(len(raw_data))]
    )
    
    return collection, raw_data

@st.cache_data
def load_image_safely(url):
    """Safely load image from URL"""
    if not url or url == '':
        return None
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            return Image.open(BytesIO(response.content))
    except Exception as e:
        st.warning(f"Could not load image: {e}")
    return None

# Load the database
collection, raw_data = load_movies_db()

# ==========================================
# UI Components
# ==========================================

# Input section
col1, col2 = st.columns([4, 1])

with col1:
    user_query = st.text_input(
        "🔍 Describe a movie you're looking for:",
        placeholder="e.g., 'A thrilling action movie with superheroes and an apocalypse'",
        help="Enter a description and we'll find the best matching movies"
    )

with col2:
    num_results = st.slider(
        "Number of results",
        min_value=1,
        max_value=5,
        value=3
    )

# ==========================================
# Search and Display Results
# ==========================================

if user_query:
    st.markdown("---")
    
    # Search
    with st.spinner("🔎 Searching for movies..."):
        results = collection.query(
            query_texts=[user_query],
            n_results=num_results
        )
    
    # Display results
    st.subheader(f"📽️ Top {num_results} Matches")
    
    if results['documents'][0]:
        # Create columns for results
        cols = st.columns(min(num_results, 3))
        
        for idx, (doc, meta, distance) in enumerate(zip(
            results['documents'][0],
            results['metadatas'][0],
            results['distances'][0]
        )):
            col = cols[idx % len(cols)]
            
            with col:
                # Movie card
                st.markdown(
                    f"""
                    <div style='border: 2px solid #1f77b4; border-radius: 10px; padding: 15px; background-color: #f8f9fa;'>
                    """,
                    unsafe_allow_html=True
                )
                
                # Load and display poster
                poster = load_image_safely(meta.get('poster_url', ''))
                if poster:
                    st.image(poster,  width="stretch", caption=meta['title'])
                else:
                    st.info("📸 No image available")
                    st.write(f"**{meta['title']}**")
                
                # Movie details
                st.markdown(f"**Title:** {meta['title']}")
                
                # Similarity score (inverted - lower distance = higher match)
                match_percentage = max(0, (1 - distance) * 100)
                st.markdown(f"**Match Score:** {match_percentage:.1f}%")
                
                # Overview
                st.markdown(f"**Overview:**")
                st.write(f"_{doc[:200]}..._")
                
                st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.error("❌ No movies found. Try a different description!")

else:
    # Show welcome message
    st.info(
        "👈 Enter a movie description to get started! "
        "The system will use AI to find the best matching movies from the database."
    )
    
    # Show sample queries
    st.markdown("### 📝 Example Queries:")
    st.markdown("""
    - "A superhero movie with action and adventure"
    - "Funny comedy film"
    - "Scary horror movie"
    - "Romantic story"
    - "Science fiction with robots"
    """)

# ==========================================
# Footer
# ==========================================
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #888; font-size: 12px;'>
    Powered by ChromaDB + Streamlit | Movie Recommendation Engine
</div>
""", unsafe_allow_html=True)
