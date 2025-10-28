import express from "express";
import { createServer } from "http";
import { Server } from "socket.io";
import path from "path";
import { fileURLToPath } from "url";
import { createClient } from "redis";
import { createProxyMiddleware } from 'http-proxy-middleware';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const app = express();
const httpServer = createServer(app);
const io = new Server(httpServer, {
  cors: {
    origin: "*",
    methods: ["GET", "POST"]
  }
});

const publicDir = path.join(__dirname, "public");

const redisClient = createClient({
  url: process.env.REDIS_URL || "redis://redis:6379"
});

redisClient.on("error", (err) => console.error("Redis Client Error", err));

await redisClient.connect();

app.use(express.json());

// Reverse proxy để chuyển /api/* sang backend API ở port 8000
const API_TARGET = process.env.API_URL || "http://api:8000";
app.use('/api', createProxyMiddleware({
  target: API_TARGET,
  changeOrigin: true,
  pathRewrite: {
    '^/api': '', // Xóa /api prefix khi gửi tới backend
  },
  timeout: 300000, // 5 phút timeout cho long-running submissions
  proxyTimeout: 300000,
  onProxyReq: (proxyReq, req, res) => {
    console.log(`[Proxy] ${req.method} ${req.path} -> ${API_TARGET}${req.path.replace('/api', '')}`);
  },
  onProxyRes: (proxyRes, req, res) => {
    console.log(`[Proxy Response] ${req.method} ${req.path} -> ${proxyRes.statusCode}`);
  },
  onError: (err, req, res) => {
    console.error('[Proxy Error]', err.message);
    res.status(500).json({ error: 'Proxy error', message: err.message });
  }
}));

app.use(express.static(publicDir));

app.get("/", (_req, res) => res.redirect("/mainmenu.html"));
app.get("/mainmenu.html", (_req, res) => res.sendFile(path.join(publicDir, "mainmenu.html")));
app.get("/workspace.html", (_req, res) => res.sendFile(path.join(publicDir, "workspace.html")));
app.get("/dashboard", (_req, res) => res.sendFile(path.join(publicDir, "dashboard.html")));
app.get("/roomhost.html", (_req, res) => res.sendFile(path.join(publicDir, "roomhost.html")));
app.get("/problem-add", (_req, res) => res.sendFile(path.join(publicDir, "problem-add.html")));
app.get("/problem-edit", (_req, res) => res.sendFile(path.join(publicDir, "problem-edit.html")));
app.get("/problem", (_req, res) => res.sendFile(path.join(publicDir, "workspace.html")));

app.post("/api/compare-submissions", async (req, res) => {
  try {
    const { submissionA, submissionB } = req.body;
    
    if (!submissionA || !submissionB) {
      return res.status(400).json({ error: "Both submission IDs required" });
    }
    
    const resultA = await redisClient.get(`run_result:${submissionA}`);
    const resultB = await redisClient.get(`run_result:${submissionB}`);
    
    if (!resultA || !resultB) {
      return res.status(404).json({ error: "One or both submissions not found" });
    }
    
    const perfA = JSON.parse(resultA).performance;
    const perfB = JSON.parse(resultB).performance;
    
    const comparison = comparePerformance(perfA, perfB);
    
    res.json({
      submissionA: {
        id: submissionA,
        performance: perfA
      },
      submissionB: {
        id: submissionB,
        performance: perfB
      },
      comparison
    });
  } catch (error) {
    console.error("Error comparing submissions:", error);
    res.status(500).json({ error: "Internal server error" });
  }
});

function comparePerformance(perfA, perfB) {
  const TOLERANCE = 0.10;
  
  const accuracyA = perfA.accuracy || 0;
  const accuracyB = perfB.accuracy || 0;
  
  if (accuracyA !== accuracyB) {
    return {
      winner: accuracyA > accuracyB ? "A" : "B",
      reason: "accuracy",
      details: {
        accuracyA: `${accuracyA.toFixed(2)}%`,
        accuracyB: `${accuracyB.toFixed(2)}%`,
        diff: `${Math.abs(accuracyA - accuracyB).toFixed(2)}%`
      }
    };
  }
  
  const timeA = perfA.median_elapsed_seconds || perfA.avg_elapsed_seconds || perfA.max_elapsed_seconds;
  const timeB = perfB.median_elapsed_seconds || perfB.avg_elapsed_seconds || perfB.max_elapsed_seconds;
  
  if (timeA && timeB) {
    const diff = Math.abs(timeA - timeB);
    const avg = (timeA + timeB) / 2;
    
    if (diff / avg >= TOLERANCE) {
      return {
        winner: timeA < timeB ? "A" : "B",
        reason: "time",
        details: {
          timeA: `${(timeA * 1000).toFixed(3)} ms`,
          timeB: `${(timeB * 1000).toFixed(3)} ms`,
          diff: `${(diff * 1000).toFixed(3)} ms`,
          tolerance: `${(TOLERANCE * 100)}%`
        }
      };
    }
  }
  
  const memA = perfA.median_memory_kb || perfA.avg_memory_kb || perfA.max_memory_kb;
  const memB = perfB.median_memory_kb || perfB.avg_memory_kb || perfB.max_memory_kb;
  
  if (memA && memB) {
    const diff = Math.abs(memA - memB);
    const avg = (memA + memB) / 2;
    
    if (diff / avg >= TOLERANCE) {
      return {
        winner: memA < memB ? "A" : "B",
        reason: "memory",
        details: {
          memoryA: `${(memA / 1024).toFixed(2)} MB`,
          memoryB: `${(memB / 1024).toFixed(2)} MB`,
          diff: `${(diff / 1024).toFixed(2)} MB`,
          tolerance: `${(TOLERANCE * 100)}%`
        }
      };
    }
  }
  
  return {
    winner: "TIE",
    reason: "all_metrics_equal_within_tolerance",
    details: {
      accuracy: `${accuracyA.toFixed(2)}%`,
      time: timeA ? `${(timeA * 1000).toFixed(3)} ms` : "N/A",
      memory: memA ? `${(memA / 1024).toFixed(2)} MB` : "N/A"
    }
  };
}

