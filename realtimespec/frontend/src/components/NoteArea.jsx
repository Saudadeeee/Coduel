function NoteArea({ value, onChange, readOnly }) {
  const handleChange = (event) => {
    if (readOnly) {
      return;
    }
    onChange?.(event.target.value);
  };

  return (
    <textarea
      value={value}
      onChange={handleChange}
      readOnly={readOnly}
      rows={12}
      style={{ width: "100%", fontFamily: "monospace", fontSize: "1rem", padding: "0.75rem" }}
      placeholder="Share notes with the session"
    />
  );
}

export default NoteArea;
