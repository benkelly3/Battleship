import random

BOARD_SIZE = 10 # 10x10 grid
SHIP_SIZES = [5, 4, 3, 3, 2]
POWERUP_WEIGHTS = (0.5, 0.2, 0.2, 0.1) # probabilities for powerups

def create_board(): # creates the 10x10 board
    board = []
    for row in range(BOARD_SIZE):
        board.append(['~'] * BOARD_SIZE)
    return board

def print_board(board): # prints the gameboard with header and footer
    print("    " + " ".join(str(i) for i in range(1, BOARD_SIZE + 1)))
    print("   +" + "---" * BOARD_SIZE + "+")
    for row_num in range(1, BOARD_SIZE + 1):
        print(f"{row_num:2} | {' '.join(board[row_num - 1])} |")
    print("   +" + "---" * BOARD_SIZE + "+")

def is_valid_placement(board, row, col, ship_length, orientation): # logic for placing ships on the board
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

def place_ships(board, ship_sizes): # Places CPU ships
    for ship_length in ship_sizes:
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
                break

def place_player_ships(board, ship_sizes): # Placing player ships
    for ship_length in ship_sizes:
        while True:
            print_board(board) # updates the board after each ship is placed
            print(f"Place your ship of length {ship_length}.")
            try:
                row, col, orientation = input("Enter starting position and orientation (row,col,orientation): ").split(",")
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
                    break
                else:
                    print("Invalid placement. Try again.")
            except ValueError:
                print("Invalid input. Use the format (row,col,orientation).")

def generate_powerups(board, num_powerups=3, weights=POWERUP_WEIGHTS): # function for creating and placing powerups
    powerups = ['Extra Turn', 'Thermite', 'UAV', 'Extra Ship']
    total_weights = sum(weights)
    normalized_weights = [w / total_weights for w in weights]
    board_positions = [(r, c) for r in range(BOARD_SIZE) for c in range(BOARD_SIZE)]
    random.shuffle(board_positions)

    powerup_positions = {} 
    for i in range(num_powerups):
        if not board_positions: # Cannot place a powerup outside the board
            break
        position = board_positions.pop()
        powerup = random.choices(powerups, weights=normalized_weights)[0]
        powerup_positions[position] = powerup # Places a powerup at a random position from a list of available board positions

    return powerup_positions

def describe_powerup(powerup): # Text printed after a powerup is obtained
    descriptions = {
        'Extra Turn': "Attack twice on your next turn.",
        'Thermite': "On hit, destroy the target ship after 3 turns.",
        'UAV': "Reveals ships in a 3x3 grid around the hit.",
        'Extra Ship': "Place a new 1x3 ship on the board."
    }
    return descriptions.get(powerup, "Unknown powerup")

def handle_powerup(player, powerup, board, row, col, ships, fire_locations, thermite_active):
    print(f"{player} found a power-up: {powerup}! {describe_powerup(powerup)}")
    if powerup == 'Extra Turn':
        return True, thermite_active
    elif powerup == 'Thermite':
        thermite_active = True  # Activate Thermite for the next hit
        fire_locations.append((row, col))  # Optionally mark the location for immediate effects
    elif powerup == 'UAV':
        for dr in range(-1, 2):
            for dc in range(-1, 2):
                nr, nc = row + dr, col + dc
                if 0 <= nr < BOARD_SIZE and 0 <= nc < BOARD_SIZE:
                    board[nr][nc] = '!'
    elif powerup == 'Extra Ship':
        place_ships(board, [3])
    return False, thermite_active

def check_fire(fire_locations, board, ships):
    for row, col in fire_locations:
        ship = next((s for s in ships if (row, col) in s), None)
        if ship:
            for r, c in ship:
                board[r][c] = 'X'
            ships.remove(ship)

def reveal_powerups(player_powerups, computer_powerups):
    print("\n--- Debug: Power-Up Locations ---")
    print("Player Power-Ups:")
    for position, powerup in player_powerups.items():
        print(f"  {powerup} at {position[0] + 1},{position[1] + 1} (P)")

    print("Computer Power-Ups:")
    for position, powerup in computer_powerups.items():
        print(f"  {powerup} at {position[0] + 1},{position[1] + 1} (P)")
    print("---------------------------------")

def play_game():
    player_board = create_board()
    computer_board = create_board()

    print("Place your ships on the board.")
    place_player_ships(player_board, SHIP_SIZES)

    print("\nThe computer is placing its ships...")
    place_ships(computer_board, SHIP_SIZES)

    print("\nGenerating powerups...")
    player_powerups = generate_powerups(player_board)
    computer_powerups = generate_powerups(computer_board)

    fire_locations = []
    player_extra_turn = False
    computer_extra_turn = False
    target_queue = []

    while True:
        print("\nYour board:")
        print_board(player_board)
        print("\nComputer's board (hidden):")
        print_board([['~' if cell == 'S' else cell for cell in row] for row in computer_board])

        # Player's turn
        print("\nYour turn! (Type 'debug' to reveal power-ups)")
        guess = input("Enter your guess (row,col): ")

        if guess.lower() == "debug":
            reveal_powerups(player_powerups, computer_powerups)
            continue

        try:
            row, col = map(int, guess.split(","))
            row, col = row - 1, col - 1
        except ValueError:
            print("Invalid input! Enter row and column as numbers, separated by a comma.")
            continue

         if (row, col) in computer_powerups:
            powerup = computer_powerups.pop((row, col))
            print(f"You found a power-up: {powerup}! {describe_powerup(powerup)}")
            computer_board[row][col] = 'P'  # Mark power-up location
            player_extra_turn = handle_powerup("Player", powerup, computer_board, row, col, [], fire_locations)
            continue  # Skip to the next turn
     
        if computer_board[row][col] == 'S':
    print("You hit a ship!")
    computer_board[row][col] = 'X'
    
    # Check for Thermite activation
    if thermite_active:
        # Mark the ship as burning (optionally with a specific character like 'F')
        fire_locations.append((row, col))
        print("Thermite activated! This ship will be destroyed in 3 turns.")
        thermite_active = False  # Reset the flag after using Thermite
else:
    print("You missed!")
    computer_board[row][col] = 'O'

        if not any('S' in row for row in computer_board):
            print("Congratulations! You sank all the computer's ships!")
            break

        if not player_extra_turn:
            print("\nComputer's turn!")

            if target_queue:
                row, col = target_queue.pop(0)
            else:
                row, col = random.randint(0, BOARD_SIZE - 1), random.randint(0, BOARD_SIZE - 1)

            if player_board[row][col] == 'S':
                print(f"Computer hit your ship at ({row + 1},{col + 1})!")
                player_board[row][col] = 'X'

                for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    nr, nc = row + dr, col + dc
                    if 0 <= nr < BOARD_SIZE and 0 <= nc < BOARD_SIZE and player_board[nr][nc] == '~':
                        target_queue.append((nr, nc))
            else:
                print(f"Computer missed at ({row + 1},{col + 1}).")
                player_board[row][col] = 'O'

            if not any('S' in row for row in player_board):
                print("The computer sank all your ships. You lose!")
                break

        check_fire(fire_locations, player_board, [])
        check_fire(fire_locations, computer_board, [])

if __name__ == "__main__":
    play_game()
