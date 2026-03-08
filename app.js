const express = require("express");
const cors = require("cors");
const { MongoClient } = require("mongodb");

const app = express();
const PORT = 5000;

app.use(express.json());
app.use(cors());

/* MongoDB Connection String */
const uri = "mongodb://diya2006717_db_user:BaPvyKKHju6OWDzF@ac-arfooev-shard-00-00.ey03qyb.mongodb.net:27017,ac-arfooev-shard-00-01.ey03qyb.mongodb.net:27017,ac-arfooev-shard-00-02.ey03qyb.mongodb.net:27017/?ssl=true&replicaSet=atlas-yh86o3-shard-0&authSource=admin";

/* Create Mongo Client */
const client = new MongoClient(uri);

let collection;

/* Connect to MongoDB */
async function connectDB() {
  try {
    await client.connect();
    console.log("Connected to MongoDB");

    const db = client.db("semantic_search");
    collection = db.collection("documents");

  } catch (error) {
    console.error(" MongoDB Connection Error:", error);
  }
}

connectDB();

/* Root route */
app.get("/", (req, res) => {
  res.send("Hybrid Search API Running");
});

/* Search API */
app.post("/search", async (req, res) => {
  try {
    const query = req.body.query;

    const results = await collection.find({
      text: { $regex: query, $options: "i" }
    }).toArray();

    res.json(results);

  } catch (error) {
    res.status(500).json({ error: "Search failed" });
  }
});

/* Start Server */
app.listen(PORT, () => {
  console.log(` Server running on port ${PORT}`);
});