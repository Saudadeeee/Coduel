# cd /home/khenh/Code/Project/Cowar/online-judge-mvp
# DOCKER_BUILDKIT=0 docker compose up -d --build 





import os, json, time, subprocess, tempfile, shutil, uuid, re, shlex
import redis

REDIS_HOST = os.getenv("REDIS_HOST","localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT","6379"))
r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

JUDGE_IMAGE = "oj_judge:latest"  # image name from judge build (will be built via compose or manually)
def _env_limit(name, default):
    val = os.getenv(name)
    if val is None:
        return default() if callable(default) else default
    val = val.strip()
    # Remove inline comments (after #)
    if '#' in val:
        val = val.split('#')[0].strip()
    return val if val else (default() if callable(default) else default)

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
                        half_kb = max(total_kb // 2, 256 * 1024)  # minimum 256MB
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
RUNS_PER_TEST = int(os.getenv("RUNS_PER_TEST", "3"))  # Số lần chạy mỗi test để lấy median
PERFORMANCE_TOLERANCE = float(os.getenv("PERFORMANCE_TOLERANCE", "0.10"))  # 10% tolerance
JOB_TMP_ROOT = os.getenv("JOB_TMP_ROOT", "/worker_tmp")
HOST_JOB_TMP_ROOT = os.getenv("HOST_JOB_TMP_ROOT", JOB_TMP_ROOT)
PROBLEMS_ROOT = os.getenv("PROBLEMS_ROOT", "/problems")
HOST_PROBLEMS_ROOT = os.getenv("HOST_PROBLEMS_ROOT", PROBLEMS_ROOT)
os.makedirs(JOB_TMP_ROOT, exist_ok=True)

SOURCE_FILE_MAP = {
    "c": "main.c",
    "cpp": "main.cpp",
    "py": "main.py",
    "java": "Main.java",
    "js": "main.js"
}

def _parse_elapsed_seconds(val):
    if val is None:
        return None
    if isinstance(val, (int, float)):
        try:
            return float(val)
        except (TypeError, ValueError):
            return None
    if isinstance(val, str):
        stripped = val.strip()
        if not stripped:
            return None
        try:
            parts = stripped.split(":")
            if len(parts) == 1:
                return float(parts[0])
            seconds = 0.0
            for p in parts:
                seconds = seconds * 60 + float(p)
            return seconds
        except ValueError:
            return None
    return None

def _calculate_median(values):
    """Calculate median from a list of numbers"""
    if not values:
        return None
    sorted_values = sorted(values)
    n = len(sorted_values)
    if n % 2 == 0:
        return (sorted_values[n//2 - 1] + sorted_values[n//2]) / 2
    else:
        return sorted_values[n//2]

def _calculate_accuracy(passed_count, total_tests):
    """Calculate accuracy percentage"""
    if total_tests == 0:
        return 0.0
    return (passed_count / total_tests) * 100.0

def _compare_performance_with_tolerance(value_a, value_b, tolerance=PERFORMANCE_TOLERANCE):
    """
    Compare two performance values with tolerance
    Returns: 'A_BETTER', 'B_BETTER', or 'TIE'
    """
    if value_a is None and value_b is None:
        return 'TIE'
    if value_a is None:
        return 'B_BETTER'
    if value_b is None:
        return 'A_BETTER'
    
    diff = abs(value_a - value_b)
    avg = (value_a + value_b) / 2
    
    if avg == 0:
        return 'TIE'
    
    if diff / avg < tolerance:
        return 'TIE'
    
    return 'A_BETTER' if value_a < value_b else 'B_BETTER'

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
    std = meta.get("std")
    problem_id = meta["problem_id"]

    # Create temporary directory
    tmpdir = tempfile.mkdtemp(prefix=f"job_{sub_id}_", dir=JOB_TMP_ROOT)
    os.chmod(tmpdir, 0o777)
    cleanup_tmp = True
    try:
        src_name = SOURCE_FILE_MAP.get(lang, "main.cpp")
        src_file = os.path.join(tmpdir, src_name)
        with open(src_file, "w", encoding="utf-8") as f:
            f.write(code)

        # Run container to compile (not running tests at this step)
        host_tmpdir = tmpdir
        if tmpdir.startswith(JOB_TMP_ROOT):
            suffix = tmpdir[len(JOB_TMP_ROOT):]
            host_tmpdir = HOST_JOB_TMP_ROOT.rstrip("/") + suffix
        mounts = [(host_tmpdir, "/work", "rw")]
        std_arg = std or ""
        
        # Escape shell arguments properly
        src_basename = os.path.basename(src_file)
        cmd = ["bash", "-lc", f"compile_run.sh --compile-only {shlex.quote(lang)} {shlex.quote(src_basename)} {shlex.quote(std_arg)}"]
        res = docker_run(cmd, mounts=mounts, timeout=COMPILE_TIMEOUT)
        compile_log = (res.stdout or "") + "\n" + (res.stderr or "")
        r.set(f"compile_log:{sub_id}", compile_log, ex=3600)

        if res.returncode not in (0,):  # compile_run.sh returns 0 if compile OK
            r.hset(f"sub:{sub_id}", "status", "compile_error")
            return

        # After successful compilation: push to run queue
        cleanup_tmp = False  # keep directory for run step, will clean up in run_submission
        r.hset(f"sub:{sub_id}", "status", "compiled")
        r.lpush("queue:run", json.dumps({"submission_id": sub_id, "tmpdir": tmpdir, "problem_id": problem_id, "lang": lang, "std": std}))
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
    lang = job["lang"]
    std = job.get("std")

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
        # Call container to run binary on test set (compile_run.sh already generated main)
        source_for_run = SOURCE_FILE_MAP.get(lang, "main.cpp")
        std_arg = std or ""
        cmd = ["bash", "-lc", f"compile_run.sh --run-only {shlex.quote(lang)} {shlex.quote(source_for_run)} {shlex.quote(std_arg)}"]
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
        # Parse result: based on verdict_*.txt + metrics_*.txt files in /work
        verdicts = []
        metrics = []
        for i in range(1, 1000):
            vfile = os.path.join(tmpdir, f"verdict_{i}.txt")
            json_metrics = os.path.join(tmpdir, f"metrics_{i}.json")
            txt_metrics = os.path.join(tmpdir, f"metrics_{i}.txt")
            if not os.path.exists(vfile):
                break
            verdicts.append(open(vfile).read().strip())

            elapsed_sec = None
            elapsed_str = None
            maxrss = None
            exit_code = None

            if os.path.exists(json_metrics):
                try:
                    data = json.loads(open(json_metrics, encoding="utf-8").read())
                except json.JSONDecodeError:
                    data = {}
                elapsed_sec = _parse_elapsed_seconds(data.get("elapsed_seconds"))
                if elapsed_sec is not None:
                    elapsed_str = f"{elapsed_sec:.6f}"
                maxrss = data.get("max_rss_kb")
                exit_code = data.get("exit_code")
            elif os.path.exists(txt_metrics):
                txt = open(txt_metrics, encoding="utf-8").read()
                m1 = re.search(r"Elapsed \\(wall clock\\) time.*:\\s*(.*)", txt)
                m2 = re.search(r"Maximum resident set size \\(kbytes\\):\\s*(\\d+)", txt)
                if m1:
                    elapsed_str = m1.group(1).strip()
                    elapsed_sec = _parse_elapsed_seconds(elapsed_str)
                if m2:
                    maxrss = int(m2.group(1))

            if elapsed_sec is not None or maxrss is not None:
                metrics.append({
                    "test": i,
                    "elapsed": elapsed_str,
                    "elapsed_seconds": elapsed_sec,
                    "max_rss_kb": maxrss,
                    "exit_code": exit_code
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
        memory_values = [m["max_rss_kb"] for m in metrics if m.get("max_rss_kb") is not None]
        
        max_elapsed = max(elapsed_values) if elapsed_values else None
        avg_elapsed = sum(elapsed_values) / len(elapsed_values) if elapsed_values else None
        median_elapsed = _calculate_median(elapsed_values)
        
        max_mem = max(memory_values) if memory_values else None
        avg_mem = sum(memory_values) / len(memory_values) if memory_values else None
        median_mem = _calculate_median(memory_values)
        
        accuracy = _calculate_accuracy(passed_count, len(verdicts))

        performance = {
            "total_tests": len(verdicts),
            "passed": passed_count,
            "failed": len(verdicts) - passed_count,
            "accuracy": accuracy,  # NEW: Accuracy percentage (0-100)
            
            # Time metrics
            "max_elapsed_seconds": max_elapsed,
            "avg_elapsed_seconds": avg_elapsed,
            "median_elapsed_seconds": median_elapsed,  # NEW: More stable than average
            
            # Memory metrics
            "max_memory_kb": max_mem,
            "avg_memory_kb": avg_mem,  # NEW
            "median_memory_kb": median_mem,  # NEW
            
            "overall": "passed" if ok else "failed",
            
            # Metadata for ranking
            "ranking_priority": {
                "1_accuracy": accuracy,
                "2_time": median_elapsed or avg_elapsed or max_elapsed,
                "3_memory": median_mem or avg_mem or max_mem
            }
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
        # Clean up temporary working directory
        try:
            shutil.rmtree(tmpdir, ignore_errors=True)
        except:
            pass

def main():
    # simple infinite loop
    print("Worker started.", flush=True)
    # Build judge image beforehand if not available (optional):
   # subprocess.run(["docker","build","-t","oj_judge:latest","./judge"], check=True)

    while True:
        # compile queue
        msg = r.brpop("queue:compile", timeout=1)
        if msg:
            _, payload = msg
            sub_id = json.loads(payload)["submission_id"]
            print(f"[COMPILE] Processing submission {sub_id}", flush=True)
            compile_submission(sub_id)

        # run queue
        msg2 = r.brpop("queue:run", timeout=1)
        if msg2:
            _, payload2 = msg2
            job = json.loads(payload2)
            print(f"[RUN] Processing submission {job['submission_id']}", flush=True)
            run_submission(job)

def compare_submissions(sub_id_a, sub_id_b):
    """
    Compare two submissions using ranking priority:
    1. Accuracy (higher is better)
    2. Time (lower is better, with tolerance)
    3. Memory (lower is better, with tolerance)
    
    Returns: dict with comparison results
    """
    result_a_raw = r.get(f"run_result:{sub_id_a}")
    result_b_raw = r.get(f"run_result:{sub_id_b}")
    
    if not result_a_raw or not result_b_raw:
        return {"error": "One or both submissions not found"}
    
    try:
        result_a = json.loads(result_a_raw)
        result_b = json.loads(result_b_raw)
    except json.JSONDecodeError:
        return {"error": "Failed to parse results"}
    
    perf_a = result_a.get("performance", {})
    perf_b = result_b.get("performance", {})
    
    accuracy_a = perf_a.get("accuracy", 0)
    accuracy_b = perf_b.get("accuracy", 0)
    
    # Priority 1: Accuracy
    if accuracy_a != accuracy_b:
        winner = "A" if accuracy_a > accuracy_b else "B"
        return {
            "winner": winner,
            "reason": "accuracy",
            "details": {
                "accuracy_a": accuracy_a,
                "accuracy_b": accuracy_b,
                "diff": abs(accuracy_a - accuracy_b)
            }
        }
    
    # If accuracy is equal, compare time
    time_a = perf_a.get("median_elapsed_seconds") or perf_a.get("avg_elapsed_seconds")
    time_b = perf_b.get("median_elapsed_seconds") or perf_b.get("avg_elapsed_seconds")
    
    time_comparison = _compare_performance_with_tolerance(time_a, time_b)
    
    # Priority 2: Time (with tolerance)
    if time_comparison != 'TIE':
        winner = "A" if time_comparison == "A_BETTER" else "B"
        return {
            "winner": winner,
            "reason": "time",
            "details": {
                "time_a_ms": time_a * 1000 if time_a else None,
                "time_b_ms": time_b * 1000 if time_b else None,
                "diff_ms": abs(time_a - time_b) * 1000 if time_a and time_b else None,
                "tolerance": f"{PERFORMANCE_TOLERANCE * 100}%"
            }
        }
    
    # If time is within tolerance, compare memory
    mem_a = perf_a.get("median_memory_kb") or perf_a.get("avg_memory_kb")
    mem_b = perf_b.get("median_memory_kb") or perf_b.get("avg_memory_kb")
    
    mem_comparison = _compare_performance_with_tolerance(mem_a, mem_b)
    
    # Priority 3: Memory (with tolerance)
    if mem_comparison != 'TIE':
        winner = "A" if mem_comparison == "A_BETTER" else "B"
        return {
            "winner": winner,
            "reason": "memory",
            "details": {
                "memory_a_mb": mem_a / 1024 if mem_a else None,
                "memory_b_mb": mem_b / 1024 if mem_b else None,
                "diff_mb": abs(mem_a - mem_b) / 1024 if mem_a and mem_b else None,
                "tolerance": f"{PERFORMANCE_TOLERANCE * 100}%"
            }
        }
    
    # Complete tie
    return {
        "winner": "TIE",
        "reason": "all_metrics_equal_within_tolerance",
        "details": {
            "accuracy": accuracy_a,
            "time_ms": time_a * 1000 if time_a else None,
            "memory_mb": mem_a / 1024 if mem_a else None
        }
    }

if __name__ == "__main__":
    main()
