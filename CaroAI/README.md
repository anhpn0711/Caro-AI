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

## ✨ Điểm Nổi Bật & Tính Năng Vượt Trội Của Dự Án

Dự án phát triển một hệ thống cờ Caro AI (kích thước bàn cờ **12x12**, luật chơi **4 quân liên tiếp để chiến thắng**) với các điểm nhấn đặc sắc về công nghệ lẫn mỹ thuật:
1. **Giao diện Premium Dark Mode**: Thiết kế tối giản, phối màu tinh tế dựa trên hệ màu HSL hiện đại, đem lại trải nghiệm mượt mà, bảo vệ mắt và cực kỳ chuyên nghiệp.
2. **Lõi AI Đa Tầng Cắt Tỉa (Level 1, 2, 3)**: Tích hợp đầy đủ các giải thuật tìm kiếm tiên tiến từ Minimax cổ điển đến hệ thống tối ưu hóa cắt tỉa hàng đầu trong lý thuyết lý thuyết trò chơi (Game Theory).
3. **Chế Độ Tự Do (Sandbox/Edit Mode)**: Tính năng độc đáo cho phép người dùng click tự do để thay đổi quân cờ trên bàn (Trống ⭢ X ⭢ O) nhằm tự thiết lập các thế cờ hiểm hóc từ bên ngoài, sau đó nhấn **"AI đi tiếp"** để chứng kiến cách AI giải quyết tình huống.
4. **Log Lịch Sử Thông Minh**: Cập nhật trực tiếp điểm thế trận tĩnh, nhận định chiến thuật theo thời gian thực (VD: *"AI đang ép sân rất mạnh"*, *"Thế trận cân bằng"*), số node đã duyệt, độ sâu đạt được và thời gian phản hồi ở mỗi nước đi.
5. **Bộ Đánh Giá Hiệu Năng Tự Động**: Tích hợp công cụ benchmark tự động xuất báo cáo chi tiết so sánh 3 thuật toán trên 5 thế cờ tiêu chuẩn.

---

## 📂 1. Cấu Trúc Thư Mục Nộp Bài (Repository Structure)

Mã nguồn được tổ chức khoa học, tách biệt hoàn toàn giữa logic đồ họa (GUI), luật chơi (Game Rules) và lõi thuật toán tìm kiếm (AI Engine):

```text
23021215_23021223_23021241_CaroAI/
├── play.py                 # Điểm khởi chạy chính của trò chơi (Khởi tạo cửa sổ GUI)
├── performance_eval.py     # Script tự động đo đạc, đánh giá hiệu năng 3 chế độ AI (Level 3)
├── requirements.txt        # Khai báo thông tin môi trường và thư viện chuẩn
├── README.md               # Tài liệu hướng dẫn cài đặt và vận hành (Tệp này)
├── benchmark_report.md     # Báo cáo kết quả thực nghiệm chi tiết tự động tạo
├── core/                   # Thư mục chứa mã nguồn logic cốt lõi (Game & AI Core)
│   ├── ai_engine.py        # Lõi thuật toán AI (Minimax, Alpha-Beta, Zobrist TT, History Heuristic, PVS)
│   ├── gomoku_rules.py     # Logic kiểm tra luật chơi (Tính nước thắng, kiểm tra đầy bàn)
│   └── constants.py        # Định nghĩa hằng số hệ thống (BOARD_SIZE = 12, bộ 5 ca kiểm thử mẫu)
└── gui/                    # Thư mục chứa giao diện đồ họa (Tkinter UI)
    ├── interface.py        # Quản lý luồng giao diện bàn cờ, threading, log cờ, timer
    └── button.py           # Tiện ích xây dựng các nút bấm phong cách Dark Mode đồng nhất
```

---

## 🧠 2. Các Thuật Toán AI Đã Cài Đặt (Kiến Trúc & Thuật Toán)

### 2.1. Phân Cấp Các Chế Độ Chơi (Chế độ Mode)
* **Level 1 - Chế Độ Dễ (Easy - Chỉ Minimax)**:
  * Giải thuật Minimax tìm kiếm toàn bộ cây quyết định đến giới hạn độ sâu.
  * Phản ánh chính xác tư duy tính toán cơ bản nhưng tốn chi phí trạng thái rất lớn do không cắt nhánh.
