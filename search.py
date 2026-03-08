from pymongo import MongoClient
from sentence_transformers import SentenceTransformer

print("Hybrid search started")

uri = "mongodb://diya2006717_db_user:BaPvyKKHju6OWDzF@ac-arfooev-shard-00-00.ey03qyb.mongodb.net:27017,ac-arfooev-shard-00-01.ey03qyb.mongodb.net:27017,ac-arfooev-shard-00-02.ey03qyb.mongodb.net:27017/?ssl=true&replicaSet=atlas-yh86o3-shard-0&authSource=admin&appName=semantic-search-cluster"
client = MongoClient(uri)

db = client["semantic_search"]
collection = db["documents"]

query = input("Enter your search query: ")

# Load embedding model
model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")
query_embedding = model.encode(query).tolist()

# Vector Search
vector_pipeline = [
    {
        "$vectorSearch": {
            "index": "semantic_search",
            "path": "embedding",
            "queryVector": query_embedding,
            "numCandidates": 50,
            "limit": 5
        }
    },
    {
        "$project": {
            "title": 1,
            "content": 1,
            "score": {"$meta": "vectorSearchScore"}
        }
    }
]

vector_results = list(collection.aggregate(vector_pipeline))

if vector_results:
    print("Sample vector result:", vector_results[0])
else:
    print("No vector results found")

# Keyword Search
keyword_pipeline = [
    {
        "$search": {
            "index": "keyword_index",
            "text": {
                "query": query,
                "path": ["title", "content"]
            }
        }
    },
    {
        "$project": {
            "title": 1,
            "content": 1,
            "score": {"$meta": "searchScore"}
        }
    },
    {"$limit": 5}
]

keyword_results = list(collection.aggregate(keyword_pipeline))

# Merge results
combined = {}

for doc in vector_results:
    combined[str(doc["_id"])] = {
        "title": doc.get("title", ""),
        "content": doc.get("content", ""),
        "score": doc["score"] * 0.7
    }

for doc in keyword_results:
    doc_id = str(doc["_id"])

    if doc_id in combined:
        combined[doc_id]["score"] += doc["score"] * 0.3
    else:
        combined[doc_id] = {
            "title": doc.get("title", ""),
            "content": doc.get("content", ""),
            "score": doc["score"] * 0.3
        }

sorted_results = sorted(combined.values(), key=lambda x: x["score"], reverse=True)

print("\n========== TRUE HYBRID RESULTS ==========\n")

for i, doc in enumerate(sorted_results, 1):
    print(f"Rank {i}")
    print("Title   :", doc["title"])
    print("Content :", doc["content"])
    print("Score   :", round(doc["score"], 4))
    print("-" * 50)