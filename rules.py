#the pieces are global variables to be used along the program
empty_black = "▪"  #empty playable (black) squares
player2 = "●"  #white pieces
player1 = "○"  #black pieces
white_king = "♚" #white king
black_king = "♔" #black king


#checks if there are any white or black pieces left on the board
def endGameCheck(board):

    from rules import player1, player2, black_king, white_king  # or use module‐level names

    black_count = 0
    white_count = 0
    for row in board:
        for cell in row:
            if cell == player1 or cell == black_king:
                black_count += 1
            if cell == player2 or cell == white_king:
                white_count += 1

    # terminal if one side is wiped out
    return (black_count == 0) or (white_count == 0)


def isValidMove(board, turn, src_row, src_col, dest_row, dest_col):
    #if there is no piece on the diagnal then we dont even need to check
    if board[dest_row][dest_col] != empty_black:
        return False, None
    #initialize the piece here again to not have to have two cases
    piece = board[src_row][src_col]
    #check if the piece we are moving is a king
    is_king = (piece == black_king or piece == white_king)

    #if we are playing whites then we need to check for opponent pieces. the direction is
    #used for rows later

    if turn == 0:
        opponent = [player2, white_king]
        move_dir = 1  #black moves down
    else:
        opponent = [player1, black_king]
        move_dir = -1  #white moves up

    #get the differences in row to check if it is a valid move
    row_diff = dest_row - src_row
    col_diff = dest_col - src_col

    #move must be diagnal so we need to move 1 step both ways. if we dont then it is not valid
    if abs(row_diff) != abs(col_diff):
        return False, None

    #new checking for a simple one-step move
    if abs(row_diff) == 1:
        #if it is not a king and it is trying to move backwards, then it is invalid
        if not is_king and row_diff != move_dir:
            return False, None
        return True, None

    # checking for capturing move which is a two diagnal step
    elif abs(row_diff) == 2:
        #check if it is trying to capture backwards. if it is not a king this returns false
        if not is_king and row_diff != move_dir * 2:
            return False, None
        #we already checked if the space being tried to move is empty, now we check if there is actually
        #a piece to capture if there is a free space ahead

        #get the diagnal coordinate
        mid_row = (src_row + dest_row) // 2
        mid_col = (src_col + dest_col) // 2

        if board[mid_row][mid_col] not in opponent:
            return False, None
        return True, (mid_row, mid_col)
    else:
        # anything other than 2-step is not permitted so we return false

        return False, None

#this method returns a list of all capture moves available for the current player. i represent
#these as tuples and the user will be promted for which they want to capture.

def getAllCaptureMoves(board, turn):

    #get all the possible capture directions according to the turn and store it.
    moves = []
    if turn == 0:
        piece = player1
        king = black_king
        opponent = [player2, white_king]
        capture_dirs = [(2, 2), (2, -2)]
    else:
        piece = player2
        king = white_king
        opponent = [player1, black_king]
        capture_dirs = [(-2, 2), (-2, -2)]
    #get all the directions available (this is in case we are working with a king)
    all_dirs = [(-2, -2), (-2, 2), (2, -2), (2, 2)]

    #check across the board
    for r in range(8):
        for c in range(8):
            #check if the observed piece is king, if it is then we use all directions
            if board[r][c] == piece or board[r][c] == king:
                if board[r][c] == king:
                    directions = all_dirs
                else:
                    directions = capture_dirs

                for dr, dc in directions:
                    #check all the two-step directions
                    new_r = r + dr
                    new_c = c + dc
                    #if it is in range check if there are opponent pieces peices
                    if 0 <= new_r < 8 and 0 <= new_c < 8:
                        mid_r = r + dr // 2
                        mid_c = c + dc // 2
                        #mid_r and mid_c are possible coordinates of possible opponent pieces
                        #if there is possible capture then append the possible move to the moves list
                        if board[new_r][new_c] == empty_black and board[mid_r][mid_c] in opponent:
                            moves.append((r, c, new_r, new_c, (mid_r, mid_c)))
    return moves

#this method is implemented for multiple captures with one piece because we need to check after we capture
#a piece whether we can capture more.
def getCaptureMovesForPiece(board, turn, src_row, src_col):

    moves = []
    piece = board[src_row][src_col]


    if turn == 0:
        opponent_pieces = [player2, white_king]
        capture_dirs = [(2, 2), (2, -2)]
    else:
        opponent_pieces = [player1, black_king]
        capture_dirs = [(-2, 2), (-2, -2)]
    all_dirs = [(-2, -2), (-2, 2), (2, -2), (2, 2)]
    # check if the piece is a king piece and if it is update possible directions accordingly
    if piece == black_king or piece == white_king:
        directions = all_dirs
    else:
        directions = capture_dirs
    #check for possible captures of an individual piece, the same way we did in all possible captures method
    for dr, dc in directions:
        new_r = src_row + dr
        new_c = src_col + dc
        if 0 <= new_r < 8 and 0 <= new_c < 8:
            mid_r = src_row + dr // 2
            mid_c = src_col + dc // 2
            if board[new_r][new_c] == empty_black and board[mid_r][mid_c] in opponent_pieces:
                moves.append((src_row, src_col, new_r, new_c, (mid_r, mid_c)))
    return moves

def makeBoard():
    board = [[" " for _ in range(8)] for _ in range(8)]
    # place black pieces top three rows
    for i in range(3):
        for j in range(8):
            if (i % 2 == 0 and j % 2 == 1) or (i % 2 == 1 and j % 2 == 0):
                board[i][j] = player1
    # two middle rows empty
    for i in range(3, 5):
        for j in range(8):
            if (i % 2 == 0 and j % 2 == 1) or (i % 2 == 1 and j % 2 == 0):
                board[i][j] = empty_black
    # white pieces on buttom 3 rows
    for i in range(5, 8):
        for j in range(8):
            if (i % 2 == 0 and j % 2 == 1) or (i % 2 == 1 and j % 2 == 0):
                board[i][j] = player2
    return board