#!/usr/bin/env python3
"""
Simple test script để kiểm tra hệ thống có hoạt động không
"""
import sys
import requests

def test_api_connection():
    """Test xem API có đang chạy không"""
    print("🔍 Testing API connection...")
    try:
        response = requests.get("http://localhost:8000/problems", timeout=5)
        if response.status_code == 200:
            print("✅ API is running and accessible")
            data = response.json()
            print(f"   Current problems: {len(data.get('problems', []))}")
            return True
        else:
            print(f"❌ API returned status code: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to API at http://localhost:8000")
        print("   Make sure API server is running:")
        print("   → cd ../api && python app.py")
        print("   → or: docker-compose up api")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_scraper():
    """Test xem scraper có hoạt động không"""
    print("\n🔍 Testing Kattis scraper...")
    try:
        from kattis_scrape import build_problem_json
        print("✅ Scraper module imported successfully")
        return True
    except ImportError as e:
        print(f"❌ Cannot import scraper: {e}")
        print("   Make sure you're in the right directory")
        return False

def test_dependencies():
    """Test xem dependencies có đủ không"""
    print("\n🔍 Testing dependencies...")
    missing = []
    
    try:
        import requests
        print("✅ requests installed")
    except ImportError:
        missing.append("requests")
        print("❌ requests not installed")
    
    try:
        from bs4 import BeautifulSoup
        print("✅ beautifulsoup4 installed")
    except ImportError:
        missing.append("beautifulsoup4")
        print("❌ beautifulsoup4 not installed")
    
    if missing:
        print(f"\n⚠️  Missing dependencies: {', '.join(missing)}")
        print(f"   Install with: pip install {' '.join(missing)}")
        return False
    
    return True

def main():
    print("╔════════════════════════════════════════╗")
    print("║  Kattis to Coduel - System Check      ║")
    print("╚════════════════════════════════════════╝\n")
    
    results = []
    
    # Test dependencies
    results.append(("Dependencies", test_dependencies()))
    
    # Test scraper
    results.append(("Scraper", test_scraper()))
    
    # Test API
    results.append(("API Connection", test_api_connection()))
    
    # Summary
    print("\n" + "="*50)
    print("📊 SUMMARY")
    print("="*50)
    
    all_pass = True
    for name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"  {status} - {name}")
        if not passed:
            all_pass = False
    
    print("="*50)
    
    if all_pass:
        print("\n🎉 All checks passed! System is ready.")
        print("\n📝 Next steps:")
        print("   1. python kattis_to_api.py hello --dry-run")
        print("   2. python kattis_to_api.py hello")
        print("   3. Open http://localhost:3000/mainmenu.html")
        return 0
    else:
        print("\n⚠️  Some checks failed. Please fix the issues above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
