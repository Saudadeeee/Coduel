# Coduel 🏆

> **A competitive programming platform inspired by Clash of Code, but with enhanced features for real-time code battles**

Coduel is a multiplayer online judge system that allows programmers to compete head-to-head by solving algorithmic challenges. Built with modern web technologies and Docker-based isolation, it provides a secure, scalable, and engaging platform for coding competitions.

## ✨ Features

### 🎮 Competitive Programming
- **Real-time Multiplayer Battles**: Compete against opponents in private rooms
- **Multiple Rounds**: Configurable best-of-N format (default: 3 rounds)
- **Performance-Based Judging**: Winner determined by accuracy → execution time → memory usage
- **Anti-Cheat System**: Real-time code spectating prevents cheating

### 💻 Language Support
- **C** (C17 standard)
- **C++** (C++20 standard)
- **Python 3**
- **Java**
- **JavaScript** (Node.js)

### 🔒 Secure Execution
- **Docker Isolation**: Each submission runs in isolated containers
- **Resource Limits**: CPU and memory constraints prevent abuse
- **Timeout Protection**: Configurable time limits per test case
- **Multi-Run Testing**: Each test runs multiple times for accurate performance metrics

### 📊 Real-time Features
- **Live Code Spectating**: Watch opponent's code as they type
- **Socket.IO Integration**: Instant updates for all room participants
- **Ready Check System**: Both players must be ready before match starts
- **Match Results**: Detailed performance comparison after each round

### 🛠️ Problem Management
- **CRUD Operations**: Create, read, update, and delete problems
- **Markdown Support**: Rich problem statements with formatting
- **Test Case Visibility**: Public samples + hidden test cases
- **Difficulty Levels**: Easy, Medium, Hard, Fast
- **Tagging System**: Organize problems by topics

## 🏗️ Architecture

### System Overview
```
┌──────────────────────────────────────────────────────────────┐
│                        User Browser                          │
│  (HTML/CSS/JS + Socket.IO Client + Monaco Editor)          │
└────────────┬─────────────────────────────────┬──────────────┘
             │                                 │
             │ HTTP/REST                       │ WebSocket
             ▼                                 ▼
┌─────────────────────┐           ┌──────────────────────────┐
│    Web Server       │           │   Socket.IO Server      │
│   (Express.js)      │◄─────────►│   (Real-time Sync)     │
│   Port: 5173        │           │   - Room Management     │
└──────────┬──────────┘           │   - Code Broadcasting   │
           │                      │   - Match Coordination  │
           │                      └──────────┬───────────────┘
           │                                 │
           │ HTTP                            │
           ▼                                 │
┌─────────────────────┐                     │
│    API Server       │                     │
│    (FastAPI)        │                     │
│    Port: 8000       │                     │
│  - Submit Code      │                     │
│  - Problem CRUD     │                     │
│  - Judge Queue      │                     │
└──────────┬──────────┘                     │
           │                                 │
           │                                 │
           └────────────┬────────────────────┘
                        │
                        ▼
              ┌──────────────────┐
              │      Redis       │
              │    Port: 6379    │
              │  - Message Queue │
              │  - Room State    │
              │  - Results Cache │
              └─────────┬────────┘
                        │
                        │ Job Queue
                        ▼
              ┌──────────────────┐
              │      Worker      │
              │  (Python Daemon) │
              │  - Compile Code  │
              │  - Run Tests     │
              └─────────┬────────┘
                        │
                        │ Docker API
                        ▼
              ┌──────────────────┐
              │   Judge Engine   │
              │ (Docker-in-Docker)│
              │  - Isolated Exec │
              │  - Resource Limit│
              │  - Metrics       │
              └──────────────────┘
```

### Component Details

#### 🌐 Web Server (`web/`)
- **Technology**: Node.js + Express + Socket.IO
- **Port**: 5173
- **Responsibilities**:
  - Serve static HTML/CSS/JS files
  - WebSocket connections for real-time features
  - Room state management
  - Code synchronization between players
  - Match result broadcasting

#### 🔌 API Server (`api/`)
- **Technology**: FastAPI (Python)
- **Port**: 8000
- **Endpoints**:
  - `GET /problems` - List all problems
  - `GET /problem/{id}` - Problem details with test cases
  - `POST /problem-add` - Create new problem
  - `POST /problem-edit` - Update/delete problem
  - `POST /problem/submit` - Submit code for judging
  - `GET /problem/submission/{id}` - Get submission status
- **Features**:
  - Pydantic validation
  - Redis queue integration
  - Problem metadata management

