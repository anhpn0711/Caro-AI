import time
import math
from source_code.constants import BOARD_SIZE, WIN_COUNT, EMPTY, ZOBRIST_TABLE

class AISolver:
    def __init__(self, board_snapshot, ai_piece, player_piece, request_id, max_depth, time_limit, mode="hard"):
        self.board = board_snapshot
        self.ai_piece = ai_piece
        self.player_piece = player_piece
        self.request_id = request_id
        self.max_depth = max_depth
        self.time_limit = time_limit
        self.mode = mode 
        
        self.current_hash = self._compute_initial_hash()
        self.transposition_table = {}
        self.history_heuristic = [[0 for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        self.killer_moves = [[None, None] for _ in range(max_depth + 1)]
        
        self.nodes_evaluated = 0
        self.cache_hits = 0
        self.start_time = 0
        self.timeout_flag = False

        self.empty_cells = 0
        self.ai_pieces = set()
        self.player_pieces = set()
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                if self.board[r][c] == EMPTY:
                    self.empty_cells += 1
                elif self.board[r][c] == self.ai_piece:
                    self.ai_pieces.add((r, c))
                elif self.board[r][c] == self.player_piece:
                    self.player_pieces.add((r, c))

    def _compute_initial_hash(self):
        h = 0
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                p = self.board[r][c]
                if p != EMPTY: h ^= ZOBRIST_TABLE[r][c][p]
        return h

    def make_move(self, r, c, piece):
        self.board[r][c] = piece
        self.current_hash ^= ZOBRIST_TABLE[r][c][piece]
        self.empty_cells -= 1
        if piece == self.ai_piece:
            self.ai_pieces.add((r, c))
        else:
            self.player_pieces.add((r, c))

    def undo_move(self, r, c, piece):
        self.board[r][c] = EMPTY
        self.current_hash ^= ZOBRIST_TABLE[r][c][piece]
        self.empty_cells += 1
        if piece == self.ai_piece:
            self.ai_pieces.remove((r, c))
        else:
            self.player_pieces.remove((r, c))

    def is_full(self):
        return self.empty_cells == 0

    def check_win_logic(self, r, c, piece):
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
        for dr, dc in directions:
            count = 1
            nr, nc = r + dr, c + dc
            while 0 <= nr < BOARD_SIZE and 0 <= nc < BOARD_SIZE and self.board[nr][nc] == piece:
                count += 1; nr += dr; nc += dc
            nr, nc = r - dr, c - dc
            while 0 <= nr < BOARD_SIZE and 0 <= nc < BOARD_SIZE and self.board[nr][nc] == piece:
                count += 1; nr -= dr; nc -= dc
            if count >= WIN_COUNT: return True
        return False

    def detect_pattern(self, line_str):
        """
        Nhận diện mẫu hình mạnh nhất trong chuỗi 7 ô (chứa X ở tâm index 3).
        Duyệt qua 4 cửa sổ kích thước 4 bao phủ index 3, đánh giá và lấy MAX score.
        """
        max_score = 0
        pattern_name = "NONE"
        
        # 4 cửa sổ dài 4 bao phủ tâm index 3
        for start_idx in range(4):
            win = line_str[start_idx : start_idx + 4]
            # Nếu chứa quân đối thủ/biên thì không thể tạo thành 4-in-a-row
            if "O" in win:
                continue
                
            count_x = win.count("X")
            
            # Đếm số đầu thoáng ở hai phía của cửa sổ
            L_neighbor = line_str[start_idx - 1] if start_idx > 0 else "O"
            R_neighbor = line_str[start_idx + 4] if start_idx + 4 < 7 else "O"
            
            open_ends = 0
            if L_neighbor == "_": open_ends += 1
            if R_neighbor == "_": open_ends += 1
            
            score = 0
            current_name = "NONE"
            
            if count_x == 4:
                score = 1000000
                current_name = "WIN"
            elif count_x == 3:
                # Phân biệt mẫu liền kề và mẫu gãy
                if win in ["_XXX", "XXX_"]:
                    if open_ends == 2:
                        score = 50000
                        current_name = "OPEN_3"
                    elif open_ends == 1:
                        score = 10000
                        current_name = "CLOSED_3"
                else: # Mẫu gãy XX_X hoặc X_XX
                    if open_ends == 2:
                        score = 40000
                        current_name = "OPEN_BROKEN_3"
                    elif open_ends == 1:
                        score = 8000
                        current_name = "CLOSED_BROKEN_3"
            elif count_x == 2:
                # Phân biệt Open 2, Open Gapped 2 (_X_X_), Gapped 2 (X_X), Closed 2
                if win in ["_XX_", "XX__", "__XX"]:
                    if open_ends == 2:
                        score = 2000
                        current_name = "OPEN_2"
                    elif open_ends == 1:
                        score = 500
                        current_name = "CLOSED_2"
                elif win in ["_X_X", "X_X_"]:
                    if open_ends == 2:
                        score = 1800  # _X_X_
                        current_name = "OPEN_GAPPED_2"
                    elif open_ends == 1:
                        score = 400
                        current_name = "CLOSED_GAPPED_2"
                else: # X__X
                    if open_ends == 2:
                        score = 1500  # X_X
                        current_name = "GAPPED_2"
                    elif open_ends == 1:
                        score = 300
                        current_name = "CLOSED_GAPPED_2"
            elif count_x == 1:
                if open_ends == 2:
                    score = 10
                    current_name = "SINGLE"
            
            if score > max_score:
                max_score = score
                pattern_name = current_name
                
        return max_score, pattern_name

    def evaluate_cell_score(self, r, c, piece):
        """
        Giả lập đặt 'piece' tại ô trống (r, c) và trả về:
        - max_score: điểm của hướng mạnh nhất (bao gồm cả điểm nuôi thế cờ trung gian)
        - threat_count: số lượng mối đe dọa mạnh (OPEN_3, CLOSED_3, OPEN_BROKEN_3, CLOSED_BROKEN_3)
        """
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
        max_score = 0
        threat_count = 0
        intermediate_threats = 0
        
        for dr, dc in directions:
            line_vals = []
            for i in range(-3, 4):
                nr, nc = r + i * dr, c + i * dc
                if 0 <= nr < BOARD_SIZE and 0 <= nc < BOARD_SIZE:
                    if i == 0:
                        line_vals.append("X")
                    else:
                        board_val = self.board[nr][nc]
                        if board_val == EMPTY:
                            line_vals.append("_")
                        elif board_val == piece:
                            line_vals.append("X")
                        else:
                            line_vals.append("O")
                else:
                    line_vals.append("O")
            
            line_str = "".join(line_vals)
            score, pattern = self.detect_pattern(line_str)
            
            if score > max_score:
                max_score = score
                
            # Đếm đe dọa mạnh: thắng ngay trong nước sau
            if pattern in ["OPEN_3", "CLOSED_3", "OPEN_BROKEN_3", "CLOSED_BROKEN_3"]:
                threat_count += 1
                
            # Đếm đe dọa trung gian để nuôi fork sau này: X_X, _X_X_, XX_
            if pattern in ["OPEN_2", "OPEN_GAPPED_2", "GAPPED_2"]:
                intermediate_threats += 1
                
        # Nếu có từ 2 đe dọa trung gian trở lên ở các hướng độc lập, thưởng điểm "nuôi cờ" để kiến tạo thế đôi
        if intermediate_threats >= 2:
            max_score += 15000
            
        return max_score, threat_count

    def evaluate_cell_total(self, r, c):
        # 1. Tính điểm tấn công (AI đánh)
        atk_score, atk_threats = self.evaluate_cell_score(r, c, self.ai_piece)
        
        # 2. Tính điểm phòng thủ (Đối thủ đánh)
        def_score, def_threats = self.evaluate_cell_score(r, c, self.player_piece)
        
        # --- ÁP DỤNG HỆ THỐNG ƯU TIÊN TUYỆT ĐỐI (TACTICAL HIERARCHY) ---
        
        # Ưu tiên 1: AI có thể thắng ngay lập tức
        if atk_score >= 1000000:
            return 100000000 + atk_score
            
        # Ưu tiên 2: Đối thủ chuẩn bị thắng ngay lập tức, AI bắt buộc phải chặn
        if def_score >= 1000000:
            return 90000000 + def_score
            
        # Ưu tiên 3: AI kiến tạo nước đôi (Fork) tạo thế thắng ép không thể cản phá
        if atk_threats >= 2:
            return 80000000 + atk_score * 5.0
            
        # Ưu tiên 4: Chặn nước đôi (Fork) hiểm ác của đối phương
        if def_threats >= 2:
            return 70000000 + def_score * 5.0
            
        # Điểm cơ sở
        total_score = atk_score + def_score
        
        # Điểm vị trí: ưu tiên trung tâm, giảm dần ra biên và góc (căn chỉnh theo tỉ lệ bàn cờ 12x12)
        center_dist = abs(r - BOARD_SIZE // 2) + abs(c - BOARD_SIZE // 2)
        position_score = max(0, 15 - center_dist)
        total_score += position_score
        
        # Nhân hệ số gần quân đã có (x1.2)
        has_adj = False
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0: continue
                nr, nc = r + dr, c + dc
                if 0 <= nr < BOARD_SIZE and 0 <= nc < BOARD_SIZE:
                    if self.board[nr][nc] != EMPTY:
                        has_adj = True
                        break
            if has_adj: break
            
        if has_adj:
            total_score *= 1.2
            
        return total_score

    def evaluate_board_incremental(self):
        # Đánh giá trạng thái toàn bộ bàn cờ dựa trên tổng điểm các ô trống tiềm năng trong phạm vi bán kính 2
        total_eval = 0
        moves_set = set()
        all_pieces = self.ai_pieces | self.player_pieces
        
        for r, c in all_pieces:
            for i in range(max(0, r-2), min(BOARD_SIZE, r+3)):
                for j in range(max(0, c-2), min(BOARD_SIZE, c+3)):
                    if self.board[i][j] == EMPTY:
                        moves_set.add((i, j))
                        
        for r, c in moves_set:
            atk_score, atk_threats = self.evaluate_cell_score(r, c, self.ai_piece)
            def_score, def_threats = self.evaluate_cell_score(r, c, self.player_piece)
            
            # Tăng vọt giá trị đánh giá trong Minimax nếu có nước đôi (Fork)
            if atk_threats >= 2:
                atk_score += 1500000
            if def_threats >= 2:
                def_score += 1500000
                
            # Hệ số 2.0 cho phòng thủ (được tối ưu hóa an toàn)
            total_eval += atk_score - (def_score * 2.0)
            
        return total_eval

    def get_ordered_moves(self, depth):
        if self.empty_cells == BOARD_SIZE * BOARD_SIZE:
            return [(BOARD_SIZE//2, BOARD_SIZE//2)]
            
        moves_set = set()
        all_pieces = self.ai_pieces | self.player_pieces
        
        for r, c in all_pieces:
            for i in range(max(0, r-2), min(BOARD_SIZE, r+3)):
                for j in range(max(0, c-2), min(BOARD_SIZE, c+3)):
                    if self.board[i][j] == EMPTY:
                        moves_set.add((i, j))
        
        move_list = list(moves_set)
        
        def move_score(move):
            if getattr(self, 'mode', 'hard') == "hard":
                if move == self.killer_moves[depth][0]: return 900000000
                if move == self.killer_moves[depth][1]: return 800000000

            r, c = move
            hist_score = self.history_heuristic[r][c] if getattr(self, 'mode', 'hard') == "hard" else 0
            return self.evaluate_cell_total(r, c) + hist_score
            
        move_list.sort(key=move_score, reverse=True)
        return move_list

    def minimax(self, depth, alpha, beta, is_maximizing, last_r, last_c, cancel_token_func):
        self.nodes_evaluated += 1

        if cancel_token_func() != self.request_id or time.time() - self.start_time > self.time_limit:
            self.timeout_flag = True
            return 0, None

        if self.mode == "hard" and self.current_hash in self.transposition_table:
            cached_depth, cached_score, cached_flag = self.transposition_table[self.current_hash]
            if cached_depth >= depth:
                self.cache_hits += 1
                if cached_flag == 'EXACT': return cached_score, None
                elif cached_flag == 'LOWERBOUND': alpha = max(alpha, cached_score)
                elif cached_flag == 'UPPERBOUND': beta = min(beta, cached_score)
                if alpha >= beta: return cached_score, None

        if last_r is not None:
            if not is_maximizing and self.check_win_logic(last_r, last_c, self.ai_piece): 
                return 100000000 + depth * 1000, None
            if is_maximizing and self.check_win_logic(last_r, last_c, self.player_piece): 
                return -100000000 - depth * 1000, None

        if depth == 0 or self.is_full():
            score = self.evaluate_board_incremental()
            if self.mode == "hard": self.transposition_table[self.current_hash] = (depth, score, 'EXACT')
            return score, None

        valid_moves = self.get_ordered_moves(depth)
        best_move = None
        orig_alpha = alpha
        orig_beta = beta

        if is_maximizing:
            max_eval = -math.inf
            first_move = True
            for r, c in valid_moves:
                self.make_move(r, c, self.ai_piece)
                if first_move or self.mode != "hard":
                    eval_score, _ = self.minimax(depth - 1, alpha, beta, False, r, c, cancel_token_func)
                else:
                    # Principal Variation Search (NegaScout) - Tìm kiếm cửa sổ hẹp
                    eval_score, _ = self.minimax(depth - 1, alpha, alpha + 1, False, r, c, cancel_token_func)
                    if alpha < eval_score < beta:
                        eval_score, _ = self.minimax(depth - 1, eval_score, beta, False, r, c, cancel_token_func)
                self.undo_move(r, c, self.ai_piece)
                
                if self.timeout_flag: break

                if eval_score > max_eval:
                    max_eval = eval_score
                    best_move = (r, c)
                
                if self.mode in ["normal", "hard"]:
                    alpha = max(alpha, eval_score)
                    if beta <= alpha:
                        if self.mode == "hard": 
                            self.history_heuristic[r][c] += depth ** 2 
                            if self.killer_moves[depth][0] != (r, c):
                                self.killer_moves[depth][1] = self.killer_moves[depth][0]
                                self.killer_moves[depth][0] = (r, c)
                        break 
                first_move = False
                    
            if max_eval <= orig_alpha: flag = 'UPPERBOUND'
            elif max_eval >= orig_beta: flag = 'LOWERBOUND'
            else: flag = 'EXACT'
                
            if not self.timeout_flag and self.mode == "hard": self.transposition_table[self.current_hash] = (depth, max_eval, flag)
            return max_eval, best_move
        else:
            min_eval = math.inf
            first_move = True
            for r, c in valid_moves:
                self.make_move(r, c, self.player_piece)
                if first_move or self.mode != "hard":
                    eval_score, _ = self.minimax(depth - 1, alpha, beta, True, r, c, cancel_token_func)
                else:
                    # PVS cho người chơi (Minimizer)
                    eval_score, _ = self.minimax(depth - 1, beta - 1, beta, True, r, c, cancel_token_func)
                    if alpha < eval_score < beta:
                        eval_score, _ = self.minimax(depth - 1, alpha, eval_score, True, r, c, cancel_token_func)
                self.undo_move(r, c, self.player_piece)
                
                if self.timeout_flag: break

                if eval_score < min_eval:
                    min_eval = eval_score
                    best_move = (r, c)
                
                if self.mode in ["normal", "hard"]:
                    beta = min(beta, eval_score)
                    if beta <= alpha:
                        if self.mode == "hard": 
                            self.history_heuristic[r][c] += depth ** 2
                            if self.killer_moves[depth][0] != (r, c):
                                self.killer_moves[depth][1] = self.killer_moves[depth][0]
                                self.killer_moves[depth][0] = (r, c)
                        break 
                first_move = False

            if min_eval <= orig_alpha: flag = 'UPPERBOUND'
            elif min_eval >= orig_beta: flag = 'LOWERBOUND'
            else: flag = 'EXACT'
                
            if not self.timeout_flag and self.mode == "hard": self.transposition_table[self.current_hash] = (depth, min_eval, flag)
            return min_eval, best_move

    def search(self, cancel_token_func):
        self.start_time = time.time()
        best_move_overall = None
        best_score_overall = 0
        reached_depth = 0

        for depth in range(1, self.max_depth + 1):
            score, move = self.minimax(depth, -math.inf, math.inf, True, None, None, cancel_token_func)
            if self.timeout_flag and best_move_overall is not None:
                break
            if move:
                best_move_overall = move
                best_score_overall = score
            reached_depth = depth
            if score > 5000000: break 

        t_spent = round(time.time() - self.start_time, 3)
        return best_move_overall, best_score_overall, reached_depth, self.nodes_evaluated, self.cache_hits, t_spent