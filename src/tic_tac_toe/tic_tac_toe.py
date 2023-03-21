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

import board


class Board(board.Board):
    def show(self) -> None:
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


class TicTacToe:
    def __init__(self) -> None:
        self.board = Board()
        self.player = "X"

    def change_player(self) -> None:
        self.player = "O" if self.player == "X" else "X"

    def get_row_col_from_move(self, move: int) -> tuple[int, int]:
        """Map the user move number to row and col

        Args:
            move (int): User input move from 1 to ROWS * COLS

        Returns:
            tuple[int, int]: row, col equivalents of the game board
        """
        return (move - 1) // self.board.ROWS, (move - 1) % self.board.COLS

    def make_move(self) -> None:
        """Prompts a player for their next mark location and place it in the board

        Returns:
            int: Player's chosen mark location
        """

        while True:
            try:
                move = int(
                    input(f"\tPlayer '{self.player}', your turn. Where's your move? ")
                )
                row, col = self.get_row_col_from_move(move)
                self.board.insert_mark(self.player, row, col)
            except ValueError:
                print("\nInvalid input. Please enter a number between 1 and 9!")
            else:
                return

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
            self.board.show()
            self.make_move()

            if (win := self.board.check_win()) or self.board.check_tie():
                self.board.show()

                msg = f"Player '{self.player}', you win!" if win else "It's a tie!"
                print(f"\t***** {msg} *****\n")

                if self.should_play_again():
                    self.board.clean()
                else:
                    print("\nSee you later!\n")
                    break

            self.change_player()


if __name__ == "__main__":
    game = TicTacToe()
    game.run()
