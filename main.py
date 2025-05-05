import random
import pickle
from alpha_beta import minimax
from rules import (getAllCaptureMoves, getCaptureMovesForPiece, isValidMove, endGameCheck, empty_black, player1,
                   player2, black_king, white_king, makeBoard, )
from rl_player import train_rl, QLearningAgent, CheckersEnv

#ending the game message
def endGame(winner):
    print()
    if winner == 1:
        print("White won the game!")
    elif winner == 0:
        print("Black won the game!")
    else:
        print("Draw!")

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
    board = makeBoard()
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

def executeMove(board, move, turn, totalblack, totalwhite):
    src_row, src_col, dest_row, dest_col, cap_coord = move
    #move the piece
    piece = board[src_row][src_col]
    board[dest_row][dest_col] = piece
    board[src_row][src_col] = empty_black

    #if a capture is made then remove the piece of the opponent from the board
    if cap_coord is not None:
        cap_row, cap_col = cap_coord
        board[cap_row][cap_col] = empty_black
        if turn == 0:
            totalblack += 1
        else:
            totalwhite += 1

        #handle further jumps for this piece
        while True:
            #check if there is a further move
            further_moves = getCaptureMovesForPiece(board, turn, dest_row, dest_col)
            #if there is only one, then we automatically capture otherwise
            # promt the user for further instructions on which piece to capture.

            if not further_moves:
                break
            if len(further_moves) == 1:
                next_move = further_moves[0]
                print(
                    f"Automatically capturing further: ({next_move[0]}, {next_move[1]}) to ({next_move[2]}, {next_move[3]})")
            else:
                print("Multiple further capture moves available:")
                #give selections to the user

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

    # promotion
    promoteKing(turn, dest_row, dest_col, board)
    return totalblack, totalwhite

#sets up alpha, changing depth can change results.
def getAlphaMove(board,turn,depth=4):
    score, move = minimax(board, depth, -float('inf'), float('inf'), turn, True)
    return move

#this function gets rl ai's move
def getRLMove(board, turn, agent, env):
    # opy board manually
    new_board = []
    for r in range(len(board)):
        row = board[r]
        new_row = []
        for c in range(len(row)):
            new_row.append(row[c])
        new_board.append(new_row)
    env.board = new_board
    env.turn = turn
    moves = env.legal_actions()
    #prepare state key manually
    state_rows = []
    for r in range(len(board)):
        row = board[r]
        tup_row = ()
        for c in range(len(row)):
            tup_row = tup_row + (row[c],)
        state_rows.append(tup_row)
    state = ()
    for tup in state_rows:
        state = state + (tup,)
    state = (state, turn)
    #find best
    best_move = None
    best_val = None
    for m in moves:
        val = agent.Q.get(state, {}).get(m, 0)
        if best_val is None or val > best_val:
            best_val = val
            best_move = m
    return best_move

#get winner index with 0 being black and 1 being white
def getWinner(board):
    black_count = 0
    white_count = 0
    for r in range(8):
        for c in range(8):
            cell = board[r][c]
            if cell == player1 or cell == black_king:
                black_count += 1
            if cell == player2 or cell == white_king:
                white_count += 1
    if black_count == 0:
        return 1
    if white_count == 0:
        return 0
    return None

#play a single game with specified players
def playGame(move_black, move_white, show):
    board = initGame()
    tb = 0
    tw = 0
    turn = 0
    while True:
        #i added show so that we dont have to see board every time for simulations
        if show:
            printBoard(board, tb, tw, turn)
        if endGameCheck(board):
            break
        if turn == 0:
            move = move_black(board, turn)
        else:
            move = move_white(board, turn)
        tb, tw = executeMove(board, move, turn, tb, tw)
        turn = 1 - turn
    if show:
        printBoard(board, tb, tw, turn)
        endGame(getWinner(board))
    return getWinner(board)

#simulate multiple games between alpha-beta and rl
def simulateAlphaVsRL(num_games):
    #set up agent
    agent = QLearningAgent()
    with open("q_table.pkl", "rb") as f:
        agent.Q = pickle.load(f)
    env = CheckersEnv(agent_id=1)

    def rlPlayer(board, turn):
        return getRLMove(board, turn, agent, env)

    alpha_wins = 0
    rl_wins    = 0
    draws      = 0

    #we play so alpha and rl and randomly selected as white and black players
    for _ in range(num_games):
        if random.random() < 0.5:
            black_fn, white_fn = getAlphaMove, rlPlayer
        else:
            black_fn, white_fn = rlPlayer, getAlphaMove

        winner = playGame(black_fn, white_fn, False)
        if winner == 0:
            #black won
            if black_fn is getAlphaMove:
                alpha_wins += 1
            else:
                rl_wins += 1
        elif winner == 1:
            #white won
            if white_fn is getAlphaMove:
                alpha_wins += 1
            else:
                rl_wins += 1
        else:
            draws += 1

    print("After", num_games, "games:")
    print("Alpha-beta wins:", alpha_wins)
    print("RL wins:", rl_wins)
    print("Draws:", draws)

#function that allows user to select a game mode
def selectGameMode():
    while True:
        print("Select game mode:")
        print("1: Player vs Player")
        print("2: Player vs Alpha Player")
        print("3: Train RL Player")
        print("4: Play vs RL Player")
        print("5: Simulate Alpha vs RL")
        choice = input("Enter 1-5: ").strip()
        if choice == "1" or choice == "2" or choice == "3" or choice == "4" or choice == "5":
            return int(choice)
        print("Invalid selection. Please try again.")


#main game loop.
def main():
    #get mode and do actions accordingly
    mode = selectGameMode()

    if mode == 3:
        x = input("Training episodes (default 1000): ")
        eps = int(x) if x.isdigit() else 1000
        train_rl(eps)
        return

    if mode == 5:
        x = input("Number of games (default 100): ")
        n = int(x) if x.isdigit() else 100
        simulateAlphaVsRL(n)
        return

    #setup players
    if mode == 1:
        move_black = getHumanMove
        move_white = getHumanMove
    #for alpha vs player, alpha gets a random color
    elif mode == 2:
        ai_color = random.choice([0,1])
        if ai_color == 0:
            move_black = getAlphaMove
            move_white = getHumanMove
        else:
            move_black = getHumanMove
            move_white = getAlphaMove
    else:  #mode == 4 (player vs rl player)
        #set up rl player
        agent = QLearningAgent()
        with open("q_table.pkl","rb") as f:
            agent.Q = pickle.load(f)
        env = CheckersEnv(agent_id=1)
        def rlPlayer(b, t):
            return getRLMove(b, t, agent, env)
        #rl player takes a random color
        ai_color = random.choice([0,1])
        print("RL plays", "Black" if ai_color==0 else "White")
        if ai_color == 0:
            move_black = rlPlayer
            move_white = getHumanMove
        else:
            move_black = getHumanMove
            move_white = rlPlayer

    playGame(move_black, move_white, True)

if __name__ == "__main__":
    main()
