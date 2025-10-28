# 🎉 Hệ thống Import Kattis đã được tạo xong!

## 📁 Files đã tạo

```
problemadd_script/
├── kattis_scrape.py       (đã có sẵn) - Scrape dữ liệu từ Kattis
├── kattis_to_api.py       (MỚI) - Submit dữ liệu đến API
├── batch_import.py        (MỚI) - Import hàng loạt
├── test_system.py         (MỚI) - Test hệ thống
├── requirements.txt       (MỚI) - Dependencies
├── README.md              (MỚI) - Hướng dẫn chi tiết
├── QUICKSTART.md          (MỚI) - Quick start
├── CHEATSHEET.txt         (MỚI) - Reference nhanh
└── demo.sh                (MỚI) - Demo script
```

## 🚀 Cách sử dụng ngay

### Bước 1: Cài đặt
```bash
cd /home/khenh/Code/Project/Cowar/Coduel/problemadd_script
pip install -r requirements.txt
```

### Bước 2: Test hệ thống
```bash
python test_system.py
```

### Bước 3: Thử import 1 bài
```bash
# Preview trước (không add vào DB)
python kattis_to_api.py hello --dry-run

# Add thật vào hệ thống
python kattis_to_api.py hello
```

### Bước 4: Import nhiều bài
```bash
# Import 3 bài cùng lúc
python kattis_to_api.py hello carrots r2

# Hoặc dùng batch import
python batch_import.py --difficulty easy
```

## 📖 Documentation

1. **QUICKSTART.md** - Hướng dẫn nhanh cho người mới
2. **README.md** - Documentation đầy đủ
3. **CHEATSHEET.txt** - Reference card để xem nhanh
4. **demo.sh** - Script demo tương tác

## ⚡ Commands quan trọng

```bash
# Test hệ thống
python test_system.py

# Import 1 bài
python kattis_to_api.py <slug>

# Import nhiều bài
python kattis_to_api.py <slug1> <slug2> <slug3>

# Preview (không submit)
python kattis_to_api.py <slug> --dry-run

# Batch import easy problems
python batch_import.py --difficulty easy

# Xem help
python kattis_to_api.py --help
```

## 🎯 Workflow

```
1. Tìm bài trên Kattis
   https://open.kattis.com/problems/hello
                                      └─────┘ slug

2. Import vào hệ thống
   python kattis_to_api.py hello

3. Kiểm tra kết quả
   http://localhost:3000/mainmenu.html
```

## 📝 Example Usage

```bash
# Import "Hello World" problem
python kattis_to_api.py hello

# Import 5 bài easy
python kattis_to_api.py hello carrots r2 planina quadrant

# Import tất cả easy problems trong list
python batch_import.py --difficulty easy

# Preview một bài khó trước khi add
python kattis_to_api.py somehard --dry-run
```

## ✅ Features

- ✅ Tự động lấy title, description từ Kattis
- ✅ Parse time limit và memory limit
- ✅ Tự động map difficulty dựa trên Kattis rating
- ✅ Lấy sample input/output làm test case
- ✅ Tạo đầy đủ cấu trúc file theo format hệ thống
- ✅ Support batch import nhiều bài
- ✅ Preview mode (--dry-run)
- ✅ Error handling và retry logic
- ✅ Pretty output với emoji và colors

## 🐛 Troubleshooting

**Lỗi Connection Refused:**
```bash
# Khởi động API server trước
cd ../api
python app.py
# hoặc
cd ../
docker-compose up api
```

**Lỗi Module Not Found:**
```bash
pip install -r requirements.txt
```

**Lỗi 404 từ Kattis:**
- Kiểm tra lại slug có đúng không
- Thử truy cập URL trên browser: https://open.kattis.com/problems/<slug>

## 🎓 Tips

1. Luôn dùng `--dry-run` để preview trước khi add
2. Import từng batch nhỏ (5-10 bài) để tránh rate limit
3. Có thể edit thêm test cases sau qua web UI
4. Hệ thống tự động tạo problem number unique

## 📞 Need Help?

```bash
# Xem docs
cat README.md
cat QUICKSTART.md
cat CHEATSHEET.txt

# Run test
python test_system.py

# Help command
python kattis_to_api.py --help
```

## 🎊 Ready to go!

Hệ thống đã sẵn sàng! Hãy thử:
```bash
python test_system.py
```

Nếu mọi thứ OK, bắt đầu import:
```bash
python kattis_to_api.py hello --dry-run
python kattis_to_api.py hello
```

Happy coding! 🚀
