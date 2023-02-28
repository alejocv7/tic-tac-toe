import textwrap
import unittest.mock

import pytest

from tic_tac_toe import tic_tac_toe


def format_board(board: list[str]) -> list[str]:
    """Returns the formatter board with the index number instead of the symbol "-"

    Args:
        board (list[str]): Tictactoe Game board

    Returns:
        list[str]: Formatted output with "-" replaced by the corresponding index + 1
    """
    for i in range(len(board)):
        if board[i] == "-":
            board[i] = str(i + 1)
    return board


@pytest.mark.parametrize(
    "board, expected",
    [
        (
            ["1", "2", "3", "4", "5", "6", "7", "8", "9"],
            textwrap.dedent(
                """
                 7 | 8 | 9
                -----------
                 4 | 5 | 6
                -----------
                 1 | 2 | 3\n
                """
            ),
        ),
        (
            ["X", "2", "O", "4", "X", "6", "X", "8", "O"],
            textwrap.dedent(
                """
                 X | 8 | O
                -----------
                 4 | X | 6
                -----------
                 X | 2 | O\n
                """
            ),
        ),
    ],
)
def test_print_board(capsys, board: list[str], expected: str) -> None:  # type: ignore
    """Test that printed board is well formatted

    Args:
        board (list[str]): Game board
    """
    tic_tac_toe.print_board(board)
    assert capsys.readouterr().out == expected


@pytest.mark.parametrize(
    "board",
    # fmt: off
    [
        # Test horizontal wins
        ["X", "X", "X",
         "O", "O", "-",
         "-", "-", "-"],

        ["O", "-", "-",
         "X", "X", "X",
         "O", "-", "-"],

        ["-", "-", "-",
         "O", "O", "O",
         "X", "X", "X"],

        # Vertical wins
        ["O", "X", "-",
         "O", "X", "-",
         "O", "-", "-"],

        ["-", "O", "X",
         "-", "O", "X",
         "-", "O", "-"],

        ["X", "-", "O",
         "X", "-", "O",
         "-", "-", "O"],

        # Diagonal wins
        ["X", "-", "-",
         "-", "X", "-",
         "-", "-", "X"],

        ["O", "-", "X",
         "-", "O", "-",
         "X", "-", "O"],
    ]
    # fmt: on
)
def test_check_win_with_a_winner(board: list[str]) -> None:
    """Test that check_win returns True when there is a winner

    Args:
        board (list[str]): Game board containing a winner
    """
    assert tic_tac_toe.check_win(format_board(board))


@pytest.mark.parametrize(
    "board",
    # fmt: off
    [
        ["X", "O", "X",
         "O", "X", "O",
         "O", "X", "O"],

        ["X", "O", "X",
         "O", "O", "X",
         "X", "X", "O"],

        ["-", "-", "-",
         "-", "-", "-",
         "-", "-", "-"],
    ]
    # fmt: on
)
def test_check_win_no_winner(board: list[str]) -> None:
    """Test that check_win returns False if there are no winners

    Args:
        board (list[str]): Game board without a winner
    """
    assert not tic_tac_toe.check_win(format_board(board))


@pytest.mark.parametrize(
    "board",
    # fmt: off
    [
        ["X", "O", "X",
         "O", "X", "O",
         "O", "X", "O"],

        ["X", "O", "X",
         "O", "O", "X",
         "X", "X", "O"],
    ]
    # fmt: on
)
def test_check_tie_with_tie(board: list[str]) -> None:
    """Test that check_tie returns True with boards containing a tie

    Args:
        board (list[str]): Game board with a tie
    """
    assert tic_tac_toe.check_tie(format_board(board))


@pytest.mark.parametrize(
    "board",
    # fmt: off
    [
        # Wins
        ["X", "X", "X",
         "O", "O", "-",
         "-", "-", "-"],

        ["O", "X", "-",
         "O", "X", "-",
         "O", "-", "-"],

        ["X", "-", "-",
         "-", "X", "-",
         "-", "-", "X"],

        # In-play boards
        ["-", "-", "O",
         "-", "-", "-",
         "X", "-", "-"],

        ["X", "-", "O",
         "-", "O", "-",
         "-", "X", "-"],

        ["-", "-", "-",
         "-", "-", "-",
         "-", "-", "-"],
    ]
    # fmt: on
)
def test_check_tie_no_tie(board: list[str]) -> None:
    """Test that check_tie returns False with boards that don't have a tie

    Args:
        board (list[str]): Game board without a tie
    """
    assert not tic_tac_toe.check_tie(format_board(board))


def test_should_play_again() -> None:
    """Test that should_play_again constantly prompts the user for a valid
    input. When the valid input is "y" the return value should be True"""
    with unittest.mock.patch("builtins.input", side_effect=["t", "3", "", "y"]):
        assert tic_tac_toe.should_play_again()


def test_should_play_again_no_play() -> None:
    """Test that should_play_again constantly prompts the user for a valid
    input. When the valid input is "n" the return value should be False"""
    with unittest.mock.patch("builtins.input", side_effect=["t", "3", "", "n"]):
        assert not tic_tac_toe.should_play_again()


