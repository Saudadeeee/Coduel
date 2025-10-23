import express from "express";
const app = express();
app.use(express.static("."));
app.listen(5173, () => console.log("Web at http://localhost:5173"));