const rooms = new Map();

// Helper function to check if all players have submitted
function checkAllPlayersSubmitted(roomCode) {
  const roomState = rooms.get(roomCode);
  if (!roomState) return false;
  
  const players = roomState.players.filter(p => p.role === 'player' || p.role === 'host');
  const submissions = roomState.submissions || {};
  
  return players.every(p => submissions[p.socketId]);
}

async function compareAndAnnounceWinner(roomCode) {
  console.log('[DEBUG] compareAndAnnounceWinner:', roomCode);
  
  const roomState = rooms.get(roomCode);
  if (!roomState || !roomState.submissions) {
    console.log('[DEBUG] No room state or submissions');
    return;
  }
  
  const submissions = Object.values(roomState.submissions);
  console.log('[DEBUG] Found submissions:', submissions.length);
  
  if (submissions.length < 2) {
    console.log('[DEBUG] Need 2 submissions, got', submissions.length);
    return;
  }
  
  const [sub1, sub2] = submissions;
  
  try {
    console.log('[DEBUG] Fetching results:', sub1.submissionId, sub2.submissionId);
    const result1 = await redisClient.get(`run_result:${sub1.submissionId}`);
    const result2 = await redisClient.get(`run_result:${sub2.submissionId}`);
    
    if (!result1 || !result2) {
      console.log('Waiting for results:', !!result1, !!result2);
      return;
    }
    
    console.log('[DEBUG] Comparing results');
    const perf1 = JSON.parse(result1).performance;
    const perf2 = JSON.parse(result2).performance;
    
    const comparison = comparePerformance(perf1, perf2);
    
    const matchResult = {
      players: {
        [sub1.username]: {
          submissionId: sub1.submissionId,
          performance: perf1
        },
        [sub2.username]: {
          submissionId: sub2.submissionId,
          performance: perf2
        }
      },
      winner: comparison.winner === 'A' ? sub1.username : comparison.winner === 'B' ? sub2.username : 'TIE',
      comparison
    };
    
    console.log('Announcing winner:', matchResult.winner);
    io.to(roomCode).emit('match-result', matchResult);
    
    console.log('Match result emitted');
    
    roomState.submissions = {};
    
  } catch (error) {
    console.error('Error comparing submissions:', error);
  }
}

