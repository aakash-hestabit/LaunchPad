const express = require("express");

const app = express();

const PORT = 5000;

app.get('/', (_,res)=>{
    res.status(200).json("hi from the backend")
})

app.listen(PORT, () => {
  console.log("app is running on port: ", PORT);
});
