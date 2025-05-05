#use pickle to store policy

import pickle
import random
from collections import defaultdict
from rules import (getAllCaptureMoves,getCaptureMovesForPiece,isValidMove,endGameCheck,empty_black,player1,player2,black_king,white_king,makeBoard,)
from alpha_beta import simulateMove, getAllMoves

#create environment for rl player

class CheckersEnv:
    #trained for white
    def __init__(self, agent_id=1):
        self.agent_id = agent_id

    #reseet gives us a plain board
    def reset(self):
        #fresh board
        self.board = makeBoard()
        self.turn = 0
        return self._encode()
    #this method turns mutable board which is a list of lists into a single immutable hashtable
    #this is so i can use it as a key in hastable in q table dictionary.
    def _encode(self):
        rows = []
        for r in range(8):
            tup = ()
            for c in range(8):
                tup = tup + (self.board[r][c],)
            rows.append(tup)
        return (tuple(rows), self.turn)

    #uses getallcapture moves
    def legal_actions(self):
        return getAllMoves(self.board, self.turn)


    #agent plays, and rewards are assigned. enemy plays random moves.
    def step(self, action):
        #agent plays
        self.board = simulateMove(self.board, action, self.turn)

        #count pieces to check terminal
        black_count = 0
        white_count = 0
        for r in range(8):
            for c in range(8):
                cell = self.board[r][c]
                if cell in (player1, black_king):
                    black_count += 1
                if cell in (player2, white_king):
                    white_count += 1

        if black_count == 0 or white_count == 0:
            #terminal
            if self.agent_id == 1 and black_count == 0:
                reward = 1
            elif self.agent_id == 0 and white_count == 0:
                reward = 1
            else:
                reward = -1
            return self._encode(), reward, True

        #opponent moves random
        self.turn = 1 - self.turn
        opp_moves = self.legal_actions()
        if opp_moves:
            choice = random.randrange(len(opp_moves))
            self.board = simulateMove(self.board, opp_moves[choice], self.turn)

        # back to agent
        self.turn = 1 - self.turn
        return self._encode(), 0, False

#set up the agent
class QLearningAgent:

    def __init__(self):
        #create q table
        self.Q = defaultdict(dict)
        #alpha is our learning rate
        self.alpha = 0.1
        #gamma is our discount factor
        self.gamma = 0.99
        #epsilon greedy exploration schedule
        #how random we start
        self.epsilon_start = 1.0
        #gradually decay to floor
        self.epsilon_end = 0.1
        self.epsilon_decay = 5000
        #calculate how many training action
        self.steps = 0

    #function to gradually yo from epsilon start to epsilon end using epsilon decay.
    def _epsilon(self):
        frac = self.steps / self.epsilon_decay
        if frac > 1:
            frac = 1
        return self.epsilon_start - frac * (self.epsilon_start - self.epsilon_end)

    #exploration probability using epsilon, increment steps
    def select_action(self, state, legal_actions):
        eps = self._epsilon()
        self.steps += 1

        #if probability is lower than epsilon, than we take a random action to explore
        if random.random() < eps:
            return random.choice(legal_actions)
        #otherwise assume first action is the best so far to initialize greedy search
        #get its q-value and if it is unseen we treat as 0
        best = legal_actions[0]
        best_val = self.Q[state].get(best, 0)

        #loop through every legal action and get current q-val. if we find a higher one we update bestval
        for a in legal_actions:
            v = self.Q[state].get(a, 0)
            if v > best_val:
                best_val = v
                best = a
        #return move with highest q-val
        return best

    #q-learning bellman update
    def update(self, state, action, reward, next_state, next_legal):
        #compute best future value
        future = 0
        #if the next legal move is nonempty we look up q value of every next possible action in next state
        if next_legal:
            future = self.Q[next_state].get(next_legal[0], 0)
            for a in next_legal:
                v = self.Q[next_state].get(a, 0)
                if v > future:
                    future = v
        #update target using discount factor
        target = reward + self.gamma * future
        #get current qval, default to 0 if we havent seen previously
        old = self.Q[state].get(action, 0)
        #using learning rate move old toward taget
        self.Q[state][action] = old + self.alpha * (target - old)

    #train agent
    def train(self, episodes=1000):
        #train agent as white
        env = CheckersEnv(agent_id=1)

        for ep in range(1, episodes + 1):
            state = env.reset()
            done = False

            while not done:
                legal = env.legal_actions()
                if not legal:
                    #no legal moves treat as terminal
                    break

                action = self.select_action(state, legal)
                next_state, reward, done = env.step(action)

                #next_legal only if not done
                if not done:
                    next_legal = env.legal_actions()
                else:
                    next_legal = []

                self.update(state, action, reward, next_state, next_legal)
                state = next_state

            #progress report
            if ep % 100 == 0:
                print(f"Episode {ep}/{episodes}")

        #save q table after training
        with open("q_table.pkl", "wb") as f:
            pickle.dump(dict(self.Q), f)
        print("Training complete and saved to q_table.pkl.")

#instantiates for simplicity
def train_rl(episodes=1000):
    agent = QLearningAgent()
    agent.train(episodes)
