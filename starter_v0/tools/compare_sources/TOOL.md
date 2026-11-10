---
name: compare_sources
track: core
kind: local_formatter
requires_env: []
inputs: [urls]
outputs: [domain_count, url_count, groups]
side_effect: false
---
# compare_sources

Nhóm các URL đã thu thập theo tên miền để kiểm tra bản tin hoặc bộ nguồn đang dựa vào bao nhiêu website. Dùng khi đã có danh sách URL và cần đếm hoặc nhóm theo tên miền. Dùng `lookup` để tìm nguồn mới và `fetch` để đọc nội dung URL.

- `urls` là danh sách khác rỗng gồm các URL tuyệt đối có giao thức HTTP hoặc HTTPS.
- Tên miền được viết thường, bỏ tiền tố `www.` và bỏ cổng. Các tên miền con khác được giữ riêng.
- URL được bỏ khoảng trắng hai đầu. Các URL trùng hoàn toàn sau bước này chỉ được tính một lần. Kết quả giữ thứ tự xuất hiện.
- Nếu có đầu vào sai, tool trả `error` và `message`. Với lỗi ở một phần tử, thông báo nêu vị trí bắt đầu từ 0.
- Tool chạy cục bộ. Số tên miền chỉ mô tả cách các link được phân bố giữa các website.

Ví dụ, với `["https://www.example.com/a", "https://example.com/b", "https://example.org/c"]`, kết quả có `domain_count: 2`, `url_count: 3` và hai nhóm `example.com`, `example.org`.

## Bàn giao tích hợp sau baseline v0

Đăng ký trong `tools/__init__.py`:

```python
from .compare_sources.tool import compare_sources
# Thêm vào TOOL_FUNCTIONS:
"compare_sources": compare_sources,
```

Khai báo đề xuất cho TV3, thêm bên dưới khóa `tools:` trong `artifacts/tools.yaml`:

```yaml
  - name: compare_sources
    description: >-
      Nhóm và đếm các URL đã có theo tên miền. Dùng khi người dùng đưa danh sách
      URL hoặc khi các tool trước đó đã trả về URL và người dùng muốn xem chúng
      đến từ bao nhiêu website. Khi cần tìm nguồn mới, dùng lookup. Khi cần đọc
      nội dung một URL, dùng fetch.
    parameters:
      type: object
      properties:
        urls:
          type: array
          minItems: 1
          items: {type: string}
          description: "Danh sách URL HTTP/HTTPS tuyệt đối đã có."
      required: [urls]
```

Gợi ý cho TV4: “Nhóm và đếm số tên miền trong https://www.example.com/a, https://example.com/b và https://example.org/c.” Tool kỳ vọng là `compare_sources`, với cả ba URL trong `urls`.