#### ⚙️ Worker (`worker/`)
- **Technology**: Python + Docker SDK
- **Responsibilities**:
  1. **Compilation**: Compile source code with appropriate compiler
  2. **Execution**: Run compiled binary against test cases
  3. **Metrics Collection**: Measure time, memory, accuracy
  4. **Multi-Run Testing**: Execute each test `RUNS_PER_TEST` times
  5. **Result Storage**: Save results to Redis
- **Configuration**:
  - `CPU_LIMIT`: Default = half of system CPU cores
  - `MEM_LIMIT`: Default = half of system RAM
  - `RUNS_PER_TEST`: Default = 3 (for median calculation)
  - `PERFORMANCE_TOLERANCE`: Default = 0.10 (10%)

#### 🐳 Judge Engine (`judge/`)
- **Base Image**: Ubuntu-based with multiple compilers
- **Installed Tools**:
  - GCC (C/C++)
  - Python 3
  - OpenJDK (Java)
  - Node.js (JavaScript)
  - GNU Time (resource monitoring)
- **Security**: Network disabled, filesystem read-only

#### 📦 Redis
- **Version**: 7 (Alpine)
- **Usage**:
  - Job queue (`queue:compile`)
  - Submission metadata (`sub:{id}`)
  - Source code storage (`code:{id}`)
  - Execution results (`run_result:{id}`)
  - Compilation logs (`compile_log:{id}`)
  - Room state (in-memory)

## 🚀 Getting Started

### Prerequisites
- **Docker** (20.10+)
- **Docker Compose** (2.0+)
- **Git**
- **Port Availability**: 5173 (Web), 8000 (API), 6379 (Redis)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/Saudadeeee/Cowar.git
cd Cowar/Coduel
```

2. **Configure environment** (optional)
```bash
# Create .env.judge for worker configuration
cat > .env.judge << EOF
RUNS_PER_TEST=3
PERFORMANCE_TOLERANCE=0.10
CPU_LIMIT=2.0
MEM_LIMIT=1g
EOF
```

3. **Build and start all services**
```bash
docker-compose up --build -d
```

4. **Verify services are running**
```bash
docker ps
# Should show: oj_web, oj_api, oj_worker, oj_redis
```

5. **Access the application**
- **Web UI**: http://localhost:5173
- **API Docs**: http://localhost:8000/docs

### First Time Setup

1. **Add a Problem**:
   - Navigate to http://localhost:5173/problem-add
   - Fill in problem details:
     - Title: "Sum Two Numbers"
     - Difficulty: Easy
     - Description: "Calculate a + b"
     - Sample Input: `1 2`
     - Sample Output: `3`
     - Add test cases with visibility (public/hidden)
   - Click "Create Problem"

2. **View Dashboard**:
   - Go to http://localhost:5173/dashboard
   - See problem statistics and distribution

3. **Test Solo**:
   - Click "Training Mode" from main menu
   - Select a problem
   - Write code in the Monaco editor
   - Click "Submit & Run"

4. **Host Multiplayer Match**:
   - Click "Host Room" from main menu
   - Configure settings:
     - Enable/disable code spectator
     - Select difficulty
     - Choose default language
     - Set number of rounds
   - Share room code with opponent

5. **Join a Match**:
   - Click "Join Room" from main menu
   - Enter room code
   - Wait for host to start match

## 🎮 How to Play

### Solo Training Mode
1. Select "Training Mode" from main menu
2. Choose a problem from the list
3. Read problem statement carefully
4. Write solution in preferred language
5. Test with sample inputs
6. Submit when ready
7. View detailed results (verdict, time, memory)

### Multiplayer Battle Mode

#### As Host:
1. **Create Room**:
   - Click "Host Room"
   - Configure match settings
   - Copy generated room code

2. **Wait for Opponent**:
   - Share room code with friend
   - Wait for them to join
   - Both players mark "Ready"

3. **Start Match**:
   - Click "Start Match" button
   - Problem appears for both players
   - Code editor unlocks

4. **Compete**:
   - Write solution
   - Submit when ready
   - Wait for opponent to submit
   - View performance comparison

5. **Multi-Round**:
   - Winner of round gets 1 point
   - Next problem loads automatically
   - First to win majority wins match

#### As Player:
1. **Join Room**:
   - Click "Join Room"
   - Enter room code from host
   - Click "Ready" when prepared

2. **Follow host's lead**:
   - Wait for match to start
   - Solve problems as they appear
   - Submit before opponent to gain advantage

### Code Spectating (Anti-Cheat)
If enabled by host:
- Click eye icon (👁️) in workspace
- Watch opponent's code in real-time
- See when they submit
- Promotes fair play and transparency

## 📚 API Documentation

### Problem Management

#### List Problems
```http
GET /problems
```
**Response**:
```json
{
  "problems": [
    {
      "problem_id": "001-sum-two",
      "title": "Sum Two Numbers",
      "difficulty": "easy",
      "number": 1,
      "time_limit_ms": 2000,
      "memory_limit_kb": 262144,
      "tags": ["math", "implementation"],
      "tests": 2
    }
  ]
}
```

#### Get Problem Details
```http
GET /problem/{problem_id}
```
**Response**: Includes statement, samples, tests, metadata

#### Create Problem
```http
POST /problem-add
Content-Type: application/json

