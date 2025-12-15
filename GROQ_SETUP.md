# YouTube RAG with Groq AI Analysis

This project demonstrates a Retrieval-Augmented Generation (RAG) pipeline that:
1. Chunks video transcript data
2. Creates embeddings using ChromaDB
3. Retrieves relevant results based on queries
4. **Uses Groq AI to provide step-by-step analysis** ✨

## Setup

### 1. Install Dependencies (Already Done)
```bash
pip install youtube-transcript-api chromadb sentence-transformers groq
```

### 2. Get Groq API Key
To enable AI-powered analysis, you need a Groq API key:

1. Visit: https://console.groq.com/
2. Sign up (free account)
3. Navigate to API Keys section
4. Copy your API key

### 3. Set Environment Variable

**On Linux/Mac:**
```bash
export GROQ_API_KEY=your_api_key_here
```

**On Windows (PowerShell):**
```powershell
$env:GROQ_API_KEY = "your_api_key_here"
```

**On Windows (CMD):**
```cmd
set GROQ_API_KEY=your_api_key_here
```

### 4. Run the App

```bash
python app_demo.py
```

## Features

### Without Groq API Key
- ✅ Search through transcript chunks
- ✅ Find relevant timestamps
- ✅ See similarity scores

### With Groq API Key
- ✅ All of the above, PLUS:
- ✅ AI-powered step-by-step breakdown
- ✅ Comprehensible analysis of search results
- ✅ Clear instructions and tips extracted from video content

## Example Output

```
🔍 Search Results for: 'How to install Ubuntu?'
--------------------------------------------------

Result 1:
  ⏱️  Timestamp: 00:00
  📝 Text: hi friends my name is Raj and you are watching Tech white...
  📏 Distance: 0.367
  🔗 Video URL: youtube.com/watch?v=POf5mCs5YgI&t=0s

============================================================
🤖 AI-Powered Analysis (using Groq)
============================================================

📋 Step-by-Step Breakdown:

1. **Download Ubuntu**
   - Visit the official Ubuntu website
   - Click on Desktop version
   - Download the 4.6 GB ISO file

2. **Create Bootable USB Drive**
   - Download Rufus software
   - Use Rufus to create bootable pen drive
   - Press F12 during boot to access boot menu

3. **Installation Process**
   - Select "Try or Install Ubuntu"
   - Choose language
   - Select keyboard layout
   - Continue with default settings

4. **Important Tips**
   - Don't modify default settings
   - Press enter to boot from USB
   - The installation is straightforward
```

## Two Versions Available

### `app_demo.py` (Recommended for testing)
- Uses mock/demo data (no network needed)
- Fast to run
- Perfect for testing the Groq integration

### `app.py` (For real YouTube videos)
- Fetches real YouTube transcripts
- Uses Docker proxy to handle cloud IP blocking
- Includes fallback to demo data

## Using Docker Proxy (For Real Transcripts)

If you want to use real YouTube transcripts:

```bash
# Terminal 1: Start the Squid proxy
docker-compose up -d proxy

# Terminal 2: Set proxy and run the app
export HTTP_PROXY=http://127.0.0.1:8888
export HTTPS_PROXY=http://127.0.0.1:8888
python app.py
```

## Technology Stack

- **ChromaDB**: Vector database for embeddings
- **Sentence Transformers**: Creating semantic embeddings
- **Groq**: Fast AI model for analysis
- **Docker**: Local proxy for handling cloud IP blocking
- **youtube-transcript-api**: Fetching YouTube transcripts

## Free Resources

- Groq API: https://console.groq.com/ (free tier available)
- YouTube Transcript API: https://github.com/jdepoix/youtube-transcript-api
- ChromaDB: https://docs.trychroma.com/

Enjoy! 🚀