io.on("connection", (socket) => {
  console.log("User connected:", socket.id);

  socket.on("join-room", async ({ roomCode, username, role }) => {
    try {
      socket.join(roomCode);
      
      let roomState = rooms.get(roomCode);
      if (!roomState) {
        roomState = {
          roomCode,
          players: [],
          spectators: [],
          settings: {
            spectatorEnabled: false,
            difficulty: "fast",
            language: "cpp",
            timeLimit: "none",
            rounds: 3
          },
          playerCodes: {},
          submissions: {}
        };
        rooms.set(roomCode, roomState);
      }

      const user = { socketId: socket.id, username, role, ready: role === 'host' ? true : false };
      
      if (role === "player" || role === "host") {
        if (roomState.players.length < 2) {
          roomState.players.push(user);
          roomState.playerCodes[socket.id] = "";
        } else {
          socket.emit("room-full");
          return;
        }
      } else if (role === "spectator") {
        roomState.spectators.push(user);
      }

      socket.emit("room-joined", {
        roomCode,
        role,
        roomState: {
          players: roomState.players.map(p => ({ 
            username: p.username, 
            socketId: p.socketId, 
            role: p.role,
            ready: p.ready 
          })),
          spectators: roomState.spectators.map(s => ({ username: s.username })),
          settings: roomState.settings
        }
      });

      io.to(roomCode).emit("player-joined", { 
        username, 
        role,
        players: roomState.players.map(p => ({ 
          username: p.username, 
          socketId: p.socketId, 
          role: p.role,
          ready: p.ready 
        })),
        settings: roomState.settings
      });

      socket.emit("room-state", {
        players: roomState.players.map(p => ({ 
          username: p.username, 
          socketId: p.socketId, 
          role: p.role,
          ready: p.ready 
        })),
        settings: roomState.settings
      });

      console.log(`${username} joined room ${roomCode} as ${role}`);
    } catch (error) {
      console.error("Error joining room:", error);
      socket.emit("error", { message: "Failed to join room" });
    }
  });

  socket.on("update-settings", ({ roomCode, settings }) => {
    const roomState = rooms.get(roomCode);
    if (roomState && roomState.players[0]?.socketId === socket.id) {
      roomState.settings = { ...roomState.settings, ...settings };
      io.to(roomCode).emit("settings-updated", { 
        settings: roomState.settings 
      });
      console.log(`Settings updated for room ${roomCode}:`, settings);
    }
  });

  socket.on("player-ready", ({ roomCode, ready }) => {
    const roomState = rooms.get(roomCode);
    if (roomState) {
      const player = roomState.players.find(p => p.socketId === socket.id);
      if (player) {
        player.ready = ready;
        
        io.to(roomCode).emit("player-ready-update", {
          players: roomState.players.map(p => ({ 
            username: p.username, 
            socketId: p.socketId, 
            role: p.role,
            ready: p.ready 
          }))
        });
        
        console.log(`Player ${player.username} in room ${roomCode} ready status: ${ready}`);
      }
    }
  });

  socket.on("code-change", ({ roomCode, code, language }) => {
    const roomState = rooms.get(roomCode);
    if (roomState) {
      roomState.playerCodes[socket.id] = code;
      
      socket.to(roomCode).emit("opponent-code-update", {
        socketId: socket.id,
        code,
        language,
        username: roomState.players.find(p => p.socketId === socket.id)?.username || "Unknown"
      });
    }
  });

  socket.on("start-match", ({ roomCode }) => {
    const roomState = rooms.get(roomCode);
    if (roomState && roomState.players[0]?.socketId === socket.id) {
      io.to(roomCode).emit("match-started", {
        settings: roomState.settings
      });
      console.log(`Match started in room ${roomCode}`);
    }
  });

  socket.on("submit-code", ({ roomCode, submissionId }) => {
    console.log('[DEBUG] submit-code:', roomCode, submissionId, socket.id);
    
    const roomState = rooms.get(roomCode);
    if (!roomState) {
      console.log('[ERROR] Room not found:', roomCode);
      return;
    }
    
    const player = roomState.players.find(p => p.socketId === socket.id);
    if (!player) {
      console.log('[ERROR] Player not found:', socket.id);
      console.log('[DEBUG] Players:', roomState.players);
      return;
    }
    
    if (!roomState.submissions) {
      roomState.submissions = {};
    }
    
    roomState.submissions[socket.id] = {
      submissionId,
      username: player.username,
      timestamp: Date.now()
    };
    
    console.log('Player submitted:', player.username, submissionId);
    console.log('Total submissions:', Object.keys(roomState.submissions).length);
    
    socket.to(roomCode).emit("opponent-submitted", {
      socketId: socket.id,
      username: player.username,
      submissionId
    });
    
    if (checkAllPlayersSubmitted(roomCode)) {
      console.log('All players submitted. Waiting for results');
      
      let attempts = 0;
      const maxAttempts = 15;
      
      const pollInterval = setInterval(async () => {
        attempts++;
        
        await compareAndAnnounceWinner(roomCode);
        
        const currentState = rooms.get(roomCode);
        if (!currentState || Object.keys(currentState.submissions || {}).length === 0) {
          clearInterval(pollInterval);
          return;
        }
        
        if (attempts >= maxAttempts) {
          clearInterval(pollInterval);
          io.to(roomCode).emit('match-timeout', {
            message: 'Results taking too long. Please check individual submissions.'
          });
        }
      }, 2000);
    }
  });

  socket.on("disconnect", () => {
    console.log("User disconnected:", socket.id);
    
    for (const [roomCode, roomState] of rooms.entries()) {
      const playerIndex = roomState.players.findIndex(p => p.socketId === socket.id);
      const spectatorIndex = roomState.spectators.findIndex(s => s.socketId === socket.id);
      
      if (playerIndex !== -1) {
        const player = roomState.players[playerIndex];
        roomState.players.splice(playerIndex, 1);
        delete roomState.playerCodes[socket.id];
        
        // Broadcast updated player list
        io.to(roomCode).emit("player-left", { 
          username: player.username, 
          role: player.role,
          players: roomState.players.map(p => ({ 
            username: p.username, 
            socketId: p.socketId, 
            role: p.role,
            ready: p.ready 
          }))
        });
      }
      
      if (spectatorIndex !== -1) {
        const spectator = roomState.spectators[spectatorIndex];
        roomState.spectators.splice(spectatorIndex, 1);
        io.to(roomCode).emit("user-left", { username: spectator.username, role: "spectator" });
      }

      if (roomState.players.length === 0 && roomState.spectators.length === 0) {
        rooms.delete(roomCode);
        console.log(`Room ${roomCode} deleted (empty)`);
      }
    }
  });
});

httpServer.listen(5173, '0.0.0.0', () => {
  console.log("Web server with Socket.IO at http://0.0.0.0:5173");
  console.log("Proxying /api/* to", process.env.API_URL || "http://api:8000");
});
