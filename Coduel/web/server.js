import express from "express";
import { createServer } from "http";
import { Server } from "socket.io";
import path from "path";
import { fileURLToPath } from "url";
import { createClient } from "redis";

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

// Static files
app.use(express.static(publicDir));

// Routes
app.get("/", (_req, res) => res.redirect("/mainmenu.html"));
app.get("/mainmenu.html", (_req, res) => res.sendFile(path.join(publicDir, "mainmenu.html")));
app.get("/workspace.html", (_req, res) => res.sendFile(path.join(publicDir, "workspace.html")));
app.get("/dashboard", (_req, res) => res.sendFile(path.join(publicDir, "dashboard.html")));
app.get("/roomhost.html", (_req, res) => res.sendFile(path.join(publicDir, "roomhost.html")));
app.get("/problem-add", (_req, res) => res.sendFile(path.join(publicDir, "problem-add.html")));
app.get("/problem-edit", (_req, res) => res.sendFile(path.join(publicDir, "problem-edit.html")));
app.get("/problem", (_req, res) => res.sendFile(path.join(publicDir, "workspace.html")));

const rooms = new Map();

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
          playerCodes: {}
        };
        rooms.set(roomCode, roomState);
      }

      // Add user to room
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

      // Notify others with updated player list
      io.to(roomCode).emit("player-joined", { 
        username, 
        role,
        players: roomState.players.map(p => ({ 
          username: p.username, 
          socketId: p.socketId, 
          role: p.role,
          ready: p.ready 
        }))
      });

      // Send full room state to the joining player
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

  // Update room settings (host only)
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

  // Handle player ready status
  socket.on("player-ready", ({ roomCode, ready }) => {
    const roomState = rooms.get(roomCode);
    if (roomState) {
      const player = roomState.players.find(p => p.socketId === socket.id);
      if (player) {
        player.ready = ready;
        
        // Broadcast updated player list to all in room
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

  // Sync code in real-time
  socket.on("code-change", ({ roomCode, code, language }) => {
    const roomState = rooms.get(roomCode);
    if (roomState) {
      roomState.playerCodes[socket.id] = code;
      
      // Broadcast to room (for spectating)
      socket.to(roomCode).emit("opponent-code-update", {
        socketId: socket.id,
        code,
        language,
        username: roomState.players.find(p => p.socketId === socket.id)?.username || "Unknown"
      });
    }
  });

  // Start match
  socket.on("start-match", ({ roomCode }) => {
    const roomState = rooms.get(roomCode);
    if (roomState && roomState.players[0]?.socketId === socket.id) {
      io.to(roomCode).emit("match-started", {
        settings: roomState.settings
      });
      console.log(`Match started in room ${roomCode}`);
    }
  });

  // Submit code
  socket.on("submit-code", ({ roomCode, code }) => {
    socket.to(roomCode).emit("opponent-submitted", {
      socketId: socket.id
    });
  });

  // Disconnect
  socket.on("disconnect", () => {
    console.log("User disconnected:", socket.id);
    
    // Remove from all rooms
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

      // Clean up empty rooms
      if (roomState.players.length === 0 && roomState.spectators.length === 0) {
        rooms.delete(roomCode);
        console.log(`Room ${roomCode} deleted (empty)`);
      }
    }
  });
});

httpServer.listen(5173, () => console.log("Web server with Socket.IO at http://localhost:5173"));
