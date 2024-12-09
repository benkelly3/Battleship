import random

BOARD_SIZE = 10
SHIP_SIZES = [5, 4, 3, 3, 2]
POWERUP_WEIGHTS = (0.5, 0.2, 0.2, 0.1)

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

def place_ships(board, ship_sizes):
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

def generate_powerups(board, num_powerups=3, weights=POWERUP_WEIGHTS):
    powerups = ['Extra Turn', 'Thermite', 'UAV', 'Extra Ship']
    total_weights = sum(weights)
    normalized_weights = [w / total_weights for w in weights]
    board_positions = [(r, c) for r in range(BOARD_SIZE) for c in range(BOARD_SIZE)]
    random.shuffle(board_positions)

    powerup_positions = {}
    for _ in range(num_powerups):
        if not board_positions:
            break
        position = board_positions.pop()
        powerup = random.choices(powerups, weights=normalized_weights)[0]
        powerup_positions[position] = powerup

    return powerup_positions

def describe_powerup(powerup):
    descriptions = {
        'Extra Turn': "Attack twice on your next turn.",
        'Thermite': "On hit, destroy the target ship after 3 turns.",
        'UAV': "Reveals ships in a 3x3 grid around the hit.",
        'Extra Ship': "Place a new 1x3 ship on the board."
    }
    return descriptions.get(powerup, "Unknown powerup")

def handle_powerup(player, powerup, board, row, col, ships, fire_locations):
    print(f"{player} found a powerup: {powerup}! {describe_powerup(powerup)}")
    if powerup == 'Extra Turn':
        return True
    elif powerup == 'Thermite':
        fire_locations.append((row, col))
    elif powerup == 'UAV':
        for dr in range(-1, 2):
            for dc in range(-1, 2):
                nr, nc = row + dr, col + dc
                if 0 <= nr < BOARD_SIZE and 0 <= nc < BOARD_SIZE:
                    board[nr][nc] = '!'
    elif powerup == 'Extra Ship':
        place_ships(board, [3])
    return False

def check_fire(fire_locations, board, ships):
    for row, col in fire_locations:
        ship = next((s for s in ships if (row, col) in s), None)
        if ship:
            for r, c in ship:
                board[r][c] = 'X'
            ships.remove(ship)

def play_game():
    player_board = create_board()
    computer_board = create_board()

    print("Placing ships...")
    place_ships(player_board, SHIP_SIZES)
    place_ships(computer_board, SHIP_SIZES)

    print("\nGenerating powerups...")
    player_powerups = generate_powerups(player_board)
    computer_powerups = generate_powerups(computer_board)

    fire_locations = []
    player_extra_turn = False
    computer_extra_turn = False

    while True:
        print("\nYour board:")
        print_board(player_board)
        print("\nComputer's board (hidden):")
        print_board([['~' if cell == 'S' else cell for cell in row] for row in computer_board])

        # Player's turn
        print("\nYour turn!")
        row, col = map(int, input("Enter your guess (row,col): ").split(","))
        row, col = row - 1, col - 1

        if (row, col) in computer_powerups:
            powerup = computer_powerups.pop((row, col))
            player_extra_turn = handle_powerup("Player", powerup, computer_board, row, col, [], fire_locations)

        if computer_board[row][col] == 'S':
            print("You hit a ship!")
            computer_board[row][col] = 'X'
        else:
            print("You missed!")
            computer_board[row][col] = 'O'

        if not any('S' in row for row in computer_board):
            print("Congratulations! You sank all the computer's ships!")
            break

        if not player_extra_turn:
            print("\nComputer's turn!")
            row, col = random.randint(0, BOARD_SIZE - 1), random.randint(0, BOARD_SIZE - 1)

            if (row, col) in player_powerups:
                powerup = player_powerups.pop((row, col))
                computer_extra_turn = handle_powerup("Computer", powerup, player_board, row, col, [], fire_locations)

            if player_board[row][col] == 'S':
                print(f"Computer hit your ship at ({row + 1},{col + 1})!")
                player_board[row][col] = 'X'
            else:
                print(f"Computer missed at ({row + 1},{col + 1}).")
                player_board[row][col] = 'O'

            if not any('S' in row for row in player_board):
                print("The computer sank all your ships. You lose!")
                break

        # Process fire effects
        check_fire(fire_locations, player_board, [])
        check_fire(fire_locations, computer_board, [])


if __name__ == "__main__":
    play_game()
