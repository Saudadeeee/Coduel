# CODUEL - Hướng Dẫn Làm Việc (Work Instruction)

## 📋 Tổng Quan Dự Án

**Coduel** là một nền tảng lập trình thi đấu (competitive programming platform) cho phép người dùng thi đấu code 1-1 theo thời gian thực, lấy cảm hứng từ "Clash of Code".

### Đặc Điểm Chính:
- 🎮 **Multiplayer Real-time**: Thi đấu code 1v1 theo thời gian thực
- 🔒 **Docker Isolation**: Chạy code trong container cô lập
- 📊 **Performance-Based Judging**: Chấm điểm dựa trên độ chính xác → thời gian → bộ nhớ
- 👀 **Anti-Cheat**: Xem code đối thủ real-time để chống gian lận
- 🌐 **5 Ngôn Ngữ**: C, C++, Python 3, Java, JavaScript (Node.js)

---

## 🏗️ Kiến Trúc Hệ Thống

### Các Component Chính:

```
┌─────────────────────────────────────────────────────────────┐
│                    USER BROWSER                             │
│            (HTML/CSS/JS + Monaco Editor)                    │
└──────┬────────────────────────────────┬─────────────────────┘
       │ HTTP/REST                      │ WebSocket
       ▼                                ▼
┌──────────────┐              ┌─────────────────────┐
│  WEB SERVER  │◄────────────►│ SOCKET.IO SERVER    │
│  (Express)   │              │ (Real-time Sync)    │
│  Port: 5173  │              │  - Rooms            │
└──────┬───────┘              │  - Code Broadcast   │
       │                      └──────────┬──────────┘
       │ HTTP                            │
       ▼                                 │
┌──────────────┐                        │
│  API SERVER  │                        │
│  (FastAPI)   │                        │
│  Port: 8000  │                        │
└──────┬───────┘                        │
       │                                 │
       └───────────┬─────────────────────┘
                   │
                   ▼
         ┌─────────────────┐
         │      REDIS      │
         │   Port: 6379    │
         │  - Queue        │
         │  - Cache        │
         └────────┬────────┘
                  │
                  ▼
         ┌─────────────────┐
         │     WORKER      │
         │  (Python Daemon)│
         │  - Compile      │
         │  - Execute      │
         └────────┬────────┘
                  │
                  ▼
         ┌─────────────────┐
         │  JUDGE ENGINE   │
         │    (Docker)     │
         │  - Run Code     │
         │  - Metrics      │
         └─────────────────┘
```

---

## 📁 Cấu Trúc Thư Mục

```
Coduel/
├── docker-compose.yml          # Orchestration tất cả services
├── .env.judge                  # Config cho worker (CPU/Memory limits)
│
├── api/                        # FastAPI REST API
│   ├── app.py                  # Main API endpoints
│   ├── requirements.txt        # Python dependencies
│   └── Dockerfile              # Container definition
│
├── web/                        # Node.js Web Server + Socket.IO
│   ├── server.js               # Express + Socket.IO server
│   ├── package.json            # NPM dependencies
│   ├── public/                 # Static files (HTML/CSS/JS)
│   └── Dockerfile              
│
├── worker/                     # Background job processor
│   ├── worker.py               # Main daemon (compile & run jobs)
│   ├── requirements.txt        # Python dependencies
│   └── Dockerfile              
│
├── judge/                      # Execution environment
│   ├── Dockerfile              # Ubuntu + compilers (GCC, Python, Java, Node)
│   ├── compile_run.sh          # Compile & run script
│   ├── run_with_metrics.py     # Measure time/memory
│   └── compare_output.py       # Token-based output comparison
│
├── problems/                   # Problem repository
│   ├── 001-sum-two/
│   │   ├── meta.json           # Problem metadata
│   │   ├── statement.md        # Problem description (Markdown)
│   │   ├── sample_input.txt    # Sample test input
│   │   ├── sample_output.txt   # Sample test output
│   │   ├── input1.txt          # Hidden test case 1
│   │   ├── output1.txt         
│   │   ├── input2.txt          # Hidden test case 2
│   │   └── ...
│   ├── 002-99-problems/
│   └── ...
│
└── worker_tmp/                 # Temporary directory for worker jobs
```

---

## 🔧 Chi Tiết Từng Component

