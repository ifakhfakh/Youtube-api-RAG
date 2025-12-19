import pandas as pd
import pprint
import chromadb
from chromadb.utils import embedding_functions

# This reads the CSV and turns it into a neat table (DataFrame)
df = pd.read_csv("./movies/movies-1000.csv")

# Print the first 5 rows to check if it worked
print(df.head())

# To access just the plot summaries for your project:
plots = df['overview'].tolist()

# pprint.pprint(plots)

raw_data = []

for index, row in df.iterrows():
    raw_data.append({
        'title': row['title'],
        'overview': row['overview'] if pd.notna(row['overview']) else '',
        'poster_url': row['poster_url']
    })

# pprint.pprint(raw_data)

client = chromadb.Client()

embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)

collection = client.create_collection(
    name='movies',
    embedding_function=embedding_fn
)

collection.add(
    documents=[c['overview'] for c in raw_data],
    metadatas=[{
        'title': c['title'],
        'image': c['poster_url']
    } for c in raw_data],
    ids=[f"movie_{i}" for i in range(len(raw_data))]
)

n_results = 4
query = "man with zombie appocalypse"

results = collection.query(
    query_texts=[query],
    n_results=n_results
)

print("\n📦 Raw results structure:")
pprint.pprint(results)
pprint.pprint(results['documents'][0][0])
pprint.pprint(results['ids'][0][0])
pprint.pprint(results['metadatas'][0][0])