{
  "title": "Sum Two Numbers",
  "difficulty": "easy",
  "description": "Calculate a + b",
  "sample_input": "1 2",
  "sample_output": "3",
  "tests": [
    {
      "input": "1 2",
      "output": "3",
      "visibility": "public"
    },
    {
      "input": "100 200",
      "output": "300",
      "visibility": "hidden"
    }
  ],
  "time_limit_ms": 2000,
  "memory_limit_kb": 262144,
  "tags": ["math"]
}
```

#### Update Problem
```http
POST /problem-edit
Content-Type: application/json

{
  "problem_id": "001-sum-two",
  "title": "Updated Title",
  "difficulty": "medium",
  // ... other fields
}
```

#### Delete Problem
```http
POST /problem-edit
Content-Type: application/json

{
  "problem_id": "001-sum-two",
  "delete": true
}
```

### Submission

#### Submit Code
```http
POST /problem/submit
Content-Type: application/json

{
  "problem_id": "001-sum-two",
  "language": "cpp",
  "code": "#include <iostream>\nusing namespace std;\nint main() { int a,b; cin>>a>>b; cout<<a+b; }",
  "std": "c++20"
}
```
**Response**:
```json
{
  "submission_id": "uuid-here"
}
```

#### Check Submission Status
```http
GET /problem/submission/{submission_id}
```
**Response**:
```json
{
  "meta": {
    "status": "completed",
    "problem_id": "001-sum-two",
    "language": "cpp",
    "created_at": "1730000000"
  },
  "compile_log": "Success",
  "run_result": {
    "verdict": "AC",
    "tests_passed": 2,
    "tests_total": 2,
    "performance": {
      "accuracy": 100.0,
      "median_elapsed_seconds": 0.005,
      "median_memory_kb": 2048
    },
    "test_details": [...]
  }
}
```

## 🔧 Configuration

### Environment Variables

#### Worker Configuration (`.env.judge`)
```bash
# Number of times to run each test (for median calculation)
RUNS_PER_TEST=3

# Performance tolerance for time comparison (10%)
PERFORMANCE_TOLERANCE=0.10

# CPU limit per container (cores)
CPU_LIMIT=2.0

# Memory limit per container
MEM_LIMIT=1g

# Timeout for compilation (seconds)
COMPILE_TIMEOUT=60

# Timeout for execution (seconds)
RUN_TIMEOUT=60
```

#### Docker Compose Override
```yaml
# docker-compose.override.yml
version: "3.9"
services:
  web:
    ports:
      - "3000:5173"  # Change web port
  
  api:
    environment:
      - DEFAULT_TIME_LIMIT_MS=5000  # 5 second default
      - DEFAULT_MEMORY_LIMIT_KB=524288  # 512MB default
```

### Performance Comparison Algorithm

The system uses a 3-tier comparison:

1. **Accuracy** (Priority 1):
   - Compare `tests_passed / tests_total`
   - Higher accuracy wins immediately

2. **Execution Time** (Priority 2):
   - Uses median time from multiple runs
   - Tolerance: ±10% (configurable)
   - If within tolerance → tie, move to memory

3. **Memory Usage** (Priority 3):
   - Uses median memory from multiple runs
   - Tolerance: ±10% (configurable)
   - If within tolerance → tie

**Example**:
```
Player A: 100% accuracy, 0.005s, 2048KB
Player B: 100% accuracy, 0.006s, 2048KB

