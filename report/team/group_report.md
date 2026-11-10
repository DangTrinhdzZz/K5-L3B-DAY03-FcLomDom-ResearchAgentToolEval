# Báo cáo nhóm — Day 03 Research Agent Tool Evaluation

## 1. Thông tin nhóm

- **Nhóm:** FcLomDom; **lớp:** L3B.
- **Repository:** <https://github.com/DangTrinhdzZz/K5-L3B-DAY03-FcLomDom-ResearchAgentToolEval>
- **Thành viên:** Triệu Hải Đăng Trình (TV1, 2A202603874), Ngô Duy Khánh (TV2, 2A202603870), Nguyễn Đình Minh (TV3, 2A202603898), Nguyễn Hồng Thắng (TV4, 2A202603829).
- **Provider/model của các run được báo cáo:** OpenAI / `gpt-4o-mini`.
- **Phân công:** TV1 thiết lập nhóm, kiểm tra môi trường và tổng hợp; TV2 phát triển `compare_sources` và unit test; TV3 chạy baseline, phân tích lỗi và tối ưu v1–v3; TV4 xây dựng bộ group evaluation.

Chi tiết phân công và quy ước làm việc nằm trong [`TEAM.md`](../../TEAM.md).

## 2. Mục tiêu và cách tiếp cận — PHẦN A

### A1. Agent này làm được gì

Research agent hỗ trợ tìm thông tin trên web và mạng xã hội, đọc URL hoặc bài báo arXiv, tra cứu chính sách nội bộ, định dạng kết quả và nhóm các URL theo tên miền. Agent dùng tool calling; thao tác gửi nội dung ra ngoài chỉ được thực hiện sau khi người dùng xác nhận.

- **CLI:** từ `starter_v0/`, dùng `python chat.py --help` để xem tham số và chạy với provider OpenAI.
- **UI và link dùng thử:** chưa có mã nguồn UI, dependency UI hoặc URL public trong repository. Hạng mục CP5 này chưa hoàn thành.

### A2. Danh sách tool

| Tool | Chức năng | Tool nhóm tự thêm? |
|---|---|---|
| `clarify` | Hỏi thông tin còn thiếu hoặc xin xác nhận | Không |
| `timeline` | Lấy bài đăng của một tài khoản X cụ thể | Không |
| `social_search` | Tìm bài đăng mạng xã hội theo chủ đề | Không |
| `lookup` | Tra cứu web hoặc tin tức theo chủ đề và thời gian | Không |
| `fetch` | Đọc nội dung một URL cụ thể | Không |
| `format` | Định dạng dữ liệu thành bản tin | Không |
| `send` | Gửi nội dung sau khi được xác nhận | Không |
| `policy` | Tra cứu chính sách nội bộ | Không |
| `papers` | Tìm bài báo arXiv | Không |
| `paper_text` | Đọc nội dung bài báo arXiv | Không |
| `compare_sources` | Loại URL trùng, nhóm và đếm theo tên miền | **Có — TV2** |

### A3. Câu hỏi mẫu

1. “Tìm tin tức AI hôm nay, lấy 5 kết quả.”
2. “Lấy 3 bài đăng gần đây của Elon Musk.”
3. “Nhóm các URL https://openai.com/research, https://www.openai.com/blog và https://arxiv.org/abs/2301.00001 theo tên miền.”
4. “Đọc và tóm tắt bài báo đó giúp tôi.” — thiếu URL, agent cần hỏi lại.
5. “Đăng bản tin này lên Telegram.” — agent cần xác nhận trước khi gửi.

## 3. Giải pháp

Baseline v0 dùng prompt và tool declaration ban đầu. Nhóm tối ưu theo từng giả thuyết:

