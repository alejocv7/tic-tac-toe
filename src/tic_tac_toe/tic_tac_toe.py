"""
This is a two player Tic-tac-toe game

The players take turns to input their marks on the board.
The board is represented as a common number pad:

 7 | 8 | 9
-----------
 4 | 5 | 6
-----------
 1 | 2 | 3
"""

import os
import textwrap


class TicTacToe:
    STARTING_BOARD = [str(num) for num in range(1, 10)]

    def __init__(self) -> None:
        self.board: list[str] = self.STARTING_BOARD[:]
        self.player_mark = "X"

    def print_board(self) -> None:
        """Prints the game board"""

        print(
            textwrap.dedent(
                f"""
                 {self.board[6]} | {self.board[7]} | {self.board[8]}
                -----------
                 {self.board[3]} | {self.board[4]} | {self.board[5]}
                -----------
                 {self.board[0]} | {self.board[1]} | {self.board[2]}
                """
            )
        )

    def change_player(self) -> None:
        self.player_mark = "O" if self.player_mark == "X" else "X"

    def get_next_player_move(self) -> int:
        """Prompts a player for their next mark location

        Returns:
            int: Player's chosen mark location
        """

        while True:
            try:
                player_move = int(
                    input(
                        f"\tPlayer '{self.player_mark}', your turn. Where's your move? "
                    )
                )
                if not 1 <= player_move <= len(self.board):
                    raise ValueError
                return player_move - 1

            except ValueError:
                print("\nInvalid input. Please enter a number between 1 and 9!")

    def check_win(self) -> bool:
        """Checks if a player has won the game

        Returns:
            bool: Whether a player has won
        """

        WINNING_COMBINATIONS = [
            # Rows
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
            if (
                self.board[combination[0]]
                == self.board[combination[1]]
                == self.board[combination[2]]
            ):
                return True
        return False

    def check_tie(self) -> bool:
        """Checks if the game has ended on a tie

        Returns:
            bool: Whether a tie exists
        """

        for mark in self.board:
            if mark not in {"X", "O"}:
                return False
        return True

    def should_play_again(self) -> bool:
        """Prompts player to check if they would like to keep playing

        Returns:
            bool: Whether user wants to play
        """

        while True:
            replay = input("Do you want to play again? - y or n: ").lower()
            if replay in {"y", "n"}:
                return replay == "y"
            print("Please, enter 'y' or 'n'")

    def run(self) -> None:
        # Clear the terminal
        os.system("clear" if os.name == "posix" else "cls")

        print("Welcome to Tic Tac Toe!")

        while True:
            # Player move
            self.print_board()
            player_move = self.get_next_player_move()
            self.board[player_move] = self.player_mark

            if (win := self.check_win()) or self.check_tie():
                self.print_board()
                if win:
                    print(f"\t***** Player '{self.player_mark}', you win! *****\n")
                else:
                    print("\t***** It's a tie! *****\n")

                if self.should_play_again():
                    self.board = self.STARTING_BOARD[:]
                else:
                    print("\nSee you later!\n")
                    break

            self.change_player()


if __name__ == "__main__":
    game = TicTacToe()
    game.run()
