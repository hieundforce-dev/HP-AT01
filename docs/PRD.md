# PRD — HP-AT01: PMIC Automated Test Software

## Vấn đề

Test PMIC hiện được thực hiện thủ công trên bench: người đo phải thao tác lần lượt PSU, electronic load,
oscilloscope, DMM và ghi/đọc register qua FT232H. Hệ quả:

- Tốn thời gian, đặc biệt khi test nhiều rail (1–7 rail) và nhiều điều kiện quét.
- Kết quả phụ thuộc người đo, thiếu nhất quán giữa các lần chạy.
- Log nằm rải rác (giấy, Excel tay, ảnh chụp màn hình scope), khó truy vết và so sánh.
- Khó tái lập một lần đo cũ để điều tra lỗi.

## Người dùng mục tiêu

- **Chân dung:** kỹ sư test/validation nội bộ, biết Python cơ bản, làm việc trên PC Windows 11
  kết nối bench thiết bị.
- **Nhu cầu chính:**
  - Khai báo bài test bằng CSV, chạy bằng một lệnh.
  - Nhận kết quả CSV + ảnh waveform PNG có thể mở bằng Excel/ảnh thông thường.
  - Tái lập và so sánh được giữa các lần chạy.
  - Thêm bài test mới nhanh, không đụng vào core.

## Phạm vi DUT

| Hạng mục | Giá trị |
|---|---|
| PMIC model | Cập nhật sau (không hard-code) |
| Số rail | 1–7 |
| Vout | 0.5 V – 12 V |
| Iout | 1 A – 20 A mỗi rail |
| Điều khiển | I2C + GPIO qua FT232H |

## Tính năng

### Must have

- [ ] Chạy test từ file CSV; **mỗi test item có format input CSV riêng**, có validate schema.
- [ ] **Repeat N lần/case**; ghi `run_index`; tổng hợp mean/min/max/stddev.
- [ ] 8 nhóm test:
  - (a) Efficiency (η theo Iout)
  - (b) Line regulation (quét Vin)
  - (c) Load regulation (quét Iout)
  - (d) Output ripple / noise (scope)
  - (e) Load transient response (eload dynamic + scope)
  - (f) Startup / shutdown timing & power sequencing
  - (g) Protections: UVLO / OVP / OCP / OTP
  - (h) I2C register read/write & verify; GPIO qua FT232H
- [ ] Điều khiển PSU / e-load / scope / DMM qua PyVISA; I2C/GPIO qua FT232H.
- [ ] Output: CSV kết quả + PNG waveform (dữ liệu waveform lấy bằng lệnh SCPI của scope).
- [ ] Đánh giá Pass/Fail theo `limit_min` / `limit_max` trong plan.
- [ ] Safety interlocks: set current limit trước khi bật output, tắt output trong `finally`,
      validate V/I trước khi gửi lệnh.
- [ ] Plugin registry: thêm test item mới = thêm module + đăng ký, không sửa core.
- [ ] Sim mode: phát triển và test không cần bench thật.
- [ ] Log từng run ra file.

### Nice to have

- [ ] `hpat bench-check`: chẩn đoán kết nối tất cả thiết bị.
- [ ] `hpat validate`: kiểm tra plan trước khi chạy.
- [ ] Script so sánh kết quả 2 run.
- [ ] GUI (PySide6) — chỉ sau khi CLI ổn định.

### Không nằm trong phạm vi (Out of scope)

- Web GUI, MES/DB server, SQLite lịch sử, báo cáo HTML/PDF.
- Chạy song song nhiều DUT hoặc nhiều rail đồng thời.
- Đóng gói `.exe`.
- Hard-code thông số/địa chỉ register của một PMIC cụ thể.

## Tiêu chí thành công

1. Một plan nhiều rail × nhiều repeat chạy hết mà không cần can thiệp tay.
2. CSV kết quả mở được bằng Excel (UTF-8 BOM), đủ cột để truy vết điều kiện đo.
3. PNG waveform đọc được Vpp / overshoot / settling time, có tiêu đề và đơn vị.
4. Khi thiết bị lỗi hoặc Ctrl+C: output PSU/e-load tắt, log ghi rõ nguyên nhân.
5. Thêm một test item mới chỉ cần 1 module + 1 dòng đăng ký + 1 file plan mẫu.

## Ràng buộc

| Loại | Nội dung |
|---|---|
| Nền tảng | Windows 11, Python 3.12, `.venv` + pip, có internet |
| PSU | GW Instek GPD-3303S (USB) |
| E-load | 3315D DC Electronic Load (GPIB qua NI GPIB-USB-HS) |
| Oscilloscope | Tektronix TBS2204B (4 kênh) |
| DMM | UNI-T UT8805E / Keithley 2000 / Keithley 2100 (USB, PyVISA) |
| I2C/GPIO | FT232H (ftd2xx / D2XX driver, MPSSE) |
| Thời gian | Không giới hạn cứng; ưu tiên bản chạy được trên bench sớm |

## Rủi ro & câu hỏi mở

1. **Công suất PSU:** GPD-3303S chỉ 3 A / 32 V mỗi kênh. **Đã chốt:** nếu plan yêu cầu dòng vào
   > 3 A thì kẹp ở 3 A, in cảnh báo và ghi vào `notes` của kết quả (không fail case). Khi có PSU
   công suất cao hơn thì chỉ cần sửa `max_current` trong `config/instruments.yaml`.
2. **FT232H không có ADC:** đo analog dùng DMM (đã chốt), FT232H chỉ I2C/GPIO qua `ftd2xx`.
3. **SCPI command set** của 3315D và GPD-3303S cần manual để hoàn thiện driver; kiến trúc dùng
   **command map trong config** để có thể chỉnh không sửa code.
4. Địa chỉ GPIB của e-load, resource VISA của từng máy: điền vào `config/instruments.yaml` khi có bench.
5. **FT232H D2XX:** cần driver D2XX (CDM) và phải gỡ VCP cho thiết bị đó; I2C phải tự cài trên MPSSE.
