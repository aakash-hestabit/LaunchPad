const express = require("express");
const mongoose = require("mongoose");
const elementRoutes = require("./routes/elementRoutes.js");
const dotenv = require("dotenv");
const cors = require("cors");

dotenv.config({ path: ".env" });

const app = express();
app.use(cors(
  {
    origin : "*"
  }
));
app.use(express.json());

const mongourl = process.env.MONGO_URI;
console.log(mongourl);

mongoose
  .connect(mongourl)
  .then(() => {
    console.log("Connected to MongoDB");
  })
  .catch((err) => {
    console.error("MongoDB connection error:", err);
  });

app.use("/api/elements", elementRoutes);
app.get("/", (req, res) => {
  res.send("Hello from the Element API!");
});

app.get("/health",(_,res)=>{
  console.log("health route hit");
  
  res.status(200).json("server is running fine")
})

const PORT = process.env.PORT || 5000;
app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
