# Tài liệu thiết bị & tập lệnh

Thư mục này chứa tài liệu điều khiển thiết bị dùng cho driver trong `hpat/drivers/`.

```text
docs/instruments/
├── ate_scpi_command_extraction.md   # quy tắc đọc/tách SCPI (bắt buộc tuân thủ)
├── raw/                             # PDF gốc — chỉ lưu trữ
└── processed/                       # NGUỒN CHUẨN cho mọi lệnh SCPI
```

## Quy tắc nguồn (bắt buộc)

1. **`processed/` là nguồn chuẩn duy nhất** khi viết driver. Mọi lệnh dùng trong code phải có
   trong file tương ứng, kèm page reference.
2. **Không đọc `raw/` để lấy lệnh SCPI.** `raw/` chỉ là bản lưu PDF gốc để đối chiếu khi cần.
3. Không dùng nguồn ngoài (internet, manual hãng khác) — theo
   [`ate_scpi_command_extraction.md`](ate_scpi_command_extraction.md).
4. Lệnh chưa có trong `processed/` → **không được tự bịa**; dừng lại, yêu cầu bổ sung tài liệu.
5. Cập nhật `processed/` khi có manual mới, giữ nguyên định dạng mục 1–3 của quy tắc.

## Đặt tên

`processed/<hang>_<model>.md` (snake_case), ví dụ `prodigit_3315g.md`.

| File | Thiết bị |
|---|---|
| `gwinstek_gpd3303s.md` | PSU GW Instek GPD-3303S |
| `prodigit_3315g.md` | E-load Prodigit 3315G (mainframe 3302G) |
| `prodigit_3311g.md` | E-load Prodigit 3311G (tham khảo, chưa dùng) |
| `tektronix_tbs2000b.md` | Oscilloscope Tektronix TBS2000B series |
| `unit_ut8805e.md` | DMM UNI-T UT8805E |
| `keithley_2100.md` | DMM Keithley 2100 (⚠️ manual hiện có chỉ là **calibration manual**) |
| `ft232_i2c_mpsse_sample.md` | Ghi chú sample I2C/MPSSE (ftd2xx) |

## Thiết bị của dự án

| Thiết bị | Model | Kết nối | Giới hạn chính |
|---|---|---|---|
| PSU | GW Instek GPD-3303S | USB (virtual COM, 9600) | CH1/CH2: 0–30 V / 3 A; CH3 cố định; `OUT1/OUT0` bật/tắt **toàn bộ** output; `TRACK0/1/2` |
| E-load | Prodigit **3315G** trong mainframe 3302G | GPIB (NI GPIB-USB-HS) | **15 A / 60 V / 75 W**; CC/CV/CR/CP; có dynamic, OCP/OPP |
| Oscilloscope | Tektronix TBS2204B (TBS2000B series) | USB/LAN | 4 kênh; `CURVe?` + `WFMOutpre` để lấy waveform |
| DMM | UNI-T UT8805E | USB | Có `MEASure:VOLT/CURR`; manual không nêu chi tiết interface |
| DMM | Keithley 2100 | USB | ⚠️ tài liệu hiện tại chỉ có lệnh calibration/configuration, **không có lệnh đo** |
| I2C/GPIO | FT232H | USB (D2XX driver) | Dùng `ftd2xx` + MPSSE; sample tham khảo `ftdi_mpsse_python` (MIT) |
