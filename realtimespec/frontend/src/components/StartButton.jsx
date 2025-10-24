function StartButton({ started, onStart, disabled }) {
  return (
    <button type="button" onClick={onStart} disabled={disabled}>
      {started ? "Started" : "Start"}
    </button>
  );
}

export default StartButton;
