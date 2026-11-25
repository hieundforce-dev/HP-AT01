# RULES — HP-AT01

## Quy tắc code

| Mục | Quy định |
|---|---|
| Ngôn ngữ comment / docstring | English |
| Ngôn ngữ tài liệu `.md` | Tiếng Việt |
| Đặt tên | `snake_case` cho hàm/biến/module, `PascalCase` cho class, hằng số `UPPER_CASE` |
| Type hints | Bắt buộc ở public API (core, drivers, plugin) |
| Docstring | Google style, mô tả đơn vị tham số đo |
| Format / lint | `ruff format .` + `ruff check .`, line length 100 |
| Test | `pytest`; unit test cho parser / evaluator / runner / limits; integration qua `sim` |
| Coverage | ≥ 70% cho `hpat/core/`; không bắt buộc với `hpat/drivers/` |
| Dependency | Chỉ thêm khi đã được duyệt; pin trong `requirements.txt` |

## Quy tắc an toàn thiết bị (bắt buộc)

1. Luôn set **current limit / OCP** trước khi bật output PSU.
2. Luôn tắt output PSU và e-load trong `finally`, kể cả khi exception hoặc Ctrl+C.
3. Validate `Vset ≤ Vmax rail`, `Iset ≤ Imax rail`, công suất ≤ giới hạn thiết bị **trước** khi gửi lệnh.
4. E-load chỉ chạy đúng mode (CC/CV/CR/CP) khai báo trong plan.
5. Thứ tự power-up / power-down theo `config/instruments.yaml`, không tuỳ tiện.
6. **Không bao giờ** tự nâng limit, bỏ qua limit, hoặc sửa kết quả để test "pass".
7. Không gửi lệnh thay đổi trạng thái thiết bị khi chưa nằm trong một test case hợp lệ.
8. Nếu dòng vào yêu cầu > `max_current` của PSU (GPD-3303S: 3 A): **kẹp ở `max_current`**, in WARN,
   ghi `notes` = `PSU current clamped to 3.0 A` trong CSV. Không âm thầm chạy sai điều kiện.

## AI tuyệt đối KHÔNG được

- Tự ý đổi tech stack, thư viện hoặc cấu trúc thư mục.
- Xoá hoặc ghi đè file không liên quan tới task.
- Thêm dependency mới mà không hỏi.
- Tự đoán yêu cầu khi thông tin chưa rõ.
- Làm nhiều task cùng lúc trong một lần.
- Commit / push khi chưa được yêu cầu.
- Hard-code địa chỉ VISA, GPIB address, hay địa chỉ register PMIC trong code test item
  (phải qua `config/instruments.yaml` hoặc file plan).
- Viết/sửa driver khi chưa đọc tài liệu tương ứng trong `docs/instruments/processed/`
  (hoặc `raw/` nếu chưa xử lý); lệnh mới dùng phải được ghi lại vào `processed/`.
- Bỏ qua bước tắt output khi thiết kế luồng lỗi.

## Git

- Chỉ commit khi được yêu cầu.
- Conventional Commits: `feat|fix|test|docs|refactor(scope): mô tả`.
- Không commit `runs/`, `.venv/`, file log.

## Lệnh chuẩn

```powershell
.venv\Scripts\activate
python -m hpat --help
python -m hpat run hpat\plans\efficiency_buck1.csv --dut-sn SN12345
python -m hpat bench-check
pytest
ruff check .
ruff format .
```

## Definition of Done

- [ ] Code chạy được, không lỗi import/lint.
- [ ] Đúng Acceptance Criteria của task trong `docs/TASKS.md`.
- [ ] Có test cho logic mới (hoặc chạy được qua `sim`).
- [ ] Không vi phạm quy tắc an toàn thiết bị.
- [ ] Đã cập nhật `docs/PROGRESS.md`.
