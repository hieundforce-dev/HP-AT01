# TASKS — HP-AT01

> Tài liệu dự án nằm trong `docs/`. Mỗi task làm xong trong 1 phiên. Task quá lớn thì tách nhỏ.
> Thứ tự theo phụ thuộc: core → driver → plugin → test item → tích hợp bench.
> **SCPI:** mọi lệnh dùng trong driver phải lấy từ `docs/instruments/processed/` (kèm page ref);
> không đọc `raw/`, không dùng nguồn ngoài.

- [x] **T01 — Khởi tạo project** — tạo cấu trúc thư mục, `.venv`, `requirements.txt`, `pyproject.toml`
      (ruff + pytest), `git init` + `.gitignore`, package `hpat/` rỗng.
      **AC:** `python -m hpat --help` in ra 5 lệnh; `ruff check .` sạch; `pytest` chạy (0 test).
      ✅ Đạt: 5 lệnh hiển thị, ruff + format sạch, 3 smoke test pass.

- [x] **T02 — Core nền: config, logging, run folder** — load `config/instruments.yaml` bằng pydantic,
      setup logging ra `logs/run.log`, tạo `runs/<timestamp>_<plan>_<sn>/`, class lỗi riêng.
      **AC:** config sai → thông báo lỗi rõ trường nào; chạy lệnh tạo được run folder đúng tên.
      ✅ Đạt: 23 test pass; `run` preflight tạo `runs/2026-11-25_220518_plan_SN12345/` + log.

- [x] **T03 — Driver base + thiết bị giả lập + `bench-check`** — `VisaInstrument` (query/write, retry,
      log SCPI), sim driver cho PSU/eload/scope/DMM/FT232H, lệnh `hpat bench-check --sim`.
      **AC:** `bench-check --sim` báo OK tất cả role đã cấu hình; unit test cho base pass.
      ✅ Đạt: 7/7 role OK; 43 test pass.

- [x] **T04 — FT232H: I2C + GPIO (ftd2xx/MPSSE)** — driver `ftd2xx` + MPSSE engine (clock, bit-bang),
      I2C master (start/stop/address/read/write + ACK, **clock stretching**), GPIO set/read, sim tương ứng,
      tham khảo sample `ftdi_mpsse_python` (MIT — ghi attribution trong `THIRD_PARTY_NOTICES.md`),
      hướng dẫn cài D2XX (gỡ VCP) trong README.
      **AC:** ghi rồi đọc lại register qua sim đúng giá trị; unit test MPSSE/I2C pass;
      `bench-check` báo lỗi rõ khi thiếu D2XX; scan bus I2C chạy trên bench thật.
      ✅ Code + 22 unit test pass (fake transport); `bench-check` báo lỗi D2XX rõ ràng.
      ⏳ Scan bus thật kiểm tra ở T16 (chưa có FT232H trên máy dev).

- [ ] **T05 — Plugin framework + runner + results** — `BaseTest`/registry, load plan CSV theo schema
      từng test, vòng lặp `repeat`, ghi `results/*.csv` + `summary.csv`, bảng tổng hợp console,
      test item `dummy` để kiểm chứng.
      **AC:** plan dummy 3 case × repeat 2 → CSV 6 dòng + summary đúng mean/min/max.

- [ ] **T06 — Test item: I2C register R/W** — plan CSV (address, value, expected, repeat), ghi/đọc
      verify, Pass/Fail.
      **AC:** plan mẫu chạy trên sim, sai expected → FAIL; đúng → PASS.

- [ ] **T07 — DMM drivers** — UT8805E trước (đủ tài liệu đo); Keithley 2000/2100 chỉ dùng các lệnh
      có trong `processed/` (hiện K2100 chỉ có lệnh calibration → **chưa đo được**); map vai trò
      `dmm_vin` / `dmm_vout` / `dmm_iout` (+ shunt) trong config, sim.
      **AC:** bench-check đọc được giá trị từ sim; đổi vai trò DMM chỉ sửa YAML;
      role đo thật dùng UT8805E cho tới khi có tài liệu K2100.

- [ ] **T08 — PSU GPD-3303S + e-load Prodigit 3315G + safety interlocks** — driver + SCPI command map
      (nguồn: `docs/instruments/processed/{gwinstek_gpd3303s,prodigit_3315g}.md`):
      PSU 30 V/3 A, baud 9600, `OUT1/OUT0` bật/tắt **toàn bộ** output, `TRACK0/1/2`;
      e-load 15 A/60 V/75 W, CC/CV/CR/CP, dynamic, OCP/OPP.
      Validate V/I/**P** trước khi bật, shutdown trong `finally`, xử lý OCP trip.
      **AC:** sim test: current limit set trước output; exception → output tắt; vượt 15 A hoặc 75 W → từ chối chạy.

- [ ] **T09 — Scope TBS2204B + render waveform** — cấu hình kênh/timebase/trigger, lấy `WFMPre?` +
      `CURVe?`, render PNG theo `DESIGN.md`.
      **AC:** PNG sinh từ dữ liệu sim, có tiêu đề/trục/đơn vị/annotation; unit test chuyển đổi dữ liệu.

- [ ] **T10 — Test item: Efficiency** — quét Iout, đo Vin/Vout/Iout bằng DMM, tính η, PNG (nếu cần),
      Pass/Fail theo limit.
      **AC:** plan mẫu 1 rail × 6 điểm × repeat 2 → CSV đủ cột + summary; η tính đúng với dữ liệu sim.

- [ ] **T11 — Test item: Line regulation + Load regulation** — quét Vin / quét Iout, tính độ biến thiên
      (mV, %), Pass/Fail.
      **AC:** plan mẫu chạy sim, kết quả khớp tính tay.

- [ ] **T12 — Test item: Ripple / Noise** — capture scope, tính Vpp/RMS, lưu PNG, Pass/Fail.
      **AC:** PNG + CSV có `vpp_mv`, `rms_mv`; so khớp dữ liệu sim.

- [ ] **T13 — Test item: Load transient** — e-load dynamic (low/high, slew), capture scope,
      tính overshoot/undershoot + settling time, PNG.
      **AC:** plan mẫu sim → CSV có overshoot/settling, PNG có limit line.

- [ ] **T14 — Test item: Startup/Shutdown + Sequencing** — capture nhiều kênh, đo delay/rise/fall,
      kiểm tra thứ tự rail theo config.
      **AC:** plan mẫu 2 rail (giới hạn 2 kênh PSU), phát hiện sai thứ tự → FAIL.

- [ ] **T15 — Test item: Protections (UVLO/OVP/OCP/OTP)** — quét điều kiện tới điểm trip, ghi trip point,
      so với spec.
      **AC:** plan mẫu sim, trip point nằm trong limit → PASS; ngoài → FAIL.

- [ ] **T16 — Tích hợp bench thật + tài liệu** — `bench-check` với thiết bị thật, README hướng dẫn
      cài đặt (NI-VISA, NI-488.2, D2XX, gỡ VCP cho FT232H), checklist chạy bench, plan mẫu cho cả 8 test.
      **AC:** `bench-check` nhận đủ thiết bị; README đủ để người khác dựng lại môi trường.

- [ ] **T17 — Hardening & so sánh run** — timeout/retry, thông báo lỗi, script so sánh 2 run,
      rà soát toàn bộ, cập nhật tài liệu.
      **AC:** `pytest` pass, `ruff check .` sạch, so sánh 2 run ra bảng khác biệt.

## Đang làm

- T05 — Plugin framework + runner + results
