import copy
import random as rand

from othello import Othello, Player


class AlphaBetaAgent:
    def __init__(self, board_size, max_depth: int = 5):
        self.max_depth = max_depth
        self.state = Othello(board_size)

    def play_game(self):
        player = Player.Black
        board = self.state.init_board()

        print(self.state.to_string(board))
        print(self.value(board, player, 0, float("-inf"), float("inf")))

    def value(self, board, player, depth, alpha, beta):
        print(str(player) + " " + str(depth))
        print(self.random_num())
        print(self.state.to_string(board))

        # terminal states
        if self.state.game_over(board) or depth >= self.max_depth:
            # return self.corner_heuristic(board)
            return self.random_num()

        if player == Player.Black:
            # actions are only taken/returned by max agent
            return self.max_value(board, depth, alpha, beta)

        return self.min_value(board, depth, alpha, beta)

    def max_value(self, board, depth, alpha, beta):
        v = float("-inf")
        possible_moves = self.state.get_all_valid_moves(board, Player.Black)

        best_action = None
        for a in possible_moves:
            next_state = self.state.place_disc(self.copy_board(board), Player.Black, a[0], a[1])
            potential_val = self.value(next_state, Player.White, depth + 1, alpha, beta)
            if potential_val > v:
                v = potential_val
                best_action = a
            if v > beta:
                print("max: v > beta, " + str(v) +" > " + str(beta))
                if depth == 0:
                    return best_action
                else:
                    return v
            alpha = max(alpha, v)

        if best_action is None:
            print("None")
        if depth == 0:
            return best_action
        else:
            return v

    def min_value(self, board, depth, alpha, beta):
        v = float("inf")
        possible_moves = self.state.get_all_valid_moves(board, Player.White)

        # based on pseudocode in hw2 pdf
        best_action = None
        for a in possible_moves:
            next_state = self.state.place_disc(self.copy_board(board), Player.White, a[0], a[1])
            potential_val = self.value(next_state, Player.Black, depth + 1, alpha, beta)
            if potential_val < v:
                v = potential_val
                best_action = a
            if v < alpha:
                print("min: v < alpha: " + str(alpha))
                if depth == 0:
                    return best_action
                else:
                    return v
            beta = min(beta, v)

        if best_action == None:
            print("None")
        if depth == 0:
            return best_action
        else:
            return v

    # evaluation function 1: maximizing difference between black and white discs
    def count_pieces(self, board):
        black_count = 0
        white_count = 0
        for row in board:
            for cell in row:
                if cell == Player.Black:
                    black_count += 1
                elif cell == Player.White:
                    white_count += 1
        # print("count: " + str(black_count - white_count))
        return black_count - white_count

    def random_num(self):
        return rand.randint(1, 10)

    # evaluation function 2: minimizing black's distance to corner
    def corner_heuristic(self, board):
        size = len(board)
        corners = [(0, 0), (0, size), (size, 0), (size, size)]
        total_distance = 0
        num_pieces = 0

        for row in range(size):
            for col in range(size):
                corner_distances = []
                if board[row][col] == Player.Black:
                    for corner in corners:
                        dist = self.manhattan_distance(corner[0], corner[1], row, col)
                        corner_distances.append(dist)
                    total_distance += min(corner_distances)
                    num_pieces += 1

        if num_pieces == 0:
            return 0

        return -(total_distance / num_pieces)


    @staticmethod
    def manhattan_distance(r, c, new_r, new_c):
        return abs(r - new_r) + abs(c - new_c)

    @staticmethod
    def copy_board(board):
        new_board = []
        for rows in board:
            row = []
            for cell in rows:
                row.append(cell)
            new_board.append(row)
        return new_board

    # def minimax(self, board, depth, maximizing):
    #     print(self.state.to_string(board))
    #     if depth == 0 or self.state.game_over(board):
    #         return self.count_pieces(self, board), None
    #
    #     if maximizing:
    #         print("Player Black")
    #         best_val = float("-inf")
    #         best_move = None
    #         for move in self.state.get_all_valid_moves(board, Player.Black):
    #             new_board = self.state.place_disc(board.copy(), Player.Black, move[0], move[1])
    #             val, _ = self.minimax(new_board, depth - 1, False)
    #             best_val = max(best_val, val)
    #             if val > best_val:
    #                 best_move = move
    #                 best_val = val
    #         print(best_val)
    #         print(best_move)
    #         print("maximizing")
    #         print(self.state.to_string(board))
    #         return best_val, best_move
    #
    #     else:
    #         print("Player White")
    #         best_val = float("inf")
    #         best_move = None
    #         for move in self.state.get_all_valid_moves(board, Player.White):
    #             new_board = self.state.place_disc(board.copy(), Player.White, move[0], move[1])
    #             val, _ = self.minimax(new_board, depth - 1, True)
    #             if val < best_val:
    #                 best_move = move
    #                 best_val = val
    #         print(best_val)
    #         print(best_move)
    #         print("minimizing")
    #         print(self.state.to_string(board))
    #         return best_val, best_move
