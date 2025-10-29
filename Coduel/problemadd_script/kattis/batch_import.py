#!/usr/bin/env python3
"""
Script mẫu để thêm hàng loạt bài tập Kattis easy/fast vào hệ thống
"""
from pathlib import Path
from kattis_to_api import add_multiple_problems

# Danh sách bài tập Kattis theo độ khó
EASY_PROBLEMS = [
    "hello",           # Hello World!
    "carrots",         # Solving for Carrots
    "r2",              # R2
    "planina",         # Planina
    "quadrant",        # Quadrant Selection
    "timeloop",        # Stuck In A Time Loop
    "oddities",        # Oddities
    "fizzbuzz",        # FizzBuzz
    "twostones",       # Take Two Stones
    "spavanac",        # Spavanac
]

MEDIUM_PROBLEMS = [
    "addtwonumbers",   # Add Two Numbers
    "different",       # A Different Problem
    "sumkindofproblem", # Sum Kind of Problem
    "grassseed",       # Grass Seed Inc.
    "pet",             # Pet
    "bijele",          # Bijele
    "cold",            # Cold-puter Science
    "nastyhacks",      # Nasty Hacks
]

HARD_PROBLEMS = [
    # Thêm các bài khó vào đây nếu muốn
]

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Batch import Kattis problems")
    parser.add_argument(
        "--difficulty",
        choices=["easy", "medium", "hard", "all"],
        default="easy",
        help="Chọn độ khó muốn import"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview mode"
    )
    parser.add_argument(
        "--from-file",
        help="Đường dẫn tới file chứa danh sách slug (mỗi dòng một slug, dòng bắt đầu bằng # sẽ bị bỏ qua)"
    )
    parser.add_argument(
        "--chunk-size",
        type=int,
        default=10,
        help="Số lượng bài import mỗi batch để tránh rate limit (default: 10)"
    )
    
    args = parser.parse_args()
    
    problems: list[str] = []
    
    if args.from_file:
        slug_file = Path(args.from_file)
        if not slug_file.is_file():
            parser.error(f"Không tìm thấy file: {slug_file}")
        for raw_line in slug_file.read_text(encoding="utf-8").splitlines():
            line = raw_line.strip()
            if not line or line.startswith("#"):
                continue
            if "#" in line:
                line = line.split("#", 1)[0].strip()
            if not line:
                continue
            slug = line.split()[0]
            problems.append(slug)
        if not problems:
            parser.error(f"File {slug_file} không chứa slug hợp lệ.")
    else:
        # Chọn danh sách bài tập
        if args.difficulty == "easy":
            problems = EASY_PROBLEMS
        elif args.difficulty == "medium":
            problems = MEDIUM_PROBLEMS
        elif args.difficulty == "hard":
            problems = HARD_PROBLEMS
        else:  # all
            problems = EASY_PROBLEMS + MEDIUM_PROBLEMS + HARD_PROBLEMS
    
    # Loại bỏ slug trùng lặp trong khi giữ thứ tự
    seen = set()
    deduped = []
    for slug in problems:
        if slug not in seen:
            deduped.append(slug)
            seen.add(slug)
    problems = deduped
    
    print(f"📚 Importing {len(problems)} problems from Kattis")
    print("=" * 60)
    
    if not problems:
        print("⚠️ Không có slug nào để import.")
        raise SystemExit(1)
    
    chunk_size = max(1, args.chunk_size)
    all_results = []
    all_failed = []
    
    for start in range(0, len(problems), chunk_size):
        batch = problems[start:start + chunk_size]
        print(f"\n🚀 Processing batch {start // chunk_size + 1} ({len(batch)} problems)...")
        results, failed = add_multiple_problems(batch, dry_run=args.dry_run)
        all_results.extend(results)
        all_failed.extend(failed)
        if failed:
            print("⚠️ Batch encountered failures; tiếp tục với batch kế tiếp.")
    
    print("\n📊 OVERALL SUMMARY")
    print("=" * 60)
    print(f"Total problems requested: {len(problems)}")
    print(f"✅ Success: {len([r for r in all_results if r is not None])}")
    print(f"❌ Failed: {len(all_failed)}")
    if all_failed:
        for slug, error in all_failed:
            print(f"   - {slug}: {error}")
    
    print("\n✅ Done!")
