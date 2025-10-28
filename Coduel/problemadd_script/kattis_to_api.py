#!/usr/bin/env python3
"""
Script để lấy bài tập từ Kattis và tự động add vào hệ thống thông qua API
"""
import requests
import json
import sys
from kattis_scrape import build_problem_json

API_URL = "http://localhost:8000"

def submit_problem_to_api(problem_data: dict) -> dict:
    """
    Gửi problem data đến API /problem-add
    
    Args:
        problem_data: Dictionary chứa thông tin bài toán từ Kattis
        
    Returns:
        Response từ API
    """
    endpoint = f"{API_URL}/problem-add"
    
    try:
        response = requests.post(
            endpoint,
            json=problem_data,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"❌ Error submitting to API: {e}")
        if hasattr(e, 'response') and e.response is not None:
            try:
                error_detail = e.response.json()
                print(f"   Detail: {error_detail}")
            except:
                print(f"   Response: {e.response.text}")
        raise

def add_kattis_problem(slug: str, dry_run: bool = False):
    """
    Lấy bài toán từ Kattis và add vào hệ thống
    
    Args:
        slug: Kattis problem slug (ví dụ: "hello", "carrots", "planina")
        dry_run: Nếu True, chỉ hiển thị data mà không submit
    """
    print(f"📥 Fetching problem '{slug}' from Kattis...")
    
    try:
        # Lấy dữ liệu từ Kattis
        problem_data = build_problem_json(slug)
        
        print(f"✅ Successfully fetched: {problem_data['title']}")
        print(f"   Difficulty: {problem_data['difficulty']}")
        print(f"   Time limit: {problem_data['time_limit_ms']}ms")
        print(f"   Memory limit: {problem_data['memory_limit_kb']}KB")
        print(f"   Tests: {len(problem_data['tests'])}")
        
        if dry_run:
            print("\n📋 Preview (dry run mode):")
            print(json.dumps(problem_data, ensure_ascii=False, indent=2))
            return None
        
        # Submit đến API
        print(f"\n📤 Submitting to API...")
        response = submit_problem_to_api(problem_data)
        
        print(f"\n✨ Success!")
        print(f"   Problem ID: {response['problem_id']}")
        print(f"   Number: {response['number']}")
        print(f"   Difficulty: {response['difficulty']}")
        print(f"   Tests: {response['tests_count']}")
        
        return response
        
    except Exception as e:
        print(f"❌ Failed to add problem: {e}")
        raise

def add_multiple_problems(slugs: list[str], dry_run: bool = False):
    """
    Thêm nhiều bài toán cùng lúc
    
    Args:
        slugs: List các Kattis problem slugs
        dry_run: Nếu True, chỉ hiển thị data mà không submit
    """
    results = []
    failed = []
    
    print(f"🚀 Adding {len(slugs)} problems from Kattis...\n")
    
    for i, slug in enumerate(slugs, 1):
        print(f"[{i}/{len(slugs)}] Processing '{slug}'...")
        try:
            result = add_kattis_problem(slug, dry_run=dry_run)
            results.append(result)
            print()
        except Exception as e:
            print(f"   ⚠️  Skipping due to error\n")
            failed.append((slug, str(e)))
    
    # Summary
    print("=" * 60)
    print("📊 SUMMARY")
    print("=" * 60)
    print(f"Total: {len(slugs)}")
    print(f"✅ Success: {len(results)}")
    print(f"❌ Failed: {len(failed)}")
    
    if failed:
        print("\n⚠️  Failed problems:")
        for slug, error in failed:
            print(f"   - {slug}: {error}")
    
    return results, failed

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Lấy bài tập từ Kattis và add vào hệ thống"
    )
    parser.add_argument(
        "slugs",
        nargs="+",
        help="Kattis problem slug(s). Ví dụ: hello carrots planina"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Chỉ preview data mà không submit đến API"
    )
    parser.add_argument(
        "--api-url",
        default="http://localhost:8000",
        help="API base URL (default: http://localhost:8000)"
    )
    
    args = parser.parse_args()
    
    # Update API URL if provided
    API_URL = args.api_url
    
    try:
        if len(args.slugs) == 1:
            add_kattis_problem(args.slugs[0], dry_run=args.dry_run)
        else:
            add_multiple_problems(args.slugs, dry_run=args.dry_run)
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        sys.exit(1)
