#!/bin/bash

# Script demo để test import từ Kattis

echo "🚀 Kattis to Coduel Importer Demo"
echo "=================================="
echo ""

# Kiểm tra API server
echo "1️⃣ Checking API server..."
if curl -s http://localhost:8000/problems > /dev/null; then
    echo "   ✅ API server is running"
else
    echo "   ❌ API server is not running!"
    echo "   Please start it with: cd ../api && python app.py"
    exit 1
fi

echo ""
echo "2️⃣ Installing dependencies..."
pip install -q -r requirements.txt

echo ""
echo "3️⃣ Demo: Preview a problem (dry-run)"
echo "   Command: python kattis_to_api.py hello --dry-run"
echo ""
read -p "   Press Enter to continue..."
python kattis_to_api.py hello --dry-run

echo ""
echo ""
echo "4️⃣ Demo: Add one problem"
echo "   Command: python kattis_to_api.py hello"
echo ""
read -p "   Press Enter to add the problem (Ctrl+C to cancel)..."
python kattis_to_api.py hello

echo ""
echo ""
echo "5️⃣ Demo: Add multiple problems"
echo "   Command: python kattis_to_api.py carrots r2 planina"
echo ""
read -p "   Press Enter to add 3 problems (Ctrl+C to cancel)..."
python kattis_to_api.py carrots r2 planina

echo ""
echo ""
echo "✅ Demo completed!"
echo ""
echo "📋 Available commands:"
echo "   - Add one:     python kattis_to_api.py <slug>"
echo "   - Add many:    python kattis_to_api.py <slug1> <slug2> ..."
echo "   - Preview:     python kattis_to_api.py <slug> --dry-run"
echo "   - Batch easy:  python batch_import.py --difficulty easy"
echo ""
echo "🌐 Check your problems at: http://localhost:3000/mainmenu.html"