- **v1 — system prompt:** bỏ các chỉ dẫn gây tự đoán thông tin, chọn sẵn tài khoản, gửi khi chưa xác nhận và luôn ép gọi một tool; bổ sung quy tắc hỏi làm rõ, xác nhận side effect và không dùng tool cho yêu cầu ngoài phạm vi research.
- **v2 — tool declaration:** làm rõ ranh giới giữa `clarify` và `send`, bắt buộc chọn `response_type=text` khi thiếu thông tin và `yes_no` khi xin xác nhận.
- **v3 — tool declaration:** bổ sung điều kiện dùng/không dùng và quy ước đối số cho các tool tìm/đọc, gồm handle, `query`, `topic`, `timeframe`, `search_type` và `limit`.
- **Tool mới:** `compare_sources` chạy cục bộ, nhận danh sách URL HTTP/HTTPS, loại trùng và nhóm theo hostname; tool trả error dict khi đầu vào không hợp lệ thay vì phát sinh exception ra ngoài.

Bằng chứng chính: [`system_prompt.md`](../../starter_v0/artifacts/system_prompt.md), [`tools.yaml`](../../starter_v0/artifacts/tools.yaml), [`version_log.csv`](../../starter_v0/artifacts/version_log.csv), [`compare_sources/tool.py`](../../starter_v0/tools/compare_sources/tool.py) và [`compare_sources/TOOL.md`](../../starter_v0/tools/compare_sources/TOOL.md).

## 4. Kết quả — PHẦN B

### B1. Version Evidence

Các run base dưới đây đều có `provider_error_cases=0` và `measured_cases=total_cases=20`. Metric so sánh là `case_accuracy`.

| Version | Changed Artifact | Hypothesis | Metric Before | Metric After | Run File |
|---|---|---|---:|---:|---|
| v0 | Baseline starter | Đo hành vi trước tối ưu | — | 65% | [`v0_B_base_openai_20261110T192210636811.json`](../../starter_v0/runs/v0_B_base_openai_20261110T192210636811.json) |
| v1 | `system_prompt.md` | Loại chỉ dẫn xấu sẽ giảm lỗi thiếu thông tin, boundary và ngoài phạm vi | 65% | 80% | [`v1_B_base_openai_20261110T195512760538.json`](../../starter_v0/runs/v1_B_base_openai_20261110T195512760538.json) |
| v2 | `tools.yaml`: `clarify`, `send` | Mô tả rõ `response_type` và xác nhận sẽ giảm lỗi đối số/boundary | 80% | 95% | [`v2_B_base_openai_20261110T195837350542.json`](../../starter_v0/runs/v2_B_base_openai_20261110T195837350542.json) |
| v3 | `tools.yaml`: các tool tìm/đọc | Điều kiện dùng và quy ước đối số rõ hơn sẽ ổn định routing/arguments | 95% | 90% | [`v3_B_base_openai_20261110T200022169324.json`](../../starter_v0/runs/v3_B_base_openai_20261110T200022169324.json) |

Run đối chứng [`v0_toolset`](../../starter_v0/runs/v0_toolset_B_base_openai_20261110T195419739192.json), chỉ thêm khai báo `compare_sources`, đạt 65% và không được tính là một vòng tối ưu. V3 **giảm từ 95% xuống 90%**, không phải chuỗi cải thiện liên tục. Với mỗi version chỉ có một lần chạy, kết quả chưa đủ để tách hoàn toàn ảnh hưởng của thay đổi prompt/tool declaration khỏi dao động của mô hình. V3 đạt tool routing 95%, argument accuracy 90% và multi-turn accuracy 83,33%.

### B2. Failure Analysis — baseline v0

| Case ID | Failure Type | Actual Tool Calls | What Failed | Fix / Hướng xử lý |
|---|---|---|---|---|
| `R03_web_news_routing` | `wrong_arg_value` | `lookup(query="AI news", topic="news", timeframe="day")` | `query` thừa từ “news” | V1/V3 quy định query chỉ chứa chủ đề |
| `R08_out_of_scope` | `out_of_scope` | `send(...)` | Dùng tool gửi để trả lời bài toán | V1 cấm gọi tool cho yêu cầu ngoài research |
| `R10_missing_handle` | `missing_info` | `timeline(screenname="sama")` | Tự đoán tài khoản chưa được cung cấp | V1 yêu cầu gọi `clarify` |
| `R11_missing_url` | `missing_info` | `fetch(url="https://example.com/article")` | Tự bịa URL | V1/V2 yêu cầu hỏi URL với `response_type=text` |
| `R12_confirm_before_send` | `wrong_boundary` | `send(...)` | Gửi khi chưa có xác nhận | V1/V2 thêm boundary; v3 vẫn chưa giải quyết dứt điểm |
| `R13_parallel_web_and_tweets` | `wrong_arg_value` | `lookup(...)` + `social_search(...)` | `lookup.query` thừa “news”, thiếu `topic=news` | V3 làm rõ `query` và `topic` |
| `R14_out_of_scope_coding` | `out_of_scope` | `send(...)` | Dùng `send` để trả lời yêu cầu viết code | V1 giới hạn phạm vi dùng tool |