* **Level 2 - Chế Độ Thường (Normal - Minimax + Alpha-Beta Pruning)**:
  * Tích hợp cơ chế cắt tỉa **Alpha-Beta Pruning** chuẩn mực giúp loại bỏ sớm các nhánh tìm kiếm chắc chắn không mang lại nước đi tối ưu hơn cho cả hai bên.
  * Giảm số trạng thái duyệt từ hàng vạn xuống hàng nghìn mà vẫn giữ nguyên độ chính xác 100% so với Minimax gốc.
* **Level 3 - Chế Độ Khó (Hard - Alpha-Beta + Zobrist Table + History Heuristic + Killer Moves + NegaScout/PVS)**:
  * **Bảng băm Zobrist (Transposition Table)**: Mã hóa trạng thái bàn cờ 12x12 thành mã băm 64-bit ngẫu nhiên cực nhanh. Lưu trữ kết quả cờ đã tính kèm theo biên giá trị toán học chuẩn (`EXACT`, `LOWERBOUND`, `UPPERBOUND`) nhằm tái sử dụng tức thì khi gặp trạng thái trùng lặp hoặc xoay vòng.
  * **Sắp xếp nước đi thông minh (Move Ordering)**:
    1. Ưu tiên các nước đi **Killer Moves** (nước cờ cực mạnh gây cắt nhánh sớm ở cùng độ sâu).
    2. Sắp xếp các nước đi tiềm năng theo điểm đánh giá thế trận tĩnh (`evaluate_cell_total`).
    3. **History Heuristic**: Lưu trữ lịch sử cắt nhánh, các ô cờ mang lại hiệu quả cắt tỉa cao ở các độ sâu trước sẽ được cộng điểm ưu tiên để duyệt sớm ở lượt tiếp theo.
  * **Principal Variation Search (NegaScout/PVS)**: Thuật toán tìm kiếm cửa sổ hẹp giúp gia tăng tốc độ kiểm tra các nhánh cờ phụ, tối ưu hóa thời gian xử lý lên gấp 2-3 lần so với Alpha-Beta thông thường.
  * **Tìm Kiếm Sâu Dần (Iterative Deepening)**: Cho phép AI tìm kiếm tăng dần từ Depth 1 đến Depth đích. Hỗ trợ cơ chế **Time Control** (Giới hạn thời gian) giúp AI luôn có sẵn nước đi dự phòng tối ưu nhất ngay cả khi bị buộc dừng đột ngột do hết giờ.

### 2.2. Hệ Thống Ưu Tiên Chiến Thuật Tuyệt Đối (Tactical Priority Hierarchy)
Để AI chơi cờ sắc sảo và mang tính người nhất, hàm lượng giá tĩnh của chúng tôi sử dụng cấu trúc phân tầng điểm số phi tuyến tính (Geometric/Priority Scaling):
1. **Ưu tiên 1 (Thắng ngay - ATK)**: Phát hiện nước đi giúp AI tạo chuỗi 4 quân thắng ngay lập tức ⭢ *Thưởng 100,000,000+ điểm*.
2. **Ưu tiên 2 (Chặn thắng - DEF)**: Phát hiện đối thủ sắp tạo chuỗi 4 quân thắng, AI buộc phải đánh chặn ⭢ *Thưởng 90,000,000+ điểm*.
3. **Ưu tiên 3 (Kiến tạo nước đôi - ATK Fork)**: AI tự tạo thế nước đôi (ví dụ hai đầu mở hoặc hai hàng 3 quân) ép đối thủ vào thế không thể phòng ngự đồng thời ⭢ *Thưởng 80,000,000+ điểm*.
4. **Ưu tiên 4 (Chặn nước đôi của đối phương - DEF Fork)**: AI chủ động đánh chặn vào tọa độ trọng yếu mà đối thủ chuẩn bị kiến tạo thế nước đôi nguy hiểm ⭢ *Thưởng 70,000,000+ điểm*.
5. **Điểm Cơ Sở & Cự Ly**: Cộng điểm dựa trên các cấu trúc thế cờ đơn lẻ (Open 3, Closed 3, Broken 3, Open 2, Closed 2, Gapped 2...) kết hợp ưu tiên vị trí trung tâm bàn cờ và nhân hệ số co cụm **x1.2** nếu nằm kề các quân cờ đã đánh để tạo tính liên kết chiến thuật.

