# Báo cáo cá nhân — Triệu Hải Đăng Trình

## 1. Thông tin thành viên

- **Họ và tên:** Triệu Hải Đăng Trình
- **MSSV:** 2A202603874
- **Vai trò:** TV1 — trưởng nhóm
- **GitHub theo `TEAM.md`:** `DangTrinhdzZz`
- **Phạm vi chính:** G1 — thiết lập nhóm, kiểm tra môi trường/repository, kiểm thử, bàn giao cho TV3 và tổng hợp kết quả.

## 2. Phần việc phụ trách

Theo [`TEAM.md`](../../TEAM.md), G1 gồm năm nội dung:

1. Hoàn thiện thông tin nhóm và phân công.
2. Kiểm tra môi trường Python, dependencies và OpenAI provider.
3. Chạy kiểm thử, ghi nhận số lượng pass/fail/skip.
4. Kiểm tra tính toàn vẹn của cấu hình, dữ liệu đánh giá và tool contract.
5. Viết biên bản bàn giao G1 cho TV3.

Phạm vi G1 không bao gồm viết `compare_sources`, xây dựng 10 group eval case hoặc trực tiếp tối ưu prompt v1–v3. Các phần đó do TV2–TV4 thực hiện; tôi chỉ tổng hợp và đối chiếu bằng chứng khi hoàn thiện báo cáo nhóm.

## 3. Công việc trực tiếp thực hiện

### 3.1. Thiết lập nhóm và repository

- Cập nhật `TEAM.md` với tên nhóm FcLomDom, lớp L3B, repository, nhánh làm việc, vai trò TV1–TV4 và quy ước không push trực tiếp lên `main`.
- Ghi rõ nguyên tắc không commit `.env`/API key và không tự ý sửa dữ liệu baseline.
- Tạo tài liệu [`G1_TV1_to_TV3.md`](../../G1_TV1_to_TV3.md) để xác định phạm vi, file cần kiểm tra, lệnh kiểm tra và các mục còn mở trước khi TV3 tiếp nhận.

Bằng chứng kỹ thuật là commit `2ebd720` trên nhánh `trinh`, sau đó được tích hợp qua merge commit `f55e503`. Git lưu tên tác giả của commit G1 là `totoca6969`; báo cáo không dùng tên này để suy diễn thêm về danh tính ngoài thông tin đã có trong `TEAM.md`.

### 3.2. Kiểm tra môi trường và cấu trúc repository

Trong biên bản G1, tôi đã kiểm tra sự hiện diện và vai trò của:

- `starter_v0/env_loader.py` và OpenAI provider;
- `starter_v0/artifacts/system_prompt.md`, `tools.yaml`;
- các file eval base/extension và thư mục test;
- yêu cầu sử dụng `OPENAI_API_KEY` từ môi trường riêng, không ghi secret vào Git;
- lệnh preflight và pytest cần chạy từ đúng thư mục `starter_v0/`.

Biên bản ban đầu phân biệt rõ “file tồn tại” với “đã chạy thành công”. Tại thời điểm commit G1, preflight OpenAI, cài dependency và pytest chưa có log thực thi, nên tôi không ghi các hạng mục này là PASS.

### 3.3. Phối hợp và bàn giao

- Chuyển phạm vi và checklist G1 cho TV3, bao gồm yêu cầu giữ nguyên `eval_base.json`, làm việc trên nhánh riêng và báo lỗi bằng lệnh có thể tái hiện.
- Theo dõi phân công: TV2 phụ trách tool/test; TV3 phụ trách baseline và v1–v3; TV4 phụ trách group eval.
- Khi tổng hợp báo cáo, đối chiếu version log với summary của từng run, đối chiếu 10 case trong `eval_group.json` với kết quả group run, và tách lỗi chấm exact-match khỏi lỗi hành vi.

## 4. Công việc tổng hợp và kiểm tra, không nhận là đóng góp trực tiếp

| Nội dung | Người/nguồn thực hiện chính | Phần tôi thực hiện |
|---|---|---|
| Tool `compare_sources` và unit test | TV2; commits `925aac1`, `cf70685` | Kiểm tra đường dẫn, registry, tài liệu và số test để đưa vào báo cáo |
| Baseline và tối ưu v1–v3 | TV3; commits `cd4a7e9`, `dd0c808` | Đọc `version_log.csv` và run JSON, xác minh metric/failure đã báo cáo |
| 10 group eval case | TV4; commit `8cd569a` | Kiểm tra đủ 5 single-turn + 5 multi-turn, đọc từng expected/actual |
| Group evaluation run | Run JSON do nhóm cung cấp | Tổng hợp 10/10 measured, 0 provider error, 6/10 PASS và phân tích bốn case FAIL |
| Báo cáo nhóm | Dựa trên bằng chứng của cả nhóm | Biên tập cấu trúc, chuẩn hóa liên kết, nêu giới hạn và các mục thiếu bằng chứng |

Việc tổng hợp không được quy đổi thành quyền tác giả đối với code, eval case hoặc run của thành viên khác.

## 5. Kiểm thử và đánh giá kết quả

### 5.1. Pytest

Kết quả thực nghiệm được cung cấp từ máy người dùng:

```text
79 passed, 14 skipped, 0 failed in 0.59s
```

