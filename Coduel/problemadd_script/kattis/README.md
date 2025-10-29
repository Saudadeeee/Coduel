# Kattis Problem Importer

Script để tự động lấy bài tập từ Kattis và thêm vào hệ thống Coduel.

## Cài đặt

```bash
pip install requests beautifulsoup4
```

## Cách sử dụng

### 1. Thêm một bài toán

```bash
python kattis_to_api.py hello
```

### 2. Thêm nhiều bài toán cùng lúc

```bash
python kattis_to_api.py hello carrots planina
```

### 3. Preview trước khi thêm (dry run)

```bash
python kattis_to_api.py hello --dry-run
```

### 4. Sử dụng API URL khác

```bash
python kattis_to_api.py hello --api-url http://your-server:8000
```

## Tìm Kattis Problem Slug

1. Vào trang bài toán trên Kattis, ví dụ: `https://open.kattis.com/problems/hello`
2. Lấy phần cuối của URL: `hello` là slug

## Các bài toán Kattis phổ biến

### Easy / Fast
- `hello` - Hello World!
- `carrots` - Solving for Carrots
- `r2` - R2
- `planina` - Planina
- `quadrant` - Quadrant Selection
- `timeloop` - Stuck In A Time Loop
- `oddities` - Oddities
- `fizzbuzz` - FizzBuzz
- `twostones` - Take Two Stones
- `spavanac` - Spavanac

### Medium
- `addtwonumbers` - Add Two Numbers
- `different` - A Different Problem
- `sumkindofproblem` - Sum Kind of Problem
- `grassseed` - Grass Seed Inc.
- `pet` - Pet
- `bijele` - Bijele
- `cold` - Cold-puter Science
- `nastyhacks` - Nasty Hacks

## Ví dụ thực tế

```bash
# Thêm 10 bài easy
python kattis_to_api.py hello carrots r2 planina quadrant timeloop oddities fizzbuzz twostones spavanac

# Preview một bài trước
python kattis_to_api.py hello --dry-run

# Sau khi xem OK, thêm vào thật
python kattis_to_api.py hello
```

## Cấu trúc dữ liệu

Script sẽ tự động:
- ✅ Lấy tiêu đề, mô tả từ Kattis
- ✅ Parse time limit và memory limit
- ✅ Tự động map difficulty (dựa trên rating Kattis)
- ✅ Lấy sample input/output
- ✅ Tạo test case đầu tiên từ sample
- ✅ Submit đến API `/problem-add`

## Lưu ý

- Đảm bảo API server đang chạy (`docker-compose up` hoặc chạy `api/app.py`)
- Mặc định API ở `http://localhost:8000`
- Sample input/output sẽ được dùng làm test case đầu tiên với visibility = "public"
- Bạn có thể thêm test cases sau thông qua giao diện web `/problem-edit`

## Troubleshooting

### Connection refused
```
❌ Error submitting to API: Connection refused
```
→ Kiểm tra API server có đang chạy không

### Problem not found
```
❌ Failed to add problem: 404 Not Found
```
→ Kiểm tra lại slug có đúng không trên Kattis

### Rate limiting
Nếu thêm quá nhiều bài cùng lúc, Kattis có thể rate limit. Hãy thêm từng batch nhỏ.
