import copy

from game import Player


class MinimaxAgent:
    def __init__(self, player: str, max_depth: int = 5) -> None:
        self.player = player
        self.max_depth = max_depth

    def get_action(self, board):
        best_move = None
        best_score = float('-inf')
        for move in self.get_valid_moves(board, self.player):
            new_board = self.get_new_board(board, move, self.player)
            score = self.minimax(new_board, self.max_depth - 1, False)
            if score > best_score:
                best_score = score
                best_move = move
        return best_move

    def minimax(self, board, depth, maximizing) -> int:
        if depth == 0 or self.game_over(board):
            return self.evaluate(board)

        if maximizing:
            max_score = float('-inf')
            for move in self.get_valid_moves(board, self.player):
                new_board = self.get_new_board(board, move, self.player)
                score = self.minimax(new_board, depth - 1, False)
                max_score = max(max_score, score)
            return max_score
        else:
            min_score = float('inf')
            opponent = self.get_opponent(self.player)
            for move in self.get_valid_moves(board, opponent):
                new_board = self.get_new_board(board, move, opponent)
                score = self.minimax(new_board, depth - 1, True)
                min_score = min(min_score, score)
            return min_score

    def get_valid_moves(self, board, player):
        all_valid_moves = []
        for row in range(8):
            for col in range(8):
                move = (row, col)
                if self.is_valid_move(board, player, row, col) and move not in all_valid_moves:
                    all_valid_moves.append(move)
        return all_valid_moves

    # can the current player move to given row and col
    def is_valid_move(self, board, player, to_row, to_col):
        if board[to_row][to_col] == Player.Empty:
            # look at each neighbor around given row and col
            # try to get back to player position
            for neighbor in self.get_neighbors_of(to_row, to_col):
                r, c = neighbor[0], neighbor[1]
                r_dir, c_dir = neighbor[2], neighbor[3]
                count = 0
                while self.in_board_bounds(board, r, c):
                    # move further down the line in the same direction
                    # trying to find path to current player piece
                    if self.is_opponent(board, player, r, c):
                        r += r_dir
                        c += c_dir
                        count += 1
                    # stop once you encounter own player (piece to flip from)
                    # if there was at least one piece in the middle, this is a valid move
                    elif board[r][c] == player and count > 0:
                        return True
                    else:
                        break
        return False

    def get_new_board(self, board, move, player):
        to_row, to_col = move[0], move[1]
        if board[to_row][to_col] == Player.Empty:
            for neighbor in self.get_neighbors_of(to_row, to_col):
                r, c = neighbor[0], neighbor[1]
                r_dir, c_dir = neighbor[2], neighbor[3]
                count = 0
                while self.in_board_bounds(board, r, c):
                    if self.is_opponent(board, player, r, c):
                        r += r_dir
                        c += c_dir
                        count += 1
                    elif board[r][c] == player and count > 0:
                        r -= r_dir
                        c -= c_dir
                        while self.is_opponent(board, player, r, c):
                            board[r][c] = player
                            r -= r_dir
                            c -= c_dir
                        board[r][c] = player
                        break
                    else:
                        break

            print(self.str(board))
        else:
            print("invalid move")

    def is_opponent(self, board, player, r, c):
        if player == Player.Black:
            return board[r][c] == Player.White
        return board[r][c] == Player.Black

    @staticmethod
    def get_neighbors_of(r, c):
        neighbors = []
        for row_move in [-1, 0, 1]:
            for col_move in [-1, 0, 1]:
                if not (row_move == 0 and col_move == 0):
                    neighbor = (r + row_move, c + col_move, row_move, col_move)
                    neighbors.append(neighbor)
        return neighbors

    def in_board_bounds(self, board, r, c):
        return 0 <= r < len(board) and \
               0 <= c < len(board)

    def game_over(self, board):
        b_moves_left = self.get_valid_moves(board, Player.Black)
        w_moves_left = self.get_valid_moves(board, Player.White)
        return len(b_moves_left) == 0 or len(w_moves_left) == 0


    def str(self, board):
        result = ''
        for row in board:
            for cell in row:
                result += cell.value
            result += '\n'
        return result