@pytest.mark.parametrize("user_input", [str(num) for num in range(1, 10)])
def test_get_next_player_move_all_valid_moves(user_input: str) -> None:
    """Test that get_next_player_move return value is (input_value - 1) for valid inputs

    Args:
        user_input (list[str]): List of possible valid user inputs
    """
    with unittest.mock.patch("builtins.input", return_value=user_input):
        assert tic_tac_toe.get_next_player_move("X") == int(user_input) - 1


def test_get_next_player_move_wrong_inputs_first() -> None:
    """Test that get_next_player_move constantly prompts the user for a valid input.
    When the input is finally valid the returned value should be (input - 1)"""
    user_inputs = [str(num) for num in range(0, 50, 10)]
    user_inputs += ["1.1", "x", "", "$", "9"]
    with unittest.mock.patch("builtins.input", side_effect=user_inputs):
        assert tic_tac_toe.get_next_player_move("X") == int(user_inputs[-1]) - 1


def test_main_player_x_wins(capsys) -> None:  # type: ignore
    """Test that the main function makes a full game flow once and it gives X as winner"""
    moves = ["1", "2", "3", "4", "5", "6", "7", "n"]
    with unittest.mock.patch("builtins.input", side_effect=moves):
        tic_tac_toe.main()
    outputs = capsys.readouterr().out

    # Check that the welcome message was shown
    assert "Welcome to Tic Tac Toe!" in outputs

    # Check that the board was printed at the start of the game
    assert " 7 | 8 | 9\n-----------\n 4 | 5 | 6\n-----------\n 1 | 2 | 3\n\n" in outputs

    # Check that the end board was shown correctly during the game
    assert " X | 8 | 9\n-----------\n O | X | O\n-----------\n X | O | X\n\n" in outputs

    # Check that the game ended with a win
    assert "\t***** Player 'X', you win! *****\n\n" in outputs

    # Check that the game did not repeat
    assert "\nSee you later!\n\n" in outputs


def test_main_player_o_wins(capsys) -> None:  # type: ignore
    """Test that the main function makes a full game flow once and it gives O as winner"""
    moves = ["1", "2", "6", "8", "7", "4", "9", "5", "n"]
    with unittest.mock.patch("builtins.input", side_effect=moves):
        tic_tac_toe.main()
    outputs = capsys.readouterr().out

    # Check that the welcome message was shown
    assert "Welcome to Tic Tac Toe!" in outputs

    # Check that the board was printed at the start of the game
    assert " 7 | 8 | 9\n-----------\n 4 | 5 | 6\n-----------\n 1 | 2 | 3\n\n" in outputs

    # Check that the end board was shown correctly during the game
    assert " X | O | X\n-----------\n O | O | X\n-----------\n X | O | 3\n\n" in outputs

    # Check that the game ended with a win
    assert "\t***** Player 'O', you win! *****\n\n" in outputs

    # Check that the game did not repeat
    assert "\nSee you later!\n\n" in outputs


def test_main_player_tie(capsys) -> None:  # type: ignore
    """Test that the main function makes a full game flow once and it ends with a tie"""
    moves = ["1", "3", "2", "4", "6", "5", "7", "9", "8", "n"]
    with unittest.mock.patch("builtins.input", side_effect=moves):
        tic_tac_toe.main()
    outputs = capsys.readouterr().out

    # Check that the welcome message was shown
    assert "Welcome to Tic Tac Toe!" in outputs

    # Check that the board was printed at the start of the game
    assert " 7 | 8 | 9\n-----------\n 4 | 5 | 6\n-----------\n 1 | 2 | 3\n\n" in outputs

    # Check that the end board was shown correctly during the game
    assert " X | X | O\n-----------\n O | O | X\n-----------\n X | X | O\n\n" in outputs

    # Check that the game ended with a win
    assert "\t***** It's a tie! *****\n\n" in outputs

    # Check that the game did not repeat
    assert "\nSee you later!\n\n" in outputs


def test_main_play_twice_both_wins(capsys) -> None:  # type: ignore
    """Test that the main function makes a full game flow twice
    and it gives X and O as winners
    """

    moves = [
        "1", "4", "7", "6", "5", "2", "3", "y",  # Player X win
        "2", "1", "8", "6", "4", "7", "5", "n",  # Player O win
    ]  # fmt: skip

    with unittest.mock.patch("builtins.input", side_effect=moves):
        tic_tac_toe.main()
    outputs = capsys.readouterr().out

    # Check that the welcome message was shown
    assert "Welcome to Tic Tac Toe!" in outputs

    # Check that the board was printed twice at the start of the game (one per new game)
    assert (
        outputs.count(
            " 7 | 8 | 9\n-----------\n 4 | 5 | 6\n-----------\n 1 | 2 | 3\n\n"
        )
        == 2
    )

    # # Check that the end board was shown correctly during the game
    assert " X | 8 | 9\n-----------\n O | X | O\n-----------\n X | O | X\n\n" in outputs
    assert " X | O | 9\n-----------\n O | O | X\n-----------\n X | O | 3\n\n" in outputs

    # Check that the game ended with a win
    assert "\t***** Player 'X', you win! *****\n\n" in outputs
    assert "\t***** Player 'O', you win! *****\n\n" in outputs

    # Check that the game did not repeat
    assert "\nSee you later!\n\n" in outputs
