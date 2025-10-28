#!/usr/bin/env python3
"""
Script mẫu để thêm hàng loạt bài tập Kattis easy/fast vào hệ thống
"""
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
    
    args = parser.parse_args()
    
    # Chọn danh sách bài tập
    if args.difficulty == "easy":
        problems = EASY_PROBLEMS
    elif args.difficulty == "medium":
        problems = MEDIUM_PROBLEMS
    elif args.difficulty == "hard":
        problems = HARD_PROBLEMS
    else:  # all
        problems = EASY_PROBLEMS + MEDIUM_PROBLEMS + HARD_PROBLEMS
    
    print(f"📚 Importing {len(problems)} {args.difficulty} problems from Kattis")
    print("=" * 60)
    
    # Import
    results, failed = add_multiple_problems(problems, dry_run=args.dry_run)
    
    print("\n✅ Done!")