### 1. **API Server** (`api/`)
**Technology**: FastAPI (Python)  
**Port**: 8000

**Endpoints chính:**
- `GET /problems` - Lấy danh sách bài toán
- `GET /problem/{id}` - Chi tiết bài toán + test cases
- `POST /problem-add` - Tạo bài toán mới
- `POST /problem-edit` - Sửa/xóa bài toán
- `POST /problem/submit` - Nộp code để chấm
- `GET /problem/submission/{id}` - Lấy kết quả submission

**Nhiệm vụ:**
- Validate dữ liệu với Pydantic
- Quản lý metadata bài toán
- Đẩy job vào Redis queue
- Trả kết quả từ Redis cache

**File quan trọng:**
- `app.py` (700 dòng) - Toàn bộ logic API

---

### 2. **Web Server** (`web/`)
**Technology**: Express.js + Socket.IO (Node.js)  
**Port**: 5173

**Nhiệm vụ:**
- Serve static files (HTML/CSS/JS)
- WebSocket server cho real-time features:
  - Room management (create/join/leave)
  - Code broadcasting (live code sync giữa 2 players)
  - Match coordination (ready check, round start)
  - Result broadcasting
- Proxy API requests tới FastAPI

**File quan trọng:**
- `server.js` (900 dòng) - Express + Socket.IO logic
- `public/` - Frontend files (Monaco Editor, UI)

---

### 3. **Worker** (`worker/`)
**Technology**: Python + Docker SDK  
**Nhiệm vụ**: Background job processor

**Flow:**
1. **Poll Redis** queue (`queue:compile`) cho submission jobs
2. **Compile** code trong Docker container
3. **Run** code với tất cả test cases
4. **Collect metrics** (time, memory, accuracy)
5. **Multi-run testing**: Chạy mỗi test `RUNS_PER_TEST` lần (default: 3)
6. **Calculate median** time/memory để tránh outliers
7. **Store results** vào Redis

**Environment Variables:**
- `CPU_LIMIT` - Max CPU cores cho judge container (default: half system CPU)
- `MEM_LIMIT` - Max memory (default: half system RAM)
- `RUNS_PER_TEST` - Số lần chạy mỗi test (default: 3)
- `PERFORMANCE_TOLERANCE` - Sai số cho so sánh performance (default: 10%)
- `COMPILE_TIMEOUT` - Timeout cho compile (default: 10s)
- `RUN_TIMEOUT` - Timeout cho mỗi test run (default: 10s)

**File quan trọng:**
- `worker.py` (533 dòng) - Main daemon logic

---

### 4. **Judge Engine** (`judge/`)
**Technology**: Docker container với Ubuntu + compilers

**Installed Tools:**
- GCC (C/C++) - C17, C++20
- Python 3
- OpenJDK (Java)
- Node.js (JavaScript)
- GNU Time - Resource monitoring

**Security:**
- Network disabled (`--network none`)
- Filesystem read-only (chỉ `/work` writable)
- Resource limits (CPU, Memory)
- Timeout protection

**Scripts:**
1. **compile_run.sh** (109 dòng)
   - Compile code theo ngôn ngữ
   - Run với từng test case
   - Gọi `run_with_metrics.py` và `compare_output.py`

2. **run_with_metrics.py**
   - Chạy program với stdin/stdout redirect
   - Đo thời gian với `time.perf_counter()`
   - Đo memory với `resource.getrusage()`
   - Xuất metrics ra JSON

3. **compare_output.py**
   - **Token-based comparison** (whitespace-insensitive)
   - So sánh từng token (số/chữ), bỏ qua khoảng trắng
   - `"1 2 3"` = `"1  2  3"` = `"1\n2\n3"` ✅

---

### 5. **Redis**
**Version**: 7 (Alpine)  
**Port**: 6379

**Data Structures:**

#### Queues:
- `queue:compile` - Job queue cho submissions

#### Submission Data:
- `sub:{id}` - Submission metadata (JSON)
- `code:{id}` - Source code
- `run_result:{id}` - Test results (JSON)
- `compile_log:{id}` - Compilation output/errors

#### Room State (in-memory):
- Room configurations
- Player states
- Match scores

---

### 6. **Problems Directory** (`problems/`)

Mỗi bài toán có folder riêng theo format: `{number}-{slug}/`

**Ví dụ:** `001-sum-two/`

**Files trong mỗi problem:**

