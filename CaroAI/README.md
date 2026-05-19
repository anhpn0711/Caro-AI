# 🎮 Báo Cáo & Hướng Dẫn Vận Hành Game Caro AI
### Dự Án Thực Hành Giữa Kỳ - Môn học: Trí tuệ Nhân tạo (AI)
**Tên Repository**: `23021215_23021223_23021241_CaroAI`

---

## 👥 Thông Tin Nhóm Thực Hiện

| STT | Họ và Tên | Mã số Sinh viên (MSSV) | Lớp học | Nhiệm vụ đảm nhiệm |
| :---: | :--- | :---: | :---: | :--- |
| 1 | Phùng Nam Anh | 23021215 | QH-2023-I/CQ | Thiết kế thuật toán AI & Xây dựng Giao diện GUI |
| 2 | Nguyễn Tá Cường | 23021223 | QH-2023-I/CQ | Tối ưu hóa mã nguồn & Thiết lập thông số thực nghiệm |
| 3 | Nguyễn Đức Đạt | 23021241 | QH-2023-I/CQ | Phân tích dữ liệu hiệu năng & Viết tài liệu báo cáo |

---

## 📂 1. Cấu Trúc Thư Mục Nộp Bài (Repository Structure)
Dự án được tổ chức khoa học, tách biệt rõ ràng giữa giao diện (GUI), logic luật chơi (Game Logic) và lõi thuật toán AI (AI Solver):

```text
mssv1_mssv2_mssv3_CaroAI/
├── play.py               # Điểm kích hoạt chương trình chính (Khởi chạy GUI game)
├── performance_eval.py   # Script tự động đo đạc, đánh giá hiệu năng 3 chế độ AI (Level 3)
├── requirements.txt      # Khai báo danh mục thư viện (Đã đi kèm sẵn theo chuẩn đề bài)
├── README.md             # Tài liệu hướng dẫn cài đặt và vận hành game (File này)
├── benchmark_report.md   # Báo cáo kết quả thực nghiệm chi tiết cho 5 ca kiểm thử (Tự động tạo)
├── source/               # Thư mục mã nguồn cốt lõi (Source Code) chứa logic & AI
│   ├── AI.py             # Lõi AI tìm kiếm (Minimax, Alpha-Beta, Transposition Table, History Heuristic)
│   ├── gomoku.py         # Logic cờ Caro (Kiểm tra nước đi hợp lệ, kiểm tra chiến thắng)
│   └── utils.py          # Cấu hình hằng số (BOARD_SIZE, WIN_COUNT) và 5 bộ kiểm thử Level 3
└── gui/                  # Thư mục chứa giao diện đồ họa người dùng
    ├── interface.py      # Xử lý giao diện bàn cờ Tkinter, vẽ quân cờ, luồng (threading) và Log di chuyển
    └── button.py         # Tiện ích tùy biến nút bấm đồng nhất giao diện Dark Mode
```

---

## 🧠 2. Các Thuật Toán AI Đã Cài Đặt (Level 1, 2, 3)
Dự án đã đáp ứng trọn vẹn các mức thực hiện theo đúng đề bài yêu cầu:

1. **Level 1 - Chế độ Easy (Chỉ Minimax)**:
   - Thuật toán Minimax tìm kiếm đầy đủ cây quyết định đến giới hạn độ sâu (Depth Limit).
   - Hàm lượng giá thế trận cục bộ tăng tiến (`evaluate_local`) tính toán điểm số dựa trên chuỗi quân cờ liên tiếp và số đầu trống của hai bên.
2. **Level 2 - Chế độ Normal (Minimax + Alpha-Beta Pruning)**:
   - Nâng cấp cắt nhánh Alpha-Beta giúp loại bỏ sớm các nhánh tìm kiếm không triển vọng, cho kết quả nước đi tối ưu hoàn toàn trùng khớp với Minimax nhưng với thời gian xử lý nhanh gấp nhiều lần.
   - Cho phép so sánh trực diện hiệu năng hai thuật toán trên cùng một bàn cờ.
3. **Level 3 - Chế độ Hard (Alpha-Beta + Bảng băm Zobrist + History Heuristic)**:
   - **Zobrist Hashing (Transposition Table)**: Mã hóa trạng thái bàn cờ 9x9 thành khóa băm 64-bit cực nhanh để lưu trữ kết quả cờ đã tính, tái sử dụng tức thì ở các nhánh tuần hoàn.
   - **History Heuristic (Sắp xếp nước đi)**: Ưu tiên thử nghiệm các nước đi có lịch sử mang lại hiệu quả cắt tỉa cao để tối ưu tối đa tốc độ cắt nhánh Alpha-Beta.

