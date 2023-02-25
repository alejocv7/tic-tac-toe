"""
This is a two player Tic-tac-toe game

The players take turns to input their marks on the board.
The board is represented as a common number pad:

 7 | 8 | 9 
-----------
 4 | 5 | 6 
-----------
 1 | 2 | 3

TODO:
    1. Check for ties
    2. Change to OOP 
"""

import os
import textwrap
from typing import Literal

STARTING_BOARD = list(range(1, 10))


def print_board(board: list) -> None:
    """Prints the game board

    Args:
        board (list): The game board
    """

    print(
        textwrap.dedent(
            f"""
             {board[6]} | {board[7]} | {board[8]}
            -----------
             {board[3]} | {board[4]} | {board[5]}
            -----------
             {board[0]} | {board[1]} | {board[2]}
            """
        )
    )


def select_mark() -> Literal["X", "O"]:
    """Asks a player to select a mark ("x|o") to play with

    Returns:
        Literal["X", "O"]: player mark
    """

    player_mark = None
    while player_mark not in {"X", "O"}:
        if player_mark is not None:
            print("\nWe're not off to a good start here!")

        player_mark = input(
            "\tPlayer 1, please pick a mark ('X' or 'O') and hit 'Enter': "
        ).upper()

    return player_mark


def get_next_player_move(player_mark: str) -> int:
    """Prompts a player for their next mark location

    Args:
        player_mark (str)

    Returns:
        int: Player's chosen mark location
    """

    while True:
        try:
            player_move = int(
                input(f"\tPlayer '{player_mark}', your turn. Where's your move? ")
            )

            if not 1 <= player_move <= 9:
                raise ValueError
            return player_move - 1

        except ValueError:
            print("\nInvalid input. Please enter a number between 1 and 9!")


def check_win(board: list) -> bool:
    """Checks if a player has won the game

    Args:
        board (list): The game board to check

    Returns:
        bool: Whether a player has won
    """

    WINNING_COMBINATIONS = [
        # Rows:
        (0, 1, 2),
        (3, 4, 5),
        (6, 7, 8),
        # Columns
        (0, 3, 6),
        (1, 4, 7),
        (2, 5, 8),
        # Diagonals
        (0, 4, 8),
        (2, 4, 6),
    ]

    for combination in WINNING_COMBINATIONS:
        if board[combination[0]] == board[combination[1]] == board[combination[2]]:
            return True
    return False


def check_tie(board: list) -> bool:
    """Checks if the game has ended on a tie

    Args:
        board (list): The game board to check

    Returns:
        bool: Whether a tie exists
    """

    for mark in board:
        if mark not in {"X", "O"}:
            return False
    return True


def should_play_again() -> bool:
    """Prompts player to check if they would like to keep playing

    Returns:
        bool: Whether user wants to play
    """

    replay = None
    while replay not in {"y", "n"}:
        if replay is not None:
            print("Please, enter 'y' or 'n'")

        replay = input("Do you want to play again? - y or n: ").lower()

    return replay == "y"


def main():
    # Clear the terminal
    if os.name == "posix":
        os.system("clear")
    else:
        os.system("cls")

    # Introduce and initialize the game
    print("Welcome to Tic Tac Toe!")
    player_mark = select_mark()
    board = STARTING_BOARD.copy()

    while True:
        # Player move
        print_board(board)
        player_move = get_next_player_move(player_mark)
        board[player_move] = player_mark

        if (win := check_win(board)) or check_tie(board):
            print_board(board)
            if win:
                print(f"\t***** Player '{player_mark}', you win! *****\n")
            else:
                print(f"\t***** It's a tie! *****\n")

            if should_play_again():
                board = STARTING_BOARD.copy()
            else:
                print("\nSee you later!\n")
                break

        player_mark = "O" if player_mark == "X" else "X"


if __name__ == "__main__":
    main()
