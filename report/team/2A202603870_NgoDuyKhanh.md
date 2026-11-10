# Báo cáo cá nhân — Ngô Duy Khánh

## 1. Thông tin thành viên

- Họ tên: Ngô Duy Khánh
- MSSV: 2A202603870
- Vai trò: TV2, phát triển tool và unit test

## 2. Phần việc phụ trách

- Xây dựng một tool hỗ trợ xử lý các URL đã thu thập trong quá trình research.
- Kiểm thử tool cục bộ và chuẩn bị khai báo để TV3 tích hợp sau baseline.

## 3. Đóng góp cụ thể

- `compare_sources` nhóm URL theo tên miền, loại link trùng và trả số lượng URL cùng số nhóm. Tool trả lỗi có cấu trúc nếu đầu vào không hợp lệ.
- Unit test kiểm tra kết quả nhóm, URL trùng, đầu vào sai kiểu, URL thiếu giao thức phù hợp, tên máy chủ lỗi và cổng không hợp lệ.
- Tài liệu tool có khai báo YAML đề xuất và tình huống mẫu để TV4 viết eval kiểm tra khả năng chọn tool.

## 4. Bằng chứng

- [Code tool](../../starter_v0/tools/compare_sources/tool.py), [tài liệu và khai báo đề xuất](../../starter_v0/tools/compare_sources/TOOL.md), [unit test](../../starter_v0/tests/test_tools_todo.py).
- Codex hỗ trợ viết code, tài liệu và test. Lần rà soát trước khi tích hợp, Codex chạy `python -m pytest -q -p no:cacheprovider` và ghi nhận `74 passed, 14 skipped, 0 failed`. Khai báo đề xuất và ví dụ trong tài liệu đã được đối chiếu với code.
- Commit tích hợp vào agent: _Bổ sung sau khi có baseline `v0`._
- Kiểm thử ban đầu: Codex chạy `python -m pytest -q -k compare_sources` trong `starter_v0` trên nhánh `test2`. Kết quả: `10 passed, 76 deselected in 0.22s`.
- Trạng thái tích hợp: Chờ TV3 bàn giao đường dẫn run baseline `v0`. Code tool và unit test đã sẵn sàng.

## 5. Tự đánh giá

_Bổ sung sau khi tự kiểm tra và xem kết quả eval tích hợp._
