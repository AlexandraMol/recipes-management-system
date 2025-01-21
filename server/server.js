require("dotenv").config();
const express = require("express");
const morgan = require("morgan");
const cors = require("cors");

const app = express();
const PORT = process.env.PORT;

app.use(cors());
app.use(express.json());
app.use(express.urlencoded());
app.use(morgan("dev"));

app.get("/", async (req, res) => {
  res.send({ message: "1" });
});

app.listen(PORT, () => console.log(`Server is running on port ${PORT}`));