```
001-sum-two/
├── meta.json              # Metadata (title, difficulty, tags, time/memory limits)
├── statement.md           # Problem description (Markdown)
├── sample_input.txt       # Sample test cho user xem
├── sample_output.txt      
├── input1.txt             # Test case 1
├── output1.txt            
├── input2.txt             # Test case 2
├── output2.txt            
└── ...                    # More test cases
```

**meta.json structure:**
```json
{
  "number": 1,
  "difficulty": "fast",
  "title": "Sum Two Numbers",
  "time_limit_ms": 2000,
  "memory_limit_kb": 262144,
  "tags": ["math", "implementation"],
  "created_at": 1761540634,
  "description": "Given two integers a and b...",
  "samples": [
    {"input": "sample_input.txt", "output": "sample_output.txt", "label": "Sample"}
  ],
  "tests": [
    {"input": "input1.txt", "output": "output1.txt", "visibility": "public"},
    {"input": "input2.txt", "output": "output2.txt", "visibility": "hidden"}
  ]
}
```

---

## 🔄 Flow Hoạt Động

### Flow 1: Submit Code (Training Mode)

```
1. User viết code trong Monaco Editor
2. Click "Submit & Run"
3. Browser gửi POST /problem/submit với {language, code, problem_id}
4. API Server:
   - Validate input
   - Generate submission_id
   - Lưu code vào Redis (code:{id})
   - Push job vào Redis queue (queue:compile)
   - Return submission_id
5. Worker:
   - Poll queue, lấy job
   - Tạo temp folder trong worker_tmp/
   - Write source code file
   - Docker run judge container:
     - Mount code folder, test folder
     - Run compile_run.sh --compile-only
   - Nếu compile thành công:
     - Chạy lại container cho từng test:
       - Run compile_run.sh --run-only
       - Lặp RUNS_PER_TEST lần
       - Collect metrics (time, memory)
     - Calculate median time/memory
     - Compare output với expected
   - Tính tổng score: accuracy% → avg_time → avg_memory
   - Lưu kết quả vào Redis (run_result:{id})
6. Browser poll GET /problem/submission/{id}
7. API trả results từ Redis
8. UI hiển thị: Pass/Fail, Time, Memory cho từng test
```

### Flow 2: Multiplayer Match

```
1. Player A tạo room:
   - Click "Host Room"
   - Config: difficulty, rounds, spectator mode
   - Server tạo room với random code (6 chars)
   - Player A join room
2. Player B join:
   - Nhập room code
   - Click "Join Room"
   - Server add player B vào room
3. Ready check:
   - Cả 2 player click "Ready"
   - Server broadcast "match_starting"
4. Round bắt đầu:
   - Server random pick 1 problem từ difficulty
   - Broadcast problem_id tới cả 2 players
   - Both players load problem statement
5. Coding phase:
   - Mỗi player viết code trong Monaco Editor
   - Nếu spectator ON: code sync real-time qua WebSocket
   - Player submit khi hoàn thành
6. Judging:
   - Giống flow 1 (submit code)
   - Cả 2 submissions được chấm song song
7. Result comparison:
   - API so sánh 2 submissions:
     - Accuracy: % test pass
     - Time: median execution time
     - Memory: median memory usage
   - Winner: accuracy > time > memory
   - Broadcast result tới room
8. Next round:
   - Nếu chưa hết rounds: lặp lại từ bước 4
   - Nếu hết: tính tổng điểm → announce winner
```

---

## 🚀 Cách Chạy Dự Án

### Prerequisites:
- Docker 20.10+
- Docker Compose 2.0+
- Port available: 5173, 8000, 6379

### Bước 1: Clone & Setup

```bash
cd Coduel/
```

### Bước 2: Config (Optional)

Tạo file `.env.judge`:
```bash
RUNS_PER_TEST=3
PERFORMANCE_TOLERANCE=0.10
CPU_LIMIT=2.0
MEM_LIMIT=1g
COMPILE_TIMEOUT=10
RUN_TIMEOUT=10
```

### Bước 3: Build & Run

```bash
docker-compose up --build -d
```

Verify services:
```bash
docker ps
# Should show: oj_web, oj_api, oj_worker, oj_redis
```

### Bước 4: Access

- **Web UI**: http://localhost:5173
- **API Docs**: http://localhost:8000/docs
- **Redis**: localhost:6379

