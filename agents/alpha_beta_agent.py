from othello import Othello, Player


class AlphaBetaAgent:
    def __init__(self, board_size=8, max_depth=5, player=Player.Black, heuristic=""):
        self.max_depth = max_depth
        self.state = Othello(board_size)
        self.maximizing_player = player
        self.minimizing_player = self.state.get_opponent(player)
        self.expanded_states = 0
        self.heuristic = heuristic

    def value(self, board, player, depth, alpha, beta):
        self.expanded_states += 1

        # terminal states
        if self.state.game_over(board) or depth >= self.max_depth:
            if self.heuristic == "pieces":
                return self.count_heuristic(board)
            elif self.heuristic == "difference":
                return self.difference_heuristic(board)
            elif self.heuristic == "mobility":
                return self.mobility_heuristic(board)
            else:
                return self.corner_heuristic(board)

        if player == self.maximizing_player:
            # actions are only taken/returned by max agent
            return self.max_value(board, depth, alpha, beta)

        return self.min_value(board, depth, alpha, beta)

    def max_value(self, board, depth, alpha, beta):
        v = float("-inf")
        possible_moves = self.state.get_all_valid_moves(board, self.maximizing_player)

        best_action = None
        for a in possible_moves:
            next_state = self.state.place_disc(self.copy_board(board), self.maximizing_player, a[0], a[1])
            potential_val = self.value(next_state, self.minimizing_player, depth + 1, alpha, beta)
            if potential_val > v:
                v = potential_val
                best_action = a
            if v > beta:
                if depth == 0:
                    return best_action
                else:
                    return v
            alpha = max(alpha, v)

        if depth == 0:
            return best_action
        else:
            return v

    def min_value(self, board, depth, alpha, beta):
        v = float("inf")
        possible_moves = self.state.get_all_valid_moves(board, self.minimizing_player)

        # based on pseudocode in hw2 pdf
        best_action = None
        for a in possible_moves:
            next_state = self.state.place_disc(self.copy_board(board), self.minimizing_player, a[0], a[1])
            potential_val = self.value(next_state, self.maximizing_player, depth + 1, alpha, beta)
            if potential_val < v:
                v = potential_val
                best_action = a
            if v < alpha:
                if depth == 0:
                    return best_action
                else:
                    return v
            beta = min(beta, v)

        if depth == 0:
            return best_action
        else:
            return v

    # EVALUATION FUNCTIONS ---------------------------------------------------------------------
    # evaluation function 1: maximizing the number of black discs
    def count_heuristic(self, board):
        black_count = 0
        for row in board:
            for cell in row:
                if cell == Player.Black:
                    black_count += 1
        return black_count

    # evaluation function 2: maximizing difference between black and white discs
    def difference_heuristic(self, board):
        black_count = 0
        white_count = 0
        for row in board:
            for cell in row:
                if cell == Player.Black:
                    black_count += 1
                if cell == Player.White:
                    white_count += 1
        return black_count - white_count

    # evaluation function 3: minimizing black's distance to corner
    def corner_heuristic(self, board):
        size = len(board)
        corners = [(0, 0), (0, size), (size, 0), (size, size)]
        total_distance = 0
        num_pieces = 0

        for row in range(size):
            for col in range(size):
                corner_distances = []
                if board[row][col] == self.maximizing_player:
                    for corner in corners:
                        dist = self.manhattan_distance(corner[0], corner[1], row, col)
                        corner_distances.append(dist)
                    total_distance += min(corner_distances)
                    num_pieces += 1

        if num_pieces == 0:
            return 0

        return -(total_distance / num_pieces)

    def mobility_heuristic(self, board):
        return len(self.state.get_all_valid_moves(board, self.maximizing_player))

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