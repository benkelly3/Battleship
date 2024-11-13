# Authors: Ben Kelly, Aidan Reekie-Mell
# Emails: benkelly@umass.edu, areekiemell@umass.edu
# Spire IDs: 34825996, 34619547
# ༄ 

import random

def print_board(player_board,enemy_board):
    print("  A B C D E F G H I J")
    print("  ↓-↓-↓-↓-↓-↓-↓-↓-↓-↓")
    row_number = 1
    for row in board:
        print("%d|%s" % (row_number,"|".join(row)))
        row_number += 1

def game_rules():
    print("Hi! Welcome to Battleship. \n Let's explain the rules before we start the game. You will place 5 ships: one is 5 units long, one is 4 units long, two are 3 units long, and one is 2 units long. \n Once you place them, you'll pick coordinates on your opponent's grid to try to sink all of their ships. If they sink all of yours, you lose.\n There are some power-ups to be found, but we'll explain those if you find them. Good luck and have fun!")

class Battleship:
    def __init__(self, name, length, orientation, start_position):
        """name: name of the ship
           length: length of the ship
           orientation: orientation of the ship
           start_position: starting position of the ship on the grid"""
        self.name = name
        self.length = length
        self.orientation = orientation
        self.start_position = start_position

        self.positions = calculate_positions():
    def calculate_positions(self):
        positions = []
        row, col = self.start_position



def create_enemy_ships(enemy_board):
    # create 5 ships for the user to place

def create_player_ships(board):

def rotate_ship(board):

def shoot_yo_shot(enemy_board):
    # pick a coordinate to shoot at

def generate_powerups(enemy_board):
    # pick 3 random unoccupied spots on the board to place powerups

sunk_ships = 0

all_sunk = sunk_ships == 5

powerup_inv = 0

have_powerup = powerup_inv == 1

def one_turn(enemy_board):
    shoot_yo_shot(enemy_board)

def choose_powerup(power):
    elements = ['Extra_turns','Thermite','Reinforcements','Spy_drone']
    weights = [.5,.2,.2,.1]
    chosen_element = random.choices(elements,weights)[0]
    return chosen_element

def begin_game(board,enemy_board):
    n = input("Have you played Battleship before?")
    if n != ('Yes', 'yes', 'yeah', 'Yeah', 'Yup', 'yup', 'Ye', 'ye', 'Yep', 'yep', 'Yurr', 'yurr'):
        game_rules()
    print_board()

