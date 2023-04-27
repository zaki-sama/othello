import tkinter as tk
from tkinter import messagebox
from agents.alpha_beta_agent import AlphaBetaAgent
from othello import Othello, Player


class SinglePlayerOthelloGUI:
    def __init__(self):
        self.gui = tk.Tk()
        self.gui.title("Othello")

        self.agent = AlphaBetaAgent(player=Player.White, max_depth=4, heuristic="difference")
        self.game = Othello()
        self.board = self.game.init_board()
        self.current_player = Player.Black

        self.turn_label = tk.Label(self.gui, text="Black's turn", font=("Helvetica", 16))
        self.turn_label.grid(row=self.game.board_size, column=0, columnspan=self.game.board_size)

        self.board_gui = None
        self.create_gui_board()

        self.gui.mainloop()

    def create_gui_board(self):
        self.board_gui = []
        for r in range(self.game.board_size):
            board_row = []
            for c in range(self.game.board_size):
                slot = tk.Button(self.gui, highlightbackground="#20693D",
                                 height=4, width=5,
                                 command=lambda row=r, col=c: self.button_clicked(row, col))
                slot.grid(row=r, column=c)
                board_row.append(slot)
            self.board_gui.append(board_row)

        self.update_board()

    def update_turn_label(self):
        if self.current_player == Player.Black:
            self.turn_label.config(text="Black's turn")
        else:
            self.turn_label.config(text="White is thinking...")

    def update_board(self):
        for i in range(self.game.board_size):
            for j in range(self.game.board_size):
                if self.board[i][j] == Player.Black:
                    self.board_gui[i][j].config(text='B', highlightbackground='#221F20')
                elif self.board[i][j] == Player.White:
                    self.board_gui[i][j].config(text='W', highlightbackground='#FFFFFF')
                else:
                    self.board_gui[i][j].config(text=' ', highlightbackground='#20693D')

    def button_clicked(self, row, col):
        print("turn: " + str(self.current_player))
        if self.game.is_valid_move(self.board, self.current_player, row, col):
            self.board = self.game.place_disc(self.board, self.current_player, row, col)
            self.update_board()
            if self.game.game_over(self.board):
                self.end_game()
            else:
                self.current_player = self.game.switch_player(self.current_player)

        if not self.game.game_over(self.board):
            if self.current_player == Player.White:
                self.update_turn_label()
                self.gui.after(500, self.pick_max_move)
            if len(self.game.get_all_valid_moves(self.board, self.current_player)) == 0:
                tk.messagebox.showinfo("Warning", "No Possible Moves")
                self.current_player = self.game.switch_player(self.current_player)
                self.gui.after(500, self.pick_max_move)
        else:
            self.end_game()

    def pick_max_move(self):
        row, col = self.agent.value(self.board, Player.White, 0, float("-inf"), float("inf"))
        self.board = self.game.place_disc(self.board, self.current_player, row, col)
        self.update_board()
        if self.game.game_over(self.board):
            self.end_game()
        else:
            self.current_player = self.game.switch_player(self.current_player)
            self.update_turn_label()

    def end_game(self):
        self.turn_label.config(text="Game Over!")
        black_count, white_count = self.game.count_pieces(self.board)
        if black_count > white_count:
            message = "Black wins!"
        elif white_count > black_count:
            message = "White wins!"
        else:
            message = "Tie game!"
        tk.messagebox.showinfo("Game Over", message)


if __name__ == '__main__':
    app = SinglePlayerOthelloGUI()
