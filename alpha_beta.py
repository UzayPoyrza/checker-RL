import copy
from rules import getAllCaptureMoves, getCaptureMovesForPiece, isValidMove, endGameCheck, empty_black, player1, player2, black_king, white_king


#This function calculates the current score. It is based on how many piece belongs to white and black
#kings are counted double point
def evaluateBoard(board):
    score = 0
    for row in board:
        for cell in row:
            if cell == player1:
                score += 1
            elif cell == black_king:
                score += 2
            elif cell == player2:
                score -= 1
            elif cell == white_king:
                score -= 2
    return score

#This function returns al the capture moves. otherwise legal non-capturing moves
def getAllMoves(board, turn):

    #firstly try to get capture moves

    captures = getAllCaptureMoves(board, turn)
    if captures:
        return captures

    #if it doesnt exist:

    moves = []
    #directions: all of the diagonals
    dirs = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
    for r in range(8):
        for c in range(8):
            piece = board[r][c]
            if (turn == 0 and piece in (player1, black_king)) or (turn == 1 and piece in (player2, white_king)):
                for dr, dc in dirs:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < 8 and 0 <= nc < 8:
                        valid, cap = isValidMove(board, turn, r, c, nr, nc)
                        if valid and cap is None:
                            moves.append((r, c, nr, nc, None))
    return moves

#create a deep copy. apply a move, return

def simulateMove(board, move, turn):
    #Make a deep copy"
    new_board = copy.deepcopy(board)
    #get the move
    sr, sc, dr, dc, cap = move
    piece = new_board[sr][sc]
    new_board[dr][dc] = piece
    new_board[sr][sc] = empty_black
    #if there is a valid capture move (if thre isnt then it is none)
    if cap:
        cr, cc = cap
        new_board[cr][cc] = empty_black
    #promotion
    if turn == 0 and dr == 7 and new_board[dr][dc] == player1:
        new_board[dr][dc] = black_king
    if turn == 1 and dr == 0 and new_board[dr][dc] == player2:
        new_board[dr][dc] = white_king
    return new_board



def minimax(board, depth, alpha, beta, turn, maximizingPlayer):
    #Alpha-beta pruning minimax implementation.

    if depth == 0 or endGameCheck(board):
        #return evaluation and move as none
        return evaluateBoard(board), None

    moves = getAllMoves(board,turn)
    if not moves:
        return evaluateBoard(board), None

    #find best move

    best_move = None
    if maximizingPlayer:
        max_eval = -float('inf')
        for m in moves:
            nb = simulateMove(board, m, turn)
            val, _ = minimax(nb, depth - 1, alpha, beta, 1 - turn, False)
            if val > max_eval:
                max_eval, best_move = val, m
            alpha = max(alpha, val)
            if beta <= alpha:
                break
        return max_eval, best_move
    else:
        min_eval = float('inf')
        for m in moves:
            nb = simulateMove(board, m, turn)
            val, _ = minimax(nb, depth - 1, alpha, beta, 1 - turn, True)
            if val < min_eval:
                min_eval, best_move = val, m
            beta = min(beta, val)
            if beta <= alpha:
                break
        return min_eval, best_move