from flask import Flask, render_template, request, jsonify  # Flask ใช้สำหรับสร้างเว็บเซิร์ฟเวอร์
import numpy as np                                          # NumPy (np) ใช้สำหรับจัดการกระดานเกมในรูปแบบเมทริกซ์ 2 มิติ
import math                            
import random

# math และ random ใช้สำหรับการคำนวณทางคณิตศาสตร์และการเลือกเดินหมากแบบสุ่มของ AI

#python app.py
#localhost http://127.0.0.1:5000/

app = Flask(__name__)

ROW_COUNT = 6             # ROW_COUNT และ COLUMN_COUNT กำหนดขนาดกระดาน (6 แถว และ 7 คอลัมน์)
COLUMN_COUNT = 7          
PLAYER_PIECE = 1          # PLAYER_PIECE และ AI_PIECE แทนสัญลักษณ์ของผู้เล่นและ AI
AI_PIECE = 2
EMPTY = 0
WINDOW_LENGTH = 4         # WINDOW_LENGTH (4) คือจำนวนช่องที่ต้องต่อกันเพื่อชนะ (คือ 4 ช่องติดกัน)

def create_board():                                # สร้างกระดานขนาด 6x7 ที่มีค่าเป็นศูนย์ (แสดงถึงช่องว่าง)
    return np.zeros((ROW_COUNT, COLUMN_COUNT))      

def drop_piece(board, row, col, piece):            # อัปเดตกระดานโดยวางหมากของผู้เล่นในตำแหน่งที่กำหนด
    board[row][col] = piece                         

def is_valid_location(board, col):                 # ตรวจสอบว่าคอลัมน์นั้นสามารถวางหมากได้หรือไม่ (ถ้าคอลัมน์นั้นยังไม่เต็ม)
    return board[ROW_COUNT-1][col] == 0             

def get_next_open_row(board, col):                 # คืนค่าแถวที่ยังว่างในคอลัมน์นั้นเพื่อวางหมาก
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r

def winning_move(board, piece):              # ตรวจสอบว่าผู้เล่นชนะเกมหรือไม่โดยดูว่าหมาก 4 ตัวเรียงติดกันในแนวนอน แนวตั้ง หรือแนวทแยง
    for c in range(COLUMN_COUNT-3):
        for r in range(ROW_COUNT):
            if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                return True
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT-3):
            if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                return True
    for c in range(COLUMN_COUNT-3):
        for r in range(ROW_COUNT-3):
            if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                return True
    for c in range(COLUMN_COUNT-3):
        for r in range(3, ROW_COUNT):
            if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                return True

def evaluate_window(window, piece):
    # ประเมินกลุ่ม 4 ช่อง ("หน้าต่าง") และให้คะแนนตามจำนวนหมากของผู้เล่นหรือฝ่ายตรงข้าม ถ้าผู้เล่นมีหมากมากกว่าจะได้คะแนนเพิ่ม ถ้าฝ่ายตรงข้ามมีหมากอยู่จะลดคะแนนลง
    # ให้คะแนนหน้าต่าง 4 ช่องตามจำนวนหมากของผู้เล่นหรือฝ่ายตรงข้ามที่อยู่ในนั้น
    score = 0
    opp_piece = PLAYER_PIECE
    if piece == PLAYER_PIECE:
        opp_piece = AI_PIECE
    if window.count(piece) == 4:
        score += 100
    elif window.count(piece) == 3 and window.count(EMPTY) == 1:
        score += 5
    elif window.count(piece) == 2 and window.count(EMPTY) == 2:
        score += 2
    if window.count(opp_piece) == 3 and window.count(EMPTY) == 1:
        score -= 4
    return score

