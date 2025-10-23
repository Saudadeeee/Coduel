import os, json, time, subprocess, tempfile, shutil, uuid, re
import redis

REDIS_HOST = os.getenv("REDIS_HOST","localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT","6379"))
r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

JUDGE_IMAGE = "oj_judge:latest"  # name từ build judge riêng (ta sẽ build bằng compose hoặc tay)
CPU_LIMIT = "1"   # 1 CPU
MEM_LIMIT = "1g"  # 1 GB

def docker_run(cmd, mounts=None, readonly_root=True):
    base = ["docker", "run", "--rm",
            "--cpus", CPU_LIMIT,
            "--memory", MEM_LIMIT,
            "--network", "none"]
    if readonly_root:
        base += ["--read-only", "--tmpfs", "/tmp", "--tmpfs", "/work"]
    if mounts:
        for host_path, cont_path, mode in mounts:
            base += ["-v", f"{host_path}:{cont_path}:{mode}"]
    base.append(JUDGE_IMAGE)
    full = base + cmd
    return subprocess.run(full, capture_output=True, text=True, timeout=60)

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
    tmpdir = tempfile.mkdtemp(prefix=f"job_{sub_id}_")
    try:
        src_file = os.path.join(tmpdir, "main.c" if lang=="c" else "main.cpp")
        with open(src_file, "w", encoding="utf-8") as f:
            f.write(code)

        # Chạy container để biên dịch (không chạy test ở bước này)
        mounts = [(tmpdir, "/work", "rw")]
        cmd = ["bash", "-lc", f"compile_run.sh {lang} {os.path.basename(src_file)} {opt} {std} && true"]
        res = docker_run(cmd, mounts=mounts)
        compile_log = (res.stdout or "") + "\n" + (res.stderr or "")
        r.set(f"compile_log:{sub_id}", compile_log, ex=3600)

        if res.returncode not in (0,):  # compile_run.sh trả 0 nếu compile OK
            r.hset(f"sub:{sub_id}", "status", "compile_error")
            return

        # Sau compile OK: đẩy sang hàng chạy
        r.hset(f"sub:{sub_id}", "status", "compiled")
        r.lpush("queue:run", json.dumps({"submission_id": sub_id, "tmpdir": tmpdir, "problem_id": problem_id, "lang": lang, "opt": opt, "std": std}))
    except subprocess.TimeoutExpired:
        r.hset(f"sub:{sub_id}", "status", "compile_timeout")
    except Exception as e:
        r.hset(f"sub:{sub_id}", "status", "error")
        r.set(f"compile_log:{sub_id}", str(e), ex=3600)

def run_submission(job):
    sub_id = job["submission_id"]
    tmpdir = job["tmpdir"]
    problem_id = job["problem_id"]
    lang = job["lang"]; opt = job["opt"]; std = job["std"]

    tests_dir = os.path.abspath(os.path.join("/problems", problem_id))
    if not os.path.isdir(tests_dir):
        r.hset(f"sub:{sub_id}", "status", "problem_not_found")
        return

    try:
        mounts = [
            (tmpdir, "/work", "rw"),
            (tests_dir, "/tests", "ro")
        ]
        # Gọi container chạy lại binary trên bộ test (compile_run.sh đã sinh main)
        cmd = ["bash", "-lc", f"ls -l && /usr/bin/time -v true && ./main </dev/null >/dev/null 2>/dev/null || true; compile_run.sh {lang} {('main.c' if lang=='c' else 'main.cpp')} {opt} {std} && true"]
        # Lưu ý: Ở compile step ta đã build rồi; câu lệnh trên gọi lại compile_run.sh chủ yếu để “RUN” vòng test.
        # Đơn giản hơn: bạn có thể tách compile và run script riêng. Để nhanh, ta tái dụng script.
        res = docker_run(cmd, mounts=mounts)
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
                # /usr/bin/time -v keys
                m1 = re.search(r"Elapsed \(wall clock\) time\s*:\s*(.*)", txt)
                m2 = re.search(r"Maximum resident set size \(kbytes\):\s*(\d+)", txt)
                if m1: elapsed = m1.group(1).strip()
                if m2: maxrss = int(m2.group(1))
                metrics.append({"test": i, "elapsed": elapsed, "max_rss_kb": maxrss})
        ok = all(v == "OK" for v in verdicts) if verdicts else False

        run_result = {
            "ok": ok,
            "verdicts": verdicts,
            "metrics": metrics,
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
