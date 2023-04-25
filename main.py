# Press the green button in the gutter to run the script.
from alpha_beta_agent import AlphaBetaAgent
from minimax_agent import MinimaxAgent
from no_agent import NoAgent

if __name__ == '__main__':
    # game = NoAgent(board_size=6)
    game = AlphaBetaAgent(board_size=8, max_depth=3)
    game.play_game()
    #minimax_agent = MinimaxAgent(Player.Black)
    # game.play_game(minimax_agent)
    # result = game.__str__()
    # print(result)
    # game.play_game()
    # game.get_winner()
    # game.place_disc(1, 2)
    # game.place_disc(1, 1)
    # game.place_disc(4, 3)
    # game.place_disc(4, 4)
    # game.place_disc(2, 1)
    # game.place_disc(4, 2)
    # game.place_disc(1, 0)
    # game.place_disc(0, 2)
    # game.place_disc(5, 3)
    # game.place_disc(0, 0)
    # game.place_disc(1, 3)
    # game.place_disc(3, 4)
    # game.place_disc(5, 2)
    # game.place_disc(4, 1)
    # game.place_disc(3, 1)
    # game.place_disc(0, 3)
    # game.place_disc(3, 5)
    # game.place_disc(0, 1)
    # game.place_disc(3, 0)
    # game.place_disc(2, 5)
    # game.place_disc(1, 4)
    # game.place_disc(2, 4)
    # game.place_disc(1, 5)
    # game.place_disc(5, 4)
    # game.place_disc(4, 5)
    # game.place_disc(5, 5)
    # game.place_disc(2, 0)
    # game.place_disc(0, 4)
    # game.place_disc(0, 5)
    # game.place_disc(4, 0)
    # game.place_disc(5, 1)
    # game.place_disc(5, 0)
    # game.get_winner()