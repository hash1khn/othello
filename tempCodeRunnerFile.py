import random


def is_valid_move(board, row, col, color):
    if board[row][col] != 0:
        return False

    opposite_color = "white" if color == "black" else "black"

    # Check if there's at least one neighbor of opposite color
    has_opposite_neighbor = False
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0:
                continue
            r, c = row + dr, col + dc
            if 0 <= r < len(board) and 0 <= c < len(board[0]) and board[r][c] == opposite_color:
                has_opposite_neighbor = True
                break
        if has_opposite_neighbor:
            break

    if not has_opposite_neighbor:
        return False

    # Check if there's a straight line starting with an opposite color and ending with the given color
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0:
                continue
            r, c = row + dr, col + dc
            while 0 <= r < len(board) and 0 <= c < len(board[0]):
                if board[r][c] == 0:
                    break
                if board[r][c] == color:
                    return True
                r += dr
                c += dc

    return False


def get_valid_moves(board, color):
    valid_moves = []
    for row in range(len(board)):
        for col in range(len(board[0])):
            if is_valid_move(board, row, col, color):
                valid_moves.append((row, col))
    return valid_moves


def select_next_play_random(board, color):
    valid_moves = get_valid_moves(board, color)
    return random.choice(valid_moves)


def count_flips(board, row, col, color, dr, dc):
    opponent_color = "white" if color == "black" else "black"
    r, c = row + dr, col + dc
    flips = 0

    while 0 <= r < len(board) and 0 <= c < len(board[0]) and board[r][c] == opponent_color:
        flips += 1
        r += dr
        c += dc

    if 0 <= r < len(board) and 0 <= c < len(board[0]) and board[r][c] == color:
        return flips
    else:
        return 0


def evaluate_move(board, row, col, color):
    if board[row][col] != 0:
        return -1  # Invalid move

    flips = 0
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0:
                continue
            flips += count_flips(board, row, col, color, dr, dc)

    return flips


def select_next_play_ai(board, color):
    valid_moves = get_valid_moves(board, color)
    best_move = valid_moves[0]
    best_score = -1

    for move in valid_moves:
        score = evaluate_move(board, move[0], move[1], color)
        if score > best_score:
            best_score = score
            best_move = move

    return best_move


def get_board_as_string(board):
    board_string = ""

    # Add column indices
    board_string += "  "
    for col in range(len(board[0])):
        board_string += f"{col % 10} "
    board_string += "\n"

    # Add horizontal line
    board_string += "  "
    for _ in range(len(board[0])):
        board_string += "- "
    board_string += "\n"

    # Add rows with row indices and cell values
    for row_idx, row in enumerate(board):
        board_string += f"{row_idx % 10}| "
        for cell in row:
            if cell == 0:
                board_string += ". "
            elif cell == 1:
                board_string += "\u25CF "  # Black token
            else:
                board_string += "\u25CB "  # White token
        board_string += "\n"

    return board_string


def set_up_board(width, height):
    board = [[0] * width for _ in range(height)]

    # Placing initial tokens in the center
    mid_row = height // 2
    mid_col = width // 2
    board[mid_row][mid_col] = 1  # White
    board[mid_row - 1][mid_col - 1] = 1  # White
    board[mid_row][mid_col - 1] = 2  # Black
    board[mid_row - 1][mid_col] = 2  # Black

    return board


def human_vs_random():
    board = set_up_board(8, 8)
    current_player = "white"
    winner = None

    while True:
        valid_moves = get_valid_moves(board, current_player)
        if not valid_moves:
            winner = "black" if current_player == "white" else "white"
            break

        print(f"Current Player: {current_player}")
        print(get_board_as_string(board))

        if current_player == "white":
            row = int(input("Select a row: "))
            col = int(input("Select a column: "))
        else:
            row, col = select_next_play_random(board, current_player)
            print(f"Random move for black: {row}, {col}")

        if is_valid_move(board, row, col, current_player):
            board[row][col] = 1 if current_player == "white" else 2
            current_player = "black" if current_player == "white" else "white"
        else:
            print("Invalid move. Try again.")

    print(f"Game Over. Winner: {winner}")
    print(get_board_as_string(board))

    return 1 if winner == "white" else 2 if winner == "black" else 0


def ai_vs_random():
    board = set_up_board(8, 8)
    current_player = "white"
    winner = None

    while True:
        valid_moves = get_valid_moves(board, current_player)
        if not valid_moves:
            winner = "black" if current_player == "white" else "white"
            break

        print(f"Current Player: {current_player}")
        print(get_board_as_string(board))

        if current_player == "white":
            row, col = select_next_play_ai(board, current_player)
            print(f"AI move for white: {row}, {col}")
        else:
            row, col = select_next_play_random(board, current_player)
            print(f"Random move for black: {row}, {col}")

        if is_valid_move(board, row, col, current_player):
            board[row][col] = 1 if current_player == "white" else 2
            current_player = "black" if current_player == "white" else "white"
        else:
            print("Invalid move. Try again.")

    print(f"Game Over. Winner: {winner}")
    print(get_board_as_string(board))

    return 1 if winner == "white" else 2 if winner == "black" else 0


def random_vs_random():
    board = set_up_board(8, 8)
    current_player = "white"
    winner = None

    while True:
        valid_moves = get_valid_moves(board, current_player)
        if not valid_moves:
            winner = "black" if current_player == "white" else "white"
            break

        print(f"Current Player: {current_player}")
        print(get_board_as_string(board))

        row, col = select_next_play_random(board, current_player)
        print(f"Random move for {current_player}: {row}, {col}")

        if is_valid_move(board, row, col, current_player):
            board[row][col] = 1 if current_player == "white" else 2
            current_player = "black" if current_player == "white" else "white"
        else:
            print("Invalid move. Try again.")

    print(f"Game Over. Winner: {winner}")
    print(get_board_as_string(board))

    return 1 if winner == "white" else 2 if winner == "black" else 0


# Example usage:
human_vs_random()
# ai_vs_random()
# random_vs_random()
