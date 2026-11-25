# ARCHITECTURE — HP-AT01

## Tech stack

| Thành phần | Công nghệ | Lý do chọn |
|---|---|---|
| Ngôn ngữ | Python 3.12 | Yêu cầu dự án; hệ sinh thái đo lường tốt |
| Môi trường | `.venv` + pip, `requirements.txt` | Đơn giản, đúng yêu cầu, dễ tái lập trên máy bench |
| CLI | Typer + Rich | Subcommand rõ ràng, progress bar, bảng tổng hợp |
| Instrument I/O | PyVISA (+ NI-VISA backend) | Chuẩn cho USB-TMC / GPIB / LAN |
| FT232H | ftd2xx (D2XX driver) + MPSSE helper tự viết cho I2C/GPIO | Yêu cầu dự án; không cần Zadig/WinUSB |
| Xử lý số liệu | numpy, pandas | Quét sweep, thống kê theo repeat, ghi CSV |
| Validate schema | pydantic v2 | Mỗi test item khai báo schema CSV riêng, báo lỗi rõ |
| Waveform | matplotlib | Vẽ PNG từ dữ liệu `CURVe?` của scope |
| Log | logging (stdlib) | Không thêm dependency; file + console |
| Test | pytest, pytest-mock | Unit test core + integration qua sim |
| Lint/format | ruff | Một tool cho cả lint và format |

## Cấu trúc thư mục

```text
HP-AT01/
├── hpat/
│   ├── __main__.py              # entry point: python -m hpat
│   ├── cli.py                   # Typer app: run / list-tests / validate / bench-check / sim
│   ├── core/
│   │   ├── config.py            # pydantic model cho instruments.yaml
│   │   ├── bench.py             # mở/đóng thiết bị, safety shutdown
│   │   ├── plugin.py            # BaseTest, registry, TestContext, TestResult
│   │   ├── runner.py            # plan → cases → repeat → measure → results
│   │   ├── results.py           # ghi CSV, tổng hợp mean/min/max/stddev
│   │   ├── limits.py            # đánh giá Pass/Fail
│   │   ├── waveform.py          # render PNG từ dữ liệu scope
│   │   ├── runfolder.py         # tạo runs/<timestamp>_<plan>_<sn>/
│   │   ├── logging_setup.py
│   │   └── errors.py
│   ├── drivers/
│   │   ├── base.py              # VisaInstrument: query/write, retry, log SCPI
│   │   ├── gwinstek_gpd3303s.py
│   │   ├── eload_3315d.py       # SCPI command map từ config
│   │   ├── tektronix_tbs2204b.py
│   │   ├── dmm_ut8805e.py
│   │   ├── dmm_keithley2000.py  # dùng chung cho K2000/K2100
│   │   ├── ft232h_mpsse.py       # MPSSE engine (clock, bit-bang) trên ftd2xx
│   │   ├── ft232h_i2c.py        # I2C master: start/stop/address/read/write ACK
│   │   ├── ft232h_gpio.py
│   │   └── sim/                 # thiết bị giả lập (deterministic)
│   ├── tests/                   # plugin test item
│   │   ├── efficiency.py
│   │   ├── line_reg.py
│   │   ├── load_reg.py
│   │   ├── ripple.py
│   │   ├── transient.py
│   │   ├── startup.py
│   │   ├── protection.py
│   │   └── i2c_reg.py
│   └── plans/                   # CSV mẫu cho từng test item
├── config/
│   └── instruments.yaml         # resource VISA, GPIB addr, kênh scope, command map
├── tests/                       # pytest
├── runs/                        # output (gitignore)
├── pyproject.toml               # ruff + pytest config
├── requirements.txt
├── README.md
└── docs/                        # tài liệu dự án
    ├── PRD.md
    ├── ARCHITECTURE.md
    ├── DESIGN.md
    ├── RULES.md
    ├── TASKS.md
    ├── PROGRESS.md
    ├── USER_MANUAL.md
    ├── vibe-coding-agent-guide.md
    └── instruments/             # tài liệu điều khiển thiết bị
        ├── raw/                 # PDF/manual gốc
        └── processed/           # Markdown đã xử lý (command map, giới hạn an toàn)
```

## Luồng dữ liệu

```text
CLI (hpat run plan.csv)
  → load config/instruments.yaml (pydantic)
  → Bench.open()  [PSU, e-load, scope, DMM, FT232H]
  → TestPlugin.parse_plan(plan.csv)  [validate từng dòng bằng schema riêng]
  → for case in cases:
       for run_index in 1..repeat:
           apply register_writes (I2C)
           set điều kiện (PSU V/I, e-load mode)
           settle
           measure (DMM / scope / e-load readback)
           waveform? → lưu PNG
           evaluate limits → PASS/FAIL
           append row → results/<test_item>.csv
  → aggregate (mean/min/max/stddev)
  → summary table (console) + logs/run.log
  → Bench.close()  [luôn tắt output, kể cả exception]
```

