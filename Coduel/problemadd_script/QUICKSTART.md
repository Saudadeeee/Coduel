# Quick Start Guide

## 🚀 Cách sử dụng nhanh

### Bước 1: Cài đặt dependencies

```bash
cd problemadd_script
pip install -r requirements.txt
```

### Bước 2: Khởi động API server

```bash
# Terminal 1 - khởi động API
cd ../
docker-compose up api

# Hoặc chạy trực tiếp
cd api
python app.py
```

### Bước 3: Import bài từ Kattis

```bash
# Terminal 2 - import problems
cd problemadd_script

# Thử preview một bài trước (không add vào database)
python kattis_to_api.py hello --dry-run

# Add một bài
python kattis_to_api.py hello

# Add nhiều bài cùng lúc
python kattis_to_api.py hello carrots r2 planina quadrant

# Add tất cả bài easy trong list có sẵn
python batch_import.py --difficulty easy
```

## 📝 Ví dụ thực tế

### Scenario 1: Thêm 1 bài cụ thể

```bash
# Tìm bài trên Kattis: https://open.kattis.com/problems/fizzbuzz
# Lấy slug: fizzbuzz
python kattis_to_api.py fizzbuzz
```

Output:
```
📥 Fetching problem 'fizzbuzz' from Kattis...
✅ Successfully fetched: FizzBuzz
   Difficulty: easy
   Time limit: 1000ms
   Memory limit: 1048576KB
   Tests: 1

📤 Submitting to API...

✨ Success!
   Problem ID: 002-fizzbuzz
   Number: 2
   Difficulty: easy
   Tests: 1
```

### Scenario 2: Import hàng loạt

```bash
# Import 10 bài easy
python batch_import.py --difficulty easy
```

### Scenario 3: Tự tạo list riêng

```python
# Tạo file my_problems.py
from kattis_to_api import add_multiple_problems

my_list = [
    "hello",
    "fizzbuzz", 
    "timeloop",
    # ... thêm các bài bạn muốn
]

add_multiple_problems(my_list)
```

Chạy:
```bash
python my_problems.py
```

## 🔍 Tìm bài toán Kattis

1. Vào https://open.kattis.com/problems
2. Filter theo độ khó (difficulty)
3. Copy slug từ URL

Ví dụ:
- URL: `https://open.kattis.com/problems/hello`
- Slug: `hello`

## 🎯 Tips

1. **Preview trước khi add**: Dùng `--dry-run` để xem data trước
2. **Add từng batch nhỏ**: Tránh quá nhiều requests đến Kattis
3. **Kiểm tra duplicate**: Hệ thống sẽ auto-increment problem number
4. **Edit sau**: Có thể edit test cases thêm qua web UI

## 🐛 Common Issues

**Issue**: Connection refused
```
❌ Error submitting to API: Connection refused
```
**Fix**: Start API server trước

**Issue**: 404 Not Found from Kattis
```
❌ Failed: 404 Not Found
```
**Fix**: Kiểm tra lại slug có đúng không

**Issue**: Duplicate problem
→ OK! Hệ thống tự tạo số mới (002, 003, ...)

## 📊 Check kết quả

Sau khi import xong:
1. Mở http://localhost:3000/mainmenu.html
2. Hoặc check qua API: `curl http://localhost:8000/problems`