### Bước 5: Test

1. Vào http://localhost:5173
2. Chọn "Training Mode"
3. Chọn problem "001-sum-two"
4. Viết code:
   ```python
   a, b = map(int, input().split())
   print(a + b)
   ```
5. Click "Submit & Run"
6. Xem kết quả: Pass/Fail, Time, Memory

---

## 🛠️ Development Guidelines

### Khi thêm bài toán mới:

**Option 1: Qua Web UI**
- Vào http://localhost:5173/problem-add
- Fill form: title, difficulty, description, test cases
- Click "Create Problem"

**Option 2: Manual (Recommend cho bulk import)**

1. Tạo folder: `problems/{number}-{slug}/`
2. Tạo files:
   ```
   meta.json
   statement.md
   sample_input.txt
   sample_output.txt
   input1.txt, output1.txt
   input2.txt, output2.txt
   ...
   ```
3. Restart API container: `docker-compose restart api`

### Khi thay đổi Judge Logic:

1. Edit `judge/compile_run.sh` hoặc `judge/*.py`
2. Rebuild judge image:
   ```bash
   docker-compose build judge
   ```
3. Restart worker:
   ```bash
   docker-compose restart worker
   ```

### Khi thay đổi API:

1. Edit `api/app.py`
2. Restart:
   ```bash
   docker-compose restart api
   ```

### Khi thay đổi Worker:

1. Edit `worker/worker.py`
2. Restart:
   ```bash
   docker-compose restart worker
   ```

### Khi thay đổi Frontend:

1. Edit files trong `web/public/`
2. Refresh browser (no restart needed for static files)
3. Nếu sửa `web/server.js`:
   ```bash
   docker-compose restart web
   ```

---

## 🔍 Debugging

### Xem logs:

```bash
# Tất cả services
docker-compose logs -f

# Specific service
docker-compose logs -f api
docker-compose logs -f worker
docker-compose logs -f web
```

### Check Redis data:

```bash
docker exec -it oj_redis redis-cli

# List all keys
KEYS *

# Get submission result
GET run_result:{submission_id}

# Check queue length
LLEN queue:compile
```

### Debug worker không chạy:

```bash
docker-compose logs worker

# Common issues:
# - Docker socket permission: Ensure worker container has access to /var/run/docker.sock
# - Redis connection: Check REDIS_HOST env var
# - Judge image missing: Run `docker-compose build judge`
```

### Debug compilation errors:

```bash
# Check compile log trong Redis
docker exec -it oj_redis redis-cli GET compile_log:{submission_id}
```

---

## 📊 Performance Metrics

### Judging Criteria (Priority Order):

1. **Accuracy**: % test cases passed
   - 100% > 90% > 50%
2. **Execution Time**: Median time across all runs
   - Faster = better
   - Tolerance: 10% (configurable)
3. **Memory Usage**: Median max RSS
   - Lower = better

### Multi-Run Testing:

- Mỗi test chạy `RUNS_PER_TEST` lần (default: 3)
- Lấy **median** time & memory (tránh outliers)
- Timeout mỗi run: `RUN_TIMEOUT` seconds

---

## 🔐 Security Features

### Docker Isolation:
- Mỗi submission chạy trong container riêng biệt
- Network disabled: `--network none`
- Filesystem read-only (trừ `/work`)
- Auto cleanup sau mỗi run

### Resource Limits:
- CPU limit: `--cpus={CPU_LIMIT}`
- Memory limit: `--memory={MEM_LIMIT}`
- Timeout: `COMPILE_TIMEOUT`, `RUN_TIMEOUT`

### Anti-Cheat:
- Real-time code spectating (nếu enabled)
- Cả 2 players thấy code nhau → không thể copy

---

## 📝 Code Style & Conventions

### Python (API, Worker, Judge):
- **Style**: PEP 8
- **Type hints**: Required cho functions
- **Imports**: Absolute imports
- **Error handling**: Try-except với logging

### JavaScript (Web):
- **Style**: ES6+
- **Async**: async/await (không dùng callbacks)
- **Socket events**: Naming convention: `{action}_{entity}`
  - Example: `join_room`, `submit_code`, `round_start`

### Shell Scripts (Judge):
- **Shebang**: `#!/usr/bin/env bash`
- **Strict mode**: `set -euo pipefail`
- **Error handling**: Check exit codes

