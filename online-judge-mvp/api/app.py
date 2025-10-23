import os, json, time, uuid
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
PROBLEMS_DIR = "/problems"  # worker mount; api chỉ làm enqueue

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

@app.post("/v1/submit")
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

@app.get("/v1/submission/{sub_id}")
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
