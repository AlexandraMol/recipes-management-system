require("dotenv").config();
const express = require("express");
const morgan = require("morgan");
const cors = require("cors");
const routes = require("./routes/index");
const { uploadDataToDatabase } = require("./scripts/uploadData");

const app = express();
const PORT = process.env.PORT;

app.use(cors());
app.use(express.json());
app.use(express.urlencoded());
app.use(morgan("dev"));

app.get("/uploadData", async (req, res) => {
  uploadDataToDatabase();
  res.send({ message: "Data uploaded" });
});

app.use("/api", routes);

app.listen(PORT, () => console.log(`Server is running on port ${PORT}`));
