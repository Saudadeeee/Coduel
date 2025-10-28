# Coduel
Clash of code but harder

## 🚀 Features
- **Competitive Coding**: Solve algorithmic problems in real-time
- **Multiple Languages**: C, C++, Java, Python, and more
- **Real-time Code Spectating**: Watch your opponent's code live (anti-cheat)
- **Docker-based Judge**: Secure code execution in isolated containers
- **Problem Management**: Create, edit, and organize coding challenges
- **Multiplayer Rooms**: Host private matches with custom settings

## 🏗️ Architecture
```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Web UI    │────▶│  API Server │────▶│   Worker    │
│  (Node.js)  │     │  (FastAPI)  │     │  (Docker)   │
└──────┬──────┘     └──────┬──────┘     └──────┬──────┘
       │                   │                    │
       │                   │                    │
       └───────────────────┴────────────────────┘
                           │
                    ┌──────▼──────┐
                    │    Redis    │
                    │   (Cache)   │
                    └─────────────┘
```

### Services
- **Web** (Port 5173): Frontend UI + Socket.IO server for real-time features
- **API** (Port 8000): FastAPI backend for problem submission and judging
- **Worker**: Background job processor for code compilation and execution
- **Redis** (Port 6379): Message queue and real-time state management
- **Judge**: Docker-in-Docker container for secure code execution

## 📦 Quick Start

### Prerequisites
- Docker
- Docker Compose

### Installation
```bash
# Clone the repository
git clone <your-repo-url>
cd Cowar/Coduel

# Start all services
docker-compose up --build

# Access the application
# Web UI: http://localhost:5173
# API: http://localhost:8000
```

### First Time Setup
1. Open `http://localhost:5173/mainmenu.html`
2. Navigate to "Add Problem" to create your first challenge
3. Go to "Dashboard" to see problem statistics
4. Choose "Training Mode" for solo practice
5. Choose "Host Room" for multiplayer matches

## 🎮 Real-time Code Spectating

### How It Works
Players can watch each other's code in real-time during competitive matches. This anti-cheat feature creates transparency and fair play.

### Usage
1. **Host a Room**:
   - Click "Host Room" from main menu
   - Enable "Code Spectator (real-time code viewing)"
   - Share the generated room code

2. **Join a Room**:
   - Click "Join Room" from main menu
   - Enter the room code
   - Start coding when match begins

3. **Watch Opponent**:
   - Click the eye icon (👁️) button in workspace (top-right)
   - See opponent's code update in real-time
   - Get notified when opponent submits

### Documentation
- **Quick Start**: See `Coduel/QUICK_START.md`
- **Technical Details**: See `Coduel/SPECTATOR_FEATURE.md`
- **Integration Summary**: See `Coduel/INTEGRATION_SUMMARY.md`

## 🛠️ Project Structure
```
Coduel/
├── api/                    # FastAPI backend
│   ├── app.py             # Main API server
│   ├── Dockerfile
│   └── requirements.txt
├── judge/                  # Code execution engine
│   ├── compile_run.sh     # Compilation and execution script
│   ├── Dockerfile
│   └── run_with_metrics.py
├── problems/               # Problem definitions
│   └── [problem-id]/
│       ├── meta.json      # Problem metadata
│       ├── statement.md   # Problem description
│       ├── input*.txt     # Test inputs
│       └── output*.txt    # Expected outputs
├── web/                    # Frontend application
│   ├── server.js          # Express + Socket.IO server
│   ├── socket-client.js   # Socket.IO client utility
│   ├── Dockerfile
│   ├── package.json
│   └── public/
│       ├── mainmenu.html
│       ├── dashboard.html
│       ├── workspace.html
│       ├── roomhost.html
│       ├── problem-add.html
│       └── problem-edit.html
├── worker/                 # Background job processor
│   ├── worker.py
│   ├── Dockerfile
│   └── requirements.txt
└── docker-compose.yml      # Service orchestration
```

## 🔧 Configuration

### Docker Compose Services
- `web`: Frontend server with Socket.IO
- `api`: Backend API server
- `worker`: Job processor
- `redis`: Cache and message queue

### Environment Variables
Set in `docker-compose.yml`:
- `REDIS_HOST`: Redis hostname (default: redis)
- `REDIS_PORT`: Redis port (default: 6379)
- `JOB_TMP_ROOT`: Temporary directory for job execution
- `PROBLEMS_ROOT`: Problems directory path

## 🧪 Testing

### Manual Testing
```bash
# Terminal 1: Start services
docker-compose up --build

# Terminal 2: Check service health
docker ps
curl http://localhost:8000/health
curl http://localhost:5173

# Browser: Open two windows
# Window 1: Host room at http://localhost:5173/roomhost.html
# Window 2: Join room with code from Window 1
```

### Testing Real-time Features
1. Host creates room with spectator enabled
2. Player joins with room code
3. Both navigate to workspace
4. Type code in one window → appears in other window's modal
5. Submit code → opponent gets notification

## 🐛 Troubleshooting

### Common Issues

**Services not starting**
```bash
docker-compose down
docker-compose up --build
```

**Redis connection failed**
```bash
docker logs oj_redis
docker-compose restart redis
```

**Code not syncing**
```bash
# Check Socket.IO connection in browser DevTools
# Network → WS → Verify connection established

# Check server logs
docker logs oj_web
```

**Judge execution errors**
```bash
# Check worker logs
docker logs oj_worker

# Verify Docker socket mounted
docker exec oj_worker ls -la /var/run/docker.sock
```

## 📚 API Endpoints

### Problems API
- `GET /problems` - List all problems
- `GET /problem/{id}` - Get problem details
- `POST /problem-add` - Create new problem
- `POST /problem-edit` - Update existing problem

### Submission API
- `POST /submit` - Submit code for judging
- `GET /submission/{id}` - Get submission status

## 🎯 Roadmap

### Completed ✅
- [x] Basic judge system with Docker isolation
- [x] Problem CRUD operations
- [x] Dashboard with statistics
- [x] Real-time code spectating
- [x] Multiplayer room system
- [x] Socket.IO integration
- [x] Redis state management

### In Progress 🔄
- [ ] User authentication
- [ ] Username display in rooms
- [ ] Syntax highlighting in spectator modal

### Planned 📋
- [ ] Tournament bracket system
- [ ] Leaderboard and ranking
- [ ] Replay functionality
- [ ] Code diff viewer
- [ ] Multiple simultaneous matches
- [ ] Spectator-only role
- [ ] Mobile responsive design

## 🤝 Contributing
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License
[Your License Here]

## 🙏 Acknowledgments
- Inspired by Clash of Code (CodinGame)
- Built with Docker, Node.js, Python, and Redis
- Socket.IO for real-time communication

## 📞 Support
For issues or questions:
1. Check documentation in `Coduel/` directory
2. Review Docker logs: `docker-compose logs`
3. Open an issue on GitHub

---

**Built with ❤️ for competitive programmers**
