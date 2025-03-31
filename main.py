#the pieces are global variables to be used along the program
empty_black = "▪"  #empty playable (black) squares
player2 = "●"  #white pieces
player1 = "○"  #black pieces
white_king = "♚" #white king
black_king = "♔" #black king

#ending the game message
def endGame(winner):
    print()
    if winner:
        print("White won the game!")
    else:
        print("Black won the game!")

#checks if there are any white or black pieces left on the board
def endGameCheck(board):

    #get total black pieces and white pieces
    black_count = 0
    for row in board:
        black_count += row.count(player1)
        black_count += row.count(black_king)

    white_count = 0
    for row in board:
        white_count += row.count(player2)
        white_count += row.count(white_king)

    #check
    if black_count == 0:
        endGame(True)
        return True

    if white_count == 0:
        endGame(False)
        return True

    return False

#printing the board. Ran after init and every time a move is made after that until end
def printBoard(board, totalblack, totalwhite, turn):

    #cols for the user the select
    print("   0  1  2  3  4  5  6  7")
    print("  -------------------------")
    #using for loop to add rows
    for i, row in enumerate(board):
        print(f"{i}| " + "  ".join(row) + " |")
    print("  -------------------------")
    print()
    print("Total pieces captured by Black: ", totalblack)
    print("Total pieces captured by White: ", totalwhite)
    print()
    if turn == 0:
        print("It is currently Black's Turn.")
    else:
        print("It is currently White's Turn.")

#this is the initialize game function. i created the board here and printed out
#the game beginning messages
def initGame():
    board = [[" " for _ in range(8)] for _ in range(8)]
    #place black pieces top three rows
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

    print("\nWelcome to the Checkers Game")
    print("Black Pieces: " + player1)
    print("White Pieces: " + player2)
    print("King Piece for Black: " + black_king)
    print("King Piece for White: " + white_king)
    print("Empty Black Squares: " + empty_black)
    print()
    print("\nHow to play:")
    print("1. If a capture is available, you must take it.")
    print("   - If only one capture move is available, it will execute automatically.")
    print("   - If more than one is available, you'll be prompted to select one.")
    print("2. If no capture is available, you'll be asked which piece and where to move.")
    print("3. Black moves first. Good luck!\n")
    return board

#getting a non capturing move from the user
def get_move(board, turn):
    #throughout the game, turn = false is black, true is white.
    #initialize smybols to be used throughout the game
    if turn == 0:
        piece = player1
        king = black_king
        player = "Black"
    else:
        piece = player2
        king = white_king
        player = "White"
    #im using except in case user enters something aside from num
    while True:
        try:
            #get the inputs
            src_row = int(input(f"[{player[0]}] Choose the row of the piece you want to move: "))
            src_col = int(input(f"[{player[0]}] Choose the column of the piece you want to move: "))
            #check if its in range
            if src_row < 0 or src_row > 7 or src_col < 0 or src_col > 7:
                print("Invalid row and column. Try again.")
                continue
            #check if it is anything other than a black king or black piece
            if board[src_row][src_col] != piece and board[src_row][src_col] != king:
                print(f"Please select a {player.lower()} piece.")
                continue
            break
        except ValueError:
            print("Invalid input. You need to enter numbers!")

    #do the same for destination coordinates
    while True:
        try:
            dest_row = int(input(f"[{player[0]}] Choose the row you want to move to: "))
            dest_col = int(input(f"[{player[0]}] Choose the column you want to move to: "))
            if dest_row < 0 or dest_row > 7 or dest_col < 0 or dest_col > 7:
                print("You cannot move there. Try again.")
                continue
            break
        except ValueError:
            print("Invalid input. You need to enter numbers!")
    return src_row, src_col, dest_row, dest_col

#validate a non-capturing move or a capturing move if it is two steps
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

def promoteKing(turn, dest_row, dest_col, board):
    #king promotion: for black, reaching row 7. forwhite, reaching row 0.
    if turn == 0 and dest_row == 7 and board[dest_row][dest_col] == player1:
        board[dest_row][dest_col] = black_king
        print("Black piece promoted to King!")
    if turn == 1 and dest_row == 0 and board[dest_row][dest_col] == player2:
        board[dest_row][dest_col] = white_king
        print("White piece promoted to King!")

