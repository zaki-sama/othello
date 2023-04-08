import copy

from othello import Othello, Player


class MinimaxAgent:
    def __init__(self, board_size, max_depth: int = 5):
        self.max_depth = max_depth
        self.state = Othello(board_size)

    def play_game(self):
        player = Player.Black
        board = self.state.init_board()
        while not self.state.game_over(board):
            print(self.state.to_string(board))

            if self.state.no_moves_left(board, player):
                player = self.state.get_opponent(player)
            # Print whose turn it is
            if player == Player.Black:
                print("Black's Turn")
            else:
                print("White's Turn")

            move = self.value(board, player, 0)
            row, col = move[0], move[1]
            board = self.state.place_disc(board, player, int(row), int(col))
            player = self.state.switch_player(player)
        self.state.get_winner(board)

    def value(self, board, player, depth):
        # if player == game_state.getNumAgents():
        #     # reset agent to pacman amd increase depth
        #     depth += 1
        #     agent = 0

        # terminal states
        if self.state.game_over(board) or depth >= self.max_depth:
            return self.count_pieces(board)

        if player == Player.Black:
            # actions are only taken/returned by max agent
            return self.max_value(board, depth)

        return self.min_value(board, depth)

    def max_value(self, board, depth):
        v = float("-inf")
        possible_moves = self.state.get_all_valid_moves(board, Player.Black)

        best_action = None
        for a in possible_moves:
            next_state = self.state.place_disc(self.copy_board(board), Player.Black, a[0], a[1])
            potential_val = self.value(next_state, Player.White, depth + 1)
            if potential_val > v:
                v = potential_val
                best_action = a
        if best_action == None:
            print(v)
        if depth == 0:
            return best_action
        else:
            return v

    def min_value(self, board, depth):
        v = float("inf")
        possible_moves = self.state.get_all_valid_moves(board, Player.White)

        # based on pseudocode in hw2 pdf
        best_action = None
        for a in possible_moves:
            next_state = self.state.place_disc(self.copy_board(board), Player.White, a[0], a[1])
            potential_val = self.value(next_state, Player.Black, depth + 1)
            if potential_val < v:
                v = potential_val
                best_action = a
        if best_action == None:
            print(v)
        if depth == 0:
            return best_action
        else:
            return v

    # evaluation function 1: maximizing difference between black and white discs
    @staticmethod
    def count_pieces(board):
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
