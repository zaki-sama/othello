#!/usr/bin/env python3

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Description of your program')

    parser.add_argument('-play', help='Play the game', action='store_true')
    parser.add_argument('-size', type=int, help='Desired board size')
    parser.add_argument('-player', type=int, choices=[1, 2], help='1 if you want to play against the agent or 2')
    parser.add_argument('-heuristic', choices=['corner', 'pieces', 'difference', 'mobility'],
                        help='Pick between corner, pieces, difference, or mobility')

    args = parser.parse_args()

    if args.play:
        # game logic here
        print("Playing the game")
        print(f"Board size: {args.size}")
        print(f"Player: {args.player}")
        print(f"Heuristic: {args.heuristic}")