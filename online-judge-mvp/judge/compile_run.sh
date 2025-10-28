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

i=1
while true; do
  IN="/tests/input${i}.txt"
  OUT="/tests/output${i}.txt"
  [ -f "$IN" ] || break

  python3 /usr/local/bin/run_with_metrics.py \
    --cmd "${RUN_CMD[@]}" \
    --stdin "$IN" \
    --stdout "user_out_${i}.txt" \
    --stderr "run_${i}.stderr" \
    --metrics "metrics_${i}.json" || true

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
