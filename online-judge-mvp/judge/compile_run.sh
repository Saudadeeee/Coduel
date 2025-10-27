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
OPT="${3:-O2}"
STD="${4:-}"

cd /work

case "$LANGUAGE" in
  c)
    BUILD_CMD=(/usr/bin/gcc -std=${STD:-c17} -$OPT -pipe -Wall -Wextra -ffile-prefix-map="$PWD"=. "$SRC_FILE" -o "$EXE_NAME")
    RUN_CMD=("./$EXE_NAME")
    ;;
  cpp)
    BUILD_CMD=(/usr/bin/g++ -std=${STD:-c++20} -$OPT -pipe -Wall -Wextra -ffile-prefix-map="$PWD"=. "$SRC_FILE" -o "$EXE_NAME")
    RUN_CMD=("./$EXE_NAME")
    ;;
  py)
    BUILD_CMD=(python3 -m py_compile "$SRC_FILE")
    RUN_CMD=(python3 "$SRC_FILE")
    ;;
  java)
    BUILD_CMD=(javac "$SRC_FILE")
    RUN_CMD=(java Main)
    ;;
  js)
    BUILD_CMD=(node --check "$SRC_FILE")
    RUN_CMD=(node "$SRC_FILE")
    ;;
  *)
    echo "Unsupported language" >&2
    exit 2
    ;;
esac

if [ "$MODE" != "run" ]; then
  "${BUILD_CMD[@]}"
fi

if [ "$MODE" = "compile" ]; then
  echo "DONE"
  exit 0
fi

if [ "$LANGUAGE" = "c" ] || [ "$LANGUAGE" = "cpp" ]; then
  if [ ! -x "$EXE_NAME" ]; then
    echo "Executable $EXE_NAME not found" >&2
    exit 3
  fi
fi

i=1
while true; do
  IN="/tests/input${i}.txt"
  OUT="/tests/output${i}.txt"
  [ -f "$IN" ] || break

  case "$LANGUAGE" in
    c|cpp)
      /usr/bin/time -v --output=metrics_${i}.txt "${RUN_CMD[@]}" < "$IN" > "user_out_${i}.txt" 2> "run_${i}.stderr" || true
      ;;
    java)
      /usr/bin/time -v --output=metrics_${i}.txt java Main < "$IN" > "user_out_${i}.txt" 2> "run_${i}.stderr" || true
      ;;
    py)
      /usr/bin/time -v --output=metrics_${i}.txt python3 "$SRC_FILE" < "$IN" > "user_out_${i}.txt" 2> "run_${i}.stderr" || true
      ;;
    js)
      /usr/bin/time -v --output=metrics_${i}.txt node "$SRC_FILE" < "$IN" > "user_out_${i}.txt" 2> "run_${i}.stderr" || true
      ;;
  esac

  if diff -q "user_out_${i}.txt" "$OUT" > /dev/null 2>&1; then
    echo "TEST $i: OK"
    echo "OK" > "verdict_${i}.txt"
  else
    echo "TEST $i: WA"
    echo "WA" > "verdict_${i}.txt"
  fi

  i=$((i+1))
done

echo "DONE"
