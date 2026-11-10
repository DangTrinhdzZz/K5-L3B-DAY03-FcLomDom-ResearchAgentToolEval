# Báo cáo cá nhân — Nguyễn Đình Minh

## 1. Thông tin thành viên

- Họ tên: Nguyễn Đình Minh
- MSSV: 2A202603898
- Email: 26ai.minhnd7@vinuni.edu.vn
- GitHub: MinhNGD76
- Vai trò: TV3, baseline v0, system prompt, tool declaration và vòng tối ưu v1–v3

## 2. Phần việc phụ trách

- G2: chạy baseline `v0` trên starter chưa sửa, phân tích từng case FAIL, ghi dòng `v0` vào version log.
- G4: khai báo tool mới `compare_sources` của TV2 vào `artifacts/tools.yaml`, chạy run đối chứng, tối ưu `v1`–`v3` (mỗi version một giả thuyết), đóng băng `v3` cho TV4/TV1.
- Sở hữu `artifacts/system_prompt.md`, `artifacts/tools.yaml`, `artifacts/version_log.csv` và các run base trong `runs/`.

## 3. Đóng góp cụ thể

Tất cả run dùng provider `openai`, model `gpt-4o-mini`, bộ `data/eval_base.json` (20 case, không sửa nội dung). Mọi run đều có `provider_error_cases = 0` và `measured_cases = total_cases = 20`.

| Version | Thay đổi | Giả thuyết | Case accuracy |
|---|---|---|---:|
| v0 | Baseline starter | Đo hành vi chưa tối ưu | 0.65 |
| v0_toolset | Chỉ thêm khai báo `compare_sources` (đối chứng, không tính là vòng tối ưu) | Thêm tool mới không đổi hành vi base | 0.65 |
| v1 | `system_prompt.md`: bỏ 4 chỉ dẫn xấu (tự đoán, chọn sẵn Sam Altman, gửi không xác nhận, luôn 1 tool); thêm rule clarify / xác nhận / ngoài phạm vi | Chỉ dẫn xấu gây lỗi `missing_info`, `wrong_boundary`, `out_of_scope` | 0.80 |
| v2 | `tools.yaml`: viết lại description `clarify` (bắt buộc `response_type`) và `send` (boundary xác nhận) | `response_type` sai/thiếu do description mơ hồ | 0.95 |
| v3 | `tools.yaml`: description các tool tìm/đọc nói rõ khi nào dùng/không dùng và quy ước args (handle, query, topic, timeframe, search_type, limit) | Thiếu quy ước args làm routing/args không ổn định | 0.90 |

Phân tích chính:

- v0 FAIL 7 case: R03, R13 (query thừa chữ "news", thiếu `topic=news`); R08, R14 (dùng `send` để trả lời câu ngoài phạm vi); R10, R11 (tự đoán handle `sama`, bịa URL `example.com`); R12 (gửi Telegram không xác nhận).
- v1 sửa được R03, R08, R10, R14. M06 bị regression (gọi thêm `social_search` sau khi người dùng nói bỏ Twitter).
- v2 sửa R11 (`clarify` có `response_type=text`). R13 và M06 cũng PASS dù v2 không sửa `lookup`/`social_search`, nên tôi đánh giá đây là dao động giữa các run chứ không phải hiệu quả của v2.
- v3 giảm từ 0.95 xuống 0.90: M06 lại FAIL. M06 đổi kết quả qua các run (FAIL v1, PASS v2, FAIL v3), cho thấy case này không ổn định với `gpt-4o-mini`; một lần chạy cho mỗi version chưa đủ để kết luận v3 kém hơn v2.
- Lỗi còn tồn tại ở v3: R12 (model hỏi nội dung bằng `response_type=text` thay vì xin xác nhận `yes_no`) và M06.
- Cấu hình v3 đóng băng: `prompt_hash` `b3e117c056e0`, `tools_hash` `2e1477d7c969`, 11 tool (10 core/bonus + `compare_sources`).

## 4. Bằng chứng

- [system_prompt.md](../../starter_v0/artifacts/system_prompt.md), [tools.yaml](../../starter_v0/artifacts/tools.yaml), [version_log.csv](../../starter_v0/artifacts/version_log.csv).
- Run JSON:
  - [v0](../../starter_v0/runs/v0_B_base_openai_20261110T192210636811.json)
  - [v0_toolset](../../starter_v0/runs/v0_toolset_B_base_openai_20261110T195419739192.json)
  - [v1](../../starter_v0/runs/v1_B_base_openai_20261110T195512760538.json)
  - [v2](../../starter_v0/runs/v2_B_base_openai_20261110T195837350542.json)
  - [v3](../../starter_v0/runs/v3_B_base_openai_20261110T200022169324.json)
- Commit kỹ thuật: `cd4a7e9` (G2: baseline v0 + version log). Commit G4: _điền SHA sau khi commit_.
- Kiểm tra: `python scripts/preflight_provider.py --provider openai` PASS; `pytest tests/test_tool_contract.py` 60 passed sau mỗi lần sửa `tools.yaml`; toàn bộ `pytest` 79 passed, 14 skipped, 0 failed ở v3; `git diff -- data` rỗng (không sửa eval base/extension).
- AI/công cụ đã dùng: Claude Code hỗ trợ chạy lệnh eval, trích case FAIL từ `results[*].result.failures` trong run JSON, soạn nháp prompt/description và báo cáo này. Tôi tự kiểm tra bằng cách: đối chiếu metric và hash trong `version_log.csv` với `summary` và `artifact_version` của từng run JSON; chạy contract test sau mỗi thay đổi `tools.yaml`; đọc lại `actual_tool_calls` của từng case FAIL thay vì chỉ nhìn số tổng.

## 5. Tự đánh giá

- Làm tốt: baseline hợp lệ trước khi thêm tool; có run đối chứng `v0_toolset` để tách ảnh hưởng của tool mới; mỗi version chỉ một giả thuyết và có số liệu trước/sau từ run thật; ghi trung thực việc v3 không tăng điểm.
- Hạn chế: mỗi version chỉ chạy một lần nên không phân biệt được hẳn hiệu quả thay đổi với dao động của model (M06, R13). R12 chưa được sửa.
- Nếu có thêm thời gian: chạy lặp mỗi version 2–3 lần để đo độ ổn định; thêm một version sửa boundary `send` cho trường hợp nội dung chưa rõ (R12) và rule "khi người dùng bỏ một nguồn thì không gọi lại tool đó" (M06).
