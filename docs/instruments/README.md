# Tài liệu thiết bị & tập lệnh

Thư mục này chứa tài liệu điều khiển thiết bị (SCPI, register map, protocol) dùng cho driver
trong `hpat/drivers/`.

```text
docs/instruments/
├── raw/         # Tài liệu gốc: PDF datasheet, programming manual, register map, ảnh chụp
└── processed/   # Tài liệu đã xử lý: Markdown tóm tắt lệnh, bảng command map, ghi chú
```

## Quy ước

- **`raw/`**: giữ nguyên file gốc, không sửa. Đặt tên `<hang>_<model>_<loai>.<ext>`,
  ví dụ `gwinstek_gpd3303s_programming.pdf`, `tektronix_tbs2000b_scpi.pdf`.
- **`processed/`**: mỗi thiết bị 1 file Markdown `<hang>_<model>.md`, gồm:
  1. Thông tin kết nối (USB/LAN/GPIB, resource VISA mẫu, baud, GPIB address).
  2. Bảng lệnh dùng trong project (chức năng → lệnh → phản hồi → ghi chú).
  3. Giới hạn an toàn (Vmax, Imax, Pmáx, thời gian settle khuyến nghị).
  4. Lệnh không dùng / cấm.
- Khi `raw/` được cập nhật, cập nhật lại file tương ứng trong `processed/`.
- Không đưa thông tin nhạy cảm (serial number thật, mật khẩu) vào tài liệu.

## Thiết bị của dự án

| Thiết bị | Model | Kết nối | Tài liệu cần |
|---|---|---|---|
| PSU | GW Instek GPD-3303S | USB | Programming manual, giới hạn 3 A/kênh |
| E-load | 3315D DC Electronic Load | GPIB (NI GPIB-USB-HS) | SCPI command set, chế độ CC/CV/CR/CP, dynamic |
| Oscilloscope | Tektronix TBS2204B | USB/LAN | SCPI waveform (`WFMPre?`, `CURVe?`), trigger, đo tự động |
| DMM | UNI-T UT8805E | USB | SCPI đo DCV/DCI, range, NPLC |
| DMM | Keithley 2000 / 2100 | USB | SCPI đo DCV/DCI, range, NPLC |
| I2C/GPIO | FT232H | USB (D2XX driver) | Không cần manual; I2C/GPIO qua `ftd2xx` + MPSSE |
