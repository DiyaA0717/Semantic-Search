import express from "express";
import cors from "cors";

const app = express();
const PORT = 3000;

app.use(cors());
app.use(express.json());
app.use(express.static("./"));

app.post("/search", (req, res) => {
  const query = req.body.query;
  res.send("You searched: " + query);
});

app.listen(PORT, () => {
  console.log("Server running at http://localhost:3000");
});
