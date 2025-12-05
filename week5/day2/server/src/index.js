const express = require("express");
const mongoose = require("mongoose");
const elementRoutes = require("./routes/elementRoutes.js");
const dotenv = require("dotenv");

dotenv.config({ path: ".env" });

const app = express();

app.use(express.json());

app.use("/api/elements", elementRoutes);
const mongourl = process.env.MONGO_URI;
mongoose
  .connect(mongourl)
  .then(() => {
    console.log("Connected to MongoDB");
  })
  .catch((err) => {
    console.error("MongoDB connection error:", err);
  });

app.get("/", (req, res) => {
  res.send("Hello from the Element API!");
});

const PORT = process.env.PORT || 5000;
app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
