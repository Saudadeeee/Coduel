import os, json, time, uuid, shutil, re
from pathlib import Path
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, field_validator
import redis
from fastapi.middleware.cors import CORSMiddleware

REDIS_HOST = os.getenv("REDIS_HOST","localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT","6379"))
r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

app = FastAPI(title="OJ API")

ALLOWED_LANG = {"c", "cpp"}
ALLOWED_OPT = {"O0","O1","O2"}
PROBLEMS_DIR = Path(os.getenv("PROBLEMS_DIR", "/problems"))
ALLOWED_DIFFICULTY = {"fast", "easy", "medium", "hard"}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],          # cho phép tất cả origin (cho dev)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class SubmitReq(BaseModel):
    language: str
    code: str
    problem_id: str
    opt: str = "O2"
    std: str | None = None

    @field_validator("language")
    def val_lang(cls, v):
        if v not in ALLOWED_LANG:
            raise ValueError("language must be c or cpp")
        return v

    @field_validator("opt")
    def val_opt(cls, v):
        if v not in ALLOWED_OPT:
            raise ValueError("opt must be O0/O1/O2")
        return v

class TestCase(BaseModel):
    input: str
    output: str

    @field_validator("input", "output")
    def ensure_not_empty(cls, v):
        if v is None or v == "":
            raise ValueError("input/output cannot be empty")
        return v

class AddProblemReq(BaseModel):
    title: str
    description: str
    sample_input: str
    sample_output: str
    difficulty: str
    tests: list[TestCase]

    @field_validator("title", "description", "sample_input", "sample_output")
    def non_empty(cls, v):
        if not v or not v.strip():
            raise ValueError("fields must not be empty")
        return v

    @field_validator("difficulty")
    def validate_difficulty(cls, v):
        if v not in ALLOWED_DIFFICULTY:
            raise ValueError(f"difficulty must be one of {', '.join(sorted(ALLOWED_DIFFICULTY))}")
        return v

    @field_validator("tests")
    def ensure_tests(cls, v):
        if not v:
            raise ValueError("tests must contain at least one test case")
        return v

def _slugify(value: str) -> str:
    """Convert arbitrary text into a safe filesystem slug."""
    value = value.lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    value = value.strip("-")
    return value or "problem"

def _write_text(path: Path, content: str):
    path.write_text(content.rstrip("\n") + "\n", encoding="utf-8")

def _existing_problem_numbers() -> list[int]:
    numbers: list[int] = []
    if not PROBLEMS_DIR.exists():
        return numbers
    for entry in PROBLEMS_DIR.iterdir():
        if not entry.is_dir():
            continue
        meta_path = entry / "meta.json"
        if meta_path.exists():
            try:
                meta = json.loads(meta_path.read_text(encoding="utf-8"))
                num = meta.get("number")
                if isinstance(num, int):
                    numbers.append(num)
                    continue
            except Exception:
                pass
        match = re.match(r"(\d+)", entry.name)
        if match:
            numbers.append(int(match.group(1)))
    return numbers

def _next_problem_number() -> int:
    numbers = _existing_problem_numbers()
    return (max(numbers) if numbers else 0) + 1

@app.post("/problem/submit")
def submit(s: SubmitReq):
    sub_id = str(uuid.uuid4())
    # Lưu tạm metadata
    r.hset(f"sub:{sub_id}", mapping={
        "status": "queued",
        "problem_id": s.problem_id,
        "language": s.language,
        "opt": s.opt,
        "std": s.std or ("c17" if s.language=="c" else "c++20"),
        "created_at": str(int(time.time()))
    })
    # Lưu code
    r.set(f"code:{sub_id}", s.code, ex=3600)
    # Đẩy job vào queue
    job = {"submission_id": sub_id}
    r.lpush("queue:compile", json.dumps(job))
    return {"submission_id": sub_id}

@app.get("/problem/submission/{sub_id}")
def status(sub_id: str):
    meta = r.hgetall(f"sub:{sub_id}")
    if not meta:
        raise HTTPException(404, "not found")
    # Kết quả (nếu có)
    compile_log = r.get(f"compile_log:{sub_id}")
    run_result = r.get(f"run_result:{sub_id}")
    return {
        "meta": meta,
        "compile_log": compile_log[:8192] if compile_log else None,
        "run_result": json.loads(run_result) if run_result else None
    }

@app.get("/problem/{problem_id}")
def problem_detail(problem_id: str):
    base = PROBLEMS_DIR / problem_id
    if not base.is_dir():
        raise HTTPException(404, "not found")
    statement_path = base / "statement.md"
    statement = None
    difficulty = None
    number = None
    meta_path = base / "meta.json"
    if meta_path.exists():
        try:
            meta = json.loads(meta_path.read_text(encoding="utf-8"))
            difficulty = meta.get("difficulty")
            number = meta.get("number")
        except Exception:
            difficulty = None

    if statement_path.exists():
        try:
            statement = statement_path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            statement = statement_path.read_text(errors="replace")
    return {
        "problem_id": problem_id,
        "statement": statement,
        "difficulty": difficulty,
        "number": number
    }

@app.post("/problem-add")
def add_problem(req: AddProblemReq):
    PROBLEMS_DIR.mkdir(parents=True, exist_ok=True)
    problem_number = _next_problem_number()
    slug = _slugify(req.title)
    base_name = f"{problem_number:03d}-{slug}"
    problem_path = PROBLEMS_DIR / base_name

    suffix = 1
    while problem_path.exists():
        problem_path = PROBLEMS_DIR / f"{base_name}-{suffix}"
        suffix += 1

    statement_sections = [
        f"# Problem {problem_number}: {req.title}",
        "",
        f"**Difficulty:** {req.difficulty}",
        "",
        req.description.strip(),
        "",
        "## Sample Input",
        "```",
        req.sample_input.rstrip("\n"),
        "```",
        "",
        "## Sample Output",
        "```",
        req.sample_output.rstrip("\n"),
        "```",
        "",
        "## How To Submit",
        "Use problem_id:",
        "",
        problem_path.name,
    ]
    try:
        problem_path.mkdir(parents=True, exist_ok=False)
        statement_path = problem_path / "statement.md"
        statement_path.write_text("\n".join(statement_sections).strip() + "\n", encoding="utf-8")

        _write_text(problem_path / "sample_input.txt", req.sample_input)
        _write_text(problem_path / "sample_output.txt", req.sample_output)

        for idx, test in enumerate(req.tests, start=1):
            _write_text(problem_path / f"input{idx}.txt", test.input)
            _write_text(problem_path / f"output{idx}.txt", test.output)

        meta = {
            "number": problem_number,
            "difficulty": req.difficulty,
            "title": req.title
        }
        (problem_path / "meta.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")
    except Exception as exc:
        shutil.rmtree(problem_path, ignore_errors=True)
        raise HTTPException(500, f"failed to create problem: {exc}")

    return {
        "message": "problem created",
        "problem_id": problem_path.name,
        "number": problem_number,
        "difficulty": req.difficulty,
        "tests_count": len(req.tests)
    }