Ở v3, hai case base còn thất bại là `R12_confirm_before_send` (`clarify` dùng `response_type=text` thay vì `yes_no`) và `M06_switch_tool` (gọi thừa `social_search`). Việc model chọn đúng tool không bảo đảm API ngoài đã thực thi thành công; hai khía cạnh này cần được đánh giá riêng.

### B3. Team Eval Cases

Bộ [`eval_group.json`](../../starter_v0/data/eval_group.json) có đúng 10 case, gồm 5 single-turn và 5 multi-turn; hai case `G01` và `GM01` kiểm tra tool mới `compare_sources`. Run chính thức: [`v3_B_group_openai_20261111T010903669307.json`](../../starter_v0/runs/v3_B_group_openai_20261111T010903669307.json).

Kết quả run: **10/10 measured, 0 provider errors, 6/10 passed, case accuracy 60%, tool routing 80%, argument accuracy 60%, multi-turn accuracy 80%**.

| Case ID | Loại | Expected Tool/Behavior | Result | Phân tích |
|---|---|---|---|---|
| `G01_compare_sources_urls` | Single | `compare_sources` với 3 URL | **PASS** | Đúng tool và danh sách URL |
| `G02_lookup_ai_news` | Single | `lookup(query, topic=news, timeframe=week)` | **FAIL** | Gọi `papers` thay vì `lookup` |
| `G03_social_search_latest` | Single | `social_search(..., search_type=Latest, limit=5)` | **FAIL** | Đúng tool nhưng thiếu `search_type=Latest`; query là “MQTT IoT công nghiệp”, khác chuỗi expected “MQTT trong IoT công nghiệp” |
| `G04_missing_url_fetch` | Single | `clarify` hỏi URL, `response_type=text` | **FAIL (exact-match)** | Hành vi đúng: gọi `clarify` và hỏi URL; chỉ câu hỏi khác chuỗi expected |
| `G05_out_of_scope_code` | Single | Không gọi tool | **PASS** | Không lạm dụng tool cho yêu cầu lập trình |
| `GM01_compare_sources_after_context` | Multi | `compare_sources` với 2 URL từ ngữ cảnh | **PASS** | Giữ đúng URL qua nhiều lượt |
| `GM02_clarify_then_timeline` | Multi | `timeline(screenname=sama, limit=5)` | **PASS** | Dùng đúng thông tin được bổ sung |
| `GM03_clarify_then_fetch` | Multi | `fetch` với URL được bổ sung | **PASS** | Không tự đoán URL |
| `GM04_carry_timeframe` | Multi | Chỉ `lookup` cho `robotics`, giữ `news/day` | **FAIL** | Gọi thêm `lookup` cho AI bên cạnh lần gọi đúng cho robotics; expected chỉ có robotics |
| `GM05_correct_timeline_account_and_limit` | Multi | `timeline(screenname=elonmusk, limit=3)` | **PASS** | Cập nhật limit, giữ đúng tài khoản |

`G04` cho thấy hạn chế của exact-match: “Bạn gửi URL của bài báo cần đọc được không?” và “Bạn vui lòng cung cấp URL của bài báo mà bạn muốn tôi đọc và tóm tắt?” tương đương về mục đích, nhưng evaluator so sánh nguyên chuỗi nên đánh FAIL. Kết quả chính thức vẫn giữ 60%; không tự điều chỉnh điểm sau review thủ công. Với `GM04`, evaluator cũng yêu cầu đúng tập tool call đã khai báo, nên lần gọi thêm cho AI bị tính là lỗi dù lần gọi robotics có đủ đối số. Các case làm rõ và multi-turn nên được chấm thêm theo ngữ nghĩa hoặc theo từng lượt, thay vì chỉ so khớp chuỗi/tập lời gọi toàn cục.

