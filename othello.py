from enum import Enum


class Player(Enum):
    Black = "B "
    White = "W "
    Empty = "_ "


class Othello:
    def __init__(self, board_size=8):
        self.board_size = board_size

    # def __str__(self):
    #     result = ''
    #     for row in self.board:
    #         for cell in row:
    #             result += cell.value
    #         result += '\n'
    #     return result

    def to_string(self, board):
        result = '  ' + ' '.join(str(i) for i in range(self.board_size)) + '\n'
        for i, row in enumerate(board):
            result += f'{i} '
            for cell in row:
                result += cell.value
            result += '\n'
        return result

    def is_valid_move(self, board, player, to_row, to_col):
        if board[to_row][to_col] == Player.Empty:
            # look at each neighbor around given row and col
            # try to get back to player position
            for neighbor in self.get_neighbors_of(to_row, to_col):
                r, c = neighbor[0], neighbor[1]
                r_dir, c_dir = neighbor[2], neighbor[3]
                count = 0
                while self.in_board_bounds(len(board), r, c):
                    # move further down the line in the same direction
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

    # places a disc at to_row, to_col for current player
    def place_disc(self, board, player, to_row, to_col):
        if board[to_row][to_col] == Player.Empty:
            for neighbor in self.get_neighbors_of(to_row, to_col):
                r, c = neighbor[0], neighbor[1]
                r_dir, c_dir = neighbor[2], neighbor[3]
                count = 0
                while self.in_board_bounds(len(board), r, c):
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

        else:
            print("invalid move")
        return board

    def game_over(self, board):
        black_over = self.no_moves_left(board, Player.Black)
        white_over = self.no_moves_left(board, Player.White)
        if black_over and white_over:
            print("Game over!")
            return True

    def no_moves_left(self, board, player):
        moves_left = self.get_all_valid_moves(board, player)
        return len(moves_left) == 0

    def get_all_valid_moves(self, board, player):
        all_valid_moves = []
        for row in range(len(board)):
            for col in range(len(board)):
                move = (row, col)
                if self.is_valid_move(board, player, row, col) and move not in all_valid_moves:
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

    # is given row and col in the bounds of the board?
    def in_board_bounds(self, board_size, r, c):
        return 0 <= r < board_size and \
               0 <= c < board_size

    def is_opponent(self, board, player, r, c):
        if player == Player.Black:
            return board[r][c] == Player.White
        return board[r][c] == Player.Black

    def get_opponent(self, player):
        if player == Player.Black:
            return Player.White
        return Player.Black

    def switch_player(self, player):
        if player == Player.Black:
            return Player.White
        return Player.Black

    def init_board(self):
        board = []
        for row in range(self.board_size):
            row = []
            for col in range(self.board_size):
                row.append(Player.Empty)
            board.append(row)

        first_line = int(self.board_size / 2) - 1
        second_line = int(self.board_size / 2)
        board[first_line][first_line] = Player.White
        board[second_line][first_line] = Player.Black
        board[second_line][second_line] = Player.White
        board[first_line][second_line] = Player.Black

        return board

    def get_winner(self, board):
        black_count = 0
        white_count = 0
        if self.game_over(board):
            for row in board:
                for cell in row:
                    if cell == Player.Black:
                        black_count += 1
                    elif cell == Player.White:
                        white_count += 1
        print("Black: " + str(black_count) + ", White: " + str(white_count))
        if black_count > white_count:
            print("Black wins!")
            return Player.Black
        elif white_count > black_count:
            print("White wins!")
            return Player.White
        return Player.Empty
