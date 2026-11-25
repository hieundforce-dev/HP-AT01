# PROGRESS — HP-AT01

> Tài liệu dự án nằm trong `docs/`. File này và `TASKS.md` được cập nhật mỗi phiên.

## Trạng thái hiện tại

- **T03 hoàn thành.** `hpat bench-check --sim` báo OK 7/7 role; driver base có retry + log SCPI.
- Đang chờ bắt đầu **T04 — FT232H: I2C + GPIO (ftd2xx/MPSSE)**.
- `run` vẫn dừng ở "not implemented (T05)" sau preflight; `sim`/`validate` chưa làm.

## Đã hoàn thành

- Vòng 1 — PRD: mục tiêu, phạm vi 8 test item, DUT 1–7 rail (0.5–12 V, 1–20 A), input CSV
  (có cột `repeat`), output CSV + PNG.
- Vòng 2 — Architecture: Python 3.12/.venv, Typer+Rich, PyVISA, `ftd2xx` + MPSSE, pydantic,
  matplotlib, file-based output, sim mode.
- Vòng 3 — Design: CLI 5 lệnh, cấu trúc `runs/<timestamp>/`, CSV UTF-8 BOM không làm tròn,
  waveform lấy bằng SCPI scope, log format.
- Vòng 4 — Rules: ruff, pytest ≥70% core, safety interlocks, cấm hard-code địa chỉ thiết bị.
- **T01:** `.venv`, `requirements.txt` (8 runtime + 3 dev deps), `pyproject.toml` (ruff, pytest,
  `pythonpath`), `.gitignore`, `git init` (chưa commit), `hpat/{__init__,__main__,cli}.py`,
  3 smoke test CLI.
- **T02:** `hpat/core/{errors,config,logging_setup,runfolder}.py`; `config/instruments.yaml`
  (7 role + safety); `run` preflight tạo run folder + log; 23 test pass.
  Thêm dependency `pyyaml` (cần cho YAML config).
- **T03:** `hpat/drivers/{base,registry}.py`, `hpat/drivers/sim/`, `hpat/core/bench.py`;
  `bench-check` in bảng trạng thái, exit code 0/1; 43 test pass.
- **Tài liệu:** `docs/USER_MANUAL.md` (cài đặt, cấu hình, lệnh, output, an toàn, xử lý sự cố).

## Lỗi / Blocker

1. ~~PSU GPD-3303S chỉ 3 A/kênh~~ → **đã chốt:** kẹp 3 A, WARN, ghi `notes` (ADR-12).
2. ~~FT232H dùng pyftdi/libusb~~ → **đã chốt:** dùng `ftd2xx` (D2XX) + MPSSE tự viết (ADR-11).
3. Chưa có SCPI manual của e-load 3315D và PSU GPD-3303S → driver dùng command map YAML,
   hoàn thiện khi có tài liệu trong `docs/instruments/raw/`.
4. Chưa có resource VISA / GPIB address thực tế của bench → điền vào `config/instruments.yaml` ở T16.

## Bước tiếp theo

- Làm **T04 — FT232H: I2C + GPIO (ftd2xx/MPSSE)**.

## Ghi chú môi trường

- Máy phát triển hiện tại: Linux, Python 3.10.12, không có `python3-venv`/pip hệ thống →
  đã dùng `get-pip.py --user` + `virtualenv` để tạo `.venv` (chỉ để chạy thử).
- Máy bench mục tiêu: Windows 11 + Python 3.12; dùng `python -m venv .venv` theo README.
- Code viết tương thích Python ≥ 3.10 (`from __future__ import annotations`).

## Nhật ký

| Ngày | Task | Thay đổi |
|---|---|---|
| 2026-11-25 | — | Tạo PRD, ARCHITECTURE, DESIGN, RULES, TASKS, PROGRESS |
| 2026-11-25 | — | Gom 6 file tài liệu vào `docs/`, cập nhật đường dẫn tham chiếu |
| 2026-11-25 | — | Chuyển guide vào `docs/`; tạo `docs/instruments/{raw,processed}` + README quy ước |
| 2026-11-25 | — | Chốt: kẹp PSU 3 A (ADR-12), FT232H dùng `ftd2xx`/MPSSE (ADR-11) |
| 2026-11-25 | T01 | Khung project, CLI 5 lệnh stub, cấu hình ruff/pytest, `.venv`, 3 smoke test pass |
| 2026-11-25 | T02 | Config pydantic + `instruments.yaml`, logging file, run folder, 23 test pass |
| 2026-11-25 | T03 | Driver base (retry + SCPI log), 7 sim driver, `bench-check`, 43 test pass |
| 2026-11-25 | — | Thêm `docs/USER_MANUAL.md` |
