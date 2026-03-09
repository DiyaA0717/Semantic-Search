const express = require("express");
const cors = require("cors");
const path = require("path");

const app = express();
const PORT = 3000;

app.use(cors());
app.use(express.json());

/* Serve frontend files (HTML, CSS, JS) */
app.use(express.static(__dirname));

/* Root route → open index.html */
app.get("/", (req, res) => {
  res.sendFile(path.join(__dirname, "index.html"));
});

/* Search API */
app.post("/search", async (req, res) => {
  try {
    const query = req.body.query;

    // For now just returning query
    res.send("You searched: " + query);

  } catch (error) {
    res.status(500).send("Search error");
  }
});

/* Start Server */
app.listen(PORT, () => {
  console.log(`Server running at http://localhost:${PORT}`);
});
