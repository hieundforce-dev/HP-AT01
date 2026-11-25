# Vibe Coding Agent Guide

> **Cách kích hoạt:** người dùng nhập
> `Hãy đọc docs/vibe-coding-agent-guide.md và ta sẽ bắt đầu với dự án <tên/mô tả>`
>
> Agent đọc file này, phỏng vấn để thu thập thông tin, tạo 6 file dự án, chia task, rồi mới code.

---

## 1. Quy trình bắt buộc

| Bước | Agent làm gì | Kết quả |
|---|---|---|
| 0 | Đọc guide + kiểm tra thư mục đã có file dự án chưa | Biết đây là dự án mới hay đang tiếp tục |
| 1 | Phỏng vấn vòng 1 — Dự án | Đủ info cho `PRD.md` |
| 2 | Phỏng vấn vòng 2 — Kỹ thuật | Đủ info cho `ARCHITECTURE.md` |
| 3 | Phỏng vấn vòng 3 — Thiết kế | Đủ info cho `DESIGN.md` |
| 4 | Phỏng vấn vòng 4 — Quy tắc | Đủ info cho `RULES.md` |
| 5 | Tạo `PRD/ARCHITECTURE/DESIGN/RULES` + tóm tắt | Người dùng duyệt |
| 6 | Chia task vào `TASKS.md`, tạo `PROGRESS.md` | Người dùng duyệt danh sách task |
| 7 | Làm task đầu tiên | Code + cập nhật `PROGRESS.md` |

**Không được code trước bước 7.** Không được bỏ qua bước 5–6.

---

## 2. Quy tắc phỏng vấn

- Mỗi lần chỉ hỏi **một vòng**, tối đa **8 câu**, đánh số rõ ràng.
- Câu nào có thể mặc định thì ghi kèm: `(mặc định: ...)`.
- Đánh dấu `[bắt buộc]` cho câu không thể tự quyết.
- Người dùng trả lời **"tuỳ bạn" / "không biết"** → chọn phương án hợp lý nhất, ghi vào file, nêu ngắn gọn đã chọn gì.
- Người dùng đã cung cấp thông tin (spec, ảnh, link Figma, mô tả) → **không hỏi lại**, chỉ hỏi phần còn thiếu.
- Cuối mỗi vòng: tóm tắt 3–5 dòng và hỏi "đúng chưa?" trước khi sang vòng tiếp.
- Thông tin xung đột hoặc thiếu nghiêm trọng → dừng lại hỏi, không tự đoán.

---

## 3. Bộ câu hỏi phỏng vấn

### Vòng 1 — Dự án → `PRD.md`

1. Tên dự án? `[bắt buộc]`
2. Mô tả 1–2 câu: xây cái gì?
3. Ai là người dùng? (cá nhân / nội bộ / khách hàng)
4. Vấn đề chính cần giải quyết?
5. Nền tảng: web / mobile / desktop / API / extension?
6. 3–5 tính năng bắt buộc cho bản đầu tiên? `[bắt buộc]`
7. Những gì **không** làm trong bản này?
8. Có spec, tài liệu, ảnh hay link tham khảo không? (đường dẫn)

### Vòng 2 — Kỹ thuật → `ARCHITECTURE.md`

1. Stack mong muốn, hay để agent đề xuất? `(mặc định: theo loại dự án)`
2. Database? `(mặc định: SQLite cho local, Postgres cho production)`
3. Đăng nhập / phân quyền? `(mặc định: chưa có)`
4. Chạy và deploy ở đâu? `(mặc định: local + Vercel/VPS)`
5. Mô hình dữ liệu chính: các entity/bảng và quan hệ? `(nếu chưa rõ: agent đề xuất)`
6. Tích hợp bên ngoài? (thanh toán, email, AI API, storage…)
7. Ràng buộc kỹ thuật? (phiên bản Node, package manager, thiết bị đích)

### Vòng 3 — Thiết kế → `DESIGN.md`

1. Phong cách? (tối giản / hiện đại / playful / corporate / dark…)
2. Màu chủ đạo hoặc màu thương hiệu? (mã màu nếu có)
3. Font chữ? `(mặc định: Inter)`
4. Light / Dark / cả hai? `(mặc định: Light)`
5. Có ảnh, Figma hay website tham chiếu? (đường dẫn/link)
6. Component library? `(mặc định: Tailwind + shadcn/ui)`
7. Responsive: mobile-first? breakpoint?
8. Ngôn ngữ giao diện? `(mặc định: tiếng Việt)`

### Vòng 4 — Quy tắc → `RULES.md`

1. Ngôn ngữ comment trong code? `(mặc định: tiếng Anh)`
2. Có viết test không, mức nào? `(mặc định: test cho logic chính)`
3. Lint / format? `(mặc định: ESLint + Prettier)`
4. Git: agent tự commit hay chỉ khi được yêu cầu? `(mặc định: chỉ khi được yêu cầu)`
5. Điều gì tuyệt đối cấm? (ngoài danh sách mặc định bên dưới)
6. Lệnh chạy project? `(nếu đã có sẵn)`

