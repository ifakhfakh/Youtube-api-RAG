# 🎬 Movie Recommendation Engine - Streamlit UI

A beautiful Streamlit interface for searching and recommending movies based on natural language descriptions.

## Features

✨ **AI-Powered Search**
- Input movie descriptions and get intelligent recommendations
- Uses semantic embeddings to find the best matches
- Shows similarity scores for each result

🖼️ **Movie Cards**
- Display movie posters with metadata
- Show movie titles and overviews
- Display match percentage

⚙️ **Customizable Results**
- Adjust the number of results (1-5)
- Real-time search
- Instant feedback

## Setup

### 1. Install Dependencies

All packages are already installed in the main environment. If running fresh:

```bash
pip install streamlit pandas chromadb sentence-transformers pillow requests
```

### 2. Run the App

From the `/movies` directory:

```bash
streamlit run app.py
```

Or from the root directory:

```bash
cd movies
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## Usage

1. **Enter a Description:**
   - Type a natural language description of the movie you're looking for
   - Example: "A thrilling action movie with superheroes"

2. **Select Number of Results:**
   - Use the slider to choose how many matches (1-5)
   - Default is 3 results

3. **View Results:**
   - See matching movies with posters
   - Check match scores
   - Read movie overviews

## Example Queries

- "A superhero movie with action and adventure"
- "Funny comedy film that makes me laugh"
- "Scary horror movie"
- "Romantic love story"
- "Science fiction with robots and aliens"
- "Animated children's movie"

## File Structure

```
movies/
├── app.py              # Main Streamlit application
├── movies.py           # Original data processing script
├── movies-10.csv       # Movie dataset
└── README.md          # This file
```

## How It Works

1. **Data Loading:**
   - Reads movie data from `movies-10.csv`
   - Extracts title, overview, and poster URL

2. **Embedding & Storage:**
   - Uses ChromaDB with Sentence Transformers
   - Creates semantic embeddings of movie descriptions
   - Stores in vector database

3. **Search:**
   - User enters a description
   - System generates embedding of query
   - Finds most similar movies using cosine similarity
   - Returns results with match scores

## Troubleshooting

**"Could not load image" warning:**
- This happens if the image URL is invalid
- The app continues working and shows the movie info

**App runs slowly first time:**
- Downloading the embedding model takes time
- Subsequent runs are faster due to caching

**No results found:**
- Try a more general description
- The dataset might be small, so be flexible

## Technologies Used

- **Streamlit** - Interactive web UI
- **ChromaDB** - Vector database
- **Sentence Transformers** - AI embeddings
- **Pandas** - Data processing
- **PIL** - Image handling

## Notes

- Movie images are loaded from URLs in the CSV
- Similarity scores are normalized to 0-100%
- Results are cached for performance
- Works best with descriptive queries

Enjoy finding your next favorite movie! 🎬🍿
