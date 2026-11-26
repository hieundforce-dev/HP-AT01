# USER MANUAL — HP-AT01

Hướng dẫn sử dụng phần mềm test tự động PMIC (HP-AT01) trên bench.
Tài liệu kỹ thuật nội bộ: [`ARCHITECTURE.md`](ARCHITECTURE.md), [`DESIGN.md`](DESIGN.md).

---

## 1. Phần mềm làm gì

- Chạy các bài test PMIC theo **file CSV** (mỗi bài test một format riêng).
- Điều khiển PSU, electronic load, oscilloscope, DMM qua **PyVISA**; I2C/GPIO qua **FT232H (ftd2xx)**.
- Xuất **CSV kết quả** + **ảnh waveform PNG** vào một thư mục run riêng.
- Chạy được **chế độ giả lập (sim)** khi không có bench.

## 2. Trạng thái phiên bản

Bản hiện tại đã xong T01–T04 (xem [`TASKS.md`](TASKS.md)).

| Lệnh | Trạng thái |
|---|---|
| `hpat --help`, `--version` | ✅ hoạt động |
| `hpat list-tests` | ✅ hoạt động (chưa có test item nào) |
| `hpat bench-check [--sim]` | ✅ hoạt động (FT232H thật đã có; PSU/e-load/scope/DMM ở T07–T09) |
| `hpat run <plan.csv>` | ⚠️ mới chạy **preflight** (kiểm config + tạo run folder), chưa đo |
| `hpat sim <plan.csv>` | ⏳ chưa triển khai (T05) |
| `hpat validate <plan.csv>` | ⏳ chưa triển khai (T05) |

## 3. Yêu cầu hệ thống

| Hạng mục | Yêu cầu |
|---|---|
| OS | Windows 11 (máy bench) |
| Python | 3.12 khuyến nghị (tối thiểu 3.10) |
| Phần mềm | NI-VISA + NI-488.2 (GPIB), driver D2XX cho FT232H |
| Kết nối | PSU USB, e-load GPIB (NI GPIB-USB-HS), scope USB/LAN, DMM USB |

## 4. Cài đặt

### 4.1 Windows

```powershell
cd HP-AT01

python -m venv .venv
.venv\Scripts\Activate.ps1

pip install -U pip
pip install -r requirements.txt
pip install -e .          # tạo lệnh `hpat`
```

Nếu PowerShell chặn script:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.venv\Scripts\Activate.ps1
```

Không muốn activate:

```powershell
.venv\Scripts\python.exe -m hpat --help
```

### 4.2 Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install -e .
```

### 4.3 VS Code

1. `File → Open Folder…` → chọn thư mục `HP-AT01`.
2. `Ctrl+Shift+P` → **Python: Select Interpreter** → chọn `.venv`.
3. Mở Terminal trong VS Code và chạy lệnh `hpat ...`.

### 4.4 Driver thiết bị

| Thiết bị | Cần cài | Kiểm tra |
|---|---|---|
| Tất cả VISA | NI-VISA (kèm NI MAX) | `python -m visa info` |
| E-load GPIB | NI-488.2 + GPIB-USB-HS | NI MAX → Devices |
| FT232H | FTDI D2XX (CDM) | `python -c "import ftd2xx; print(ftd2xx.listDevices())"` |
| FT232H | **Gỡ VCP** cho thiết bị FT232H (D2XX và VCP không bind cùng lúc) | Device Manager |

## 5. Cấu hình bench

File: `config/instruments.yaml`. Sửa resource theo bench thật.

```yaml
simulation: false

instruments:
  psu:
    driver: gwinstek_gpd3303s
    resource: "ASRL3::INSTR"      # COM3 nếu dùng cổng ảo
    options:
      channel: 1
      baud_rate: 9600
      max_voltage_v: 30.0         # CH1/CH2: 0-30 V
      max_current_a: 3.0          # CH1/CH2: 3 A

  eload:
    driver: prodigit_3315g
    resource: "GPIB0::5::INSTR"   # địa chỉ GPIB đặt trên mặt máy
    options: {module: 3315G, gpib_address: 5, max_current_a: 15.0, max_power_w: 75.0}

  scope:
    driver: tektronix_tbs2204b
    resource: "USB0::0x0699::0x0000::C000000::INSTR"

  dmm_vin:  {driver: dmm_ut8805e,      resource: "USB0::...::INSTR"}
  dmm_vout: {driver: dmm_keithley2000, resource: "USB0::...::INSTR"}
  dmm_iout: {driver: dmm_keithley2100, resource: "USB0::...::INSTR", options: {shunt_ohm: 0.01}}

  ft232h:
    driver: ft232h
    resource: "FT232H-A"        # nhãn; chọn thiết bị bằng options bên dưới
    options:
      serial: ""                # serial D2XX; rỗng = dùng index
      index: 0
      i2c_frequency_hz: 100000
      clock_stretching: false   # true: bật adaptive clocking (xem mục FT232H)
      timeout_s: 2.0

safety:
  max_voltage_v: 12.0
  max_current_a: 15.0
  max_power_w: 75.0
  settle_ms_default: 200
  power_up_order: [psu, eload]
  power_down_order: [eload, psu]
```

