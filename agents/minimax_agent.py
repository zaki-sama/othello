from othello import Othello, Player


class MinimaxAgent:
    def __init__(self, board_size=8, max_depth: int = 5, player=Player.Black):
        self.max_depth = max_depth
        self.state = Othello(board_size)
        self.maximizing_player = player
        self.minimizing_player = self.state.get_opponent(player)

    def value(self, board, player, depth):
        # print(str(player) + " " + str(depth))
        # print(self.corner_heuristic(board))
        # print(self.state.to_string(board))

        # terminal states
        if self.state.game_over(board) or depth >= self.max_depth:
            return self.corner_heuristic(board)

        if player == self.maximizing_player:
            # actions are only taken/returned by max agent
            return self.max_value(board, depth)

        return self.min_value(board, depth)

    def max_value(self, board, depth):
        v = float("-inf")
        possible_moves = self.state.get_all_valid_moves(board, self.maximizing_player)

        best_action = None
        for a in possible_moves:
            next_state = self.state.place_disc(self.copy_board(board), self.maximizing_player, a[0], a[1])
            potential_val = self.value(next_state, self.minimizing_player, depth + 1)
            if potential_val > v:
                v = potential_val
                best_action = a
        if best_action is None:
            print("None")
        if depth == 0:
            return best_action
        else:
            return v

    def min_value(self, board, depth):
        v = float("inf")
        possible_moves = self.state.get_all_valid_moves(board, self.minimizing_player)

        best_action = None
        for a in possible_moves:
            next_state = self.state.place_disc(self.copy_board(board), self.minimizing_player, a[0], a[1])
            potential_val = self.value(next_state, self.maximizing_player, depth + 1)
            if potential_val < v:
                v = potential_val
                best_action = a
        if best_action is None:
            print("None")
        if depth == 0:
            return best_action
        else:
            return v

    @staticmethod
    def copy_board(board):
        new_board = []
        for rows in board:
            row = []
            for cell in rows:
                row.append(cell)
            new_board.append(row)
        return new_board

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

    @staticmethod
    def manhattan_distance(r, c, new_r, new_c):
        return abs(r - new_r) + abs(c - new_c)