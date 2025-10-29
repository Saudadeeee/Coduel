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

const jsonParser = express.json();

app.post("/api/compare-submissions", jsonParser, async (req, res) => {
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

    if (!req.body || !Object.keys(req.body).length) {
      return;
    }

    const bodyData = JSON.stringify(req.body);
    console.log(`[Proxy] forwarding body (${bodyData.length} bytes)`);
    proxyReq.setHeader('Content-Type', 'application/json');
    proxyReq.setHeader('Content-Length', Buffer.byteLength(bodyData));
    proxyReq.write(bodyData);
    proxyReq.end();
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

const FINAL_STATUSES = new Set([
  "done",
  "failed",
  "compile_error",
  "compile_timeout",
  "run_timeout",
  "error",
  "problem_not_found"
]);

const coerceNumber = (value) => {
  if (value === undefined || value === null) return null;
  const num = Number(value);
  return Number.isFinite(num) ? num : null;
};

const formatPercent = (value) => {
  const num = coerceNumber(value);
  return num === null ? "N/A" : `${num.toFixed(2)}%`;
};

const formatMilliseconds = (value) => {
  const num = coerceNumber(value);
  return num === null ? "N/A" : `${(num * 1000).toFixed(3)} ms`;
};

const formatMegabytes = (value) => {
  const num = coerceNumber(value);
  return num === null ? "N/A" : `${(num / 1024).toFixed(2)} MB`;
};

function comparePerformance(perfA = {}, perfB = {}) {
  const TOLERANCE = 0.10;

  const accuracyA = coerceNumber(perfA.accuracy) ?? 0;
  const accuracyB = coerceNumber(perfB.accuracy) ?? 0;

  if (accuracyA !== accuracyB) {
    return {
      winner: accuracyA > accuracyB ? "A" : "B",
      reason: "accuracy",
      details: {
        accuracyA: formatPercent(accuracyA),
        accuracyB: formatPercent(accuracyB),
        diff: formatPercent(Math.abs(accuracyA - accuracyB))
      }
    };
  }

  const timeA = coerceNumber(perfA.median_elapsed_seconds)
    ?? coerceNumber(perfA.avg_elapsed_seconds)
    ?? coerceNumber(perfA.max_elapsed_seconds);
  const timeB = coerceNumber(perfB.median_elapsed_seconds)
    ?? coerceNumber(perfB.avg_elapsed_seconds)
    ?? coerceNumber(perfB.max_elapsed_seconds);

  if (timeA !== null && timeB !== null) {
    const diff = Math.abs(timeA - timeB);
    const avg = (timeA + timeB) / 2 || 0;

    if (avg > 0 && diff / avg >= TOLERANCE) {
      return {
        winner: timeA < timeB ? "A" : "B",
        reason: "time",
        details: {
          timeA: formatMilliseconds(timeA),
          timeB: formatMilliseconds(timeB),
          diff: formatMilliseconds(diff),
          tolerance: `${(TOLERANCE * 100)}%`
        }
      };
    }
  }

  const memA = coerceNumber(perfA.median_memory_kb)
    ?? coerceNumber(perfA.avg_memory_kb)
    ?? coerceNumber(perfA.max_memory_kb);
  const memB = coerceNumber(perfB.median_memory_kb)
    ?? coerceNumber(perfB.avg_memory_kb)
    ?? coerceNumber(perfB.max_memory_kb);

  if (memA !== null && memB !== null) {
    const diff = Math.abs(memA - memB);
    const avg = (memA + memB) / 2 || 0;

    if (avg > 0 && diff / avg >= TOLERANCE) {
      return {
        winner: memA < memB ? "A" : "B",
        reason: "memory",
        details: {
          memoryA: formatMegabytes(memA),
          memoryB: formatMegabytes(memB),
          diff: formatMegabytes(diff),
          tolerance: `${(TOLERANCE * 100)}%`
        }
      };
    }
  }

  return {
    winner: "TIE",
    reason: "all_metrics_equal_within_tolerance",
    details: {
      accuracy: formatPercent(accuracyA),
      time: formatMilliseconds(timeA),
      memory: formatMegabytes(memA)
    }
  };
}

function normalizePerformance(rawPerformance, status) {
  const perf = rawPerformance && typeof rawPerformance === "object" ? { ...rawPerformance } : {};
  const statusLower = (status || "").toLowerCase();
  const isSuccess = statusLower === "done" || statusLower === "completed";

  return {
    total_tests: coerceNumber(perf.total_tests) ?? 0,
    passed: coerceNumber(perf.passed) ?? 0,
    failed: coerceNumber(perf.failed) ?? 0,
    accuracy: coerceNumber(perf.accuracy) ?? (isSuccess ? 100 : 0),
    max_elapsed_seconds: coerceNumber(perf.max_elapsed_seconds),
    avg_elapsed_seconds: coerceNumber(perf.avg_elapsed_seconds),
    median_elapsed_seconds: coerceNumber(perf.median_elapsed_seconds),
    max_memory_kb: coerceNumber(perf.max_memory_kb),
    avg_memory_kb: coerceNumber(perf.avg_memory_kb),
    median_memory_kb: coerceNumber(perf.median_memory_kb),
    overall: perf.overall || (isSuccess ? "passed" : statusLower || "unknown"),
    ranking_priority: perf.ranking_priority || null
  };
}

function buildPlayerSnapshot(submission, parsedResult, status) {
  const normalizedPerformance = normalizePerformance(parsedResult?.performance, status);
  return {
    submissionId: submission.submissionId,
    status: status || "unknown",
    performance: normalizedPerformance,
    error: parsedResult?.error || null
  };
}

function safeParseJSON(raw) {
  if (!raw) return null;
  try {
    return JSON.parse(raw);
  } catch (err) {
    console.error("Failed to parse JSON payload from Redis", err);
    return null;
  }
}

function getActivePlayers(roomState) {
  return roomState.players
    .filter(p => p.role === "player" || p.role === "host")
    .map(p => p.username);
}

function resetMatchState(roomState) {
  const totalRounds = parseInt(roomState.settings?.rounds, 10) || 1;
  const scores = {};
  getActivePlayers(roomState).forEach(name => {
    scores[name] = 0;
  });
  roomState.match = {
    status: "in_progress",
    totalScheduledRounds: totalRounds,
    totalRounds,
    extraRoundsUsed: 0,
    roundsPlayed: 0,
    roundResults: [],
    scores
  };
  return roomState.match;
}

function ensureMatchState(roomState) {
  if (!roomState.match) {
    return resetMatchState(roomState);
  }
  const knownScores = roomState.match.scores || {};
  getActivePlayers(roomState).forEach(name => {
    if (typeof knownScores[name] !== "number") {
      knownScores[name] = 0;
    }
  });
  roomState.match.scores = knownScores;
  return roomState.match;
}

function computeStandings(scores) {
  const entries = Object.entries(scores);
  if (!entries.length) return [];
  entries.sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0]));
  return entries;
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

  const matchState = ensureMatchState(roomState);
  
  const submissions = Object.values(roomState.submissions).sort((a, b) => (a.timestamp || 0) - (b.timestamp || 0));
  console.log('[DEBUG] Found submissions:', submissions.length);
  
  if (submissions.length < 2) {
    console.log('[DEBUG] Need 2 submissions, got', submissions.length);
    return;
  }
  
  const [sub1, sub2] = submissions;
  const [meta1, meta2] = await Promise.all([
    redisClient.hGetAll(`sub:${sub1.submissionId}`),
    redisClient.hGetAll(`sub:${sub2.submissionId}`)
  ]);
  const status1 = meta1?.status ? String(meta1.status).toLowerCase() : null;
  const status2 = meta2?.status ? String(meta2.status).toLowerCase() : null;
  
  try {
    console.log('[DEBUG] Fetching results:', sub1.submissionId, sub2.submissionId);
    const result1 = await redisClient.get(`run_result:${sub1.submissionId}`);
    const result2 = await redisClient.get(`run_result:${sub2.submissionId}`);
    
    const parsed1 = safeParseJSON(result1);
    const parsed2 = safeParseJSON(result2);

    const finalStatus1 = status1 ? FINAL_STATUSES.has(status1) : Boolean(parsed1);
    const finalStatus2 = status2 ? FINAL_STATUSES.has(status2) : Boolean(parsed2);

    if (!parsed1 && !finalStatus1) {
      console.log('[DEBUG] Waiting for submission result 1 - status:', status1);
      return;
    }
    if (!parsed2 && !finalStatus2) {
      console.log('[DEBUG] Waiting for submission result 2 - status:', status2);
      return;
    }
    
    console.log('[DEBUG] Comparing results');
    const player1 = buildPlayerSnapshot(sub1, parsed1, status1);
    const player2 = buildPlayerSnapshot(sub2, parsed2, status2);
    const perf1 = player1.performance;
    const perf2 = player2.performance;
    
    const comparison = comparePerformance(perf1, perf2);
    const roundWinner = comparison.winner === 'A' ? sub1.username : comparison.winner === 'B' ? sub2.username : 'TIE';

    matchState.roundResults.push({
      round: matchState.roundResults.length + 1,
      winner: roundWinner,
      timestamp: Date.now(),
      comparison,
      players: {
        [sub1.username]: player1,
        [sub2.username]: player2
      }
    });
    matchState.roundsPlayed = matchState.roundResults.length;

    if (roundWinner !== 'TIE') {
      matchState.scores[roundWinner] = (matchState.scores[roundWinner] || 0) + 1;
    }

    const standings = computeStandings(matchState.scores);
    const topWins = standings.length ? standings[0][1] : 0;
    const leaders = standings.filter(([_, wins]) => wins === topWins);

    let matchStatus = matchState.status || "in_progress";
    let overallWinner = null;
    let needsTieBreak = false;

    if (matchState.roundsPlayed >= matchState.totalRounds) {
      if (leaders.length === 1) {
        matchStatus = "completed";
        overallWinner = leaders[0][0];
      } else if (matchState.extraRoundsUsed === 0) {
        matchState.extraRoundsUsed = 1;
        matchState.totalRounds += 1;
        matchStatus = "tiebreak";
        needsTieBreak = true;
      } else {
        matchStatus = "completed";
        overallWinner = "TIE";
      }
    } else {
      matchStatus = "in_progress";
    }

    matchState.status = matchStatus;
    matchState.overallWinner = overallWinner;
    
    const matchResult = {
      round: matchState.roundsPlayed,
      roundWinner,
      players: {
        [sub1.username]: player1,
        [sub2.username]: player2
      },
      winner: roundWinner,
      comparison,
      match: {
        status: matchStatus,
        scores: matchState.scores,
        roundsPlayed: matchState.roundsPlayed,
        totalRounds: matchState.totalRounds,
        scheduledRounds: matchState.totalScheduledRounds,
        extraRoundsUsed: matchState.extraRoundsUsed,
        needsTieBreak,
        overallWinner,
        roundResults: matchState.roundResults
      }
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
      resetMatchState(roomState);
      roomState.submissions = {};
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
    if (roomState.match && roomState.match.status === "completed") {
      console.log('[DEBUG] Submission ignored, match already completed');
      socket.emit("match-complete", {
        message: "Match already finished",
        match: roomState.match
      });
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