## Data model

Không dùng database. Các entity là dataclass/pydantic:

| Entity | Trường chính |
|---|---|
| `InstrumentConfig` | `name`, `driver`, `resource` (VISA), `options` (baud, gpib_addr, kênh, shunt) |
| `TestCase` | `test_id`, `rail`, `repeat`, điều kiện đo (Vin/Vout/Iout/duration/sweep…), `limit_min/max`, `register_writes` |
| `Measurement` | `run_index`, `timestamp`, `values{name: (value, unit)}`, `pass_fail`, `notes` |
| `RunFolder` | `runs/<YYYY-MM-DD_HHMMSS>_<plan>_<dut_sn>/` chứa `results/`, `waveforms/`, `logs/`, `plan_copy.csv` |
| `TestResult` | `test_id`, `rows[]`, `artifacts[]` (PNG), `aggregate` |

**Quan hệ:** 1 RunFolder → N TestResult → N Measurement (mỗi repeat 1 dòng).

## Hợp đồng plugin

```python
class BaseTest(ABC):
    name: ClassVar[str]                       # "efficiency", "ripple", ...
    plan_schema: ClassVar[type[BaseModel]]    # schema CSV riêng của test này

    @abstractmethod
    def run(self, ctx: TestContext) -> TestResult: ...
```

- Đăng ký bằng `@register_test` → `hpat list-tests` tự thấy.
- `TestContext` cấp: `bench` (thiết bị), `case`, `run_index`, `run_folder`, `logger`.
- Thêm test mới: tạo file trong `hpat/tests/`, khai báo schema + `run()`, thêm 1 dòng import
  trong `hpat/tests/__init__.py`. **Không sửa runner.**

## Quyết định kiến trúc (ADR)

| # | Quyết định | Lý do |
|---|---|---|
| ADR-01 | Mỗi test item có schema CSV riêng, không dùng 1 bảng CSV chung | Yêu cầu người dùng; mỗi bài test có tham số khác nhau, tránh CSV 50 cột rỗng |
| ADR-02 | Output lõi dùng chung cột chuẩn + cột riêng từng test | Đủ để gộp/so sánh, vẫn linh hoạt |
| ADR-03 | Không DB, chỉ `runs/<timestamp>/` | Đơn giản, dễ copy/share log; SQLite để sau nếu cần |
| ADR-04 | Waveform lấy bằng SCPI (`CURVe?` + preamble) rồi vẽ matplotlib | Ảnh có tiêu đề/limit/annotation theo chuẩn chung, không phụ thuộc screenshot scope |
| ADR-05 | SCPI command map đặt trong YAML | 3315D/GPD chưa có manual đầy đủ; đổi lệnh không cần sửa code |
| ADR-06 | Sim driver song song với driver thật | Code/test được toàn bộ pipeline khi không có bench; CI chạy được |
| ADR-07 | Đo analog bằng DMM, không dùng FT232H | FT232H không có ADC |
| ADR-08 | Safety layer trong `Bench` (context manager + finally) | Không thể để output bật khi crash |
| ADR-09 | Chạy tuần tự, 1 tiến trình | Tránh tranh chấp VISA/GPIB; đủ nhanh cho quy mô 7 rail |
| ADR-10 | Log stdlib, không loguru | Giảm dependency, đủ nhu cầu |
| ADR-11 | FT232H dùng **ftd2xx (D2XX)** + MPSSE tự viết, không dùng pyftdi/libusb | Yêu cầu dự án; tránh Zadig/WinUSB; đổi lại phải tự cài đặt I2C master trên MPSSE |
| ADR-12 | Dòng vào PSU vượt 3 A → **kẹp ở 3 A**, chạy tiếp + cảnh báo, không fail case | GPD-3303S giới hạn 3 A/kênh; vẫn thu được dữ liệu, ghi rõ trong kết quả để không hiểu nhầm |

## Rủi ro kỹ thuật

| Rủi ro | Ảnh hưởng | Giảm thiểu |
|---|---|---|
| GPD-3303S chỉ 3 A/kênh | Không test được rail 20 A | Validate `Iset` theo `max_current` trong config; cảnh báo rõ; chờ PSU mới |
| FT232H cần driver D2XX | VCP và D2XX không bind cùng lúc | README hướng dẫn cài D2XX (CDM) và gỡ VCP cho thiết bị; `bench-check` báo lỗi rõ |
| PSU 3 A/kênh | Không đạt dòng vào yêu cầu | Kẹp 3 A, WARN trên console, ghi `notes` trong CSV |
| SCPI 3315D chưa rõ | Driver sai lệnh | Command map YAML + sim test trước |
| GPIB NI-VISA | Resource string khác nhau | `bench-check` liệt kê resource; config hoá |
| Scope 4 kênh, nhiều rail | Thiếu kênh đo đồng thời | Giới hạn số tín hiệu/1 lần chạy; ghi rõ trong plan |
