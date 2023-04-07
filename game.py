from enum import Enum


class Player(Enum):
    Black = "B "
    White = "W "
    Empty = "_ "


class Othello:
    # initializes an empty board of othello with:
    # - a default board size of 8x8
    # - two players (0: black and 1: white), 2 is empty
    # - four discs in the middle (starting positions)
    def __init__(self, board_size=8):
        self.board_size = board_size
        self.current_player = Player.Black
        self.board = []
        self.last_flipped = []  # location of pieces last flipped by current player
        for row in range(board_size):
            row = []
            for col in range(board_size):
                row.append(Player.Empty)
            self.board.append(row)

        first_line = int(board_size / 2) - 1
        second_line = int(board_size / 2)
        self.board[first_line][first_line] = Player.White
        self.board[second_line][first_line] = Player.Black
        self.board[second_line][second_line] = Player.White
        self.board[first_line][second_line] = Player.Black

        print("next move: " + str(self.current_player))

    # def __str__(self):
    #     result = ''
    #     for row in self.board:
    #         for cell in row:
    #             result += cell.value
    #         result += '\n'
    #     return result

    def __str__(self):
        result = '  ' + ' '.join(str(i) for i in range(self.board_size)) + '\n'
        for i, row in enumerate(self.board):
            result += f'{i} '
            for cell in row:
                result += cell.value
            result += '\n'
        return result

    """ GAME LOGIC CODE """
    # undoes the last move made by a player
    def remove_disc(self, to_row, to_col):
        self.board[to_row][to_col] = Player.Empty
        for flipped_disc in self.last_flipped:
            r, c = flipped_disc[0], flipped_disc[1]
            self.board[r][c] = self.current_player


    # places a disc at to_row, to_col for current player
    def place_disc(self, to_row, to_col):
        self.last_move = []
        if self.board[to_row][to_col] == Player.Empty:
            for neighbor in self.get_neighbors_of(to_row, to_col):
                r, c = neighbor[0], neighbor[1]
                r_dir, c_dir = neighbor[2], neighbor[3]
                count = 0
                while self.in_board_bounds(r, c):
                    if self.is_opponent(r, c):
                        r += r_dir
                        c += c_dir
                        count += 1
                    elif self.board[r][c] == self.current_player and count > 0:
                        r -= r_dir
                        c -= c_dir
                        while self.is_opponent(r, c):
                            self.board[r][c] = self.current_player
                            self.last_flipped.append((r, c))
                            r -= r_dir
                            c -= c_dir
                        self.board[r][c] = self.current_player
                        break
                    else:
                        break

            self.switch_player()
        else:
            print("invalid move")

    # can the current player move to given row and col
    def is_valid_move(self, to_row, to_col):
        if self.board[to_row][to_col] == Player.Empty:
            # look at each neighbor around given row and col
            # try to get back to player position
            for neighbor in self.get_neighbors_of(to_row, to_col):
                r, c = neighbor[0], neighbor[1]
                r_dir, c_dir = neighbor[2], neighbor[3]
                count = 0
                while self.in_board_bounds(r, c):
                    # move further down the line in the same direction
                    # trying to find path to current player piece
                    if self.is_opponent(r, c):
                        r += r_dir
                        c += c_dir
                        count += 1
                    # stop once you encounter own player (piece to flip from)
                    # if there was at least one piece in the middle, this is a valid move
                    elif self.board[r][c] == self.current_player and count > 0:
                        return True
                    else:
                        break
        return False

    # returns all valid moves (row, col) tuples for current player
    def get_all_valid_moves(self):
        all_valid_moves = []
        for row in range(self.board_size):
            for col in range(self.board_size):
                move = (row, col)
                if self.is_valid_move(row, col) and move not in all_valid_moves:
                    all_valid_moves.append(move)
        return all_valid_moves

    @staticmethod
    def get_neighbors_of(r, c):
        neighbors = []
        for row_move in [-1, 0, 1]:
            for col_move in [-1, 0, 1]:
                if not (row_move == 0 and col_move == 0):
                    neighbor = (r + row_move, c + col_move, row_move, col_move)
                    neighbors.append(neighbor)
        return neighbors

    def get_all_positions(self):
        positions = []
        for row in range(self.board_size):
            for col in range(self.board_size):
                cell = self.board[row][col]
                if cell == self.current_player:
                    positions.append((row, col))
        return positions

    def is_opponent(self, r, c):
        if self.current_player == Player.Black:
            return self.board[r][c] == Player.White
        return self.board[r][c] == Player.Black

    def get_opponent(self):
        if self.current_player == Player.Black:
            return Player.White
        return Player.Black

    def switch_player(self):
        if self.current_player == Player.Black:
            self.current_player = Player.White
        else:
            self.current_player = Player.Black

    # is given row and col in the bounds of the board?
    def in_board_bounds(self, r, c):
        return 0 <= r < self.board_size and \
               0 <= c < self.board_size

    def game_over(self):
        moves_left = self.get_all_valid_moves()
        return len(moves_left) == 0

    def get_winner(self):
        black_count = 0
        white_count = 0
        if self.game_over():
            for row in self.board:
                for cell in row:
                    if cell == Player.Black:
                        black_count += 1
                    elif cell == Player.White:
                        white_count += 1
        print("black: " + str(black_count) + ", white: " + str(white_count))

    """ EVALUATION/HEURISTIC CODE """
    def corner_heuristics(self):
        size = self.board_size
        corners = [(0, 0), (0, size), (size, 0), (size, size)]
        total_distance = 0
        num_pieces = 0

        for row in range(self.board_size):
            for col in range(self.board_size):
                corner_distances = []
                if self.board[row][col] == self.current_player:
                    for corner in corners:
                        dist = self.manhattan_distance(corner[0], corner[1], row, col)
                        corner_distances.append(dist)
                    total_distance += min(corner_distances)
                    num_pieces += 1

        if num_pieces == 0:
            return 0

        return total_distance / num_pieces

    @staticmethod
    def manhattan_distance(r, c, new_r, new_c):
        return abs(r - new_r) + abs(c - new_c)

    """MINIMAX CODE"""
    def play_game(self):
        while True:
            moves = self.get_all_valid_moves()
            if len(moves) == 0:
                print("No more moves available")
                break

            if self.current_player == Player.Black:
                best_move = self.maximize()
            else:
                best_move = self.minimize()

            print(f"Player {self.current_player} played {best_move}")
            self.place_disc(best_move[0], best_move[1])

        print(self)

    def maximize(self):
        _, best_move = self.minimax(3, True)
        return best_move

    def minimize(self):
        _, best_move = self.minimax(3, False)
        return best_move

    def minimax(self, depth, is_maximizing):
        if depth == 0:
            print("depth reached: " + str(self.get_board_score()))
            return self.get_board_score(), None

        valid_moves = self.get_all_valid_moves()
        if len(valid_moves) == 0:
            if self.current_player == Player.Black:
                self.current_player = Player.White
            else:
                self.current_player = Player.Black
            return self.minimax(depth - 1, not is_maximizing)

        if is_maximizing:
            best_score = float('-inf')
            best_move = None
            print(valid_moves)
            for move in valid_moves:
                self.place_disc(move[0], move[1])
                score, _ = self.minimax(depth - 1, False)
                self.remove_disc(move[0], move[1])
                print("score: " + str(score) + ", best_score: " + str(best_score))
                if score > best_score:
                    best_score = score
                    best_move = move
            return best_score, best_move
        else:
            best_score = float('inf')
            best_move = None
            for move in valid_moves:
                self.place_disc(move[0], move[1])
                score, _ = self.minimax(depth - 1, True)
                self.remove_disc(move[0], move[1])
                if score < best_score:
                    best_score = score
                    best_move = move
            return best_score, best_move

    def get_board_score(self):
        black_score = 0
        white_score = 0
        for row in range(self.board_size):
            for col in range(self.board_size):
                if self.board[row][col] == Player.Black:
                    black_score += 1
                elif self.board[row][col] == Player.White:
                    white_score += 1
        return 0
        # if self.current_player == Player.Black:
        #     return black_score
        # if self.current_player == Player.White:
        #     return white_score

