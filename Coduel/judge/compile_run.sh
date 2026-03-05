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
    ;;
  cpp)
    BUILD_CMD=(/usr/bin/g++ -std=${STD:-c++20} -O2 -pipe -Wall -Wextra -ffile-prefix-map="$PWD"=. "$SRC_FILE" -o "$EXE_NAME")
    RUN_CMD=("./$EXE_NAME")
    ;;
  py)
    BUILD_CMD=(python3 -m py_compile "$SRC_FILE")
    RUN_CMD=(python3 "$SRC_FILE")
    ;;
  java)
    BUILD_CMD=(javac "$SRC_FILE")
    MAIN_CLASS=$(grep -E "^\s*public\s+class\s+\w+" "$SRC_FILE" | head -1 | sed -E 's/.*public\s+class\s+(\w+).*/\1/' || echo "Main")
    RUN_CMD=(java "$MAIN_CLASS")
    ;;
  js)
    BUILD_CMD=(node --check "$SRC_FILE")
    RUN_CMD=(node "$SRC_FILE")
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

RUNS_PER_TEST=${RUNS_PER_TEST:-3}

i=1
while true; do
  IN="/tests/input${i}.txt"
  OUT="/tests/output${i}.txt"
  [ -f "$IN" ] || break

  echo "Running test $i (${RUNS_PER_TEST} run(s))..." >&2

  FINAL_VERDICT="OK"
  for run in $(seq 1 "$RUNS_PER_TEST"); do
    if python3 /usr/local/bin/run_with_metrics.py \
      --cmd "${RUN_CMD[@]}" \
      --stdin "$IN" \
      --stdout "user_out_${i}.txt" \
      --stderr "run_${i}_run${run}.stderr" \
      --metrics "metrics_${i}_run${run}.json"; then

      if ! python3 /usr/local/bin/compare_output.py "user_out_${i}.txt" "$OUT" > /dev/null 2>&1; then
        FINAL_VERDICT="WA"
      fi
    else
      FINAL_VERDICT="RE"
    fi
  done

  echo "TEST $i: $FINAL_VERDICT"
  echo "$FINAL_VERDICT" > "verdict_${i}.txt"

  i=$((i+1))
done

echo "DONE"
