from alpha_beta import minimax
from rules import getAllCaptureMoves, getCaptureMovesForPiece, isValidMove, endGameCheck
from rules import empty_black, player1, player2, black_king, white_king


#ending the game message
def endGame(winner):
    print()
    if winner:
        print("White won the game!")
    else:
        print("Black won the game!")


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


def promoteKing(turn, dest_row, dest_col, board):
    #king promotion: for black, reaching row 7. forwhite, reaching row 0.
    if turn == 0 and dest_row == 7 and board[dest_row][dest_col] == player1:
        board[dest_row][dest_col] = black_king
        print("Black piece promoted to King!")
    if turn == 1 and dest_row == 0 and board[dest_row][dest_col] == player2:
        board[dest_row][dest_col] = white_king
        print("White piece promoted to King!")

#function that allows user to select a game mode
def selectGameMode():
    while True:
        print("Select game mode: ")
        print("1: Player vs Player")
        print("2: Player vs Alpha Player")
        choice = input("Enter 1 or 2: ").strip()
        if choice in ("1","2"):
            return int(choice)
        print("Invalid selection. Please try again.")

def getHumanMove(board, turn):
    # check globally for any capture moves available for the current player.

    all_captures = getAllCaptureMoves(board, turn)

    if all_captures:
        # force a capture move.
        # if there is only one available then we automatically take
        if len(all_captures) == 1:
            chosen = all_captures[0]
            print(f"Automatically capturing: Piece at ({chosen[0]}, {chosen[1]}) to ({chosen[2]}, {chosen[3]})")
        else:
            # otherwise we give option
            print("Multiple capture moves available:")
            # ask for an index from the user
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
        return chosen

    #no capture move available, ask for normal move

    src_row, src_col, dest_row, dest_col = get_move(board, turn)
    valid, cap_coord = isValidMove(board, turn, src_row, src_col, dest_row, dest_col)
    if not valid:
        print("Invalid move, try again.\n")
        return getHumanMove(board, turn)
    return (src_row, src_col, dest_row, dest_col, cap_coord)

def getAlphaMove(board,turn,depth=4):
    print("Ai is thinking..")
    score, move = minimax(board, depth, -float('inf'), float('inf'), turn, True)
    return move


def executeMove(board, move, turn, totalblack, totalwhite):
    src_row, src_col, dest_row, dest_col, cap_coord = move
    # move the piece
    piece = board[src_row][src_col]
    board[dest_row][dest_col] = piece
    board[src_row][src_col] = empty_black

    # if a capture is made then remove the piece of the opponent from the board
    if cap_coord is not None:
        cap_row, cap_col = cap_coord
        board[cap_row][cap_col] = empty_black
        if turn == 0:
            totalblack += 1
        else:
            totalwhite += 1

        # handle further jumps for this piece
        while True:
            # check if there is a further move
            further_moves = getCaptureMovesForPiece(board, turn, dest_row, dest_col)
            # if there is only one, then we automatically capture otherwise
            # promt the user for further instructions on which piece to capture.

            if not further_moves:
                break
            if len(further_moves) == 1:
                next_move = further_moves[0]
                print(
                    f"Automatically capturing further: ({next_move[0]}, {next_move[1]}) to ({next_move[2]}, {next_move[3]})")
            else:
                print("Multiple further capture moves available:")
                # give selections to the user

                for idx, mv in enumerate(further_moves):
                    print(f"{idx}: Move from ({mv[0]}, {mv[1]}) to ({mv[2]}, {mv[3]}) capturing piece at {mv[4]}")
                # error handle in case user enters an invalid input

                while True:
                    try:
                        choice = int(input("Select move index: "))
                        next_move = further_moves[choice]
                        break
                    except (ValueError, IndexError):
                        print("Invalid selection. Please enter a valid number")

            # execute further capture
            src_row, src_col, dest_row, dest_col, cap_coord = next_move
            # destination is replaced with peice
            board[dest_row][dest_col] = piece
            # source is blank
            board[src_row][src_col] = empty_black
            # capture coordinates are stores
            cap_row, cap_col = cap_coord
            # captured piece is replaced with blank
            board[cap_row][cap_col] = empty_black
            # the turn changes after execution
            if turn == 0:
                totalblack += 1
            else:
                totalwhite += 1

    # promotion
    promoteKing(turn, dest_row, dest_col, board)
    return totalblack, totalwhite

#main game loop, unified for player vs player and player vs ai
def main():
    mode = selectGameMode()
    alphaflag = (mode == 2) #true if alpha flag is on

    board = initGame() #start game
    totalblack = 0
    totalwhite = 0
    turn = 0  # 0 for black, 1 for white

    while True:
        printBoard(board, totalblack, totalwhite, turn)
        if endGameCheck(board):
            break

        if alphaflag and turn == 1: #get the alpha beta turn
            move = getAlphaMove(board, turn)
        else:
            move = getHumanMove(board, turn)

        totalblack, totalwhite = executeMove(board, move, turn, totalblack, totalwhite)
        turn = 1 - turn #change turn