Kết quả cho thấy suite không có test thất bại; 14 test TODO của starter vẫn bị skip, nên chưa đáp ứng điều kiện bonus “0 skipped”. Trong phiên rà soát báo cáo hiện tại, lệnh `python -m pytest` không tái chạy được vì môi trường Python đang dùng chưa cài package `pytest`. Repository cũng chưa lưu file log pytest, do đó tôi ghi rõ nguồn của số liệu thay vì coi đây là bằng chứng tái lập độc lập.

### 5.2. Base evaluation

| Version | Case accuracy | Nhận xét |
|---|---:|---|
| v0 | 65% | Baseline trước tối ưu |
| v1 | 80% | Cải thiện sau khi bỏ chỉ dẫn xấu trong system prompt |
| v2 | 95% | Kết quả cao nhất trong bốn run |
| v3 | 90% | Giảm 5 điểm phần trăm so với v2; không phải cải thiện liên tục |

Mọi run base được dùng đều đo đủ 20/20 case và có 0 provider error. V3 còn thất bại ở `R12_confirm_before_send` và `M06_switch_tool`. Do mỗi version chỉ chạy một lần, chưa thể kết luận chắc chắn mức thay đổi là hoàn toàn do prompt/tool declaration.

### 5.3. Group evaluation

Run [`v3_B_group_openai_20261111T010903669307.json`](../../starter_v0/runs/v3_B_group_openai_20261111T010903669307.json) có:

- 10/10 case được đo, 0 lỗi provider;
- 6/10 PASS, case accuracy 60%;
- tool routing 80%, argument accuracy 60%, multi-turn accuracy 80%.

Bốn case FAIL được kiểm tra trực tiếp từ `results[*].result`:

- `G02`: gọi `papers` thay vì `lookup`.
- `G03`: gọi đúng `social_search` nhưng thiếu `search_type=Latest`; query khác chuỗi expected.
- `G04`: gọi đúng `clarify`, dùng đúng `response_type=text` và hỏi URL, nhưng câu hỏi khác chuỗi expected. Đây là lỗi exact-match, không phải lỗi hành vi làm rõ.
- `GM04`: ngoài `lookup` cho robotics còn gọi thêm `lookup` cho AI, trong khi expected chỉ có robotics.

Tôi giữ nguyên điểm chính thức 60%. Review thủ công chỉ dùng để giải thích hạn chế của bộ chấm, không tự sửa kết quả. Hai câu hỏi làm rõ tương đương về ngữ nghĩa không nên bị phân biệt chỉ vì khác cách diễn đạt; vòng sau nên dùng semantic predicate hoặc chỉ kiểm tra tool, `response_type` và việc câu hỏi yêu cầu URL.

Run group có artifact hash khác base v3. Vì vậy, tôi không mô tả hai run là byte-identical; cần đóng băng và commit prompt/tools trước khi đánh giá lại.

## 6. Bằng chứng

| Bằng chứng | Ý nghĩa |
|---|---|
| [`TEAM.md`](../../TEAM.md) | Thông tin nhóm, phân công G1 và quy ước làm việc |
| [`G1_TV1_to_TV3.md`](../../G1_TV1_to_TV3.md) | Phạm vi kiểm tra, checklist và bàn giao TV1 → TV3 |
| Commit `2ebd720` | Thay đổi kỹ thuật trực tiếp của G1: `TEAM.md` và biên bản bàn giao |
| [`version_log.csv`](../../starter_v0/artifacts/version_log.csv) | Giả thuyết, hash, metric trước/sau và run v0–v3 |
| [`group_report.md`](group_report.md) | Phần tổng hợp và kiểm tra bằng chứng của nhóm |
| Các run trong [`starter_v0/runs/`](../../starter_v0/runs/) | Summary, expected/actual tool calls và failure từng case |

## 7. Tự đánh giá

Điểm làm tốt là phạm vi G1 được xác định rõ, có tài liệu bàn giao và không đánh đồng việc quan sát file với kiểm thử thành công. Khi tổng hợp, tôi giữ nguyên số liệu bất lợi: v3 giảm so với v2, group eval chỉ đạt 60%, pytest còn 14 skip, UI và transcript chưa có.

Hạn chế chính là G1 ban đầu chưa có log thực thi cho Python/dependency/preflight/pytest; biên bản còn ghi sai đường dẫn dự kiến `docs/handoffs/G1_TV1_to_TV3.md` trong khi file thực tế ở root. Ngoài ra, artifact hash giữa base v3 và group v3 chưa đồng nhất, làm giảm khả năng tái lập chính xác.

Nếu có thêm thời gian, tôi sẽ chuẩn hóa đường dẫn bàn giao, lưu log pytest/preflight đã loại secret, xác nhận lại thông tin còn đánh dấu “chưa xác nhận” trong `TEAM.md`, đóng băng artifact trước khi chạy và tổ chức review thủ công cho các case exact-match/multi-turn.

## 8. Hạng mục chưa có đủ bằng chứng

- Chưa có log preflight OpenAI do TV1 trực tiếp chạy và lưu trong repo.
- Chưa có file log pytest; số liệu 79/14/0 trong 0,59 giây là kết quả được cung cấp từ máy người dùng.
- Chưa có UI, dependency UI hoặc link public.
- Chưa có live transcript ba luồng bắt buộc, đặc biệt luồng xác nhận trước khi `send`.
- Run group hiện là file chưa được Git theo dõi; cần đưa vào commit nộp bài.
- Báo cáo cá nhân này và phần tổng hợp mới chưa có commit; theo yêu cầu, tôi không tự commit hoặc push.