Time difference: 20% → Player A wins
```

## 🛠️ Project Structure

```
Coduel/
├── api/                          # FastAPI backend
│   ├── app.py                   # Main API server (712 lines)
│   ├── Dockerfile               # API container config
│   └── requirements.txt         # Python dependencies
├── judge/                        # Code execution engine
│   ├── compile_run.sh           # Compilation/execution script
│   ├── Dockerfile               # Judge container with compilers
│   └── run_with_metrics.py     # Metrics collection
├── problems/                     # Problem repository
│   ├── 001-sum-two/
│   │   ├── meta.json            # Problem metadata
│   │   ├── statement.md         # Problem description
│   │   ├── sample_input.txt     # Public sample
│   │   ├── sample_output.txt
│   │   ├── input1.txt           # Test case 1
│   │   ├── output1.txt
│   │   ├── input2.txt           # Test case 2
│   │   └── output2.txt
│   └── 002-test/
│       └── ...
├── web/                          # Frontend application
│   ├── server.js                # Express + Socket.IO (468 lines)
│   ├── socket-client.js         # Socket.IO client wrapper
│   ├── Dockerfile               # Web container config
│   ├── package.json             # Node.js dependencies
│   └── public/
│       ├── mainmenu.html        # Main navigation
│       ├── dashboard.html       # Statistics dashboard
│       ├── workspace.html       # Code editor (2061 lines)
│       ├── roomhost.html        # Room creation
│       ├── problem-add.html     # Problem creation form
│       └── problem-edit.html    # Problem edit form
├── worker/                       # Background job processor
│   ├── worker.py                # Job handler (489 lines)
│   ├── Dockerfile               # Worker container config
│   └── requirements.txt         # Python dependencies
├── worker_tmp/                   # Temporary execution directory
├── docker-compose.yml            # Service orchestration
└── .env.judge                    # Worker configuration
```

## 🧪 Testing

### Manual Testing

#### Test Services
```bash
# Start all services
docker-compose up -d

# Check container status
docker ps

# Test API health
curl http://localhost:8000/problems

# Test web server
curl http://localhost:5173

# Check Redis
docker exec oj_redis redis-cli ping
```

#### Test Problem Submission
```bash
# Create test problem
curl -X POST http://localhost:8000/problem-add \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Test",
    "difficulty": "easy",
    "sample_input": "1 2",
    "sample_output": "3",
    "tests": [{"input":"1 2","output":"3","visibility":"public"}]
  }'

# Submit solution
curl -X POST http://localhost:8000/problem/submit \
  -H "Content-Type: application/json" \
  -d '{
    "problem_id": "001-test",
    "language": "cpp",
    "code": "#include <iostream>\nusing namespace std;\nint main() { int a,b; cin>>a>>b; cout<<a+b; }"
  }'

# Check result (use submission_id from above)
curl http://localhost:8000/problem/submission/{submission_id}
```

#### Test Multiplayer
1. **Terminal 1**: Start services
```bash
docker-compose up
```

2. **Browser 1**: Host room
   - Open http://localhost:5173
   - Click "Host Room"
   - Enable spectator mode
   - Copy room code

3. **Browser 2**: Join room
   - Open http://localhost:5173 (incognito)
   - Click "Join Room"
   - Paste room code
   - Both click "Ready"

4. **Start Match**:
   - Host clicks "Start Match"
   - Both solve problem
   - Submit code
   - View winner modal

### Test Code Spectating
1. Enable spectator in room settings
2. Join room with 2 browsers
3. Type code in Browser 1
4. Click eye icon in Browser 2
5. Verify code appears in real-time

## 🐛 Troubleshooting

### Common Issues

#### Services Won't Start
```bash
# Clean up containers
docker-compose down -v

# Rebuild from scratch
docker-compose up --build --force-recreate
```

#### Port Already in Use
```bash
# Find process using port 5173
lsof -i :5173
kill -9 <PID>

# Or change port in docker-compose.yml
# ports: ["3000:5173"]
```

#### Redis Connection Failed
```bash
# Check Redis logs
docker logs oj_redis

# Restart Redis
docker-compose restart redis

# Test connection
docker exec oj_redis redis-cli ping
```

#### Worker Not Processing Jobs
```bash
# Check worker logs
docker logs oj_worker -f

# Verify Docker socket
docker exec oj_worker ls -la /var/run/docker.sock

# Check queue
docker exec oj_redis redis-cli LLEN queue:compile
```

#### Code Not Syncing in Multiplayer
```bash
# Check Socket.IO connection
# Browser DevTools → Network → WS → Should see connection

# Check web server logs
docker logs oj_web -f

# Verify Redis pub/sub
docker exec oj_redis redis-cli MONITOR
```

#### Judge Execution Timeout
```bash
# Increase timeout in .env.judge
RUN_TIMEOUT=120

