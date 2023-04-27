import random

from agents.alpha_beta_agent import AlphaBetaAgent
from agents.minimax_agent import MinimaxAgent
from othello import Othello, Player


class TestingClass:

    def __init__(self):
        self.alpha_beta = AlphaBetaAgent(player=Player.Black, max_depth=4, heuristic="difference")
        # self.minimax = MinimaxAgent()
        self.othello = Othello()

    def run_ab_agent(self):
        board = self.othello.init_board()
        current_player = self.alpha_beta.maximizing_player
        opponent = self.alpha_beta.minimizing_player
        while not self.othello.game_over(board):
            if current_player == opponent:
                valid_moves = self.othello.get_all_valid_moves(board, opponent)
                if valid_moves:
                    row, col = random.choice(valid_moves)
                    board = self.othello.place_disc(board, current_player, row, col)
                current_player = self.othello.switch_player(current_player)
            else:
                if self.alpha_beta.value(board, current_player, 0, float("-inf"), float("inf")) is not None:
                    row, col = self.alpha_beta.value(board, current_player, 0, float("-inf"), float("inf"))
                    board = self.othello.place_disc(board, current_player, row, col)
                current_player = self.othello.switch_player(current_player)
        winner = self.othello.get_winner(board)
        # print("states: " + str(self.alpha_beta.expanded_states))
        print(winner)
        return winner


if __name__ == '__main__':
    test = TestingClass()

    runs = 100
    wins = 0
    for x in range(runs):
        print(str(x))
        if test.run_ab_agent() == Player.Black:
            wins += 1

    print("Wins: " + str(wins) + ", Losses: " + str(runs - wins))
