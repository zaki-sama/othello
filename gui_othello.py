import tkinter as tk
from tkinter import messagebox
from othello import Othello, Player


class OthelloGUI:
    def __init__(self):
        self.gui = tk.Tk()
        self.gui.title("Othello")

        self.game = Othello()
        self.board = self.game.init_board()
        self.current_player = Player.Black

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

    def update_board(self):
        for i in range(self.game.board_size):
            for j in range(self.game.board_size):
                if self.board[i][j] == Player.Black:
                    self.board_gui[i][j].config(text='B', highlightbackground='#221F20')
                elif self.board[i][j] == Player.White:
                    self.board_gui[i][j].config(text='W', highlightbackground='#FFFFFF')
                else:
                    self.board_gui[i][j].config(text='_', highlightbackground='#20693D')

    def button_clicked(self, row, col):
        if self.game.is_valid_move(self.board, self.current_player, row, col):
            self.board = self.game.place_disc(self.board, self.current_player, row, col)
            self.update_board()
            if self.game.game_over(self.board):
                self.end_game()
            else:
                print("switched")
                self.current_player = self.game.switch_player(self.current_player)
        if len(self.game.get_all_valid_moves(self.board, self.current_player)) == 0:
            self.current_player = self.game.switch_player(self.current_player)

    def end_game(self):
        black_count, white_count = self.game.count_pieces(self.board)
        if black_count > white_count:
            message = "Black wins!"
        elif white_count > black_count:
            message = "White wins!"
        else:
            message = "Tie game!"
        tk.messagebox.showinfo("Game Over", message)


if __name__ == '__main__':
    app = OthelloGUI()
