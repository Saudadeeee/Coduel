import os, json, time, uuid, shutil, re
from pathlib import Path
from typing import Literal
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, field_validator, model_validator
import redis
from fastapi.middleware.cors import CORSMiddleware

REDIS_HOST = os.getenv("REDIS_HOST","localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT","6379"))
r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

app = FastAPI(title="OJ API")

LANGUAGE_ALIASES = {
    "c": "c",
    "cpp": "cpp",
    "c++": "cpp",
    "py": "py",
    "python": "py",
    "java": "java",
    "js": "js",
    "javascript": "js"
}
ALLOWED_LANG = set(LANGUAGE_ALIASES.keys())
PROBLEMS_DIR = Path(os.getenv("PROBLEMS_DIR", "/problems"))
ALLOWED_DIFFICULTY = {"fast", "easy", "medium", "hard"}
ALLOWED_VISIBILITY = {"public", "hidden"}
DEFAULT_TIME_LIMIT_MS = int(os.getenv("DEFAULT_TIME_LIMIT_MS", "2000"))
DEFAULT_MEMORY_LIMIT_KB = int(os.getenv("DEFAULT_MEMORY_LIMIT_KB", str(256 * 1024)))

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],       
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class SubmitReq(BaseModel):
    language: str
    code: str
    problem_id: str
    std: str | None = None

    @field_validator("language")
    def val_lang(cls, v):
        lang = v.lower()
        if lang not in ALLOWED_LANG:
            raise ValueError("language must be one of c, cpp, py, java, js")
        return LANGUAGE_ALIASES[lang]

class TestCase(BaseModel):
    input: str
    output: str
    visibility: Literal["public", "hidden"] = "hidden"

    @field_validator("input", "output")
    def ensure_not_empty(cls, v):
        if v is None or v == "":
            raise ValueError("input/output cannot be empty")
        return v

    @field_validator("visibility")
    def ensure_visibility(cls, v):
        if v not in ALLOWED_VISIBILITY:
            raise ValueError("visibility must be public or hidden")
        return v

class AddProblemReq(BaseModel):
    title: str
    description: str | None = None
    statement: str | None = None
    sample_input: str
    sample_output: str
    difficulty: str
    tests: list[TestCase]
    time_limit_ms: int | None = None
    memory_limit_kb: int | None = None
    tags: list[str] = []

    @field_validator("title", "sample_input", "sample_output")
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

    @field_validator("time_limit_ms", "memory_limit_kb")
    def validate_positive(cls, v):
        if v is None:
            return v
        return int(v)

    @field_validator("tags", mode="before")
    def ensure_list(cls, v):
        if v is None:
            return []
        if isinstance(v, str):
            return [v]
        if isinstance(v, list):
            return v
        raise ValueError("tags must be a list of strings")

    @field_validator("tags")
    def sanitize_tags(cls, v):
        return _normalize_tags(v)

    @model_validator(mode="after")
    def check_statement(cls, values):
        description = values.description
        statement = values.statement
        has_description = bool(description and description.strip())
        has_statement = bool(statement and statement.strip())
        if not has_description and not has_statement:
            raise ValueError("Either description or statement must be provided")
        return values

