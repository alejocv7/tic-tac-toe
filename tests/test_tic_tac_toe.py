import textwrap
import typing
import unittest.mock

import pytest

from tic_tac_toe import Board, TicTacToe


@pytest.fixture
def game() -> TicTacToe:
    return TicTacToe()


@pytest.mark.parametrize(
    "board, expected",
    [
        (
            [["1", "2", "3"], ["4", "5", "6"], ["7", "8", "9"]],
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
            [["X", "2", "O"], ["4", "X", "6"], ["X", "8", "O"]],
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
def test_print_board(
    capsys: pytest.CaptureFixture[str],
    game: TicTacToe,
    board: list[list[str | int]],
    expected: str,
) -> None:
    """Test that the printed board is well formatted"""
    game.board.board = board
    game.board.show()
    assert capsys.readouterr().out == expected


@pytest.mark.parametrize("curr_mark, next_mark", [("X", "O"), ("O", "X")])
def test_change_player(
    game: TicTacToe, curr_mark: typing.Literal["X", "O"], next_mark: str
) -> None:
    """Test that change_player function correctly gives the next player"""
    game.player = curr_mark
    game.change_player()
    assert game.player == next_mark


@pytest.mark.parametrize(
    "move, expected",
    [(1, (0, 0)), (3, (0, 2)), (5, (1, 1)), (7, (2, 0)), (9, (2, 2))],
)
def test_get_row_col_from_move(
    game: TicTacToe, move: int, expected: tuple[int, int]
) -> None:
    """Test that the calculated row, col from the player's move is correct"""
    assert game.get_row_col_from_move(move) == expected


@pytest.fixture(params=(n + 1 for n in range(Board.ROWS * Board.COLS)))
def valid_move(request: pytest.FixtureRequest) -> int:
    return int(request.param)


def test_make_move_all_valid_moves(game: TicTacToe, valid_move: int) -> None:
    """Test that make_move inserts the player's mark when a valid move is passed"""
    with unittest.mock.patch("builtins.input", return_value=str(valid_move)):
        game.make_move()
        row, col = game.get_row_col_from_move(valid_move)
        assert game.board.board[row][col] == game.player


def test_make_move_with_spot_taken(game: TicTacToe, valid_move: int) -> None:
    """Test that is invalid for an user to try to make a move on an occupied spot"""
    occupied = (valid_move % (Board.ROWS * Board.COLS)) + 1
    row, col = game.get_row_col_from_move(occupied)
    game.board.board[row][col] = "X"

    with unittest.mock.patch("builtins.input", side_effect=[occupied, valid_move]):
        game.make_move()
        row, col = game.get_row_col_from_move(valid_move)
        assert game.board.board[row][col] == game.player


def test_make_move_wrong_inputs_first(game: TicTacToe) -> None:
    """Test that make_move constantly prompts the user for a valid input.
    When the input is finally valid the mark should be placed in the board"""
    moves = [str(n) for n in range(0, 50, 10)]
    moves += ["1.1", "x", "", "$", "9"]
    with unittest.mock.patch("builtins.input", side_effect=moves):
        game.make_move()
        row, col = game.get_row_col_from_move(int(moves[-1]))
        assert game.board.board[row][col] == game.player


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


# # ------ Teting gull game-run ------

GAME_MSGS = [
    "Welcome to Tic Tac Toe!",  # Game welcome message
    " 7 | 8 | 9\n-----------\n 4 | 5 | 6\n-----------\n 1 | 2 | 3\n\n",  # Init board
    "\nSee you later!\n\n",  # Game ending message
]


@pytest.mark.parametrize(
    "winner, end_board",
    [
        ("X", " X | 8 | 9\n-----------\n O | X | O\n-----------\n X | O | X\n\n"),
        ("O", " X | O | X\n-----------\n O | O | X\n-----------\n X | O | 3\n\n"),
    ],
)
def test_run_win(
    capsys: pytest.CaptureFixture[str], game: TicTacToe, winner: str, end_board: str
) -> None:
    """Test that the run function runs once fully and that the winner is as expected"""
    winner_moves = {
        "X": ["1", "2", "3", "4", "5", "6", "7", "n"],
        "O": ["1", "2", "6", "8", "7", "4", "9", "5", "n"],
    }

    with unittest.mock.patch("builtins.input", side_effect=winner_moves[winner]):
        game.run()
    outputs = capsys.readouterr().out

    # Check that all the standard game messages were shown
    for msg in GAME_MSGS:
        assert msg in outputs

    # Check that the end board was shown correctly after the game
    assert end_board in outputs

    # Check that the game ended with a win
    assert f"\t***** Player '{winner}', you win! *****\n\n" in outputs


def test_run_tie(capsys: pytest.CaptureFixture[str], game: TicTacToe) -> None:
    """Test that the run function makes a full game flow once and it ends with a tie"""
    moves = ["1", "3", "2", "4", "6", "5", "7", "9", "8", "n"]
    with unittest.mock.patch("builtins.input", side_effect=moves):
        game.run()
    outputs = capsys.readouterr().out

    # Check that all the standard game messages were shown
    for msg in GAME_MSGS:
        assert msg in outputs

    # Check that the end board was shown correctly during the game
    assert " X | X | O\n-----------\n O | O | X\n-----------\n X | X | O\n\n" in outputs

    # Check that the game ended with a tie
    assert "\t***** It's a tie! *****\n\n" in outputs


def test_run_twice_both_players_win(
    capsys: pytest.CaptureFixture[str], game: TicTacToe
) -> None:
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

    # Check that all the standard game messages were shown
    for msg in GAME_MSGS:
        assert msg in outputs

    # # Check that the end board was shown correctly during the game
    assert " X | 8 | 9\n-----------\n O | X | O\n-----------\n X | O | X\n\n" in outputs
    assert " X | O | 9\n-----------\n O | O | X\n-----------\n X | O | 3\n\n" in outputs

    # Check that the game ended with a win
    assert "\t***** Player 'X', you win! *****\n\n" in outputs
    assert "\t***** Player 'O', you win! *****\n\n" in outputs