# Restart worker
docker-compose restart worker
```

#### Wrong Winner Declared
```bash
# Check performance tolerance
# In .env.judge:
PERFORMANCE_TOLERANCE=0.10  # 10%

# View detailed comparison logs
docker logs oj_web | grep "comparison"
```

### Debug Mode

Enable verbose logging:
```bash
# In docker-compose.yml
services:
  worker:
    environment:
      - LOG_LEVEL=DEBUG
```

Check all logs:
```bash
docker-compose logs -f
```

## 🎯 Roadmap

### Phase 1: Core Features ✅
- [x] Docker-based judge system
- [x] Multi-language support (C/C++/Python/Java/JS)
- [x] Problem CRUD operations
- [x] Solo training mode
- [x] Multiplayer room system
- [x] Real-time code spectating
- [x] Performance-based judging
- [x] Multi-round matches
- [x] Winner modal with statistics

### Phase 2: Enhanced Features 🔄
- [ ] User authentication & profiles
- [ ] Persistent leaderboard
- [ ] Problem difficulty rating
- [ ] Submission history
- [ ] Code templates per language
- [ ] Syntax highlighting in spectator
- [ ] Match replay system

### Phase 3: Advanced Features 📋
- [ ] Tournament bracket system
- [ ] Team battles (2v2)
- [ ] Spectator-only role
- [ ] Live streaming integration
- [ ] Code diff viewer
- [ ] Anti-plagiarism detection
- [ ] Rating system (ELO)
- [ ] Achievement badges

### Phase 4: Scale & Polish 🚀
- [ ] Kubernetes deployment
- [ ] CDN for static assets
- [ ] Database persistence (PostgreSQL)
- [ ] Microservices architecture
- [ ] Mobile app (React Native)
- [ ] i18n (multiple languages)
- [ ] Dark/light theme toggle
- [ ] Accessibility improvements

## 🤝 Contributing

We welcome contributions! Here's how:

1. **Fork the repository**
```bash
git clone https://github.com/YOUR_USERNAME/Cowar.git
cd Cowar
git remote add upstream https://github.com/Saudadeeee/Cowar.git
```

2. **Create a feature branch**
```bash
git checkout -b feature/amazing-feature
```

3. **Make your changes**
   - Follow existing code style
   - Add comments for complex logic
   - Test thoroughly

4. **Commit your changes**
```bash
git add .
git commit -m "Add amazing feature"
```

5. **Push to your fork**
```bash
git push origin feature/amazing-feature
```

6. **Open a Pull Request**
   - Describe your changes
   - Link related issues
   - Add screenshots if UI changes

### Development Guidelines

- **Code Style**: Follow ESLint/Prettier for JS, Black for Python
- **Commits**: Use conventional commits (feat/fix/docs/style/refactor)
- **Testing**: Test manually before submitting PR
- **Documentation**: Update README if adding features

## 📄 License

This project is licensed under the MIT License - see below for details:

```
MIT License

Copyright (c) 2025 Saudadeeee

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## 🙏 Acknowledgments

- **Inspiration**: [CodinGame's Clash of Code](https://www.codingame.com/multiplayer/clashofcode)
- **Technologies**:
  - [Docker](https://www.docker.com/) - Containerization
  - [FastAPI](https://fastapi.tiangolo.com/) - Python web framework
  - [Socket.IO](https://socket.io/) - Real-time communication
  - [Express.js](https://expressjs.com/) - Node.js web framework
  - [Redis](https://redis.io/) - In-memory data store
  - [Monaco Editor](https://microsoft.github.io/monaco-editor/) - Code editor
- **Community**: Thanks to all beta testers and contributors

## 📞 Support

Need help? Here are your options:

1. **Documentation**: Check the `/Coduel` directory for detailed guides
2. **Issues**: [Open a GitHub issue](https://github.com/Saudadeeee/Cowar/issues)
3. **Discussions**: [Join GitHub Discussions](https://github.com/Saudadeeee/Cowar/discussions)
4. **Logs**: Run `docker-compose logs -f` for debugging

### Quick Links
- [Installation Guide](#installation)
- [API Documentation](#api-documentation)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)

---

<div align="center">

**Built with ❤️ by competitive programmers, for competitive programmers**

[⭐ Star this repo](https://github.com/Saudadeeee/Cowar) | [🐛 Report Bug](https://github.com/Saudadeeee/Cowar/issues) | [✨ Request Feature](https://github.com/Saudadeeee/Cowar/issues)

</div>
