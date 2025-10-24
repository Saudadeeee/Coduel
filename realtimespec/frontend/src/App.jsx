import { useCallback, useEffect, useRef, useState } from "react";
import socket from "./socket.js";
import NoteArea from "./components/NoteArea.jsx";
import ToggleViewButton from "./components/ToggleViewButton.jsx";
import StartButton from "./components/StartButton.jsx";
import JoinButton from "./components/JoinButton.jsx";

const ROOM_ID = "default";

const initialRoomState = {
  role: "spectator",
  started: false,
  myNote: "",
  opponentNote: "",
};

function App() {
  const [status, setStatus] = useState(socket.connected ? "Connected" : "Disconnected");
  const [roomState, setRoomState] = useState(initialRoomState);
  const [noteDraft, setNoteDraft] = useState("");
  const [showOpponent, setShowOpponent] = useState(false);
  const [isJoining, setIsJoining] = useState(false);
  const noteTimerRef = useRef();

  useEffect(() => {
    const handleConnect = () => {
      setStatus("Connected");
    };

    const handleDisconnect = () => {
      setStatus("Disconnected");
      setRoomState(initialRoomState);
      setNoteDraft("");
      setShowOpponent(false);
      setIsJoining(false);
      if (noteTimerRef.current) {
        clearTimeout(noteTimerRef.current);
        noteTimerRef.current = undefined;
      }
    };

    const handleRoomInfo = (info) => {
      setIsJoining(false);
      setShowOpponent(false);
      setRoomState({
        role: info.role,
        started: info.started,
        myNote: info.myNote ?? "",
        opponentNote: info.opponentNote ?? "",
      });
      setNoteDraft(info.myNote ?? "");
    };

    const handleMyNoteSync = ({ myNote }) => {
      setRoomState((prev) => ({
        ...prev,
        myNote: myNote ?? "",
      }));
      setNoteDraft(myNote ?? "");
    };

    const handleOpponentNoteUpdate = ({ opponentNote }) => {
      setRoomState((prev) => ({
        ...prev,
        opponentNote: opponentNote ?? "",
      }));
    };

    const handleRoomStarted = ({ started }) => {
      setRoomState((prev) => ({
        ...prev,
        started: Boolean(started),
      }));
    };

    socket.on("connect", handleConnect);
    socket.on("disconnect", handleDisconnect);
    socket.on("roomInfo", handleRoomInfo);
    socket.on("myNoteSync", handleMyNoteSync);
    socket.on("opponentNoteUpdate", handleOpponentNoteUpdate);
    socket.on("roomStarted", handleRoomStarted);

    return () => {
      socket.off("connect", handleConnect);
      socket.off("disconnect", handleDisconnect);
      socket.off("roomInfo", handleRoomInfo);
      socket.off("myNoteSync", handleMyNoteSync);
      socket.off("opponentNoteUpdate", handleOpponentNoteUpdate);
      socket.off("roomStarted", handleRoomStarted);
      if (noteTimerRef.current) {
        clearTimeout(noteTimerRef.current);
      }
    };
  }, []);

  const emitNoteUpdate = useCallback((value, role) => {
    if (noteTimerRef.current) {
      clearTimeout(noteTimerRef.current);
    }
    noteTimerRef.current = setTimeout(() => {
      socket.emit("updateNote", {
        roomId: ROOM_ID,
        noteText: value,
        role,
      });
    }, 250);
  }, []);

  const handleJoinRoom = () => {
    setIsJoining(true);
    socket.emit("joinRoom", { roomId: ROOM_ID });
  };

  const handleToggleView = () => {
    setShowOpponent((prev) => !prev);
  };

  const handleStart = () => {
    if (roomState.role !== "player1" || roomState.started) {
      return;
    }
    socket.emit("startRoom", { roomId: ROOM_ID });
  };

  const handleNoteChange = (value) => {
    const canEdit = roomState.role === "player1" || roomState.role === "player2";
    if (!canEdit || showOpponent) {
      return;
    }
    setNoteDraft(value);
    setRoomState((prev) => ({
      ...prev,
      myNote: value,
    }));
    emitNoteUpdate(value, roomState.role);
  };

  const canEdit = roomState.role === "player1" || roomState.role === "player2";
  const noteValue = showOpponent ? roomState.opponentNote : noteDraft;
  const joinDisabled = isJoining || status !== "Connected";

  return (
    <div style={{ fontFamily: "sans-serif", padding: "2rem", maxWidth: "640px", margin: "0 auto" }}>
      <h1>Realtime Spec</h1>
      <p>Status: {status}</p>
      <p>Role: {roomState.role}</p>
      <div style={{ display: "flex", gap: "0.75rem", marginBottom: "1rem" }}>
        <JoinButton onJoin={handleJoinRoom} disabled={joinDisabled} joining={isJoining} />
        {roomState.role === "player1" && (
          <StartButton started={roomState.started} onStart={handleStart} disabled={roomState.started} />
        )}
        <ToggleViewButton showOpponent={showOpponent} onToggle={handleToggleView} />
      </div>
      <NoteArea value={noteValue} onChange={handleNoteChange} readOnly={!canEdit || showOpponent} />
      <div style={{ marginTop: "1rem", fontSize: "0.9rem", color: "#555" }}>
        <p>
          Started: <strong>{roomState.started ? "Yes" : "No"}</strong>
        </p>
        <p>
          Viewing: <strong>{showOpponent ? "Opponent" : "My Note"}</strong>
        </p>
      </div>
    </div>
  );
}

export default App;
