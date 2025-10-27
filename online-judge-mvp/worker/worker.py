# cd /home/khenh/Code/Project/Cowar/online-judge-mvp
# DOCKER_BUILDKIT=0 docker compose up -d --build 





import os, json, time, subprocess, tempfile, shutil, uuid, re, shlex
import redis

REDIS_HOST = os.getenv("REDIS_HOST","localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT","6379"))
r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

JUDGE_IMAGE = "oj_judge:latest"  # name từ build judge riêng (ta sẽ build bằng compose hoặc tay)
def _env_limit(name, default):
    val = os.getenv(name)
    if val is None:
        return default() if callable(default) else default
    val = val.strip()
    return val or None

def _default_cpu_limit():
    count = os.cpu_count() or 1
    half = max(1.0, count / 2.0) 
    if abs(half - round(half)) < 1e-9:
        return str(int(round(half)))
    return f"{half:.2f}".rstrip("0").rstrip(".")

def _default_mem_limit():
    try:
        with open("/proc/meminfo", encoding="utf-8") as meminfo:
            for line in meminfo:
                if line.startswith("MemTotal:"):
                    parts = line.split()
                    if len(parts) >= 2:
                        total_kb = int(parts[1])
                        half_kb = max(total_kb // 2, 256 * 1024)  # tối thiểu 256MB
                        half_mb = max(half_kb // 1024, 256)
                        return f"{half_mb}m"
    except (OSError, ValueError):
        pass
    return "1g"

CPU_LIMIT = _env_limit("CPU_LIMIT", _default_cpu_limit)
MEM_LIMIT = _env_limit("MEM_LIMIT", _default_mem_limit)
DOCKER_RUN_TIMEOUT = int(os.getenv("DOCKER_RUN_TIMEOUT", "60"))
COMPILE_TIMEOUT = int(os.getenv("COMPILE_TIMEOUT", str(DOCKER_RUN_TIMEOUT)))
RUN_TIMEOUT = int(os.getenv("RUN_TIMEOUT", str(DOCKER_RUN_TIMEOUT)))
DOCKER_RUN_EXTRA_ARGS = shlex.split(os.getenv("DOCKER_RUN_EXTRA_ARGS", ""))
JOB_TMP_ROOT = os.getenv("JOB_TMP_ROOT", "/worker_tmp")
HOST_JOB_TMP_ROOT = os.getenv("HOST_JOB_TMP_ROOT", JOB_TMP_ROOT)
PROBLEMS_ROOT = os.getenv("PROBLEMS_ROOT", "/problems")
HOST_PROBLEMS_ROOT = os.getenv("HOST_PROBLEMS_ROOT", PROBLEMS_ROOT)
os.makedirs(JOB_TMP_ROOT, exist_ok=True)

def _parse_elapsed_seconds(val):
    if not val:
        return None
    val = val.strip()
    if not val:
        return None
    try:
        parts = val.split(":")
        if len(parts) == 1:
            return float(parts[0])
        seconds = 0.0
        for p in parts:
            seconds = seconds * 60 + float(p)
        return seconds
    except ValueError:
        return None

def docker_run(cmd, mounts=None, readonly_root=True, timeout=None):
    base = ["docker", "run", "--rm", "--network", "none"]
    if CPU_LIMIT:
        base += ["--cpus", CPU_LIMIT]
    if MEM_LIMIT:
        base += ["--memory", MEM_LIMIT]
    if readonly_root:
        base += ["--read-only", "--tmpfs", "/tmp"]
        has_work_mount = mounts and any(cont_path == "/work" for _, cont_path, _ in mounts)
        if not has_work_mount:
            base += ["--tmpfs", "/work"]
    if DOCKER_RUN_EXTRA_ARGS:
        base += DOCKER_RUN_EXTRA_ARGS
    if mounts:
        for host_path, cont_path, mode in mounts:
            base += ["-v", f"{host_path}:{cont_path}:{mode}"]
    base.append(JUDGE_IMAGE)
    full = base + cmd
    return subprocess.run(full, capture_output=True, text=True, timeout=timeout or DOCKER_RUN_TIMEOUT)

def compile_submission(sub_id):
    meta = r.hgetall(f"sub:{sub_id}")
    code = r.get(f"code:{sub_id}")
    if not meta or not code:
        r.hset(f"sub:{sub_id}", "status", "error")
        return

    lang = meta["language"]
    opt = meta["opt"]
    std = meta["std"]
    problem_id = meta["problem_id"]

    # Tạo thư mục tạm
    tmpdir = tempfile.mkdtemp(prefix=f"job_{sub_id}_", dir=JOB_TMP_ROOT)
    os.chmod(tmpdir, 0o777)
    cleanup_tmp = True
    try:
        src_file = os.path.join(tmpdir, "main.c" if lang=="c" else "main.cpp")
        with open(src_file, "w", encoding="utf-8") as f:
            f.write(code)

        # Chạy container để biên dịch (không chạy test ở bước này)
        host_tmpdir = tmpdir
        if tmpdir.startswith(JOB_TMP_ROOT):
            suffix = tmpdir[len(JOB_TMP_ROOT):]
            host_tmpdir = HOST_JOB_TMP_ROOT.rstrip("/") + suffix
        mounts = [(host_tmpdir, "/work", "rw")]
        cmd = ["bash", "-lc", f"compile_run.sh --compile-only {lang} {os.path.basename(src_file)} {opt} {std} && true"]
        res = docker_run(cmd, mounts=mounts, timeout=COMPILE_TIMEOUT)
        compile_log = (res.stdout or "") + "\n" + (res.stderr or "")
        r.set(f"compile_log:{sub_id}", compile_log, ex=3600)

        if res.returncode not in (0,):  # compile_run.sh trả 0 nếu compile OK
            r.hset(f"sub:{sub_id}", "status", "compile_error")
            return

        # Sau compile OK: đẩy sang hàng chạy
        cleanup_tmp = False  # giữ thư mục cho bước run, sẽ dọn trong run_submission
        r.hset(f"sub:{sub_id}", "status", "compiled")
        r.lpush("queue:run", json.dumps({"submission_id": sub_id, "tmpdir": tmpdir, "problem_id": problem_id, "lang": lang, "opt": opt, "std": std}))
    except subprocess.TimeoutExpired:
        r.hset(f"sub:{sub_id}", "status", "compile_timeout")
    except Exception as e:
        r.hset(f"sub:{sub_id}", "status", "error")
        r.set(f"compile_log:{sub_id}", str(e), ex=3600)
    finally:
        if cleanup_tmp:
            shutil.rmtree(tmpdir, ignore_errors=True)

def run_submission(job):
    sub_id = job["submission_id"]
    tmpdir = job["tmpdir"]
    problem_id = job["problem_id"]
    lang = job["lang"]; opt = job["opt"]; std = job["std"]

    tests_dir = os.path.abspath(os.path.join(PROBLEMS_ROOT, problem_id))
    if not os.path.isdir(tests_dir):
        r.hset(f"sub:{sub_id}", "status", "problem_not_found")
        return

    try:
        host_tmpdir = tmpdir
        if tmpdir.startswith(JOB_TMP_ROOT):
            suffix = tmpdir[len(JOB_TMP_ROOT):]
            host_tmpdir = HOST_JOB_TMP_ROOT.rstrip("/") + suffix

        host_tests_dir = tests_dir
        if tests_dir.startswith(PROBLEMS_ROOT):
            suffix2 = tests_dir[len(PROBLEMS_ROOT):]
            host_tests_dir = HOST_PROBLEMS_ROOT.rstrip("/") + suffix2

        mounts = [
            (host_tmpdir, "/work", "rw"),
            (host_tests_dir, "/tests", "ro")
        ]
        # Gọi container chạy lại binary trên bộ test (compile_run.sh đã sinh main)
        cmd = ["bash", "-lc", f"compile_run.sh --run-only {lang} {('main.c' if lang=='c' else 'main.cpp')} {opt} {std} && true"]
        res = docker_run(cmd, mounts=mounts, timeout=RUN_TIMEOUT)
        if res.returncode not in (0,):
            error_payload = {
                "error": "judge_container_failed",
                "exit_code": res.returncode,
                "stdout_tail": (res.stdout or "")[-4000:],
                "stderr_tail": (res.stderr or "")[-2000:]
            }
            r.set(f"run_result:{sub_id}", json.dumps(error_payload), ex=3600)
            r.hset(f"sub:{sub_id}", "status", "error")
            return
        # Parse kết quả: dựa vào file verdict_*.txt + metrics_*.txt trong /work
        verdicts = []
        metrics = []
        for i in range(1, 1000):
            vfile = os.path.join(tmpdir, f"verdict_{i}.txt")
            mfile = os.path.join(tmpdir, f"metrics_{i}.txt")
            if not os.path.exists(vfile):
                break
            verdicts.append(open(vfile).read().strip())
            if os.path.exists(mfile):
                txt = open(mfile).read()
                elapsed = None; maxrss = None
                # /usr/bin/time -v keys (allow optional hints in parenthesis)
                m1 = re.search(r"Elapsed \(wall clock\) time.*:\s*(.*)", txt)
                m2 = re.search(r"Maximum resident set size \(kbytes\):\s*(\d+)", txt)
                if m1: elapsed = m1.group(1).strip()
                if m2: maxrss = int(m2.group(1))
                metrics.append({
                    "test": i,
                    "elapsed": elapsed,
                    "elapsed_seconds": _parse_elapsed_seconds(elapsed),
                    "max_rss_kb": maxrss
                })
        ok = all(v == "OK" for v in verdicts) if verdicts else False

        metrics_map = {m["test"]: m for m in metrics}
        tests_summary = []
        passed_count = 0
        for idx, verdict in enumerate(verdicts, start=1):
            passed = verdict.upper() == "OK"
            if passed:
                passed_count += 1
            metric = metrics_map.get(idx)
            tests_summary.append({
                "label": f"Test {idx}",
                "test": idx,
                "passed": passed,
                "verdict": verdict,
                "elapsed": metric["elapsed"] if metric else None,
                "elapsed_seconds": metric["elapsed_seconds"] if metric else None,
                "max_rss_kb": metric["max_rss_kb"] if metric else None
            })

        elapsed_values = [m["elapsed_seconds"] for m in metrics if m.get("elapsed_seconds") is not None]
        max_elapsed = max(elapsed_values) if elapsed_values else None
        avg_elapsed = sum(elapsed_values) / len(elapsed_values) if elapsed_values else None
        max_mem = max((m["max_rss_kb"] for m in metrics if m.get("max_rss_kb") is not None), default=None)

        performance = {
            "total_tests": len(verdicts),
            "passed": passed_count,
            "failed": len(verdicts) - passed_count,
            "max_elapsed_seconds": max_elapsed,
            "avg_elapsed_seconds": avg_elapsed,
            "max_memory_kb": max_mem,
            "overall": "passed" if ok else "failed"
        }

        run_result = {
            "ok": ok,
            "tests": tests_summary,
            "performance": performance,
            "stdout_tail": (res.stdout or "")[-4000:],
            "stderr_tail": (res.stderr or "")[-2000:]
        }
        r.set(f"run_result:{sub_id}", json.dumps(run_result), ex=3600)
        r.hset(f"sub:{sub_id}", "status", "done" if ok else "failed")
    except subprocess.TimeoutExpired:
        r.hset(f"sub:{sub_id}", "status", "run_timeout")
    except Exception as e:
        r.hset(f"sub:{sub_id}", "status", "error")
        r.set(f"run_result:{sub_id}", json.dumps({"error": str(e)}), ex=3600)
    finally:
        # Dọn thư mục làm việc tạm
        try:
            shutil.rmtree(tmpdir, ignore_errors=True)
        except:
            pass

def main():
    # vòng lặp vô tận đơn giản
    print("Worker started.")
    # Build trước image judge nếu chưa có (tuỳ chọn):
   # subprocess.run(["docker","build","-t","oj_judge:latest","./judge"], check=True)

    while True:
        # compile queue
        msg = r.brpop("queue:compile", timeout=1)
        if msg:
            _, payload = msg
            sub_id = json.loads(payload)["submission_id"]
            compile_submission(sub_id)

        # run queue
        msg2 = r.brpop("queue:run", timeout=1)
        if msg2:
            _, payload2 = msg2
            run_submission(json.loads(payload2))

if __name__ == "__main__":
    main()