---

## 🛠️ 3. Hướng Dẫn Cài Đặt & Vận Hành Chương Trình

### 3.1. Yêu Cầu Môi Trường
* **Ngôn ngữ**: **Python 3.8** trở lên.
* **Thư viện đồ họa**: **Tkinter** (Là thư viện chuẩn mặc định của Python, **không cần** cài thêm thư viện bên ngoài nên sẽ không sợ bị lỗi cài đặt).

### 3.2. Khởi Chạy Giao Diện Đồ Họa (GUI)
Để bắt đầu chơi cờ với máy, bạn chỉ cần mở Command Prompt / PowerShell (Windows) hoặc Terminal (macOS/Linux) tại thư mục dự án và gõ lệnh:
```bash
python play.py
```

#### 🎮 Các thao tác trên giao diện:
1. **Bắt đầu ván cờ**: Nhấn nút **Chơi X (Trước)** hoặc **Chơi O (Sau)** ở cột điều khiển bên phải. Quân X sẽ đi trước.
2. **Thiết lập AI**:
   * **Chế độ**: Chọn *Easy (Chỉ Minimax)*, *Normal (Alpha-Beta)*, hoặc *Hard (Alpha-Beta + Bảng băm)*.
   * **Độ sâu (Depth)**: Số bước tính trước của máy (Khuyên dùng: **Depth 3 đến 5** để AI vừa cực kỳ thông minh vừa phản hồi dưới 1 giây).
   * **Thời gian giới hạn**: Đặt giới hạn giây tối đa cho mỗi lượt suy nghĩ của AI.
3. **Chức năng bổ trợ**:
   * **↶ Lùi bước (Undo)**: Rút lại nước cờ vừa đi của cả bạn và AI để đi lại.
   * **⏹ Hủy trận**: Kết thúc ván hiện tại, xóa sạch bàn cờ để chuẩn bị chơi ván mới.
   * **🔄 Reset Tỉ số**: Reset tỉ số đối đầu giữa Bạn và AI về 0 - 0.
4. **Trực quan hóa Chiến thuật (Sandbox Mode)**:
   * Nhấp nút **✏️ Chế độ tự do**.
   * Bấm tự do lên bàn cờ để đặt quân (Click lần 1 ra **X**, click lần 2 ra **O**, click lần 3 xóa về **Trống**).
   * Bấm nút **🤖 AI đi tiếp** để chuyển giao thế trận vừa nạp cho AI suy nghĩ và đánh tiếp.

---

## 📊 4. Đánh Giá Hiệu Năng & Xuất Báo Cáo Tự Động (Level 3 Benchmark)

Đề bài yêu cầu đo đạc thực nghiệm số trạng thái đã xét và thời gian chạy trên **ít nhất 5 thế cờ** khác nhau ở các độ sâu 1, 2, 3. Để thực hiện việc này một cách chuẩn xác và tiết kiệm thời gian nhất, chúng tôi đã đóng gói sẵn script tự động hóa hoàn toàn.

Hãy chạy lệnh sau trong thư mục dự án:
```bash
python performance_eval.py
```

### 📈 Kết quả sau khi chạy thành công:
1. Tiến trình kiểm thử giả lập 5 thế cờ x 3 thuật toán x 3 độ sâu tìm kiếm sẽ được hiển thị trực tiếp trên màn hình terminal.
2. Một tệp báo cáo chuyên sâu mang tên **`benchmark_report.md`** sẽ tự động được tạo ra tại thư mục gốc của dự án.
3. Bạn có thể mở trực tiếp tệp **benchmark_report.md** lên và nhấn tổ hợp phím `Ctrl + Shift + V` trong VS Code để chiêm ngưỡng bảng so sánh hiệu năng trực quan cùng phần phân tích lý thuyết đầy đủ cho cả 7 câu hỏi thảo luận lý thuyết cờ Caro (có thể sao chép trực tiếp vào báo cáo word/pdf của nhóm).

---

*Chúc các thầy cô và các bạn có những trải nghiệm đấu trí thú vị và đạt điểm số tối đa với sản phẩm Caro AI của nhóm!* 🏆