### Các role

| Role | Bắt buộc | Ý nghĩa |
|---|---|---|
| `psu` | ✅ | Nguồn lập trình |
| `eload` | ✅ | Electronic load |
| `scope` | ✅ | Oscilloscope |
| `ft232h` | ✅ | Cầu I2C/GPIO |
| `dmm_vin` | ➖ | DMM đo điện áp vào |
| `dmm_vout` | ➖ | DMM đo điện áp ra |
| `dmm_iout` | ➖ | DMM đo dòng qua shunt |

### Khóa cấu hình

| Khóa | Ý nghĩa |
|---|---|
| `simulation` | `true` → luôn dùng thiết bị giả lập |
| `instruments.<role>.driver` | Tên driver (xem bảng role ở trên) |
| `instruments.<role>.resource` | Resource VISA / serial FTDI |
| `instruments.<role>.options` | Tham số riêng (channel, gpib_address, shunt_ohm, timeout_ms…) |
| `safety.max_voltage_v` / `max_current_a` | Giới hạn tuyệt đối cho mọi rail |
| `safety.max_power_w` | Giới hạn công suất (nếu có) |
| `safety.settle_ms_default` | Thời gian chờ mặc định sau khi đổi điều kiện |
| `safety.power_up_order` / `power_down_order` | Thứ tự bật/tắt thiết bị |

Config sai sẽ báo rõ, ví dụ:

```text
Error: Invalid config 'config/instruments.yaml':
  - safety.max_voltage_v: Input should be greater than 0
```

## 6. FT232H — đấu dây và sử dụng

### 6.1 Cài driver D2XX

1. Cài **FTDI D2XX driver (CDM)** cho Windows 11 (bản có `libftd2xx`/`ftd2xx.dll`).
2. Trong Device Manager, **gỡ VCP** (Virtual COM Port) khỏi FT232H — D2XX và VCP
   không bind cùng lúc.
3. Kiểm tra:

   ```powershell
   python -c "import ftd2xx; print(ftd2xx.listDevices())"
   ```

   Không có thiết bị → kiểm tra cáp USB và driver. Lỗi `libftd2xx` → cài D2XX.

### 6.2 Đấu dây I2C

| FT232H | Nối tới | Ghi chú |
|---|---|---|
| ADBUS0 | SCL | cần pull-up 2.2k–10k lên 3.3 V |
| ADBUS1 | SDA | **nối chung với ADBUS2** tại chân SDA của DUT |
| ADBUS2 | SDA | đường đọc SDA (TDO) |
| GND | GND | mass chung với DUT |

ADBUS1 và ADBUS2 **phải nối với nhau** ở phía DUT (ADBUS1 phát, ADBUS2 đọc).
Đường SCL/SDA dùng open-drain (Drive-Zero) nên **bắt buộc có pull-up**.

GPIO dùng **ACBUS0–ACBUS7** (8 chân), mặc định là input; `set_gpio(pin, level)`
tự chuyển chân thành output. `pin` = 0–7 tương ứng ACBUS0–7.

### 6.3 API driver

```python
ft = bench.instrument("ft232h")       # Ft232hDriver
ft.i2c_write(0x50, 0x10, 0xAB)        # 7-bit address, 8-bit register
value = ft.i2c_read(0x50, 0x10)       # -> int
ft.i2c_write_bytes(0x50, 0x10, [0x01, 0x02])
data = ft.i2c_read_bytes(0x50, 0x10, 2)
found = ft.i2c_scan()                 # [0x20, 0x50, ...]
ft.set_gpio(0, True)                  # ACBUS0 = high
level = ft.read_gpio(0)               # -> bool
```

### 6.4 Clock stretching

Đặt `clock_stretching: true` để bật adaptive clocking của MPSSE. Chỉ dùng khi
DUT thực sự kéo SCL; nếu đấu dây sai, MPSSE có thể chờ SCL mãi và giao dịch bị
timeout. Mặc định tắt.

## 7. Sử dụng

### 7.1 Kiểm tra kết nối bench

```powershell
hpat bench-check --sim                 # dùng thiết bị giả lập
hpat bench-check                       # thiết bị thật
hpat bench-check --verbose             # kèm log SCPI
```

Kết quả: bảng `Role / Driver / Resource / Status / Detail`.
Exit code `0` nếu tất cả OK, `1` nếu có thiết bị lỗi.

### 7.2 Chạy test

```powershell
hpat run <plan.csv> --config config\instruments.yaml --dut-sn SN12345
```

Hiện tại lệnh này:

