import textwrap
import unittest.mock

import pytest

from tic_tac_toe import TicTacToe


@pytest.fixture
def game() -> TicTacToe:
    return TicTacToe()


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
def test_print_board(  # type: ignore
    capsys, game: TicTacToe, board: list[str], expected: str
) -> None:
    """Test that printed board is well formatted

    Args:
        board (list[str]): Game board
    """
    game.board = board
    game.print_board()
    assert capsys.readouterr().out == expected


@pytest.mark.parametrize(
    "board",
    # fmt: off
    [
        # Test horizontal wins
        ["X", "X", "X",
         "O", "O", "6",
         "1", "2", "3"],

        ["O", "8", "9",
         "X", "X", "X",
         "O", "2", "3"],

        ["7", "8", "9",
         "O", "O", "O",
         "X", "X", "X"],

        # Vertical wins
        ["O", "X", "9",
         "O", "X", "6",
         "O", "2", "3"],

        ["7", "O", "X",
         "4", "O", "X",
         "1", "O", "3"],

        ["X", "8", "O",
         "X", "5", "O",
         "1", "2", "O"],

        # Diagonal wins
        ["X", "8", "9",
         "4", "X", "6",
         "1", "2", "X"],

        ["O", "8", "X",
         "4", "O", "6",
         "X", "2", "O"],
    ]
    # fmt: on
)
def test_check_win_with_a_winner(game: TicTacToe, board: list[str]) -> None:
    """Test that check_win returns True when there is a winner

    Args:
        board (list[str]): Game board containing a winner
    """
    game.board = board
    assert game.check_win()


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

        ["7", "8", "9",
         "4", "5", "6",
         "1", "2", "3"],
    ]
    # fmt: on
)
def test_check_win_no_winner(game: TicTacToe, board: list[str]) -> None:
    """Test that check_win returns False if there are no winners

    Args:
        board (list[str]): Game board without a winner
    """
    game.board = board
    assert not game.check_win()


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
def test_check_tie_with_tie(game: TicTacToe, board: list[str]) -> None:
    """Test that check_tie returns True with boards containing a tie

    Args:
        board (list[str]): Game board with a tie
    """
    game.board = board
    assert game.check_tie()


@pytest.mark.parametrize(
    "board",
    # fmt: off
    [
        # Wins
        ["X", "X", "X",
         "O", "O", "6",
         "1", "2", "3"],

        ["O", "X", "9",
         "O", "X", "6",
         "O", "2", "3"],

        ["X", "8", "9",
         "4", "X", "6",
         "1", "2", "X"],

        # In-play boards

        ["7", "8", "O",
         "4", "5", "6",
         "X", "2", "3"],

        ["X", "8", "O",
         "4", "O", "6",
         "1", "X", "3"],

        ["7", "8", "9",
         "4", "5", "6",
         "1", "2", "3"],
    ]
    # fmt: on
)
def test_check_tie_no_tie(game: TicTacToe, board: list[str]) -> None:
    """Test that check_tie returns False with boards that don't have a tie

    Args:
        board (list[str]): Game board without a tie
    """
    game.board = board
    assert not game.check_tie()


def test_should_play_again(game: TicTacToe) -> None:
    """Test that should_play_again constantly prompts the user for a valid
    input. When the valid input is "y" the return value should be True"""
    with unittest.mock.patch("builtins.input", side_effect=["t", "3", "", "y"]):
        assert game.should_play_again()


def test_should_play_again_no_play(game: TicTacToe) -> None:
    """Test that should_play_again constantly prompts the user for a valid
    input. When the valid input is "n" the return value should be False"""
    with unittest.mock.patch("builtins.input", side_effect=["t", "3", "", "n"]):
        assert not game.should_play_again()


@pytest.mark.parametrize("user_input", [str(num) for num in range(1, 10)])
def test_get_next_player_move_all_valid_moves(game: TicTacToe, user_input: str) -> None:
    """Test that get_next_player_move return value is (input_value - 1) for valid inputs

    Args:
        user_input (list[str]): List of possible valid user inputs
    """
    with unittest.mock.patch("builtins.input", return_value=user_input):
        assert game.get_next_player_move() == int(user_input) - 1


def test_get_next_player_move_wrong_inputs_first(game: TicTacToe) -> None:
    """Test that get_next_player_move constantly prompts the user for a valid input.
    When the input is finally valid the returned value should be (input - 1)"""
    user_inputs = [str(num) for num in range(0, 50, 10)]
    user_inputs += ["1.1", "x", "", "$", "9"]
    with unittest.mock.patch("builtins.input", side_effect=user_inputs):
        assert game.get_next_player_move() == int(user_inputs[-1]) - 1


def test_run_player_x_wins(capsys, game: TicTacToe) -> None:  # type: ignore
    """Test that the run function makes a full game run once and that X is the winner"""
    moves = ["1", "2", "3", "4", "5", "6", "7", "n"]
    with unittest.mock.patch("builtins.input", side_effect=moves):
        game.run()
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


def test_run_player_o_wins(capsys, game: TicTacToe) -> None:  # type: ignore
    """Test that the run function makes a full game run once and that O is the winner"""
    moves = ["1", "2", "6", "8", "7", "4", "9", "5", "n"]
    with unittest.mock.patch("builtins.input", side_effect=moves):
        game.run()
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


def test_run_tie(capsys, game: TicTacToe) -> None:  # type: ignore
    """Test that the run function makes a full game flow once and it ends with a tie"""

    moves = ["1", "3", "2", "4", "6", "5", "7", "9", "8", "n"]
    with unittest.mock.patch("builtins.input", side_effect=moves):
        game.run()
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


def test_run_twice_both_players_win(capsys, game: TicTacToe) -> None:  # type: ignore
    """Test that the run function makes a full game flow twice
    and it gives X and O as winners
    """

    moves = [
        "1", "4", "7", "6", "5", "2", "3", "y",  # Player X win
        "2", "1", "8", "6", "4", "7", "5", "n",  # Player O win
    ]  # fmt: skip

    with unittest.mock.patch("builtins.input", side_effect=moves):
        game.run()
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
