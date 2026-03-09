const express = require("express");
const cors = require("cors");
const path = require("path");

const app = express();

app.use(cors());
app.use(express.json());

// Serve frontend files
app.use(express.static(path.join(__dirname, "public")));

app.post("/search", (req, res) => {

const query = req.body.query;

const documents = [
"AI is transforming search engines",
"Semantic search understands meaning",
"Books are great sources of knowledge",
"Machine learning improves search results"
];

const results = documents.filter(doc =>
doc.toLowerCase().includes(query.toLowerCase())
);

res.json(results);

});

app.listen(5000, () => {
console.log("Server running on port 5000");
});
