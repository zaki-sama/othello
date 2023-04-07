import copy

from manual_play import Player, Othello


class MinimaxAgent:
    def __init__(self, max_depth: int = 5) -> None:
        self.current_player = Player.Black
        self.max_depth = max_depth
    # def playGame(self):

    def game_over(self, board):


    def minimax(self, board, depth, maximizing):
        if depth == 0 or game_over(board):
            return count_pieces(board)

        if maximizing:
            best_val = float("-inf")
            for move in valid_move(board, player):
                new_board = place_disc(copy(board), move, player)
                val = minimax(new_board, depth - 1, False)
                best_val = max(best_val, val)
            return best_val

        else:
            best_val = float("inf")
            for move in valid_move(board, player):
                new_board = place_disc(copy(board), move, player)
                val = minimax(new_board, depth - 1, False)
                best_val = min(best_val, val)
            return best_val