---

## 🧪 Testing

### Manual Testing:

1. **Solo mode**: Submit code trong Training Mode
2. **Multiplayer**: Tạo 2 tabs browser, host & join room
3. **Edge cases**: 
   - Compilation errors
   - Runtime errors (segfault, TLE, MLE)
   - Wrong answer vs whitespace differences
   - Empty output

### Test Cases Format:

```
# Good test case
input1.txt:  "5 10"
output1.txt: "15"

# Bad (avoid)
input.txt:   "5 10\n\n" (extra newlines)
output.txt:  "15 " (trailing spaces) - OK nhưng không cần thiết
```

---

## 🚨 Common Issues & Solutions

### Issue 1: Worker không poll jobs

**Symptoms**: Submit code nhưng không có kết quả  
**Check**:
```bash
docker-compose logs worker
```
**Solutions**:
- Ensure Redis running: `docker-compose ps redis`
- Check worker logs for errors
- Verify judge image exists: `docker images | grep oj_judge`

### Issue 2: Compilation failed

**Check Redis**:
```bash
docker exec -it oj_redis redis-cli GET compile_log:{submission_id}
```
**Common causes**:
- Syntax errors
- Missing imports
- Wrong language selected

### Issue 3: TLE (Time Limit Exceeded)

**Check**:
- Test input size
- Algorithm complexity (O(n²) vs O(n log n))
- Infinite loops

**Adjust limits** (trong `.env.judge`):
```
RUN_TIMEOUT=20  # Increase to 20s
```

### Issue 4: WebSocket disconnected

**Check**:
```bash
docker-compose logs web
```
**Solutions**:
- Restart web service: `docker-compose restart web`
- Check browser console for errors
- Verify Socket.IO version compatibility

---

## 📚 Dependencies

### API (`api/requirements.txt`):
```
fastapi==0.115.0
uvicorn[standard]==0.30.6
redis==5.0.8
pydantic==2.8.2
```

### Worker (`worker/requirements.txt`):
```
redis==5.0.8
docker==7.1.0
```

### Web (`web/package.json`):
```json
{
  "dependencies": {
    "express": "^4.18.2",
    "socket.io": "^4.6.1",
    "redis": "^4.6.5",
    "http-proxy-middleware": "^2.0.6"
  }
}
```

### Judge (Dockerfile):
- Ubuntu 22.04
- GCC 11
- Python 3.10
- OpenJDK 11
- Node.js 18

---

## 🎯 Future Improvements

### Planned Features:
- [ ] Leaderboard system
- [ ] User accounts & authentication
- [ ] Problem difficulty auto-calculation
- [ ] Code replay (playback của coding session)
- [ ] Mobile responsive UI
- [ ] More languages (Go, Rust, C#)
- [ ] Custom test cases (user-defined)
- [ ] Problem tags filtering
- [ ] Rating system (ELO)

### Optimization Ideas:
- [ ] Cache compiled binaries (cho same code)
- [ ] Parallel test execution
- [ ] Worker horizontal scaling
- [ ] Redis persistence
- [ ] CDN cho static files

---

## 📖 Key Files Reference

| File | Lines | Purpose |
|------|-------|---------|
| `api/app.py` | 700 | API endpoints, validation, problem CRUD |
| `worker/worker.py` | 533 | Job processor, compile & run logic |
| `web/server.js` | 900 | Express server, Socket.IO, rooms |
| `judge/compile_run.sh` | 109 | Compile & run script cho 5 languages |
| `judge/run_with_metrics.py` | ~40 | Measure time/memory |
| `judge/compare_output.py` | ~50 | Token-based output comparison |
| `docker-compose.yml` | ~45 | Orchestration của 5 services |

---

## 🤝 Contributing Guidelines

Khi làm việc với dự án:

1. **Đọc flow** trước khi code (phần "Flow Hoạt Động")
2. **Test local** trước khi commit
3. **Log errors** rõ ràng (include submission_id, problem_id)
4. **Document** nếu thêm env var mới
5. **Backward compatibility** khi sửa API

---

## 📞 Contact & Support

Dự án được phát triển bởi: **Saudadeeee**  
Repository: https://github.com/Saudadeeee/Cowar

---

**Last Updated**: December 21, 2025  
**Version**: 1.0  
**Status**: Production Ready ✅