1. Đọc và validate config.
2. Tạo thư mục `runs\<timestamp>_<plan>_<SN>\`.
3. Ghi `logs\run.log`.
4. Dừng với thông báo `'run' is not implemented yet (T05)` và exit code `2`.

Khi các task sau hoàn thành, bước 4 sẽ được thay bằng chạy test thật.

### 7.3 Các lệnh khác

```powershell
hpat list-tests                        # danh sách test item + cột CSV
hpat validate <plan.csv>               # kiểm tra plan (T05)
hpat sim <plan.csv>                    # chạy trên bench giả lập (T05)
```

### 7.4 Exit code

| Code | Ý nghĩa |
|---|---|
| 0 | Thành công |
| 1 | Lỗi config / thiết bị / plan |
| 2 | Chức năng chưa được triển khai |

## 8. Output của một lần chạy

```text
runs/2026-11-25_143012_efficiency_buck1_SN12345/
├── plan_copy.csv        # bản sao plan đã chạy
├── results/             # CSV kết quả (mỗi lần đo 1 dòng)
├── waveforms/           # PNG waveform
└── logs/run.log         # log của run
```

- CSV: UTF-8 BOM (mở Excel không lỗi font), dấu phẩy, thập phân `.`.
- Giá trị đo **không làm tròn**; đơn vị ở cột `unit`.
- Log: `HH:MM:SS.mmm LEVEL module — message`; `--verbose` thêm SCPI TX/RX.

## 9. Test plan CSV (dự kiến)

Mỗi test item có format riêng. Ví dụ efficiency (sẽ chốt ở T10):

```csv
test_id,enabled,rail,vin_v,iout_start_a,iout_stop_a,iout_step_a,repeat,settle_ms,limit_min,limit_max,unit,register_writes
EFF_BUCK1,1,BUCK1,12.0,0.5,3.0,0.5,2,200,85.0,,%,0x21=0x1F
```

- `repeat`: số lần lặp mỗi điểm đo; kết quả có thêm `run_index`.
- `limit_min` / `limit_max`: spec để đánh giá PASS/FAIL.
- `register_writes`: ghi I2C trước khi đo, ví dụ `0x21=0x1F;0x22=0x0A`.

## 10. An toàn khi vận hành

1. Luôn set current limit trước khi bật output.
2. Output PSU và e-load luôn được tắt trong `finally` (kể cả Ctrl+C).
3. Nếu dòng vào yêu cầu > 3 A (giới hạn GPD-3303S): phần mềm **kẹp ở 3 A**,
   in WARN và ghi `notes` vào CSV. Không tự nâng limit.
4. E-load 3315G: kiểm tra cả **15 A**, **60 V** và **75 W** (P = V × I) trước khi bật.
5. Không sửa kết quả hoặc limit để test "pass".

## 11. Xử lý sự cố

| Hiện tượng | Nguyên nhân thường gặp | Cách xử lý |
|---|---|---|
| `Config file not found` | Sai đường dẫn `--config` | Kiểm tra `config/instruments.yaml` |
| `missing required instrument roles` | Thiếu role bắt buộc | Thêm `psu`/`eload`/`scope`/`ft232h` |
| `unknown instrument roles` | Gõ sai tên role | Dùng đúng tên trong bảng role |
| `no real implementation yet` | Driver thật chưa có (T03) | Dùng `--sim`, hoặc chờ T07–T09 |
| `cannot open VISA resource` | Sai resource, thiếu NI-VISA, thiết bị đang bận | Kiểm tra NI MAX, đóng phần mềm khác |
| Keithley 2100 không đo được | Tài liệu hiện có chỉ là calibration manual | Dùng UT8805E cho role đo; bổ sung manual |
| GPIB không thấy | Thiếu NI-488.2 / sai địa chỉ | Cài NI-488.2, kiểm tra address trên e-load |
| FT232H lỗi mở | Chưa cài D2XX hoặc còn VCP | Cài D2XX, gỡ VCP cho thiết bị |
| `No module named hpat` | Chưa `pip install -e .` và không đứng ở thư mục project | Cài editable hoặc `cd` vào project |
| `No module named pyvisa` | Chưa cài requirements | `pip install -r requirements.txt` |

## 12. Phát triển

```powershell
pytest
ruff check .
ruff format .
```

Quy ước code: xem [`RULES.md`](RULES.md). Tiến độ: [`PROGRESS.md`](PROGRESS.md).

## 13. Giới hạn hiện tại

- Chưa đo thật: `run`/`sim`/`validate` sẽ hoàn thiện ở T05–T15.
- Chưa có test item nào được đăng ký.
- Driver thật: FT232H đã có (T04); PSU, e-load, scope, DMM ở T07–T09.
- FT232H: chỉ hỗ trợ I2C 7-bit + register 8-bit; chưa có 10-bit/SMBus PEC.
  Clock stretching phải bật thủ công và phụ thuộc đấu dây.
- Giới hạn phần cứng: PSU 30 V/3 A × 2 kênh (sequencing tối đa 2 rail);
  e-load 3315G 15 A/60 V/75 W.
- Keithley 2100: tài liệu hiện có chỉ có lệnh calibration → chưa dùng để đo.
- Nguồn SCPI chuẩn: [`instruments/processed/`](instruments/processed/);
  `instruments/raw/` chỉ để lưu trữ PDF gốc.
