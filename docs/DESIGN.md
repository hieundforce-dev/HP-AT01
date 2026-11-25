# DESIGN — HP-AT01

Áp dụng cho CLI, output files, log và hình waveform (không có UI đồ hoạ).

## 1. CLI

```text
hpat run <plan.csv>        # chạy test
hpat sim <plan.csv>        # chạy với thiết bị giả lập
hpat validate <plan.csv>   # chỉ validate plan, không mở thiết bị
hpat list-tests            # liệt kê test item đã đăng ký + cột CSV yêu cầu
hpat bench-check           # kiểm tra kết nối tất cả thiết bị
```

Tuỳ chọn chung: `--config PATH` (mặc định `config/instruments.yaml`),
`--dut-sn TEXT` (mặc định `NA`), `--verbose` (DEBUG + raw SCPI), `--yes` (bỏ xác nhận).

**Ví dụ output console:**

```text
HP-AT01  plan=efficiency_buck1.csv  dut=SN12345  sim=False
[1/24] BUCK1  Iout=0.50A  rep=1/2   PASS  eff=87.12%      (limit >= 85.00)
[2/24] BUCK1  Iout=0.50A  rep=2/2   PASS  eff=87.09%      (limit >= 85.00)
...
┌──────────────┬───────┬────────┬────────┬────────┬────────┐
│ test_id      │ rail  │ n      │ mean   │ min    │ max    │
├──────────────┼───────┼────────┼────────┼────────┼────────┤
│ EFF_BUCK1_05 │ BUCK1 │ 2      │ 87.10% │ 87.09% │ 87.12% │
└──────────────┴───────┴────────┴────────┴────────┴────────┘
Result: 24 PASS / 0 FAIL
Output: runs/2026-11-25_143012_efficiency_buck1_SN12345/
```

## 2. Cấu trúc thư mục output

```text
runs/2026-11-25_143012_efficiency_buck1_SN12345/
├── plan_copy.csv          # bản sao plan đã chạy
├── results/
│   ├── efficiency.csv     # 1 dòng / 1 lần đo
│   └── summary.csv        # tổng hợp theo test_id
├── waveforms/
│   ├── RIPPLE_BUCK1_0001.png
│   └── ...
└── logs/
    └── run.log
```

Tên run: `runs/<YYYY-MM-DD_HHMMSS>_<plan-stem>_<dut-sn>/`.

## 3. Định dạng CSV

- Encoding **UTF-8 with BOM**, phân cách `,`, thập phân `.`.
- Timestamp: ISO-8601 giờ local, ví dụ `2026-11-25T14:30:12.345`.
- **Không làm tròn** giá trị đọc từ thiết bị; ghi full precision.
- Đơn vị để cột riêng `unit`.

**Cột lõi (mọi test item):**

| Cột | Ví dụ |
|---|---|
| `timestamp` | `2026-11-25T14:30:12.345` |
| `test_id` | `EFF_BUCK1_0500` |
| `test_item` | `efficiency` |
| `rail` | `BUCK1` |
| `run_index` | `1` |
| `condition` | `Vin=12.0;Iout=0.5` |
| `measurement` | `efficiency` |
| `value` | `87.123456` |
| `unit` | `%` |
| `limit_min` | `85.0` |
| `limit_max` | *(rỗng)* |
| `pass_fail` | `PASS` |
| `waveform` | `waveforms/RIPPLE_BUCK1_0001.png` |
| `notes` | |

Test item được phép thêm cột riêng ở cuối (ví dụ `vin_v`, `vout_v`, `iout_a`, `vpp_mv`).

**Ví dụ plan input (efficiency):**

```csv
test_id,enabled,rail,vin_v,iout_start_a,iout_stop_a,iout_step_a,repeat,settle_ms,limit_min,limit_max,unit,register_writes
EFF_BUCK1,1,BUCK1,12.0,0.5,3.0,0.5,2,200,85.0,,%,0x21=0x1F
```

## 4. Waveform PNG

- Nguồn dữ liệu: `DATa:SOUrce`, `WFMPre?` + `CURVe?` từ scope → mảng thời gian/điện áp.
- Theme sáng, có grid, `dpi=150`, `figsize=(12, 6)`.
- Tiêu đề: `<test_id> | <rail> | <điều kiện> | <timestamp>`.
- Trục: X `Time (µs/ms)` tự chọn đơn vị, Y `Voltage (V)`; chú thích đơn vị trên trục.
- Đường limit (nếu có) vẽ nét đứt, nhãn `limit_min` / `limit_max`.
- Annotation giá trị chính: Vpp, overshoot, settling time, rise time (tuỳ test).
- Mỗi lần đo 1 file: `<TEST_ID>_<run_index:04d>.png`.

## 5. Log

```text
14:30:12.345 INFO  hpat.runner    start run plan=efficiency_buck1.csv dut=SN12345
14:30:12.401 DEBUG hpat.visa      PSU#1 TX "VSET1:12.00"
14:30:12.412 ERROR hpat.bench     e-load OCP tripped, aborting
```

- File `logs/run.log`, level INFO; `--verbose` → DEBUG (kèm raw SCPI TX/RX).
- Không log mật khẩu/token (không có trong dự án).

## 6. Ngôn ngữ & đơn vị

- Console, log, tên cột CSV, thông báo lỗi: **English**.
- Tài liệu `.md`: **tiếng Việt**.
- Đơn vị: `V`, `A`, `W`, `%`, `s`/`ms`/`µs`, `°C`, `Hz`.
- Hiển thị console: 4 chữ số có nghĩa; CSV: full precision (không làm tròn).
- So sánh limit: `numpy.isclose(value, limit, rtol=1e-6)`; giá trị đúng bằng limit → PASS.

## 7. Nên / Không nên

- **Nên:** mỗi dòng console ứng với 1 phép đo; lỗi phải nói rõ thiết bị + lệnh + giá trị.
- **Nên:** cảnh báo rõ khi phải kẹp dòng PSU: `WARN  Iset 5.0A > max 3.0A -> clamped to 3.0A`,
  và ghi lại trong `notes` của dòng kết quả.
- **Nên:** luôn in đường dẫn output ở cuối để người dùng mở ngay.
- **Không nên:** in log SCPI ở mức INFO (quá nhiễu); chỉ ở DEBUG.
- **Không nên:** tự ý làm tròn hoặc đổi đơn vị giá trị đo.
- **Không nên:** dùng màu làm nguồn thông tin duy nhất (phải kèm chữ PASS/FAIL).