class UpdateProblemReq(BaseModel):
    problem_id: str
    delete: bool = False
    title: str | None = None
    description: str | None = None
    statement: str | None = None
    sample_input: str | None = None
    sample_output: str | None = None
    difficulty: str | None = None
    tests: list[TestCase] | None = None
    time_limit_ms: int | None = None
    memory_limit_kb: int | None = None
    tags: list[str] | None = None

    @field_validator("problem_id")
    def non_empty_id(cls, v):
        v = v.strip()
        if not v:
            raise ValueError("problem_id must not be empty")
        return v

    @field_validator("difficulty")
    def validate_diff(cls, v):
        if v is None:
            return v
        if v not in ALLOWED_DIFFICULTY:
            raise ValueError(f"difficulty must be one of {', '.join(sorted(ALLOWED_DIFFICULTY))}")
        return v

    @field_validator("tags", mode="before")
    def ensure_tags_list(cls, v):
        if v is None:
            return []
        if isinstance(v, str):
            return [v]
        if isinstance(v, list):
            return v
        raise ValueError("tags must be a list of strings")

    @field_validator("tags")
    def sanitize_tags(cls, v):
        return _normalize_tags(v)

    @field_validator("time_limit_ms", "memory_limit_kb")
    def validate_limits(cls, v):
        if v is None:
            return v

        return int(v)

    @model_validator(mode="after")
    def ensure_fields(cls, values):
        if values.delete:
            return values
        required_fields = [
            ("title", values.title),
            ("sample_input", values.sample_input),
            ("sample_output", values.sample_output),
            ("difficulty", values.difficulty)
        ]
        missing = [name for name, val in required_fields if not (val and str(val).strip())]
        if missing:
            raise ValueError(f"Missing required fields: {', '.join(missing)}")
        tests = values.tests or []
        if not tests:
            raise ValueError("tests must contain at least one test case")
        description = values.description
        statement = values.statement
        has_description = bool(description and description.strip())
        has_statement = bool(statement and statement.strip())
        if not has_description and not has_statement:
            raise ValueError("Either description or statement must be provided")
        return values

def _slugify(value: str) -> str:
    """Convert arbitrary text into a safe filesystem slug."""
    value = value.lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    value = value.strip("-")
    return value or "problem"

def _write_text(path: Path, content: str):
    path.write_text(content.rstrip("\n") + "\n", encoding="utf-8")

def _infer_problem_number_from_name(name: str) -> int | None:
    match = re.match(r"(\d+)", name)
    if match:
        try:
            return int(match.group(1))
        except ValueError:
            return None
    return None

def _normalize_tags(tags: list[str] | None) -> list[str]:
    if not tags:
        return []
    cleaned: list[str] = []
    seen: set[str] = set()
    for tag in tags:
        if not isinstance(tag, str):
            continue
        norm = re.sub(r"\s+", " ", tag.strip().lower())
        if not norm or norm in seen:
            continue
        seen.add(norm)
        cleaned.append(norm)
    return cleaned

def _compose_statement(number: int | None, title: str, difficulty: str | None, description: str | None, sample_input: str, sample_output: str, problem_id: str) -> str:
    title_line = f"# Problem {number}: {title}" if number else f"# {title}"
    sections = [title_line, ""]
    if difficulty:
        sections.append(f"**Difficulty:** {difficulty}")
        sections.append("")
    if description and description.strip():
        sections.append(description.strip())
        sections.append("")
    sections.extend([
        "## Sample Input",
        "```",
        sample_input.rstrip("\n"),
        "```",
        "",
        "## Sample Output",
        "```",
        sample_output.rstrip("\n"),
        "```",
        "",

    ])
    return "\n".join(sections).strip() + "\n"

def _scan_legacy_tests(base: Path) -> list[dict]:
    tests = []
    idx = 1
    while True:
        inp = base / f"input{idx}.txt"
        outp = base / f"output{idx}.txt"
        if not inp.exists() or not outp.exists():
            break
        tests.append({
            "input": inp.name,
            "output": outp.name,
            "visibility": "hidden"
        })
        idx += 1
    return tests

