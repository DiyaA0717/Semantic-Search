from pymongo import MongoClient
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

uri = "mongodb://diya2006717_db_user:BaPvyKKHju6OWDzF@ac-arfooev-shard-00-00.ey03qyb.mongodb.net:27017,ac-arfooev-shard-00-01.ey03qyb.mongodb.net:27017,ac-arfooev-shard-00-02.ey03qyb.mongodb.net:27017/?ssl=true&replicaSet=atlas-yh86o3-shard-0&authSource=admin&appName=semantic-search-cluster"

client = MongoClient(uri)

# test connection
client.admin.command('ping')
print("Connected successfully")

db = client["semantic_search"]
collection = db["documents"]

documents = [
    {"title": "AI", "content": "Artificial Intelligence is transforming technology."},
    {"title": "Machine Learning", "content": "Machine learning is a subset of AI."},
    {"title": "Database", "content": "MongoDB is a NoSQL database."},
    {"title": "Python", "content": "Python is widely used for data science."}
]

for doc in documents:
    embedding = model.encode(doc["content"]).tolist()
    doc["embedding"] = embedding

collection.delete_many({})
collection.insert_many(documents)

print("Documents inserted with embeddings")