# main game loop, unified for PvP and PvAI

#def main():
 #   board = initGame()
  #  totalblack = 0
  #  totalwhite = 0
 #   turn = 0  #again, 0 for black, 1 for white

    #promt user to select a mode: play against player or alpha player
  #  mode = 3
  #  while mode != 0 or mode != 1 :
  #      print("Select game mode:")
  #      print("1: Player vs Player")
  #      print("2: Player vs Alpha Player")
  #      mode = int(input("Enter 1 or 2: ").strip())

    #if alpha flag is on than the opponent player is alpha player

  #  alphaflag = (mode == 2)



  #  while True:
        #print the board
  #      printBoard(board, totalblack, totalwhite, turn)
        #check if the game is over: all pieces gone for either side.
 #       if endGameCheck(board):
  #          break

        #check globally for any capture moves available for the current player.

#        all_captures = getAllCaptureMoves(board, turn)

       # if all_captures:
            #force a capture move.
            #if there is only one available then we automatically take
           # if len(all_captures) == 1:
           #     chosen = all_captures[0]
           #     print(f"Automatically capturing: Piece at ({chosen[0]}, {chosen[1]}) to ({chosen[2]}, {chosen[3]})")
           # else:
                #otherwise we give option
             #   print("Multiple capture moves available:")
                #ask for an index from the user
             #   for idx, move in enumerate(all_captures):
              #      print(f"{idx}: Move piece at ({move[0]}, {move[1]}) to ({move[2]}, {move[3]}) capturing piece at {move[4]}")
              #  while True:
              #      try:
             #           choice = int(input("Select move index: "))
             #           chosen = all_captures[choice]
            #            break
            #        except (ValueError, IndexError):
            #            print("Invalid selection.")
           #             continue
            #move to the chosen
           # src_row, src_col, dest_row, dest_col, cap_coord = chosen
       # else:
            #no capture is available so we ask the player for a normal move.
        #    src_row, src_col, dest_row, dest_col = get_move(board, turn)
            #check if the move is valid
       #     valid, cap_coord = isValidMove(board, turn, src_row, src_col, dest_row, dest_col)
            #otherwise state that it is invalid
        #    if not valid:
        #        print("Invalid move, try again.\n")
        #        continue

        #move the piece
   #     piece = board[src_row][src_col]
   #     board[dest_row][dest_col] = piece
    #    board[src_row][src_col] = empty_black

        #if a capture is made then remove the piece of the opponent from the board
   #     if cap_coord is not None:
     #       cap_row, cap_col = cap_coord
     #       board[cap_row][cap_col] = empty_black

            #increase the capture number for the respective player
    #        if turn == 0:
    #            totalblack += 1
    #        else:
      #          totalwhite += 1

            #now we need to handle further jumps for this piece.
   #         while True:
                #check if there is a further move
     #           further_moves = getCaptureMovesForPiece(board, turn, dest_row, dest_col)
    #            if further_moves:
                    #if there is only one, then we automatically capture otherwise
                    #promt the user for further instructions on which piece to capture.
      #              if len(further_moves) == 1:
       #                 next_move = further_moves[0]
       #                 print(
       #                     f"Automatically capturing further: ({next_move[0]}, {next_move[1]}) to ({next_move[2]}, {next_move[3]})")
        #            else:
         #               print("Multiple further capture moves available:")
          #              #give selections to the user
           #             for idx, move in enumerate(further_moves):
            #                print(
             #                   f"{idx}: Move from ({move[0]}, {move[1]}) to ({move[2]}, {move[3]}) capturing piece at {move[4]}")
              #          #error handle in case user enters an invalid input
               #         while True:
                #            try:
                #                choice = int(input("Select move index: "))
                #                next_move = further_moves[choice]
                #                break
                #            except (ValueError, IndexError):
                #                print("Invalid selection. Please enter a valid number")
                #                continue

                    #execute further capture
           #         src_row, src_col, dest_row, dest_col, cap_coord = next_move
                    #destination is replaced with peice
           #         board[dest_row][dest_col] = piece
                    #source is blank
           #         board[src_row][src_col] = empty_black
                    #capture coordinates are stores
           #         cap_row, cap_col = cap_coord
                    #captured piece is replaced with blank
           #         board[cap_row][cap_col] = empty_black
                    #the turn changes after execution
           #         if turn == 0:
           #             totalblack += 1
           #         else:
           #             totalwhite += 1
           #     else:
           #         break

        #check for king promotion
     #   promoteKing(turn,dest_row,dest_col,board)

        #switch turn.
        #turn = 1 - turn


if __name__ == "__main__":
    main()