def _read_problem_meta(problem_id: str, base: Path) -> dict:
    meta = {
        "problem_id": problem_id,
        "number": None,
        "title": problem_id,
        "difficulty": None,
        "time_limit_ms": DEFAULT_TIME_LIMIT_MS,
        "memory_limit_kb": DEFAULT_MEMORY_LIMIT_KB,
        "tags": [],
        "tests": [],
        "samples": [],
        "created_at": None,
        "description": None,
    }
    meta_path = base / "meta.json"
    if meta_path.exists():
        try:
            loaded = json.loads(meta_path.read_text(encoding="utf-8"))
            if isinstance(loaded, dict):
                meta.update({k: loaded.get(k, meta[k]) for k in meta})
        except Exception:
            pass

    if meta.get("number") is None:
        meta["number"] = _infer_problem_number_from_name(problem_id)

    difficulty = meta.get("difficulty")
    if difficulty not in ALLOWED_DIFFICULTY:
        meta["difficulty"] = None

    try:
        tl = int(meta.get("time_limit_ms") or DEFAULT_TIME_LIMIT_MS)
        meta["time_limit_ms"] = tl if tl > 0 else DEFAULT_TIME_LIMIT_MS
    except (TypeError, ValueError):
        meta["time_limit_ms"] = DEFAULT_TIME_LIMIT_MS

    try:
        ml = int(meta.get("memory_limit_kb") or DEFAULT_MEMORY_LIMIT_KB)
        meta["memory_limit_kb"] = ml if ml > 0 else DEFAULT_MEMORY_LIMIT_KB
    except (TypeError, ValueError):
        meta["memory_limit_kb"] = DEFAULT_MEMORY_LIMIT_KB

    meta["tags"] = _normalize_tags(meta.get("tags"))
    if not meta.get("created_at"):
        meta["created_at"] = int(time.time())
    description = meta.get("description")
    if description is not None and not isinstance(description, str):
        description = None
    meta["description"] = description

    if not meta.get("tests"):
        meta["tests"] = _scan_legacy_tests(base)
    else:
        normalized_tests = []
        for test in meta["tests"]:
            if not isinstance(test, dict):
                continue
            inp = test.get("input")
            outp = test.get("output")
            if not inp or not outp:
                continue
            visibility = test.get("visibility", "hidden")
            if visibility not in ALLOWED_VISIBILITY:
                visibility = "hidden"
            normalized_tests.append({
                "input": inp,
                "output": outp,
                "visibility": visibility
            })
        meta["tests"] = normalized_tests or _scan_legacy_tests(base)

    if not meta.get("samples"):
        sample_in = base / "sample_input.txt"
        sample_out = base / "sample_output.txt"
        if sample_in.exists() and sample_out.exists():
            meta["samples"] = [{
                "input": sample_in.name,
                "output": sample_out.name,
                "label": "Sample"
            }]
    else:
        samples = []
        for sample in meta["samples"]:
            if not isinstance(sample, dict):
                continue
            sin = sample.get("input")
            sout = sample.get("output")
            if not sin or not sout:
                continue
            samples.append({
                "input": sin,
                "output": sout,
                "label": sample.get("label")
            })
        if samples:
            meta["samples"] = samples
        else:
            meta["samples"] = []

    return meta

def _problem_sort_key(item: dict):
    number = item.get("number")
    problem_id = item.get("problem_id")
    if isinstance(number, int):
        return (0, number, problem_id)
    return (1, problem_id, 0)

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

@app.get("/problems")
def list_problems():
    if not PROBLEMS_DIR.exists():
        return {"problems": []}
    problems = []
    for entry in PROBLEMS_DIR.iterdir():
        if not entry.is_dir():
            continue
        meta = _read_problem_meta(entry.name, entry)
        problems.append({
            "problem_id": entry.name,
            "title": meta.get("title"),
            "difficulty": meta.get("difficulty"),
            "number": meta.get("number"),
            "time_limit_ms": meta.get("time_limit_ms"),
            "memory_limit_kb": meta.get("memory_limit_kb"),
            "tags": meta.get("tags"),
            "tests": len(meta.get("tests", []))
        })
    problems.sort(key=_problem_sort_key)
    return {"problems": problems}

