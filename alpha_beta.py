import copy
from main import getAllCaptureMoves, getCaptureMovesForPiece, isValidMove
from main import empty_black, player1, player2, black_king, white_king


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

def simulateMove(board, move, turn):
    # Simulate the move on a copy of the board.
    pass

def minimax(board, depth, alpha, beta, turn, maximizingPlayer):
    # Alpha-beta pruning minimax implementation.
    pass
