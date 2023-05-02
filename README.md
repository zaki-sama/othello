# Othello AI

### How to Run
To run the GUI, open agent_gui_othello.py to play against the computer or manual_gui_othello.py to play with the human player next to you. If you are running manual_gui_othello.py, just scroll down to line 77 and click the play button. If you are running agent_gui_othello.py, you can change the heuristic on line 12 (the options are "corner", "count", "difference", and "mobility) and click the play button on line 101. If you have no available moves, you can click any of the squares and the agent will make their move. 

### Files
agents
- alpha_beta_agent.py is the alpha-beta agent, which can be used with any heurisitc
- minimax_agent.py is the minimax agent, which uses the corner heuristic
- no_agent.py allows the user to play the game with another human player directly in the console using the text-based interface

gui
- agent_gui_othello.py runs the GUI so two human players can play against each other
- manual_gui_othello.py runs the GUI where a player plays against the alpha-beta agent

testing
- test_alpha_beta.py can run the alpha-beta agent against random moves and returns the number of wins and losses

- main.py is responsible for command line inputs and deciding which agent to run with which arguments
- othello.py houses all the game logic, so methods do not need to be duplicated throughout 

<img width="500" alt="Screen Shot 2023-05-02 at 1 08 18 PM" src="https://user-images.githubusercontent.com/99611638/235774493-69e1734a-7f4d-4082-abbc-e485bd75513e.png">