### Vòng 5 — Chia task

Agent không hỏi thêm, tự chia task từ `PRD.md` và trình danh sách để duyệt:

- Mỗi task làm xong trong **1 phiên**, có Acceptance Criteria kiểm chứng được.
- Đánh số `T01`, `T02`…, sắp theo thứ tự phụ thuộc.
- Task đầu tiên phải là "khởi tạo project + chạy được trang trống".

---

## 4. Mẫu 6 file

### PRD.md

```md
# PRD — <Tên dự án>

## Vấn đề
<Người dùng gặp khó khăn gì?>

## Người dùng mục tiêu
- Chân dung:
- Nhu cầu chính:

## Tính năng
### Must have
- [ ]
### Nice to have
- [ ]
### Không nằm trong phạm vi (Out of scope)
-

## Tiêu chí thành công
-

## Ràng buộc
- Thời gian / ngân sách:
- Nền tảng:
```

### ARCHITECTURE.md

````md
# ARCHITECTURE

## Tech stack
| Thành phần | Công nghệ | Lý do chọn |
|---|---|---|
| Ngôn ngữ | | |
| Framework | | |
| Database | | |
| Hosting | | |

## Cấu trúc thư mục
```text
src/
  components/
  pages/
  lib/
```

## Luồng dữ liệu
<Client → API → DB → ...>

## Data model
<Các bảng / entity chính và quan hệ>

## Quyết định kiến trúc (ADR)
- <Quyết định> — <lý do>
````

### DESIGN.md

```md
# DESIGN

## Phong cách
- Từ khoá:
- Tham chiếu (moodboard):

## Màu sắc
| Token | Mã | Dùng cho |
|---|---|---|
| primary | # | |
| background | # | |
| text | # | |

## Typography
- Font tiêu đề:
- Font nội dung:
- Thang cỡ chữ:

## Component
- Button:
- Input:
- Card:
- Modal:

## Spacing & Layout
- Đơn vị spacing:
- Breakpoint:

## Nên / Không nên
- Nên:
- Không nên:
```

### RULES.md

```md
# RULES

## Quy tắc code
- Ngôn ngữ comment:
- Đặt tên:
- Format / lint:
- Test:

## AI tuyệt đối KHÔNG được
- Tự ý đổi tech stack, thư viện hoặc cấu trúc thư mục.
- Xoá hoặc ghi đè file không liên quan tới task.
- Thêm dependency mới mà không hỏi.
- Tự đoán yêu cầu khi thông tin chưa rõ.
- Làm nhiều task cùng lúc trong một lần.
- Commit / push khi chưa được yêu cầu.

## Definition of Done
- [ ] Code chạy được, không lỗi build.
- [ ] Đúng AC trong PRD.
- [ ] Đã cập nhật PROGRESS.md.
```

### TASKS.md

```md
# TASKS

> Mỗi task phải làm xong trong 1 phiên. Task quá lớn thì tách nhỏ.

- [ ] T01 — <mô tả> — AC: <kết quả kiểm chứng được>
- [ ] T02 — ...
- [ ] T03 — ...

## Đang làm
- T0x
```

### PROGRESS.md

```md
# PROGRESS

## Trạng thái hiện tại
-

## Đã hoàn thành
-

## Lỗi / Blocker
-

## Bước tiếp theo
-

## Nhật ký
| Ngày | Task | Thay đổi |
|---|---|---|
```

---

## 5. Trong mỗi phiên làm việc

**Bắt đầu phiên:**
1. Đọc `RULES.md` và `PROGRESS.md`.
2. Chọn task tiếp theo trong `TASKS.md`.
3. Nêu ngắn gọn: làm task nào, sẽ sửa file nào.

**Kết thúc phiên:**
1. Chạy build/lint nếu có.
2. Tick task trong `TASKS.md`.
3. Cập nhật `PROGRESS.md`: đã xong, lỗi, bước tiếp theo.
4. Báo lại: đã làm gì, còn gì, cần người dùng quyết gì.

**Phiên tiếp theo**, người dùng chỉ cần nhập:
`Đọc PROGRESS.md và tiếp tục dự án.`

---

## 6. Điều cấm trong suốt dự án

- Code khi chưa có đủ 6 file và task list được duyệt.
- Đổi stack, thư viện, cấu trúc thư mục ngoài kế hoạch.
- Làm nhiều task trong một lần hoặc gộp task.
- Tự bịa yêu cầu, tự mở rộng phạm vi.
- Xoá/ghi đè file không liên quan tới task đang làm.
- Commit, push, deploy khi chưa được yêu cầu.
