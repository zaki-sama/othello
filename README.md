# Othello AI
agents
- alpha_beta_agent.py is the alpha-beta agent, which can be used with any heurisitc
- minimax_agent.py is the minimax agent, which uses the corner heuristic
- no_agent.py allows the user to play the game with another human player directly in the console using hte text-based interface

gui
- agent_gui_othello.py runs the GUI so two human players can play against each other
- manual_gui_othello.py runs the GUI where a player plays against the alpha-beta agent

testing
- test_alpha_beta.py can run the alpha-beta agent against random moves and returns the number of wins and losses

- main.py is responsible for command line inputs and deciding which agent to run with which arguments
- othello.py houses all the game logic, so methods do not need to be duplicated throughout 