def score_position(board, piece):   
    # ให้คะแนนกระดานโดยประเมินแถว คอลัมน์ และแนวทแยงโดยใช้ฟังก์ชัน evaluate_window() และให้ความสำคัญกับคอลัมน์กลางมากขึ้น เพราะมีโอกาสสูงที่จะต่อหมากได้
    # ประเมินกระดานทั้งหมดเพื่อคำนวณคะแนนของผู้เล่นหรือ AI
    score = 0
    center_array = [int(i) for i in list(board[:, COLUMN_COUNT//2])]
    center_count = center_array.count(piece)
    score += center_count * 3
    for r in range(ROW_COUNT):
        row_array = [int(i) for i in list(board[r,:])]
        for c in range(COLUMN_COUNT-3):
            window = row_array[c:c+WINDOW_LENGTH]
            score += evaluate_window(window, piece)
    for c in range(COLUMN_COUNT):
        col_array = [int(i) for i in list(board[:,c])]
        for r in range(ROW_COUNT-3):
            window = col_array[r:r+WINDOW_LENGTH]
            score += evaluate_window(window, piece)
    for r in range(ROW_COUNT-3):
        for c in range(COLUMN_COUNT-3):
            window = [board[r+i][c+i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, piece)
    for r in range(ROW_COUNT-3):
        for c in range(COLUMN_COUNT-3):
            window = [board[r+3-i][c+i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, piece)
    return score

def is_terminal_node(board):           # ตรวจสอบว่าเกมสิ้นสุดลงแล้วหรือไม่ (ผู้เล่นคนใดคนหนึ่งชนะ หรือไม่มีตำแหน่งที่สามารถเดินได้อีก)
    return winning_move(board, PLAYER_PIECE) or winning_move(board, AI_PIECE) or len(get_valid_locations(board)) == 0

def minimax(board, depth, alpha, beta, maximizingPlayer):  
    # ใช้อัลกอริทึม Minimax พร้อม Alpha-Beta Pruning เพื่อหาการเดินที่ดีที่สุด
    # Minimax เป็นอัลกอริทึมที่ใช้ในการจำลองการเดินหมากและเลือกการเดินที่ดีที่สุด โดยพิจารณาจากการเดินหมากของคู่แข่งด้วย
    # พารามิเตอร์ depth กำหนดความลึกของการคำนวณ ว่า AI จะคาดการณ์ล่วงหน้าได้กี่การเดิน
    # Alpha-Beta pruning ช่วยลดจำนวนโหนด (การเดินหมาก) ที่ต้องพิจารณา เพื่อเพิ่มประสิทธิภาพของอัลกอริทึม
    valid_locations = get_valid_locations(board)
    is_terminal = is_terminal_node(board)
    if depth == 0 or is_terminal:
        if is_terminal:
            if winning_move(board, AI_PIECE):
                return (None, 1000)
            elif winning_move(board, PLAYER_PIECE):
                return (None, -1000)
            else:
                return (None, 0)
        else:
            return (None, score_position(board, AI_PIECE))
    if maximizingPlayer:
        value = -math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, AI_PIECE)
            new_score = minimax(b_copy, depth-1, alpha, beta, False)[1]
            if new_score > value:
                value = new_score
                column = col
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return column, value
    else:
        value = math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, PLAYER_PIECE)
            new_score = minimax(b_copy, depth-1, alpha, beta, True)[1]
            if new_score < value:
                value = new_score
                column = col
            beta = min(beta, value)
            if alpha >= beta:
                break
        return column, value

def get_valid_locations(board):
    valid_locations = []
    for col in range(COLUMN_COUNT):
        if is_valid_location(board, col):
            valid_locations.append(col)
    return valid_locations

def pick_best_move(board, piece):
    valid_locations = get_valid_locations(board)
    best_score = -10000
    best_col = random.choice(valid_locations)
    for col in valid_locations:
        row = get_next_open_row(board, col)
        temp_board = board.copy()
        drop_piece(temp_board, row, col, piece)
        score = score_position(temp_board, piece)
        if score > best_score:
            best_score = score
            best_col = col
    return best_col

@app.route('/')  # เส้นทางเริ่มต้นนี้จะเรนเดอร์เทมเพลต index.html ซึ่งเป็นหน้าเว็บที่ผู้เล่นจะใช้เล่นเกม
def index():
    return render_template('index.html')


@app.route('/make_move', methods=['POST'])  
# เส้นทางนี้จะถูกเรียกเมื่อผู้เล่นทำการเดินหมาก:
#   1. การเดินหมากของผู้เล่นจะถูกตรวจสอบว่าถูกต้องและวางลงบนกระดาน
#   2. ถ้าผู้เล่นชนะ จะส่งผลลัพธ์กลับไปทันที
#   3. AI จะทำการเดินหมากโดยใช้ อัลกอริทึม Minimax เพื่อหาการเดินที่ดีที่สุด
#   4. ถ้า AI ชนะ จะส่งผลลัพธ์กลับไป
#   5. ถ้ายังไม่มีใครชนะ จะส่งกระดานที่อัปเดตและคะแนนของ AI กลับไป
def make_move():
    data = request.json
    col = data['column']
    board = np.array(data['board'])
    
    if is_valid_location(board, col):
        row = get_next_open_row(board, col)
        drop_piece(board, row, col, PLAYER_PIECE)
        if winning_move(board, PLAYER_PIECE):
            return jsonify({'board': board.tolist(), 'winner': 'Player', 'score': None})
        
        # AI ใช้ Minimax เพื่อเลือกตำแหน่งที่ดีที่สุด และเก็บคะแนน
        ai_col, ai_score = minimax(board, 4, -math.inf, math.inf, True)
        if is_valid_location(board, ai_col):
            ai_row = get_next_open_row(board, ai_col)
            drop_piece(board, ai_row, ai_col, AI_PIECE)
            if winning_move(board, AI_PIECE):
                return jsonify({'board': board.tolist(), 'winner': 'AI', 'score': ai_score})
        
    return jsonify({'board': board.tolist(), 'winner': '', 'score': ai_score})


if __name__ == "__main__":  # แอปพลิเคชัน Flask จะถูกรันในโหมด debug และสามารถเข้าถึงได้ที่ http://127.0.0.1:5000/
    app.run(debug=True)
