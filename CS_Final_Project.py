# Author: Ben Kelly
# Email: benkelly@umass.edu
# Spire ID:34825996

def print_board(board):
    print("  A B C D E F G H I J")
    print("  ↓-↓-↓-↓-↓-↓-↓-↓-↓-↓")
    row_number = 1
    for row in board:
        print("%d|%s" % (row_number,"|".join(row)))
        row_number += 1

def game_rules():
    print("Hi! Welcome to Battleship. \n Let's explain the rules before we start the game. You will place 5 ships: one is 5 units long, one is 4 units long, two are 3 units long, and one is 2 units long. \n Once you place them, you'll pick coordinates on your opponent's grid to try to sink all of their ships. If they sink all of yours, you lose.\n There are some power-ups to be found, but we'll explain those if you find them. Good luck and have fun!")

game_rules()