def main():
    board = initGame()
    totalblack = 0
    totalwhite = 0
    turn = 0  #again, 0 for black, 1 for white

    while True:
        #print the board
        printBoard(board, totalblack, totalwhite, turn)
        #check if the game is over: all pieces gone for either side.
        if endGameCheck(board):
            break

        #check globally for any capture moves available for the current player.

        all_captures = getAllCaptureMoves(board, turn)

        if all_captures:
            #force a capture move.
            #if there is only one available then we automatically take
            if len(all_captures) == 1:
                chosen = all_captures[0]
                print(f"Automatically capturing: Piece at ({chosen[0]}, {chosen[1]}) to ({chosen[2]}, {chosen[3]})")
            else:
                #otherwise we give option
                print("Multiple capture moves available:")
                #ask for an index from the user
                for idx, move in enumerate(all_captures):
                    print(
                        f"{idx}: Move piece at ({move[0]}, {move[1]}) to ({move[2]}, {move[3]}) capturing piece at {move[4]}")
                while True:
                    try:
                        choice = int(input("Select move index: "))
                        chosen = all_captures[choice]
                        break
                    except (ValueError, IndexError):
                        print("Invalid selection.")
                        continue
            #move to the chosen
            src_row, src_col, dest_row, dest_col, cap_coord = chosen
        else:
            #no capture is available so we ask the player for a normal move.
            src_row, src_col, dest_row, dest_col = get_move(board, turn)
            #check if the move is valid
            valid, cap_coord = isValidMove(board, turn, src_row, src_col, dest_row, dest_col)
            #otherwise state that it is invalid
            if not valid:
                print("Invalid move, try again.\n")
                continue

        #move the piece
        piece = board[src_row][src_col]
        board[dest_row][dest_col] = piece
        board[src_row][src_col] = empty_black

        #if a capture is made then remove the piece of the opponent from the board
        if cap_coord is not None:
            cap_row, cap_col = cap_coord
            board[cap_row][cap_col] = empty_black

            #increase the capture number for the respective player
            if turn == 0:
                totalblack += 1
            else:
                totalwhite += 1

            #now we need to handle further jumps for this piece.
            while True:
                #check if there is a further move
                further_moves = getCaptureMovesForPiece(board, turn, dest_row, dest_col)
                if further_moves:
                    #if there is only one, then we automatically capture otherwise
                    #promt the user for further instructions on which piece to capture.
                    if len(further_moves) == 1:
                        next_move = further_moves[0]
                        print(
                            f"Automatically capturing further: ({next_move[0]}, {next_move[1]}) to ({next_move[2]}, {next_move[3]})")
                    else:
                        print("Multiple further capture moves available:")
                        #give selections to the user
                        for idx, move in enumerate(further_moves):
                            print(
                                f"{idx}: Move from ({move[0]}, {move[1]}) to ({move[2]}, {move[3]}) capturing piece at {move[4]}")
                        #error handle in case user enters an invalid input
                        while True:
                            try:
                                choice = int(input("Select move index: "))
                                next_move = further_moves[choice]
                                break
                            except (ValueError, IndexError):
                                print("Invalid selection. Please enter a valid number")
                                continue

                    #execute further capture
                    src_row, src_col, dest_row, dest_col, cap_coord = next_move
                    #destination is replaced with peice
                    board[dest_row][dest_col] = piece
                    #source is blank
                    board[src_row][src_col] = empty_black
                    #capture coordinates are stores
                    cap_row, cap_col = cap_coord
                    #captured piece is replaced with blank
                    board[cap_row][cap_col] = empty_black
                    #the turn changes after execution
                    if turn == 0:
                        totalblack += 1
                    else:
                        totalwhite += 1
                else:
                    break

        #check for king promotion
        promoteKing(turn,dest_row,dest_col,board)

        #switch turn.
        turn = 1 - turn


if __name__ == "__main__":
    main()
