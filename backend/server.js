import express from "express";
import dotenv from "dotenv";
import cors from "cors";
import generateResponseRoute from "./routes/generate-response.js";

dotenv.config();

const app = express();
app.use(express.json());
app.use(cors());
// ROUTES
app.use("/api", generateResponseRoute);

app.listen(process.env.PORT || 3001, () => {
  console.log("🚀 Backend running on port", process.env.PORT || 3001);
});
