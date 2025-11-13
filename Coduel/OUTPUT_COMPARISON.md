# Output Comparison - Token-Based (Whitespace-Insensitive)

## Cách so sánh output

Coduel sử dụng **token-based comparison** - so sánh từng token (số/chữ), bỏ qua khoảng trắng.

### ✅ Các output này được chấp nhận như GIỐNG NHAU:

**Expected:**
```
1 2 3
```

**User output - TẤT CẢ ĐỀU ĐÚNG:**
```
1 2 3          (spaces khác nhau)
1  2   3       (nhiều spaces)
1
2
3              (nhiều dòng)
1 2 3
               (có trailing newline)
```

### ❌ Output SAI:

**Expected:**
```
1 2 3
```

**User output - SAI:**
```
1 2 4          (số khác)
1 2            (thiếu số)
1 2 3 4        (thừa số)
```

## Ví dụ thực tế

### Bài toán: Tính tổng hai số

**Input:**
```
2 3
```

**Expected output:**
```
5
```

**User code outputs - TẤT CẢ ĐÚNG:**
- `5` ✅
- `5\n` ✅
- `  5  ` ✅
- `5     \n\n` ✅

**User code outputs - SAI:**
- `6` ❌ (sai kết quả)
- `Sum: 5` ❌ (thừa chữ)
- `` (empty) ❌ (không có output)

## Lợi ích

✅ **Đơn giản**: Không cần lo về format khoảng trắng
✅ **Linh hoạt**: `printf("1 2 3")` hay `printf("1\n2\n3")` đều được
✅ **Giống các OJ khác**: Codeforces, AtCoder, DMOJ đều dùng token-based
✅ **Ít WA oan**: Tránh WA vì trailing space hay newline

## Tips cho người chơi

1. **Không cần lo về format**: In ra đúng số/chữ là được
2. **Trailing spaces OK**: `cout << answer << "  ";` vẫn đúng
3. **Multiple spaces OK**: `cout << a << "   " << b;` vẫn đúng
4. **Extra newlines OK**: `cout << answer << "\n\n\n";` vẫn đúng

## So với cách cũ

**Cách cũ (strict):**
- `"1 2 3"` ≠ `"1  2  3"` ❌ WA vì spaces khác
- `"5"` ≠ `"5\n"` ❌ WA vì có newline
- Rất nhiều WA oan

**Cách mới (token-based):**
- `"1 2 3"` = `"1  2  3"` ✅ Đúng
- `"5"` = `"5\n"` ✅ Đúng
- Công bằng hơn, focus vào logic
