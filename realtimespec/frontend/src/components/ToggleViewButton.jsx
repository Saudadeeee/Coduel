function ToggleViewButton({ showOpponent, onToggle }) {
  const label = showOpponent ? "View My Note" : "View Opponent";
  return (
    <button type="button" onClick={onToggle}>
      {label}
    </button>
  );
}

export default ToggleViewButton;
