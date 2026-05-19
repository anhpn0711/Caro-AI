from core.constants import BOARD_SIZE, WIN_COUNT, EMPTY

def check_win_logic(board, r, c, piece):
    """Kiểm tra điều kiện chiến thắng tại vị trí vừa đánh và trả về tọa độ đường thẳng thắng cuộc."""
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
    for dr, dc in directions:
        count = 1
        line = [(r, c)]
        nr, nc = r + dr, c + dc
        while 0 <= nr < BOARD_SIZE and 0 <= nc < BOARD_SIZE and board[nr][nc] == piece:
            count += 1; line.append((nr, nc)); nr += dr; nc += dc
        nr, nc = r - dr, c - dc
        while 0 <= nr < BOARD_SIZE and 0 <= nc < BOARD_SIZE and board[nr][nc] == piece:
            count += 1; line.append((nr, nc)); nr -= dr; nc -= dc
        if count >= WIN_COUNT: 
            return True, line
    return False, []

def is_board_full(board):
    """Kiểm tra xem bàn cờ đã kín nước đi hay chưa."""
    for row in board:
        if EMPTY in row: 
            return False
    return True