@app.post("/problem/submit")
def submit(s: SubmitReq):
    sub_id = str(uuid.uuid4())
    # Save temporary metadata
    r.hset(f"sub:{sub_id}", mapping={
        "status": "queued",
        "problem_id": s.problem_id,
        "language": s.language,
        "std": s.std or {"c": "c17", "cpp": "c++20"}.get(s.language, ""),
        "created_at": str(int(time.time()))
    })
    r.set(f"code:{sub_id}", s.code, ex=3600)
    job = {"submission_id": sub_id}
    r.lpush("queue:compile", json.dumps(job))
    return {"submission_id": sub_id}

@app.get("/problem/submission/{sub_id}")
def status(sub_id: str):
    meta = r.hgetall(f"sub:{sub_id}")
    if not meta:
        raise HTTPException(404, "not found")
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

    meta = _read_problem_meta(problem_id, base)

    statement = None
    statement_path = base / "statement.md"
    if statement_path.exists():
        try:
            statement = statement_path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            statement = statement_path.read_text(errors="replace")

    samples_payload = []
    for idx, sample in enumerate(meta.get("samples", []), start=1):
        sample_input_path = base / sample["input"]
        sample_output_path = base / sample["output"]
        if not (sample_input_path.exists() and sample_output_path.exists()):
            continue
        samples_payload.append({
            "label": sample.get("label") or f"Sample {idx}",
            "input": sample_input_path.read_text(encoding="utf-8", errors="replace"),
            "output": sample_output_path.read_text(encoding="utf-8", errors="replace"),
            "input_file": sample["input"],
            "output_file": sample["output"]
        })

    tests = meta.get("tests", [])
    public_tests = sum(1 for t in tests if t.get("visibility") == "public")
    total_tests = len(tests)

    tests_payload = []
    for idx, test in enumerate(tests, start=1):
        input_path = base / test.get("input", "")
        output_path = base / test.get("output", "")
        if not input_path.exists() or not output_path.exists():
            continue
        tests_payload.append({
            "label": f"Test {idx}",
            "input": input_path.read_text(encoding="utf-8", errors="replace"),
            "output": output_path.read_text(encoding="utf-8", errors="replace"),
            "visibility": test.get("visibility", "hidden"),
            "input_file": test.get("input"),
            "output_file": test.get("output")
        })

    return {
        "problem_id": problem_id,
        "title": meta.get("title"),
        "statement": statement,
        "difficulty": meta.get("difficulty"),
        "number": meta.get("number"),
        "description": meta.get("description"),
        "time_limit_ms": meta.get("time_limit_ms"),
        "memory_limit_kb": meta.get("memory_limit_kb"),
        "tags": meta.get("tags"),
        "samples": samples_payload,
        "tests": tests_payload,
        "tests_summary": {
            "total": total_tests,
            "public": public_tests,
            "hidden": max(total_tests - public_tests, 0)
        },
        "created_at": meta.get("created_at")
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

    description_text = req.description.strip() if req.description else None
    statement_content = req.statement.strip() if req.statement and req.statement.strip() else _compose_statement(
        problem_number,
        req.title,
        req.difficulty,
        description_text,
        req.sample_input,
        req.sample_output,
        base_name,
    )
    if not statement_content.endswith("\n"):
        statement_content += "\n"
    try:
        problem_path.mkdir(parents=True, exist_ok=False)
        statement_path = problem_path / "statement.md"
        statement_path.write_text(statement_content, encoding="utf-8")

        _write_text(problem_path / "sample_input.txt", req.sample_input)
        _write_text(problem_path / "sample_output.txt", req.sample_output)

        tests_meta = []
        for idx, test in enumerate(req.tests, start=1):
            input_name = f"input{idx}.txt"
            output_name = f"output{idx}.txt"
            _write_text(problem_path / input_name, test.input)
            _write_text(problem_path / output_name, test.output)
            tests_meta.append({
                "input": input_name,
                "output": output_name,
                "visibility": test.visibility
            })

        time_limit_ms = req.time_limit_ms if req.time_limit_ms is not None else DEFAULT_TIME_LIMIT_MS
        memory_limit_kb = req.memory_limit_kb if req.memory_limit_kb is not None else DEFAULT_MEMORY_LIMIT_KB
        tags = _normalize_tags(req.tags)

        meta = {
            "number": problem_number,
            "difficulty": req.difficulty,
            "title": req.title,
            "time_limit_ms": time_limit_ms,
            "memory_limit_kb": memory_limit_kb,
            "tags": tags,
            "created_at": int(time.time()),
            "description": description_text,
            "samples": [
                {"input": "sample_input.txt", "output": "sample_output.txt", "label": "Sample"}
            ],
            "tests": tests_meta
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
        "tests_count": len(req.tests),
        "time_limit_ms": time_limit_ms,
        "memory_limit_kb": memory_limit_kb,
        "tags": tags
    }


@app.post("/problem-edit")
def edit_problem(req: UpdateProblemReq):
    base = PROBLEMS_DIR / req.problem_id
    if not base.is_dir():
        raise HTTPException(404, "problem not found")

    if req.delete:
        shutil.rmtree(base, ignore_errors=True)
        return {"message": "problem deleted", "problem_id": req.problem_id}

    meta = _read_problem_meta(req.problem_id, base)
    problem_number = meta.get("number") or _infer_problem_number_from_name(req.problem_id)

    time_limit_ms = req.time_limit_ms if req.time_limit_ms is not None else meta.get("time_limit_ms", DEFAULT_TIME_LIMIT_MS)
    memory_limit_kb = req.memory_limit_kb if req.memory_limit_kb is not None else meta.get("memory_limit_kb", DEFAULT_MEMORY_LIMIT_KB)
    tags = _normalize_tags(req.tags if req.tags is not None else meta.get("tags"))
    description_text = req.description.strip() if req.description is not None else meta.get("description")

    statement_content = req.statement.strip() if req.statement and req.statement.strip() else _compose_statement(
        problem_number,
        req.title,
        req.difficulty,
        description_text,
        req.sample_input,
        req.sample_output,
        req.problem_id,
    )

    statement_path = base / "statement.md"
    if not statement_content.endswith("\n"):
        statement_content += "\n"
    statement_path.write_text(statement_content, encoding="utf-8")

    _write_text(base / "sample_input.txt", req.sample_input)
    _write_text(base / "sample_output.txt", req.sample_output)

    existing_meta = meta.get("tests", [])
    existing_files = set()
    for test in existing_meta:
        inp = test.get("input")
        outp = test.get("output")
        if inp:
            existing_files.add(inp)
        if outp:
            existing_files.add(outp)
    for fname in existing_files:
        fpath = base / fname
        if fpath.exists() and fpath.is_file():
            fpath.unlink()

    tests_meta = []
    for idx, test in enumerate(req.tests, start=1):
        input_name = f"input{idx}.txt"
        output_name = f"output{idx}.txt"
        _write_text(base / input_name, test.input)
        _write_text(base / output_name, test.output)
        tests_meta.append({
            "input": input_name,
            "output": output_name,
            "visibility": test.visibility
        })

    updated_meta = {
        "number": problem_number,
        "difficulty": req.difficulty,
        "title": req.title,
        "time_limit_ms": time_limit_ms,
        "memory_limit_kb": memory_limit_kb,
        "tags": tags,
        "created_at": meta.get("created_at") or int(time.time()),
        "description": description_text,
        "samples": [
            {"input": "sample_input.txt", "output": "sample_output.txt", "label": "Sample"}
        ],
        "tests": tests_meta
    }
    (base / "meta.json").write_text(json.dumps(updated_meta, indent=2), encoding="utf-8")

    return {
        "message": "problem updated",
        "problem_id": req.problem_id,
        "number": problem_number,
        "difficulty": req.difficulty,
        "tests_count": len(req.tests),
        "time_limit_ms": time_limit_ms,
        "memory_limit_kb": memory_limit_kb,
        "tags": tags
    }
