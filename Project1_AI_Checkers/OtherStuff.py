# OtherStuff.py
def convert_to_indices(move):
    """
    Converts a move in the format 'A3' to board indices (row, col).
    :param move: The move in the format 'A3'.
    :return: A tuple (row, col) representing the board indices.
    """
    col = ord(move[0].upper()) - ord('A')
    row = int(move[1]) - 1
    return row, col

def convert_to_notation(row, col):
    """
    Converts board indices (row, col) to human-readable notation (e.g., 'A3').
    :param row: The row index.
    :param col: The column index.
    :return: The move in the format 'A3'.
    """
    return f"{chr(col + ord('A'))}{row + 1}"

def is_valid_move(board, x1, y1, x2, y2):
    """
    Checks if a move is valid for a piece at (x1, y1).
    :param board: The current game board (2D list).
    :param x1, y1: The starting position of the piece.
    :param x2, y2: The target position of the move.
    :return: True if the move is valid, False otherwise.
    """
    piece = board[x1][y1]
    if piece == ' ':
        return False  # No piece to move

    # Directions for white and black pieces
    if piece == 'W':
        directions = [(1, -1), (1, 1)]  # White moves downward
    else:
        directions = [(-1, -1), (-1, 1)]  # Black moves upward

    # Check regular moves
    for dx, dy in directions:
        nx, ny = x1 + dx, y1 + dy
        if (nx, ny) == (x2, y2) and 0 <= nx < 8 and 0 <= ny < 8:
            if board[nx][ny] == ' ':
                return True  # Valid normal move

    # Check for captures (jumps)
    for dx, dy in directions:
        nx, ny = x1 + dx, y1 + dy
        jx, jy = x1 + 2 * dx, y1 + 2 * dy
        if (jx, jy) == (x2, y2) and 0 <= jx < 8 and 0 <= jy < 8 and 0 <= nx < 8 and 0 <= ny < 8:
            if board[nx][ny] not in (' ', piece) and board[jx][jy] == ' ':
                return True  # Valid jump

    return False  # Move is invalid

def print_board_state(board):
    """
    Prints the board state in a readable format.
    :param board: The current game board.
    """
    print("  A B C D E F G H")
    print(" +----------------")
    for i, row in enumerate(board):
        print(f"{i+1}|", end=" ")
        print(" ".join(row))
    print()

def log_analytics(states_expanded, time_taken, depth):
    """
    Logs analytics data to a file.
    :param states_expanded: The number of states expanded.
    :param time_taken: The time taken to compute the move.
    :param depth: The search depth.
    """
    with open("analytics.log", "a") as f:
        f.write(f"States expanded: {states_expanded}\n")
        f.write(f"Time taken: {time_taken:.2f} seconds\n")
        f.write(f"Search depth: {depth}\n")
        f.write("---\n")