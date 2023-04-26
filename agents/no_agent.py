from othello import Othello, Player


class NoAgent:
    def __init__(self, board_size=8):
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

            valid_move = False
            while not valid_move:
                # Prompt user for input
                row = input("Enter a row to move to:")
                col = input("Enter a row to move to:")

                if row.isdigit() and col.isdigit():
                    if self.state.is_valid_move(board, player, int(row), int(col)):
                        print("Moving to: (" + str(row) + ", " + str(col) + ")")
                        valid_move = True
                    else:
                        print("Invalid move, try again")
                else:
                    print("Invalid entry, try again")

            board = self.state.place_disc(board, player, int(row), int(col))
            player = self.state.switch_player(player)
        self.state.get_winner(board)