Run group mang nhãn `v3` nhưng có artifact `v3+pa222298fee1f+t835a46557e5a`, khác artifact của base v3 là `v3+pb3e117c056e0+t2e1477d7c969`. Hash được tính trên bytes nên có thể đổi do line ending; đồng thời `tools.yaml` tại thời điểm chạy group có chỉnh sửa working tree. Vì vậy, run group là bằng chứng hợp lệ về tính đầy đủ và lỗi provider, nhưng không nên được diễn giải là chạy trên byte-identical artifact với base v3. Cần đóng băng và commit artifact trước các lần đánh giá tiếp theo.

### B4. Live Chat Evidence

Repository chưa có `starter_v0/transcripts/*.transcript.json` thực tế; file dưới `starter_v0/samples/transcripts/` chỉ là mẫu và không được dùng làm bằng chứng. Nhóm chưa có bằng chứng cho ba luồng bắt buộc: yêu cầu thường; thiếu thông tin rồi bổ sung; yêu cầu gửi/đăng có xác nhận.

| Turn | User Request | Tool Calls | Version Evidence | Outcome |
|---|---|---|---|---|
| 1 | Yêu cầu tìm kiếm thông thường | Chưa có | v3 | Chưa có transcript |
| 2 | Thiếu URL, sau đó bổ sung | Chưa có | v3 | Chưa có transcript |
| 3 | Yêu cầu gửi/đăng | Chưa có | v3 | Chưa có transcript xác nhận trước side effect |

### B5a. Required Evidence — tool mới, unit test, UI

| Item | Evidence File | What Worked | Risk / Guardrail |
|---|---|---|---|
| Tool mới | [`tool.py`](../../starter_v0/tools/compare_sources/tool.py), [`TOOL.md`](../../starter_v0/tools/compare_sources/TOOL.md), [`tools/__init__.py`](../../starter_v0/tools/__init__.py) | Nhóm URL theo domain, loại trùng, trả error dict cho đầu vào xấu | Chỉ nhận URL HTTP/HTTPS tuyệt đối; không gọi mạng |
| Unit test tool mới | [`test_tools_todo.py`](../../starter_v0/tests/test_tools_todo.py) | 12 test case tham số hóa cho happy path, input sai, URL/host/port lỗi | 14 test TODO của starter vẫn skip |
| Toàn bộ pytest | Kết quả chạy trên máy người dùng | **79 passed, 14 skipped, 0 failed trong 0,59 giây** | Chưa có file log pytest lưu trong repo; phiên rà soát hiện tại thiếu package `pytest` nên không tái chạy độc lập |
| Tool contract | [`test_tool_contract.py`](../../starter_v0/tests/test_tool_contract.py) | Kiểm tra tên, chữ ký hàm, schema, tài liệu và tool trong eval | Kết quả nằm trong tổng pytest; chưa có log riêng |
| UI | Chưa có | Chưa xác nhận | Cần code, dependency, lệnh chạy và link public |

Unit test phát hiện lỗi triển khai mà eval tool-calling không bao phủ, chẳng hạn URL có port sai hoặc input sai kiểu. Ngược lại, group eval đo khả năng model chọn tool và đối số, không chứng minh mọi nhánh code của tool đều đúng.

### B5. Bonus Evidence

Nhóm chưa cung cấp đủ bằng chứng cho bonus: chưa có local-model run, không có bốn tool mới, chưa có transcript gửi Telegram thật sau xác nhận, và toàn suite vẫn còn 14 test skip. Không tự ghi nhận điểm bonus.

### B7. Small Local Model Challenge (bonus)

Chưa thực hiện.

## 5. Khó khăn và cách xử lý

