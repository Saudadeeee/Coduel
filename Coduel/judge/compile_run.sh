#!/usr/bin/env bash
set -euo pipefail

MODE="both"
case "${1-}" in
  --compile-only)
    MODE="compile"
    shift
    ;;
  --run-only)
    MODE="run"
    shift
    ;;
  --mode)
    MODE="${2-both}"
    shift 2
    ;;
esac

LANGUAGE="${1}"
SRC_FILE="${2}"
EXE_NAME="main"
STD="${3:-}"

cd /work

case "$LANGUAGE" in
  c)
    BUILD_CMD=(/usr/bin/gcc -std=${STD:-c17} -O2 -pipe -Wall -Wextra -ffile-prefix-map="$PWD"=. "$SRC_FILE" -o "$EXE_NAME")
    RUN_CMD=("./$EXE_NAME")
    NEEDS_COMPILE=true
    ;;
  cpp)
    BUILD_CMD=(/usr/bin/g++ -std=${STD:-c++20} -O2 -pipe -Wall -Wextra -ffile-prefix-map="$PWD"=. "$SRC_FILE" -o "$EXE_NAME")
    RUN_CMD=("./$EXE_NAME")
    NEEDS_COMPILE=true
    ;;
  py)
    BUILD_CMD=(python3 -m py_compile "$SRC_FILE")
    RUN_CMD=(python3 "$SRC_FILE")
    NEEDS_COMPILE=false
    ;;
  java)
    BUILD_CMD=(javac "$SRC_FILE")
    MAIN_CLASS=$(grep -E "^\s*public\s+class\s+\w+" "$SRC_FILE" | head -1 | sed -E 's/.*public\s+class\s+(\w+).*/\1/' || echo "Main")
    RUN_CMD=(java "$MAIN_CLASS")
    NEEDS_COMPILE=false
    ;;
  js)
    BUILD_CMD=(node --check "$SRC_FILE")
    RUN_CMD=(node "$SRC_FILE")
    NEEDS_COMPILE=false
    ;;
  *)
    echo "Unsupported language: $LANGUAGE" >&2
    exit 2
    ;;
esac

if [ "$MODE" != "run" ]; then
  echo "Compiling $LANGUAGE code..." >&2
  "${BUILD_CMD[@]}"
  if [ $? -ne 0 ]; then
    echo "Compilation failed" >&2
    exit 1
  fi
  echo "Compilation successful" >&2
fi

if [ "$MODE" = "compile" ]; then
  echo "DONE"
  exit 0
fi

echo "Running tests..." >&2

i=1
while true; do
  IN="/tests/input${i}.txt"
  OUT="/tests/output${i}.txt"
  [ -f "$IN" ] || break

  echo "Running test $i..." >&2
  
  if python3 /usr/local/bin/run_with_metrics.py \
    --cmd "${RUN_CMD[@]}" \
    --stdin "$IN" \
    --stdout "user_out_${i}.txt" \
    --stderr "run_${i}.stderr" \
    --metrics "metrics_${i}.json"; then
    
    if python3 /usr/local/bin/compare_output.py "user_out_${i}.txt" "$OUT" > /dev/null 2>&1; then
      echo "TEST $i: OK"
      echo "OK" > "verdict_${i}.txt"
    else
      echo "TEST $i: WA (Wrong Answer)"
      echo "WA" > "verdict_${i}.txt"
    fi
  else
    EXIT_CODE=$?
    echo "TEST $i: RE (Runtime Error, exit code: $EXIT_CODE)"
    echo "RE" > "verdict_${i}.txt"
  fi

  i=$((i+1))
done

echo "DONE"