---

## 🛠️ 3. Hướng Dẫn Cài Đặt & Vận Hành Chương Trình

### 3.1. Yêu Cầu Hệ Thống & Môi Trường
- **Hệ điều hành**: Windows, macOS, Linux.
- **Ngôn ngữ**: **Python 3.x** (Khuyên dùng Python 3.8 trở lên).
- **Thư viện đồ họa**: **Tkinter** (Thư viện chuẩn đi kèm sẵn khi cài đặt Python, không cần cài đặt ngoài).

### 3.2. Hướng Dẫn Chạy Game Caro AI (Giao diện đồ họa)
Để mở game và bắt đầu chơi đấu trí với máy tính, bạn hãy mở Command Prompt / PowerShell (Windows) hoặc Terminal (macOS/Linux) tại thư mục dự án và chạy lệnh:

```bash
python play.py
```

#### 🎮 Các tính năng chính và cách thao tác trên giao diện:
1. **Bắt đầu chơi**: Nhấn **Chơi X (Đi trước)** hoặc **Chơi O (Đi sau)** ở bảng điều khiển phía trên để khởi động ván cờ mới.
2. **Chọn thuật toán và thông số**: 
   - Thay đổi độ sâu tìm kiếm trong ô **Depth** (Khuyên dùng Depth từ 2 đến 5 để đảm bảo tốc độ phản hồi < 2s).
   - Thay đổi thời gian suy nghĩ tối đa của máy trong ô **Time(s)**.
   - Chọn chế độ thuật toán AI tại Combobox **Mode** (*Easy*, *Normal*, hoặc *Hard*).
3. **Đi lại nước đi (Undo)**: Nhấn **↶ Lùi bước (Undo)** để rút lại nước cờ vừa đi của bạn và AI.
4. **Dừng / Reset trận**: Nhấn **⏹ Dừng/Reset Trận** để xóa sạch bàn cờ và chuẩn bị cho trận đấu mới.
5. **Xem Log Lịch sử chi tiết**: Cột bên phải hiển thị đầy đủ bảng lịch sử di chuyển với các thông số bắt buộc: *Số thứ tự*, *Bên đi*, *Tọa độ ô cờ* (VD: E5), *Điểm thế trận*, *Độ sâu thực tế AI đạt được*, *Số trạng thái đã xét (Nodes)*, và *Thời gian suy nghĩ*.

---

### 3.3. Hướng Dẫn Chạy Bộ Đánh Giá Hiệu Năng & Xuất Báo Cáo Tự Động (Level 3)
Đề bài yêu cầu đo đạc thực nghiệm số trạng thái đã xét và thời gian chạy trên **ít nhất 5 thế cờ** khác nhau. Chúng tôi đã xây dựng sẵn script tự động hóa hoàn toàn quy trình này.

Chạy lệnh sau để thực hiện đo đạc:
```bash
python performance_eval.py
```

#### 📈 Kết quả thu hoạch sau khi chạy:
- Chương trình sẽ in tiến trình đo đạc của cả 3 chế độ AI ở các độ sâu 1, 2, 3 lên màn hình terminal.
- Sau khi chạy xong, chương trình tự động tạo tệp báo cáo **`benchmark_report.md`** tại thư mục gốc. 
- Bạn chỉ cần mở tệp **[benchmark_report.md](file:///c:/Users/Admin/Documents/BTL cac mon/BT AI/CaroAI/benchmark_report.md)** lên, nhấn **`Ctrl + Shift + V`** trong VS Code để xem bảng so sánh tuyệt đẹp và các câu hỏi lý thuyết phân tích lý do Alpha-Beta cắt tỉa, ảnh hưởng của độ sâu cờ... có thể copy trực tiếp vào báo cáo PDF nộp cho giảng viên.

#### 🧪 5 Ca kiểm thử có sẵn có thể nạp trực tiếp trên GUI:
Tại khung **Level 3 Test** ở thanh công cụ phía trên giao diện cờ:
1. Chọn thế cờ mong muốn từ danh sách.
2. Nhấn nút **Nạp bàn cờ**.
3. Bạn có thể nhấn vào bàn cờ để đi tiếp hoặc để AI tính toán nước đi ứng phó, quan sát các chỉ số Node và thời gian phản hồi được cập nhật trực tiếp vào bảng Log bên phải.

---

*Chúc các bạn có những trải nghiệm đấu trí thú vị và hoàn thành bài thực hành đạt điểm số tối đa!* 🏆
