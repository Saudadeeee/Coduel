import express from "express";
import http from "http";
import cors from "cors";
import { Server } from "socket.io";
import {
  ROOM_ID,
  assignRole,
  getRoomInfoForRole,
  getActivePlayerSockets,
  getSpectatorSocketIds,
  releaseRole,
  startRoom,
  updatePlayerNote,
} from "./roomState.js";

const app = express();
const server = http.createServer(app);

const PORT = process.env.PORT || 4000;
const CORS_ORIGIN = process.env.CORS_ORIGIN || "*";

const io = new Server(server, {
  cors: {
    origin: CORS_ORIGIN,
    methods: ["GET", "POST"],
  },
});

app.use(cors({ origin: CORS_ORIGIN }));
app.get("/health", (_req, res) => {
  res.json({ status: "ok" });
});

io.on("connection", (socket) => {
  socket.on("joinRoom", ({ roomId }) => {
    if (roomId !== ROOM_ID) {
      return;
    }
    socket.join(ROOM_ID);
    const role = assignRole(socket.id);
    const info = getRoomInfoForRole(role);
    socket.emit("roomInfo", info);
    getActivePlayerSockets()
      .filter(({ socketId }) => socketId !== socket.id)
      .forEach(({ role: playerRole, socketId }) => {
        io.to(socketId).emit("roomInfo", getRoomInfoForRole(playerRole));
      });
    getSpectatorSocketIds()
      .filter((spectatorId) => spectatorId !== socket.id)
      .forEach((spectatorId) => {
        io.to(spectatorId).emit("roomInfo", getRoomInfoForRole("spectator"));
      });
  });

  socket.on("startRoom", ({ roomId }) => {
    if (roomId !== ROOM_ID) {
      return;
    }
    if (startRoom(socket.id)) {
      io.to(ROOM_ID).emit("roomStarted", { started: true });
    }
  });

  socket.on("updateNote", ({ roomId, noteText }) => {
    if (roomId !== ROOM_ID) {
      return;
    }
    const update = updatePlayerNote(socket.id, noteText);
    if (!update) {
      return;
    }
    socket.emit("myNoteSync", { myNote: update.value });

    const opponentSocketId = update.opponentSocketId;
    if (opponentSocketId) {
      io.to(opponentSocketId).emit("opponentNoteUpdate", { opponentNote: update.value });
    }

    const spectatorIds = getSpectatorSocketIds();
    if (spectatorIds.length > 0) {
      spectatorIds.forEach((spectatorSocketId) => {
        if (update.role === "player1") {
          io.to(spectatorSocketId).emit("myNoteSync", { myNote: update.value });
        } else {
          io.to(spectatorSocketId).emit("opponentNoteUpdate", { opponentNote: update.value });
        }
      });
    }
  });

  socket.on("disconnect", () => {
    const { startedChanged, remainingPlayers, spectators } = releaseRole(socket.id);
    remainingPlayers.forEach(({ role, socketId }) => {
      io.to(socketId).emit("roomInfo", getRoomInfoForRole(role));
    });
    spectators?.forEach((spectatorId) => {
      io.to(spectatorId).emit("roomInfo", getRoomInfoForRole("spectator"));
    });
    if (startedChanged) {
      io.to(ROOM_ID).emit("roomStarted", { started: false });
    }
  });
});

server.listen(PORT, () => {
  console.log(`Backend listening on port ${PORT}`);
});
