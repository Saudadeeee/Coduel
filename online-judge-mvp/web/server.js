import express from "express";
import path from "path";
import { fileURLToPath } from "url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const app = express();
const publicDir = path.join(__dirname, "public");

app.use(express.static(publicDir));

app.get("/", (_req, res) => res.redirect("/problem"));
app.get("/problem", (_req, res) => res.sendFile(path.join(publicDir, "problem.html")));
app.get("/problem-add", (_req, res) => res.sendFile(path.join(publicDir, "problem-add.html")));
app.get("/problem-edit", (_req, res) => res.sendFile(path.join(publicDir, "problem-edit.html")));

app.listen(5173, () => console.log("Web at http://localhost:5173"));