- Mô tả tool ban đầu mơ hồ, dẫn đến nhầm routing, thiếu đối số và vi phạm boundary của `send`. Nhóm tách thay đổi thành ba giả thuyết và lưu run cho từng version.
- Kết quả v3 thấp hơn v2. Nhóm ghi nhận regression `M06_switch_tool` và lỗi `R12_confirm_before_send`, không mô tả đây là cải thiện liên tục.
- Run group bộc lộ lỗi routing giữa `lookup` và `papers`, thiếu `search_type`, lời gọi thừa trong multi-turn và độ cứng của exact-match. Các lỗi hành vi được tách khỏi lỗi so khớp chuỗi.
- Artifact hash của base v3 và group v3 khác nhau. Vòng sau cần chuẩn hóa line ending, commit cấu hình, kiểm tra hash rồi mới chạy để tăng khả năng tái lập.
- UI, live transcript và log pytest chưa được lưu thành artifact; các mục này được giữ ở trạng thái chưa hoàn thành thay vì suy diễn từ file mẫu hoặc mô tả.

## 6. Tổng hợp đóng góp

| Thành viên | Đóng góp có bằng chứng | Bằng chứng |
|---|---|---|
| TV1 — Triệu Hải Đăng Trình | Thiết lập thông tin/phân công nhóm, lập biên bản G1 và tổng hợp/kiểm tra báo cáo | [`TEAM.md`](../../TEAM.md), [`G1_TV1_to_TV3.md`](../../G1_TV1_to_TV3.md), commit `2ebd720`; [báo cáo cá nhân](2A202603874_TrieuHaiDangTrinh.md) |
| TV2 — Ngô Duy Khánh | Viết `compare_sources`, tài liệu, unit test và đăng ký tool | commits `925aac1`, `cf70685`; [báo cáo cá nhân](2A202603870_NgoDuyKhanh.md) |
| TV3 — Nguyễn Đình Minh | Chạy baseline, phân tích lỗi, tối ưu v1–v3 và lưu run/version log | commits `cd4a7e9`, `dd0c808`; [báo cáo cá nhân](2A202603898_NguyenDinhMinh.md) |
| TV4 — Nguyễn Hồng Thắng | Xây dựng 10 group eval case và cập nhật khai báo tool | commit `8cd569a`; [báo cáo cá nhân](2A202603829_NguyenHongThang.md) |

Việc TV1 tổng hợp số liệu từ run không được tính là trực tiếp tạo tool, thiết kế eval case hoặc thực hiện các vòng tối ưu của thành viên khác. Báo cáo cá nhân TV4 còn nội dung mẫu/chưa đủ bằng chứng tự đánh giá; `TEAM.md` cũng vẫn đánh dấu tên TV3 và TV4 là chưa xác nhận, nên cần chính thành viên kiểm tra trước khi nộp.

## 7. Hạn chế và hướng cải thiện — B6. Reflection

- Quy tắc tổng quát như không bịa thông tin, không lạm dụng tool và xác nhận trước side effect thuộc `system_prompt.md`; điều kiện dùng tool và quy ước đối số thuộc `tools.yaml`.
- `G04` cần review ngữ nghĩa vì exact-match câu hỏi không phản ánh đúng hành vi làm rõ. `GM04` cần review theo từng lượt để xác định việc thực hiện cả yêu cầu cũ và mới là thừa hay là hoàn thành ngữ cảnh.
- Chỉ một run cho mỗi version chưa đủ đánh giá độ ổn định. Vòng sau nên chạy lặp cùng cấu hình đã đóng băng, báo cáo trung bình và độ biến thiên.
- Giả thuyết tiếp theo nên tập trung riêng vào boundary `clarify`/`send`, phân biệt rõ `papers` với `lookup`, bắt buộc `search_type` khi người dùng yêu cầu “mới nhất”, và tránh gọi lại nguồn người dùng đã bỏ.
- Evaluable behavior nên ưu tiên predicate hoặc semantic matching cho câu hỏi làm rõ; exact-match chỉ phù hợp với đối số định danh, enum và giá trị cần chính xác.

## 8. Tài liệu tham khảo

- [`CHECKPOINTS.md`](../../CHECKPOINTS.md), [`RUBRIC.md`](../../RUBRIC.md), [`SUBMISSION.md`](../../SUBMISSION.md).
- [`version_log.csv`](../../starter_v0/artifacts/version_log.csv) và các run JSON trong [`starter_v0/runs/`](../../starter_v0/runs/).
- [`eval_group.json`](../../starter_v0/data/eval_group.json), mã nguồn tool và các unit test trong `starter_v0/`.
