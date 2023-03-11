"""This is a two player Tic-tac-toe game

Players take turns to input their marks on the board, represented as a number pad:

 7 | 8 | 9
-----------
 4 | 5 | 6
-----------
 1 | 2 | 3
"""

import os
import textwrap


class TicTacToe:
    ROWS, COLS = 3, 3

    def __init__(self) -> None:
        self.board = self.get_clean_board()
        self.player = "X"

    def get_clean_board(self) -> list[list[str | int]]:
        """Generate a clean state board"""
        return [
            [(row * self.COLS) + col + 1 for col in range(self.COLS)]
            for row in range(self.ROWS)
        ]

    def print_board(self) -> None:
        """Prints the game board"""

        print(
            textwrap.dedent(
                f"""
                 {" | ".join(map(str, self.board[2]))}
                -----------
                 {" | ".join(map(str, self.board[1]))}
                -----------
                 {" | ".join(map(str, self.board[0]))}
                """
            )
        )

    def change_player(self) -> None:
        self.player = "O" if self.player == "X" else "X"

    def get_row_col_from_move(self, move: int) -> tuple[int, int]:
        """Map the user move number to row and col

        Args:
            move (int): User input move from 1 to ROWS * COLS

        Returns:
            tuple[int, int]: row, col equivalents of the game board
        """
        return (move - 1) // self.ROWS, (move - 1) % self.COLS

    def is_valid_idx(self, row: int, col: int) -> bool:
        """Checks whether a new move is valid based on board index and occupied spots

        Args:
            move (int): Player move

        Returns:
            bool: Whether the move is within board's len and not on an ocupied spot
        """
        return (
            0 <= row < self.ROWS
            and 0 <= col < self.COLS
            and self.board[row][col] not in {"X", "O"}
        )

    def get_next_player_move(self) -> tuple[int, int]:
        """Prompts a player for their next mark location

        Returns:
            int: Player's chosen mark location
        """

        while True:
            try:
                move = int(
                    input(f"\tPlayer '{self.player}', your turn. Where's your move? ")
                )
                row, col = self.get_row_col_from_move(move)
                if not self.is_valid_idx(row, col):
                    raise ValueError
                return row, col

            except ValueError:
                print("\nInvalid input. Please enter a number between 1 and 9!")

    def check_win(self) -> bool:
        """Checks if a player has won the game

        Returns:
            bool: Whether a player has won
        """

        # Check rows
        for row in self.board:
            if len(set(row)) == 1:
                return True

        # Check columns
        for col in range(self.COLS):
            if len(set(row[col] for row in self.board)) == 1:
                return True

        # Check diagonals
        if len(set(self.board[i][i] for i in range(self.ROWS))) == 1:
            return True
        if len(set(self.board[i][self.COLS - i - 1] for i in range(self.ROWS))) == 1:
            return True

        return False

    def check_tie(self) -> bool:
        """Checks if the game has ended on a tie

        Returns:
            bool: Whether a tie exists
        """

        for row in self.board:
            for mark in row:
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
            row, col = self.get_next_player_move()
            self.board[row][col] = self.player

            if (win := self.check_win()) or self.check_tie():
                self.print_board()
                if win:
                    print(f"\t***** Player '{self.player}', you win! *****\n")
                else:
                    print("\t***** It's a tie! *****\n")

                if self.should_play_again():
                    self.board = self.get_clean_board()
                else:
                    print("\nSee you later!\n")
                    break

            self.change_player()


if __name__ == "__main__":
    game = TicTacToe()
    game.run()
