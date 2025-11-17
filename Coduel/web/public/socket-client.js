class SocketClient {
  constructor() {
    this.socket = null;
    this.roomCode = null;
    this.username = null;
    this.role = null;
    this.listeners = new Map();
  }

  connect(serverUrl = window.location.origin) {
    return new Promise((resolve, reject) => {
      if (this.socket) {
        console.warn("Socket already connected");
        resolve();
        return;
      }

      if (typeof io === "undefined") {
        console.error("Socket.IO client not loaded");
        reject(new Error("Socket.IO client not loaded"));
        return;
      }

      this.socket = io(serverUrl);

      this.socket.on("connect", () => {
        this.emit("connected", { socketId: this.socket.id });
        resolve();
      });

      this.socket.on("connect_error", (error) => {
        console.error("Connection error:", error);
        reject(error);
      });

      this.socket.on("disconnect", () => {
        this.emit("disconnected");
      });

      this.socket.on("room-joined", (data) => {
        this.roomCode = data.roomCode;
        this.role = data.role;
        this.emit("room-joined", data);
      });

      this.socket.on("room-full", () => {
        this.emit("room-full");
      });

      this.socket.on("user-joined", (data) => {
        this.emit("user-joined", data);
      });

      this.socket.on("user-left", (data) => {
        this.emit("user-left", data);
      });

      this.socket.on("settings-updated", (settings) => {
        this.emit("settings-updated", settings);
      });

      this.socket.on("opponent-code-update", (data) => {
        this.emit("opponent-code-update", data);
      });

    this.socket.on("match-started", (data) => {
      this.emit("match-started", data);
      });

    this.socket.on("opponent-submitted", (data) => {
      this.emit("opponent-submitted", data);
    });

    this.socket.on("match-result", (data) => {
      this.emit("match-result", data);
    });

    this.socket.on("next-round", (data) => {
      this.emit("next-round", data);
    });

    this.socket.on("match-timeout", (data) => {
      console.warn("Match timeout:", data);
      this.emit("match-timeout", data);
    });

    this.socket.on("submission-rejected", (data) => {
      this.emit("submission-rejected", data);
    });

    this.socket.on("time-expired", (data) => {
      this.emit("time-expired", data);
    });

      this.socket.on("player-joined", (data) => {
        this.emit("player-joined", data);
      });

      this.socket.on("player-left", (data) => {
        this.emit("player-left", data);
      });

      this.socket.on("player-ready-update", (data) => {
        this.emit("player-ready-update", data);
      });

      this.socket.on("room-state", (data) => {
        this.emit("room-state", data);
      });

      this.socket.on("error", (error) => {
        console.error("Socket error:", error);
        this.emit("error", error);
      });
    });
  }

  joinRoom(roomCode, username, role = "player") {
    if (!this.socket) {
      console.error("Socket not connected");
      return;
    }

    this.socket.emit("join-room", { roomCode, username, role });
  }

  updateSettings(settings) {
    if (!this.socket || !this.roomCode) {
      console.error("Not in a room");
      return;
    }

    this.socket.emit("update-settings", {
      roomCode: this.roomCode,
      settings
    });
  }

  sendCodeChange(code, language) {
    if (!this.socket || !this.roomCode) {
      return;
    }

    this.socket.emit("code-change", {
      roomCode: this.roomCode,
      code,
      language
    });
  }

  startMatch() {
    if (!this.socket || !this.roomCode) {
      console.error("Not in a room");
      return;
    }

    this.socket.emit("start-match", {
      roomCode: this.roomCode
    });
  }

  submitCode(roomCode, submissionId) {
    if (!this.socket || !roomCode) {
      console.error("Not in a room");
      return;
    }

    this.socket.emit("submit-code", {
      roomCode,
      submissionId
    });
  }

  sendReadyStatus(ready) {
    if (!this.socket || !this.roomCode) {
      console.error("Not in a room");
      return;
    }

    this.socket.emit("player-ready", {
      roomCode: this.roomCode,
      ready: ready
    });
  }

  disconnect() {
    if (this.socket) {
      this.socket.disconnect();
      this.socket = null;
      this.roomCode = null;
      this.username = null;
      this.role = null;
    }
  }

  on(event, callback) {
    if (!this.listeners.has(event)) {
      this.listeners.set(event, []);
    }
    this.listeners.get(event).push(callback);
  }

  off(event, callback) {
    if (!this.listeners.has(event)) {
      return;
    }
    const callbacks = this.listeners.get(event);
    const index = callbacks.indexOf(callback);
    if (index !== -1) {
      callbacks.splice(index, 1);
    }
  }

  emit(event, data) {
    if (!this.listeners.has(event)) {
      return;
    }
    const callbacks = this.listeners.get(event);
    callbacks.forEach(callback => callback(data));
  }

  static getInstance() {
    if (!SocketClient.instance) {
      SocketClient.instance = new SocketClient();
    }
    return SocketClient.instance;
  }
}

SocketClient.instance = null;

window.SocketClient = SocketClient;
