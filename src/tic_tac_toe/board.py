from typing import Literal


class Board:
    ROWS, COLS = 3, 3

    def __init__(self) -> None:
        self.board = self.get_clean_board()
        self.mark: Literal["X", "O"] = "X"

    def change_player(self) -> None:
        self.mark = "O" if self.mark == "X" else "X"

    def clean(self) -> None:
        """Reset the game board"""
        self.board = self.get_clean_board()

    def get_clean_board(self) -> list[list[str | int]]:
        """Generate a clean board"""
        return [
            [(row * self.COLS) + col + 1 for col in range(self.COLS)]
            for row in range(self.ROWS)
        ]

    def show(self) -> None:
        """Prints the game board"""
        print(self.board)

    def is_valid_row_col(self, row: int, col: int) -> bool:
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

    def insert_mark(self, row: int, col: int) -> None:
        if not self.is_valid_row_col(row, col):
            raise ValueError
        self.board[row][col] = self.mark

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
