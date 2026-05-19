import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time
import copy

from core.constants import BOARD_SIZE, EMPTY, X_PIECE, O_PIECE
from core.ai_engine import AISolver
from core.gomoku_rules import check_win_logic, is_board_full
from gui.button import create_action_button

class GomokuApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Caro AI Game - Nhóm: Nam Anh (23021215) - Tá Cường (23021223) - Đức Đạt (23021241)")
        self.root.geometry("1200x760")
        self.root.configure(bg="#121212")
        
        self.state_lock = threading.Lock()
        
        self.board = [[EMPTY for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        self.move_history = [] 
        
        self.player_piece = X_PIECE
        self.ai_piece = O_PIECE
        self.current_turn = X_PIECE
        self.game_active = False
        self.ai_request_id = 0
        self.ai_is_thinking = False
        self.is_edit_mode = False
        
        self.player_score = 0
        self.ai_score = 0
        
        self.last_move_ui = None
        self.winning_line_ui = []
        
        self.cell_size = 0
        self.offset_x = 0
        self.offset_y = 0
        self.cell_ids = [[None for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]

        self.timer_running = False
        self.start_time_real = 0
        self.timer_id = None

        self.setup_styles()
        self.setup_ui()

    def get_cancel_token(self):
        with self.state_lock:
            return self.ai_request_id

    def check_and_start_timer(self):
        if not self.timer_running:
            self.timer_running = True
            self.start_time_real = time.time()
            self.update_timer()

    def update_timer(self):
        if self.timer_running:
            elapsed = int(time.time() - self.start_time_real)
            mins, secs = divmod(elapsed, 60)
            self.lbl_timer.config(text=f"Thời gian: {mins:02d}:{secs:02d}")
            self.timer_id = self.root.after(1000, self.update_timer)

    def stop_timer(self):
        self.timer_running = False
        if self.timer_id:
            self.root.after_cancel(self.timer_id)
            self.timer_id = None

    def reset_score(self):
        self.player_score = 0
        self.ai_score = 0
        self.lbl_score.config(text=f"Bạn: {self.player_score}  -  AI: {self.ai_score}")

    def clear_log(self):
        if hasattr(self, 'log_tree'):
            for item in self.log_tree.get_children():
                self.log_tree.delete(item)
        if hasattr(self, 'lbl_ai_status'):
            self.lbl_ai_status.config(text="Trạng thái: Sẵn sàng", fg="#ffffff")
        if hasattr(self, 'lbl_ai_score_val'):
            self.lbl_ai_score_val.config(text="Điểm thế trận: 0", fg="#2ed573")
        if hasattr(self, 'lbl_ai_judgment'):
            self.lbl_ai_judgment.config(text="Nhận định: Trận đấu cân bằng", fg="#a4b0be")

    def stop_game(self):
        with self.state_lock:
            self.ai_request_id += 1 
            self.game_active = False
            self.ai_is_thinking = False
            
            self.board = [[EMPTY for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
            self.move_history.clear()
            self.clear_log() 
            self.last_move_ui = None
            self.winning_line_ui = []
            
            self.btn_x.config(state=tk.NORMAL)
            self.btn_o.config(state=tk.NORMAL)
            self.lbl_stats.config(text="")
            
            self.stop_timer()
            self.lbl_timer.config(text="Thời gian: 00:00")
            
            self.update_board_pieces()
            self.update_status("Đã hủy ván. Vui lòng chọn quân cờ!", "#ffa502")

    def undo_move(self):
        with self.state_lock:
            if not self.move_history: return 

            self.ai_request_id += 1
            self.ai_is_thinking = False
            self.game_active = True 
            self.btn_x.config(state=tk.DISABLED)
            self.btn_o.config(state=tk.DISABLED)

            last_piece = self.move_history[-1][2]
            moves_to_undo = 2 if (last_piece == self.ai_piece and len(self.move_history) >= 2) else 1
                
            for _ in range(moves_to_undo):
                if self.move_history:
                    r, c, p = self.move_history.pop()
                    self.board[r][c] = EMPTY
                    
                    if hasattr(self, 'log_tree'):
                        children = self.log_tree.get_children()
                        if children:
                            self.log_tree.delete(children[-1])
            
            self.current_turn = self.player_piece
            
            if self.move_history:
                self.last_move_ui = (self.move_history[-1][0], self.move_history[-1][1])
            else:
                self.last_move_ui = None
                self.stop_timer()
                self.lbl_timer.config(text="Thời gian: 00:00")
                
            self.winning_line_ui = []
            self.update_board_pieces()
            self.update_status("Đã lùi bước. Đến lượt BẠN!", "#2ed573")
            if hasattr(self, 'lbl_ai_status'):
                self.lbl_ai_status.config(text="Trạng thái: Chờ bạn di chuyển...", fg="#ffffff")

    def toggle_edit_mode(self):
        with self.state_lock:
            if not self.is_edit_mode:
                self.is_edit_mode = True
                self.game_active = False
                self.ai_request_id += 1 
                self.ai_is_thinking = False
                self.stop_timer()
                
                self.btn_x.config(state=tk.DISABLED)
                self.btn_o.config(state=tk.DISABLED)
                
                self.btn_edit.config(text="✅ Tắt tự do", bg="#27ae60")
                self.update_status("Chế độ Tự do: Click vào bàn cờ để đổi quân (Trống -> X -> O).", "#9b59b6")
            else:
                self.is_edit_mode = False
                self.btn_edit.config(text="✏️ Chế độ tự do", bg="#9b59b6")
                
                self.btn_x.config(state=tk.NORMAL)
                self.btn_o.config(state=tk.NORMAL)
                
                self.update_status("Đã tắt chế độ Tự do. Nhấn 'Cho AI đánh tiếp' hoặc tự chơi.", "#2ed573")

    def trigger_ai_from_edit(self):
        with self.state_lock:
            if self.is_edit_mode:
                self.is_edit_mode = False
                self.btn_edit.config(text="✏️ Chế độ tự do", bg="#9b59b6")
                self.btn_x.config(state=tk.NORMAL)
                self.btn_o.config(state=tk.NORMAL)

            self.ai_request_id += 1
            self.game_active = True
            self.ai_is_thinking = False
            self.stop_timer()
            
            x_count = sum(row.count(X_PIECE) for row in self.board)
            o_count = sum(row.count(O_PIECE) for row in self.board)
            
            if x_count <= o_count:
                self.ai_piece = X_PIECE
                self.player_piece = O_PIECE
            else:
                self.ai_piece = O_PIECE
                self.player_piece = X_PIECE
                
            self.current_turn = self.ai_piece
            self.update_status(f"Tạo thế cờ xong! AI ({'X' if self.ai_piece == X_PIECE else 'O'}) đang đánh...", "#ffa502")
            
            self._trigger_ai_thread_locked()



    def start_game(self, player_piece):
        with self.state_lock:
            self.ai_request_id += 1
            self.board = [[EMPTY for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
            self.move_history.clear()
            self.clear_log() 
            
            self.player_piece = player_piece
            self.ai_piece = O_PIECE if player_piece == X_PIECE else X_PIECE
            self.current_turn = X_PIECE
            self.game_active = True
            self.ai_is_thinking = False
            
            self.last_move_ui = None
            self.winning_line_ui = []
            
            self.btn_x.config(state=tk.DISABLED)
            self.btn_o.config(state=tk.DISABLED)
            self.lbl_stats.config(text="")
            
            self.stop_timer()
            self.lbl_timer.config(text="Thời gian: 00:00")
            self.update_board_pieces()

            if self.ai_piece == X_PIECE:
                self._trigger_ai_thread_locked()
            else:
                self.update_status("Lượt của BẠN!", "#2ed573")
                if hasattr(self, 'lbl_ai_status'):
                    self.lbl_ai_status.config(text="Trạng thái: Chờ bạn di chuyển...", fg="#ffffff")

    def end_game(self, winner_piece, last_r, last_c):
        self.game_active = False
        self.ai_request_id += 1 
        self.ai_is_thinking = False
        self.stop_timer()
        
        self.btn_x.config(state=tk.NORMAL)
        self.btn_o.config(state=tk.NORMAL)

        if winner_piece != EMPTY and last_r is not None:
            _, line = check_win_logic(self.board, last_r, last_c, winner_piece)
            self.winning_line_ui = line

        if winner_piece == self.player_piece:
            self.player_score += 1
            self.update_status("BẠN ĐÃ THẮNG!", "#2ed573")
            if hasattr(self, 'lbl_ai_status'): self.lbl_ai_status.config(text="Trạng thái: Game Kết Thúc", fg="#2ed573")
            if hasattr(self, 'lbl_ai_judgment'): self.lbl_ai_judgment.config(text="Nhận định: Bạn đã thắng ván này!", fg="#2ed573")
            messagebox.showinfo("Kết quả", "Bạn đã chiến thắng!")
        elif winner_piece == self.ai_piece:
            self.ai_score += 1
            self.update_status("AI ĐÃ THẮNG!", "#ff4757")
            if hasattr(self, 'lbl_ai_status'): self.lbl_ai_status.config(text="Trạng thái: Game Kết Thúc", fg="#ff4757")
            if hasattr(self, 'lbl_ai_judgment'): self.lbl_ai_judgment.config(text="Nhận định: AI hạ gục người chơi!", fg="#ff4757")
            messagebox.showinfo("Kết quả", "AI đã chiến thắng!")
        else:
            self.update_status("VÁN CỜ HÒA!", "#ffa502")
            if hasattr(self, 'lbl_ai_status'): self.lbl_ai_status.config(text="Trạng thái: Game Kết Thúc", fg="#ffa502")
            messagebox.showinfo("Kết quả", "Hòa!")

        self.update_board_pieces()
        self.lbl_score.config(text=f"Bạn: {self.player_score}  -  AI: {self.ai_score}")

    def on_canvas_click(self, event):
        with self.state_lock:
            c = int((event.x - self.offset_x) // self.cell_size)
            r = int((event.y - self.offset_y) // self.cell_size)
            
            if getattr(self, 'is_edit_mode', False) and 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE:
                current = self.board[r][c]
                if current == EMPTY:
                    self.board[r][c] = X_PIECE
                elif current == X_PIECE:
                    self.board[r][c] = O_PIECE
                else:
                    self.board[r][c] = EMPTY
                self.update_board_pieces()
                return

            if not self.game_active or self.ai_is_thinking or self.current_turn != self.player_piece: 
                return


            if 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE:
                if self.board[r][c] != EMPTY: return
                
                self.board[r][c] = self.player_piece
                self.move_history.append((r, c, self.player_piece)) 
                self.last_move_ui = (r, c)
                self.current_turn = self.ai_piece 
                
                pos_str = f"{chr(65 + c)}{r + 1}"
                if hasattr(self, 'log_tree'):
                    self.log_tree.insert("", "end", values=(len(self.move_history), "Người", pos_str, "-", "-", "-", "-"))
                    self.log_tree.yview_moveto(1.0) 

                self.check_and_start_timer()
                self.update_board_pieces()

                is_win, _ = check_win_logic(self.board, r, c, self.player_piece)
                if is_win:
                    self.end_game(self.player_piece, r, c)
                elif is_board_full(self.board):
                    self.end_game(EMPTY, None, None)
                else:
                    self._trigger_ai_thread_locked()

    def _trigger_ai_thread_locked(self):
        self.ai_request_id += 1
        current_req_id = self.ai_request_id
        self.ai_is_thinking = True
        
        if hasattr(self, 'lbl_ai_status'):
            self.lbl_ai_status.config(text="Trạng thái: AI đang suy nghĩ...", fg="#ffa502")
        
        board_snapshot = [row[:] for row in self.board]
        current_mode_text = self.mode_var.get()
        if "Easy" in current_mode_text: logic_mode = "easy"
        elif "Normal" in current_mode_text: logic_mode = "normal"
        else: logic_mode = "hard"

        t = threading.Thread(
            target=self.run_ai_logic, 
            args=(board_snapshot, self.ai_piece, self.player_piece, current_req_id, self.depth_var.get(), self.time_var.get(), logic_mode), 
            daemon=True
        )
        t.start()
        self.update_status(f"AI đang phân tích ({logic_mode})...", "#ffa502")

    def run_ai_logic(self, board_snapshot, ai_p, pl_p, req_id, d_limit, t_limit, mode):
        solver = AISolver(board_snapshot, ai_p, pl_p, req_id, d_limit, t_limit, mode)
        best_move, best_score, depth, nodes, hits, t_spent = solver.search(self.get_cancel_token)
        self.root.after(0, self.apply_ai_move, best_move, best_score, req_id, depth, nodes, hits, t_spent)

    def apply_ai_move(self, move, best_score, req_id, depth, nodes, hits, t_spent):
        with self.state_lock:
            if not self.game_active or req_id != self.ai_request_id or self.current_turn != self.ai_piece:
                return

            if move:
                r, c = move
                if self.board[r][c] != EMPTY: return
                
                self.board[r][c] = self.ai_piece
                self.move_history.append((r, c, self.ai_piece)) 
                self.last_move_ui = (r, c)
                self.ai_is_thinking = False
                self.current_turn = self.player_piece
                
                self.check_and_start_timer()
                self.update_board_pieces()
                
                display_score = best_score
                if best_score > 5000000: display_score = "Thắng tuyệt đối!"
                elif best_score < -5000000: display_score = "Thua tuyệt đối!"
                
                self.lbl_stats.config(text=f"Score: {display_score} | Depth: {depth} | Nodes: {nodes} | TT Cache: {hits} | Time: {t_spent}s")

                if hasattr(self, 'lbl_ai_status'):
                    self.lbl_ai_status.config(text="Trạng thái: Đang đợi Bạn đi...", fg="#2ed573")
                if hasattr(self, 'lbl_ai_score_val'):
                    self.lbl_ai_score_val.config(text=f"Điểm thế trận: {display_score}", fg="#5352ed" if isinstance(best_score, str) else ("#ff4757" if best_score > 500 else "#2ed573"))
                
                if isinstance(best_score, (int, float)):
                    if best_score > 10000: judgment = "AI đang ép sân rất mạnh!"; j_color = "#ff4757"
                    elif best_score > 500: judgment = "AI lợi thế chủ động công."; j_color = "#ffa502"
                    elif best_score < -10000: judgment = "Nguy hiểm! Bạn đang áp đảo AI."; j_color = "#2ed573"
                    elif best_score < -500: judgment = "Bạn đang giữ thế chủ động."; j_color = "#2ed573"
                    else: judgment = "Thế trận cân bằng giằng co."; j_color = "#a4b0be"
                else:
                    judgment = "Trận đấu đã ngã ngũ cục diện!"; j_color = "#ff4757"
                if hasattr(self, 'lbl_ai_judgment'):
                    self.lbl_ai_judgment.config(text=f"Nhận định: {judgment}", fg=j_color)

                if hasattr(self, 'log_tree'):
                    pos_str = f"{chr(65 + c)}{r + 1}"
                    self.log_tree.insert("", "end", values=(len(self.move_history), "AI", pos_str, display_score, depth, nodes, f"{t_spent}s"))
                    self.log_tree.yview_moveto(1.0) 

                is_win, _ = check_win_logic(self.board, r, c, self.ai_piece)
                if is_win:
                    self.end_game(self.ai_piece, r, c)
                elif is_board_full(self.board):
                    self.end_game(EMPTY, None, None)
                else:
                    self.update_status("Đến lượt BẠN!", "#2ed573")

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TButton", font=("Arial", 10, "bold"), padding=5)
        style.configure("Dark.TFrame", background="#121212")
        style.configure("Treeview", background="#2f3542", foreground="white", fieldbackground="#2f3542", rowheight=25, font=("Consolas", 9))
        style.configure("Treeview.Heading", background="#1e272e", foreground="white", font=("Arial", 9, "bold"))
        style.map("Treeview.Heading", background=[('active', '#2f3542')])

    def setup_ui(self):
        # Container chính chia làm 2 cột: Cột trái (Bàn cờ) và Cột phải (Hệ thống điều khiển)
        main_container = ttk.Frame(self.root, style="Dark.TFrame")
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # CỘT TRÁI: BÀN CỜ CARO (Chiếm không gian lớn nhất, tự động co giãn)
        self.canvas_frame = tk.Frame(main_container, bg="#121212")
        self.canvas_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(self.canvas_frame, bg="#1e272e", highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.canvas.bind("<Configure>", lambda e: self.draw_board())
        self.canvas.bind("<Button-1>", self.on_canvas_click)

        # CỘT PHẢI: BẢNG ĐIỀU KHIỂN & LỊCH SỬ NƯỚC ĐI (Độ rộng cố định 380px)
        right_frame = tk.Frame(main_container, bg="#121212", width=380)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=False, padx=(15, 0))
        right_frame.pack_propagate(False)

        # 1. Thẻ tiêu đề & Tác giả
        title_frame = tk.Frame(right_frame, bg="#1e272e", bd=1, relief=tk.SOLID)
        title_frame.pack(fill=tk.X, pady=(0, 10))
        tk.Label(title_frame, text="CARO AI - BÀI LẬP TRÌNH 1", font=("Arial", 12, "bold"), bg="#1e272e", fg="#ffdd59").pack(pady=(8, 2))
        tk.Label(title_frame, text="Nhóm: Nam Anh - Tá Cường - Đức Đạt", font=("Arial", 9, "italic"), bg="#1e272e", fg="#a4b0be").pack(pady=(0, 8))

        # 2. Bảng điều khiển chính & Trạng thái trò chơi
        dashboard_lf = tk.LabelFrame(right_frame, text=" 📊 BẢNG TRẠNG THÁI ", font=("Arial", 10, "bold"), bg="#1e1e24", fg="#ffdd59", bd=1, relief=tk.SOLID)
        dashboard_lf.pack(fill=tk.X, pady=(0, 10))
        
        status_row = tk.Frame(dashboard_lf, bg="#1e1e24")
        status_row.pack(fill=tk.X, padx=10, pady=4)
        self.lbl_score = tk.Label(status_row, text="Bạn: 0  -  AI: 0", font=("Consolas", 13, "bold"), bg="#1e1e24", fg="#2ed573")
        self.lbl_score.pack(side=tk.LEFT)
        self.lbl_timer = tk.Label(status_row, text="Thời gian: 00:00", font=("Consolas", 13, "bold"), bg="#1e1e24", fg="#ffdd59")
        self.lbl_timer.pack(side=tk.RIGHT)

        self.lbl_status = tk.Label(dashboard_lf, text="Vui lòng chọn quân cờ để bắt đầu!", font=("Arial", 11, "bold"), bg="#1e1e24", fg="#ffa502", wraplength=340)
        self.lbl_status.pack(fill=tk.X, padx=10, pady=4)
        self.lbl_stats = tk.Label(dashboard_lf, text="", font=("Consolas", 9), bg="#1e1e24", fg="#a4b0be", wraplength=340)
        self.lbl_stats.pack(fill=tk.X, padx=10, pady=(0, 4))

        # 3. Thiết lập thông số AI
        config_lf = tk.LabelFrame(right_frame, text=" ⚙️ THIẾT LẬP THUẬT TOÁN AI ", font=("Arial", 10, "bold"), bg="#1e1e24", fg="#ffdd59", bd=1, relief=tk.SOLID)
        config_lf.pack(fill=tk.X, pady=(0, 10))

        mode_frame = tk.Frame(config_lf, bg="#1e1e24")
        mode_frame.pack(fill=tk.X, padx=10, pady=4)
        tk.Label(mode_frame, text="Chế độ:", bg="#1e1e24", fg="white", font=("Arial", 10)).pack(side=tk.LEFT)
        self.mode_var = tk.StringVar(value="Normal (Minimax + Alpha-Beta)")
        cb_mode = ttk.Combobox(mode_frame, textvariable=self.mode_var, state="readonly", width=25)
        cb_mode['values'] = ["Easy (Chỉ Minimax)", "Normal (Minimax + Alpha-Beta)", "Hard (Alpha-Beta + Bảng băm)"]
        cb_mode.pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=(5, 0))

        params_frame = tk.Frame(config_lf, bg="#1e1e24")
        params_frame.pack(fill=tk.X, padx=10, pady=4)
        tk.Label(params_frame, text="Độ sâu:", bg="#1e1e24", fg="white", font=("Arial", 10)).pack(side=tk.LEFT)
        self.depth_var = tk.IntVar(value=4)
        ttk.Spinbox(params_frame, from_=2, to=8, textvariable=self.depth_var, width=4).pack(side=tk.LEFT, padx=(5, 10))

        tk.Label(params_frame, text="Thời gian (s):", bg="#1e1e24", fg="white", font=("Arial", 10)).pack(side=tk.LEFT, padx=(10, 0))
        self.time_var = tk.DoubleVar(value=2.0)
        ttk.Spinbox(params_frame, from_=0.5, to=10.0, increment=0.5, textvariable=self.time_var, width=5).pack(side=tk.LEFT, padx=(5, 0))

        # 4. Điều khiển trận đấu
        control_lf = tk.LabelFrame(right_frame, text=" 🎮 ĐIỀU KHIỂN TRẬN ĐẤU ", font=("Arial", 10, "bold"), bg="#1e1e24", fg="#ffdd59", bd=1, relief=tk.SOLID)
        control_lf.pack(fill=tk.X, pady=(0, 10))

        start_frame = tk.Frame(control_lf, bg="#1e1e24")
        start_frame.pack(fill=tk.X, padx=10, pady=4)
        self.btn_x = create_action_button(start_frame, "Chơi X (Trước)", "#ff4757", "white", lambda: self.start_game(X_PIECE))
        self.btn_x.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        self.btn_o = create_action_button(start_frame, "Chơi O (Sau)", "#1e90ff", "white", lambda: self.start_game(O_PIECE))
        self.btn_o.pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=(5, 0))

        action_frame = tk.Frame(control_lf, bg="#1e1e24")
        action_frame.pack(fill=tk.X, padx=10, pady=4)
        create_action_button(action_frame, "↶ Lùi bước (Undo)", "#2f3542", "white", self.undo_move).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        create_action_button(action_frame, "⏹ Hủy trận", "#2f3542", "white", self.stop_game).pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=(5, 0))

        util_frame = tk.Frame(control_lf, bg="#1e1e24")
        util_frame.pack(fill=tk.X, padx=10, pady=4)
        create_action_button(util_frame, "🔄 Reset Tỉ số", "#2f3542", "white", self.reset_score).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        create_action_button(util_frame, "🗑 Xóa dữ liệu", "#2f3542", "white", self.clear_log).pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=(5, 0))

        custom_frame = tk.Frame(control_lf, bg="#1e1e24")
        custom_frame.pack(fill=tk.X, padx=10, pady=(4, 6))
        self.btn_edit = create_action_button(custom_frame, "✏️ Chế độ tự do", "#9b59b6", "white", self.toggle_edit_mode)
        self.btn_edit.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        self.btn_ai_next = create_action_button(custom_frame, "🤖 AI đi tiếp", "#e67e22", "white", self.trigger_ai_from_edit)
        self.btn_ai_next.pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=(5, 0))



        # 6. Lịch sử nước đi (Log)
        hist_lf = tk.LabelFrame(right_frame, text=" 📜 LỊCH SỬ NƯỚC ĐI ", font=("Arial", 10, "bold"), bg="#1e1e24", fg="#ffdd59", bd=1, relief=tk.SOLID)
        hist_lf.pack(fill=tk.BOTH, expand=True, pady=(0, 5))

        columns = ("no", "player", "pos", "score", "depth", "nodes", "time")
        self.log_tree = ttk.Treeview(hist_lf, columns=columns, show="headings")
        self.log_tree.heading("no", text="#")
        self.log_tree.heading("player", text="Bên")
        self.log_tree.heading("pos", text="Vị trí")
        self.log_tree.heading("score", text="Điểm AI")
        self.log_tree.heading("depth", text="Sâu")
        self.log_tree.heading("nodes", text="Nodes")
        self.log_tree.heading("time", text="Thời gian")

        self.log_tree.column("no", width=30, anchor=tk.CENTER)
        self.log_tree.column("player", width=45, anchor=tk.CENTER)
        self.log_tree.column("pos", width=45, anchor=tk.CENTER)
        self.log_tree.column("score", width=75, anchor=tk.W)
        self.log_tree.column("depth", width=35, anchor=tk.CENTER)
        self.log_tree.column("nodes", width=70, anchor=tk.CENTER)
        self.log_tree.column("time", width=60, anchor=tk.CENTER)

        scrollbar = ttk.Scrollbar(hist_lf, orient=tk.VERTICAL, command=self.log_tree.yview)
        self.log_tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.log_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    def update_status(self, text, color):
        self.lbl_status.config(text=text, fg=color)

    def draw_board(self):
        self.canvas.delete("all")
        w, h = self.canvas.winfo_width(), self.canvas.winfo_height()
        if w < 10 or h < 10: return

        margin = 25
        board_size_px = min(w, h) * 0.95 - margin
        self.cell_size = board_size_px / BOARD_SIZE
        self.offset_x = (w - board_size_px) / 2 + margin / 2
        self.offset_y = (h - board_size_px) / 2 + margin / 2

        self.cell_ids = [[None for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]

        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                x1 = self.offset_x + c * self.cell_size
                y1 = self.offset_y + r * self.cell_size
                x2, y2 = x1 + self.cell_size, y1 + self.cell_size
                bg_color = "#57606f"
                if self.last_move_ui == (r, c): bg_color = "#3742fa"
                if (r, c) in self.winning_line_ui: bg_color = "#f1c40f"

                rect_id = self.canvas.create_rectangle(x1, y1, x2, y2, fill=bg_color, outline="#2f3542", width=2)
                self.cell_ids[r][c] = rect_id
                
                piece = self.board[r][c]
                if piece != EMPTY:
                    self.draw_piece_at(r, c, piece)

        font_size = max(8, int(self.cell_size * 0.3))
        for c in range(BOARD_SIZE):
            x = self.offset_x + c * self.cell_size + self.cell_size / 2
            y = self.offset_y - 15
            self.canvas.create_text(x, y, text=chr(65 + c), fill="#a4b0be", font=("Arial", font_size, "bold"))
            
        for r in range(BOARD_SIZE):
            x = self.offset_x - 15
            y = self.offset_y + r * self.cell_size + self.cell_size / 2
            self.canvas.create_text(x, y, text=str(r + 1), fill="#a4b0be", font=("Arial", font_size, "bold"))

    def update_board_pieces(self):
        self.canvas.delete("piece")
        
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                bg_color = "#57606f"
                if self.last_move_ui == (r, c): bg_color = "#3742fa"
                if (r, c) in self.winning_line_ui: bg_color = "#f1c40f"

                if self.cell_ids[r][c] is not None:
                    self.canvas.itemconfig(self.cell_ids[r][c], fill=bg_color)

                piece = self.board[r][c]
                if piece != EMPTY:
                    self.draw_piece_at(r, c, piece)

    def draw_piece_at(self, r, c, piece):
        x1 = self.offset_x + c * self.cell_size
        y1 = self.offset_y + r * self.cell_size
        x2, y2 = x1 + self.cell_size, y1 + self.cell_size
        pad = self.cell_size * 0.25
        thickness = max(3, int(self.cell_size * 0.08))
        if piece == X_PIECE:
            self.canvas.create_line(x1+pad, y1+pad, x2-pad, y2-pad, fill="#ff4757", width=thickness, capstyle=tk.ROUND, tags="piece")
            self.canvas.create_line(x1+pad, y2-pad, x2-pad, y1+pad, fill="#ff4757", width=thickness, capstyle=tk.ROUND, tags="piece")
        elif piece == O_PIECE:
            self.canvas.create_oval(x1+pad, y1+pad, x2-pad, y2-pad, outline="#1e90ff", width=thickness, tags="piece")