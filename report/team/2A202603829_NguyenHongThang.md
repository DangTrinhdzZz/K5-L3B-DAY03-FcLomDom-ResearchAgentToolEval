# Báo cáo cá nhân — Nguyễn Hồng Thắng - 2A202603829

## 1. Thông tin thành viên

- Họ tên: Nguyễn Hồng Thắng
- MSSV: 2A202603829
- Email: thangdktd@gmail.com
- Vai trò: Thành viên 4 — Group Eval, QA & Reporting

## 2. Phần việc phụ trách

- Thiết kế bộ đánh giá riêng của nhóm, kiểm thử phiên bản v3
- Phân tích kết quả và tổng hợp bằng chứng cho báo cáo cuối

## 3. Đóng góp cụ thể

- file data/eval_group.json theo cấu trúc của data/eval_base.json, gồm 10 case: 5 câu hỏi một lượt và 5 hội thoại nhiều lượt. Mỗi case được khai báo id, phase, failure_type, expect và metadata.what_it_tests để mô tả mục tiêu kiểm thử.
- Chạy đánh giá và phân tích kết quả
- Chuẩn bị báo cáo và QA

## 4. Bằng chứng

- data/eval_group.json — bộ 10 case kiểm thử do tôi phụ trách.
- artifacts/tools.yaml — khai báo tool, trong đó có compare_sources với tham số urls.
- runs/*group*.json — cần bổ sung tên file run v3 thực tế sau khi kiểm tra.
- report/team/group_report.md — phần nội dung nhóm cần đối chiếu với bản đã commit.
- report/team/2A202603829_NguyenHongThang.md — báo cáo cá nhân này.
- Branch cá nhân: thangdktd.

- đã sử dụng ChatGPT để hỗ trợ xây dựng các tình huống eval, chuẩn hóa cấu trúc JSON, gợi ý tiêu chí đánh giá và biên soạn báo cáo.
- So sánh cấu trúc eval_group.json với bộ base và yêu cầu trong đề; kiểm tra đúng 5 query + 5 turns, có test compare_sources. Đối chiếu tên tool và arguments với artifacts/tools.yaml; kiểm tra JSON hợp lệ trước khi chạy.

## 5. Tự đánh giá

- Hiểu rõ hơn sự khác nhau giữa agent gọi đúng tool và tool thực thi đúng chức năng. Bộ eval giúp đánh giá lựa chọn công cụ, tham số và khả năng xử lý ngữ cảnh; trong khi unit test và QA kiểm tra thêm chất lượng triển khai. 
