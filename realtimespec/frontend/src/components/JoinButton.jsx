function JoinButton({ onJoin, disabled, joining }) {
  return (
    <button type="button" onClick={onJoin} disabled={disabled}>
      {joining ? "Joining..." : "Join Room"}
    </button>
  );
}

export default JoinButton;
