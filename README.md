# HP-AT01 — PMIC Automated Test Software

Phần mềm tự động test feature & performance cho PMIC trên bench:
PSU, electronic load, oscilloscope, DMM (PyVISA) và I2C/GPIO qua FT232H (`ftd2xx`).

- Tài liệu dự án: [`docs/`](docs/) — bắt đầu từ `docs/PRD.md`, `docs/ARCHITECTURE.md`.
- **Hướng dẫn sử dụng:** [`docs/USER_MANUAL.md`](docs/USER_MANUAL.md).
- Tài liệu thiết bị / tập lệnh: [`docs/instruments/`](docs/instruments/).

## Yêu cầu

- Python 3.12 (tối thiểu 3.10)
- Windows 11 (máy bench), có internet khi cài đặt
- NI-VISA (cho GPIB/USB-TMC), driver D2XX (cho FT232H)

## Cài đặt

Windows (PowerShell):

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -U pip
pip install -r requirements.txt
```

Linux/macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Chạy

```powershell
python -m hpat --help
python -m hpat list-tests
python -m hpat run hpat\plans\<plan>.csv --dut-sn SN12345
```

## Cấu hình

Sửa `config/instruments.yaml`: resource VISA, GPIB address, kênh scope, shunt DMM và
giới hạn an toàn. Các resource hiện là placeholder — điền theo bench thật.

## Phát triển

```powershell
pytest
ruff check .
ruff format .
```

## Trạng thái

Đang ở giai đoạn khởi tạo (T01). Xem `docs/TASKS.md` và `docs/PROGRESS.md`.
