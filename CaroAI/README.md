# 🎮 Báo Cáo & Hướng Dẫn Vận Hành Game Caro AI (12x12)
### Dự Án Thực Hành Giữa Kỳ - Môn học: Trí tuệ Nhân tạo (AI)
**Tên Repository**: `23021215_23021223_23021241_CaroAI`

---

## 👥 Thông Tin Nhóm Thực Hiện

| STT | Họ và Tên | Mã số Sinh viên (MSSV) | Lớp học | Nhiệm vụ đảm nhiệm |
| :---: | :--- | :---: | :---: | :--- |
| 1 | **Phùng Nam Anh** | 23021215 | QH-2023-I/CQ | Thiết kế lõi thuật toán AI, Tối ưu hóa cắt tỉa & Xây dựng Giao diện GUI |
| 2 | **Nguyễn Tá Cường** | 23021223 | QH-2023-I/CQ | Thiết lập thông số thực nghiệm, Quản lý trạng thái & Gỡ lỗi hiệu năng |
| 3 | **Nguyễn Đức Đạt** | 23021241 | QH-2023-I/CQ | Phân tích dữ liệu hiệu năng, Viết tài liệu báo cáo & Đánh giá các ca kiểm thử |

---

## 🛠️ Hướng Dẫn Cài Đặt & Vận Hành Chương Trình

### 1. Yêu Cầu Hệ Thống
* **Ngôn ngữ**: **Python 3.8** trở lên.
* **Thư viện đồ họa**: **Tkinter** (Là thư viện chuẩn mặc định của Python, **không cần cài thêm** bằng pip).

### 2. Cấu Trúc Thư Mục
Dự án được tổ chức như sau:
```text
23021215_23021223_23021241_CaroAI/
├── play.py                 # File chính để khởi chạy trò chơi (Giao diện đồ họa)
├── performance_eval.py     # Script tự động đo đạc hiệu năng AI
├── source-code/            # Chứa mã nguồn thuật toán lõi (AI Engine & Game Rules)
└── gui/                    # Chứa mã nguồn giao diện (Tkinter)
```

---

### 3. Cách Khởi Chạy Giao Diện Đồ Họa (Chơi Game)

Để bắt đầu chơi cờ Caro với AI, bạn mở Terminal (hoặc Command Prompt / PowerShell) tại thư mục dự án và chạy lệnh sau:
```bash
python play.py
```

#### 🕹️ Các Thao Tác Cơ Bản:
1. **Chọn Lượt Đi**: Nhấn nút **"Chơi X (Trước)"** hoặc **"Chơi O (Sau)"** ở menu bên phải.
2. **Tùy Chỉnh AI**:
   * **Chế độ**: Chọn mức độ khó: *Easy* (Chỉ dùng Minimax cơ bản), *Normal* (Minimax có cắt tỉa Alpha-Beta), hoặc *Hard* (Alpha-Beta kết hợp Bảng Băm Zobrist cực mạnh).
   * **Độ sâu (Depth)**: Giới hạn số bước AI tính trước. Khuyên dùng từ **Depth 3 đến 5**.
   * **Thời gian giới hạn**: Thời gian tối đa (giây) AI được phép suy nghĩ trong mỗi lượt.
3. **Các Chức Năng Khác**:
   * **↶ Lùi bước**: Xin đi lại nước cờ (Undo).
   * **⏹ Hủy trận**: Kết thúc ván ngay lập tức và dọn dẹp bàn cờ.
4. **Chế Độ Tự Do (Sandbox)**:
   * Bấm nút **"✏️ Chế độ tự do"**.
   * Bạn có thể bấm tùy ý lên bàn cờ để đặt quân (Click lần 1 ra X, lần 2 ra O, lần 3 xóa trắng). Rất hữu ích khi muốn thiết lập một thế cờ cụ thể từ bên ngoài.
   * Xếp xong, bấm **"🤖 AI đi tiếp"** để AI giải tiếp thế cờ đó.

---

### 4. Đánh Giá Hiệu Năng Thuật Toán (Benchmark)

Chương trình cung cấp sẵn công cụ đo đạc số trạng thái được duyệt và thời gian thực thi của AI trên các thế cờ. Để chạy tự động, dùng lệnh:
```bash
python performance_eval.py
```
**Kết quả**: 
- Tiến trình sẽ hiển thị trực tiếp trên màn hình Terminal.
- Hệ thống sẽ tự động tạo ra một tệp báo cáo chi tiết mang tên **`benchmark_report.md`**. Bạn có thể dùng VS Code mở tệp này và xem kết quả phân tích rất trực quan.

---

*Chúc các thầy cô và các bạn có những trải nghiệm thú vị cùng Caro AI!* 🏆
