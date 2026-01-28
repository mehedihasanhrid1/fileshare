import random
from colorama import init, Fore, Style

init(autoreset=True)

def display_board(board):
    def format_cell(cell_value):
        if cell_value == 'X':
            return Fore.RED + cell_value
        if cell_value == 'O':
            return Fore.BLUE + cell_value
        return Fore.YELLOW + cell_value

    print()
    print(f" {format_cell(board[0])} | {format_cell(board[1])} | {format_cell(board[2])}")
    print(Fore.CYAN + "-----------")
    print(f" {format_cell(board[3])} | {format_cell(board[4])} | {format_cell(board[5])}")
    print(Fore.CYAN + "-----------")
    print(f" {format_cell(board[6])} | {format_cell(board[7])} | {format_cell(board[8])}")
    print()

def check_win(board, player_symbol):
    winning_positions = [
        (0, 1, 2), (3, 4, 5), (6, 7, 8),
        (0, 3, 6), (1, 4, 7), (2, 5, 8),
        (0, 4, 8), (2, 4, 6)
    ]
    return any(
        board[a] == board[b] == board[c] == player_symbol
        for a, b, c in winning_positions
    )

def check_full(board):
    return all(not cell.isdigit() for cell in board)

def ai_move(board, ai_symbol, player_symbol):
    for index in range(9):
        if board[index].isdigit():
            simulated_board = board.copy()
            simulated_board[index] = ai_symbol
            if check_win(simulated_board, ai_symbol):
                board[index] = ai_symbol
                return

    for index in range(9):
        if board[index].isdigit():
            simulated_board = board.copy()
            simulated_board[index] = player_symbol
            if check_win(simulated_board, player_symbol):
                board[index] = ai_symbol
                return

    available_positions = [index for index in range(9) if board[index].isdigit()]
    board[random.choice(available_positions)] = ai_symbol

def player_move(board, player_symbol):
    while True:
        try:
            move = int(input(Fore.GREEN + "Enter move (1-9): "))
            if move not in range(1, 10):
                print(Fore.RED + "Invalid input. Please choose a number between 1 and 9.")
            elif not board[move - 1].isdigit():
                print(Fore.RED + "This position is already taken. Please choose another.")
            else:
                board[move - 1] = player_symbol
                break
        except ValueError:
            print(Fore.RED + "Invalid input. Please enter a numeric value.")
