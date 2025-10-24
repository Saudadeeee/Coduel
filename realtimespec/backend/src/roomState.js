export const ROOM_ID = "default";

const roomState = {
  started: false,
  notes: {
    player1: "",
    player2: "",
  },
  players: {
    player1: null,
    player2: null,
  },
  spectators: new Set(),
};

const socketRoles = new Map();

const OPPONENT_ROLE = {
  player1: "player2",
  player2: "player1",
};

export function assignRole(socketId) {
  const existingRole = socketRoles.get(socketId);
  if (existingRole === "player1" || existingRole === "player2") {
    roomState.players[existingRole] = socketId;
    socketRoles.set(socketId, existingRole);
    return existingRole;
  }
  if (existingRole === "spectator") {
    roomState.spectators.delete(socketId);
    socketRoles.delete(socketId);
  }

  let role = "spectator";
  if (!roomState.players.player1) {
    roomState.players.player1 = socketId;
    role = "player1";
  } else if (!roomState.players.player2) {
    roomState.players.player2 = socketId;
    role = "player2";
  } else {
    roomState.spectators.add(socketId);
  }
  socketRoles.set(socketId, role);
  return role;
}

export function getRole(socketId) {
  return socketRoles.get(socketId);
}

export function getRoomInfoForRole(role) {
  const normalizedRole = role ?? "spectator";
  return {
    role: normalizedRole,
    started: roomState.started,
    myNote: selectMyNote(normalizedRole),
    opponentNote: selectOpponentNote(normalizedRole),
  };
}

export function updatePlayerNote(socketId, noteText) {
  const role = socketRoles.get(socketId);
  if (role !== "player1" && role !== "player2") {
    return null;
  }
  const value = noteText ?? "";
  roomState.notes[role] = value;
  return {
    role,
    value,
    opponentRole: OPPONENT_ROLE[role],
    opponentSocketId: roomState.players[OPPONENT_ROLE[role]],
  };
}

export function getSpectatorSocketIds() {
  return Array.from(roomState.spectators);
}

export function getActivePlayerSockets() {
  return gatherActivePlayers();
}

export function startRoom(socketId) {
  const role = socketRoles.get(socketId);
  if (role !== "player1" || roomState.started) {
    return false;
  }
  roomState.started = true;
  return true;
}

export function resetStartedIfNeeded() {
  if (!roomState.players.player1 || !roomState.players.player2) {
    roomState.started = false;
    return true;
  }
  return false;
}

export function releaseRole(socketId) {
  const role = socketRoles.get(socketId);
  if (!role) {
    return { startedChanged: false, remainingPlayers: [] };
  }
  socketRoles.delete(socketId);
  if (role === "spectator") {
    roomState.spectators.delete(socketId);
    return {
      startedChanged: false,
      remainingPlayers: gatherActivePlayers(),
      spectators: getSpectatorSocketIds(),
    };
  }
  roomState.players[role] = null;
  roomState.notes[role] = "";
  const startedChanged = resetStartedIfNeeded();
  return {
    startedChanged,
    remainingPlayers: gatherActivePlayers(),
    spectators: getSpectatorSocketIds(),
  };
}

function gatherActivePlayers() {
  return (["player1", "player2"]).reduce((acc, role) => {
    const socketId = roomState.players[role];
    if (socketId) {
      acc.push({ role, socketId });
    }
    return acc;
  }, []);
}

function selectMyNote(role) {
  if (role === "player1" || role === "player2") {
    return roomState.notes[role];
  }
  return roomState.notes.player1;
}

function selectOpponentNote(role) {
  if (role === "player1") {
    return roomState.notes.player2;
  }
  if (role === "player2") {
    return roomState.notes.player1;
  }
  return roomState.notes.player2;
}
