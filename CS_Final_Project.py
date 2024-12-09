# Authors: Ben Kelly, Aidan Reekie-Mell
# Emails: benkelly@umass.edu, areekiemell@umass.edu
# Spire IDs: 34825996, 34619547

import random

BOARD_SIZE = 10
SHIP_SIZES = [5, 4, 3, 3, 2]

def create_board():
    board = []
    for row in range(BOARD_SIZE):
        board.append(['~'] * BOARD_SIZE)
    return board

def print_board(board):
    print("    " + " ".join(str(i) for i in range(1, BOARD_SIZE + 1)))
    print("   +" + "---" * BOARD_SIZE + "+")
    for row_num in range(1, BOARD_SIZE + 1):
        print(f"{row_num:2} | {' '.join(board[row_num - 1])} |")
    print("   +" + "---" * BOARD_SIZE + "+")

def is_valid_placement(board, row, col, ship_length, orientation):
    if orientation == "horizontal":
        if col + ship_length > BOARD_SIZE:
            return False
        for i in range(ship_length):
            if board[row][col + i] != '~':
                return False
    elif orientation == "vertical":
        if row + ship_length > BOARD_SIZE:
            return False
        for i in range(ship_length):
            if board[row + i][col] != '~':
                return False
    return True

def place_player_ships(board):
    ships = []
    for ship_length in SHIP_SIZES:
        while True:
            print(f"Place your ship of length {ship_length}.")
            print_board(board)
            try:
                row, col, orientation = input(f"Enter the starting position and orientation (row,col,orientation) for the {ship_length}-long ship: ").split(",")
                row, col = int(row) - 1, int(col) - 1
                orientation = orientation.strip().lower()
                
                if orientation not in ["horizontal", "vertical"]:
                    print("Invalid orientation. Use 'horizontal' or 'vertical'.")
                    continue
                
                if is_valid_placement(board, row, col, ship_length, orientation):
                    if orientation == "horizontal":
                        for i in range(ship_length):
                            board[row][col + i] = 'S'
                    elif orientation == "vertical":
                        for i in range(ship_length):
                            board[row + i][col] = 'S'
                    ships.append((row, col, ship_length, orientation))
                    break
                else:
                    print("Invalid placement. Try again.")
            except ValueError:
                print("Invalid input format. Please enter the starting position and orientation in the format (row,col,orientation).")
    return ships

def place_computer_ships(board):
    ships = []
    for ship_length in SHIP_SIZES:
        while True:
            row = random.randint(0, BOARD_SIZE - 1)
            col = random.randint(0, BOARD_SIZE - 1)
            orientation = random.choice(["horizontal", "vertical"])

            if is_valid_placement(board, row, col, ship_length, orientation):
                if orientation == "horizontal":
                    for i in range(ship_length):
                        board[row][col + i] = 'S'
                elif orientation == "vertical":
                    for i in range(ship_length):
                        board[row + i][col] = 'S'
                ships.append((row, col, ship_length, orientation))
                break
    return ships

def get_player_guess():
    while True:
        guess = input("Enter your guess (row,col): ")
        try:
            row, col = guess.split(",")
            row = int(row) - 1
            col = int(col) - 1
            if 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE:
                return row, col
            else:
                print("Out of bounds! Try again.")
        except ValueError:
            print("Invalid input! Please enter two integers (row,col).")

def get_computer_guess():
    row = random.randint(0, BOARD_SIZE - 1)
    col = random.randint(0, BOARD_SIZE - 1)
    return row, col

def play_game():
    player_board = create_board()
    computer_board = create_board()

    print("Place your ships on the board.")
    player_ships = place_player_ships(player_board)

    print("\nThe computer is placing its ships.")
    computer_ships = place_computer_ships(computer_board)

    while True:
        print("\nYour board:")
        print_board(player_board)
        print("\nYour guesses:")
        hidden_board = [['~' if cell == '~' else 'X' for cell in row] for row in computer_board]
        print_board(hidden_board)

        row, col = get_player_guess()

        if (row, col) in computer_ships:
            print("You hit a ship!")
            computer_ships.remove((row, col))
            player_board[row][col] = 'X'
        else:
            print("You missed!")
            player_board[row][col] = 'O'

        if len(computer_ships) == 0:
            print("\nCongratulations! You sank all the computer's ships!")
            break

        print("\nComputer's turn!")
        row, col = get_computer_guess()

        if (row, col) in player_ships:
            print(f"Computer hit your ship at ({row + 1},{col + 1})!")
            player_ships.remove((row, col))
            computer_board[row][col] = 'X'
        else:
            print(f"Computer missed at ({row + 1},{col + 1}).")
            computer_board[row][col] = 'O'

        if len(player_ships) == 0:
            print("\nThe computer sank all your ships! You lose!")
            break

if __name__ == "__main__":
    play_game()
