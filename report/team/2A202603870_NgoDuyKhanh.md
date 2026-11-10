# Báo cáo cá nhân — Ngô Duy Khánh

## 1. Thông tin thành viên

- Họ tên: Ngô Duy Khánh
- MSSV: 2A202603870
- Email: 26ai.khanhnd6@vinuni.edu.vn
- Vai trò: TV2, phát triển tool và unit test

## 2. Phần việc phụ trách

- Xây dựng một tool hỗ trợ xử lý các URL đã thu thập trong quá trình research.
- Kiểm thử tool cục bộ và chuẩn bị khai báo để TV3 tích hợp sau baseline.

## 3. Đóng góp cụ thể

- `compare_sources` nhóm URL theo tên miền, loại link trùng và trả số lượng URL cùng số nhóm. Tool trả lỗi có cấu trúc nếu đầu vào không hợp lệ.
- Unit test kiểm tra kết quả nhóm, URL trùng, đầu vào sai kiểu, URL thiếu giao thức phù hợp, tên máy chủ lỗi và cổng không hợp lệ.
- Tài liệu tool có khai báo YAML đề xuất và tình huống mẫu để TV4 viết eval kiểm tra khả năng chọn tool.
- Sau khi xác minh baseline `v0`, đăng ký `compare_sources` trong `TOOL_FUNCTIONS` để agent gọi được hàm theo tên tool.

## 4. Bằng chứng

- [Code tool](../../starter_v0/tools/compare_sources/tool.py), [đăng ký tool](../../starter_v0/tools/__init__.py), [tài liệu và khai báo đề xuất](../../starter_v0/tools/compare_sources/TOOL.md), [unit test](../../starter_v0/tests/test_tools_todo.py).
- Commit kỹ thuật cho code, tài liệu và unit test: `925aac1`. Commit đăng ký tool: `cf70685`.
- [Run baseline v0](../../starter_v0/runs/v0_B_base_openai_20261110T192210636811.json) có 20/20 case được đo và 0 lỗi provider. Hash prompt và khai báo tool khớp với bản đang dùng.
- Codex hỗ trợ viết code, tài liệu và test. Sau khi đăng ký tool, Codex chạy `python -m pytest -q -p no:cacheprovider` trong `starter_v0`: **74 pass, 14 skip, 0 fail**. Chạy riêng `compare_sources`: **12/12 ca pass**.
- Kiểm tra tích hợp offline: dùng YAML đề xuất trong `TOOL.md` và provider mô phỏng để gọi `compare_sources` qua agent. Câu hỏi mẫu trả đúng **3 URL thuộc 2 tên miền**.
- Trạng thái bàn giao: TV3 thêm khai báo vào `artifacts/tools.yaml`. TV4 dùng câu hỏi mẫu trong tài liệu để kiểm tra model chọn đúng tool trong eval nhóm.

## 5. Tự đánh giá

_Bổ sung sau khi tự kiểm tra và xem kết quả eval tích hợp._
