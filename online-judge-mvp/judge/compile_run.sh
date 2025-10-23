#!/usr/bin/env bash
set -euo pipefail

LANGUAGE="${1}"         # c | cpp
SRC_FILE="${2}"         # main.c | main.cpp
EXE_NAME="main"
OPT="${3:-O2}"          # O0|O1|O2 cho MVP
STD="${4:-c17}"         # c17|c++20

cd /work

# Biên dịch
if [ "$LANGUAGE" = "c" ]; then
  /usr/bin/gcc -std=$STD -$OPT -pipe -Wall -Wextra -ffile-prefix-map="$PWD"=. "$SRC_FILE" -o "$EXE_NAME"
elif [ "$LANGUAGE" = "cpp" ]; then
  /usr/bin/g++ -std=$STD -$OPT -pipe -Wall -Wextra -ffile-prefix-map="$PWD"=. "$SRC_FILE" -o "$EXE_NAME"
else
  echo "Unsupported language" >&2
  exit 2
fi

# Chạy qua tất cả test *.txt theo cặp inputX/outputX nếu tồn tại
RESULT_JSON='{"tests":[],"ok":true,"metrics":[]}'
i=1
while true; do
  IN="/tests/input${i}.txt"
  OUT="/tests/output${i}.txt"
  [ -f "$IN" ] || break

  # Chạy với giới hạn thời gian tổng quát (demo: 2s) & đo bằng /usr/bin/time -v
  # (Ở MVP, ta chỉ demo giới hạn logic; thực tế khuyên dùng cgroups qua Docker run options)
  /usr/bin/time -v --output=metrics_${i}.txt ./"$EXE_NAME" < "$IN" > "user_out_${i}.txt" 2> "run_${i}.stderr" || true

  # So sánh exact (MVP). Sau này thay bằng checker linh hoạt.
  if diff -q "user_out_${i}.txt" "$OUT" > /dev/null 2>&1; then
    echo "TEST $i: OK"
    echo "OK" > "verdict_${i}.txt"
  else
    echo "TEST $i: WA"
    echo "WA" > "verdict_${i}.txt"
    RESULT_JSON='{"tests":[],"ok":false,"metrics":[]}'
  fi

  i=$((i+1))
done

# In gói kết quả về stdout theo format thô, worker sẽ parse file (verdict_*.txt + metrics_*.txt)
echo "DONE"
