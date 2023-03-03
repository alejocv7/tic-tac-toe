import textwrap
import typing
import unittest.mock

import pytest

from tic_tac_toe import TicTacToe

BOARD_LEN = len(TicTacToe.STARTING_BOARD)


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
def test_print_board(
    capsys: pytest.CaptureFixture[str], game: TicTacToe, board: list[str], expected: str
) -> None:
    """Test that the printed board is well formatted"""
    game.board = board
    game.print_board()
    assert capsys.readouterr().out == expected


@pytest.mark.parametrize("curr_mark, next_mark", [("X", "O"), ("O", "X")])
def test_change_player(game: TicTacToe, curr_mark: str, next_mark: str) -> None:
    """Test that the change_player function correctly gives the next player"""
    game.player = curr_mark
    game.change_player()
    assert game.player == next_mark


@pytest.fixture(params=(n + 1 for n in range(BOARD_LEN)))
def valid_move(request: pytest.FixtureRequest) -> typing.Any:
    return request.param


def test_is_valid(game: TicTacToe, valid_move: int) -> None:
    """Test that an user trying to make a move on an empty spot is valid"""
    assert game.is_valid_move(valid_move)


def test_is_valid_not_valid(game: TicTacToe, valid_move: int) -> None:
    """Test that an user trying to make a move on an already marked spot is invalid"""
    game.board[valid_move - 1] = "X"
    assert not game.is_valid_move(valid_move)


def test_get_next_player_move_with_spot_taken(game: TicTacToe, valid_move: int) -> None:
    """Test that an user trying to make a move on an already marked spot is invalid"""
    free_spot = (valid_move % BOARD_LEN) + 1
    game.board[valid_move - 1] = "X"
    with unittest.mock.patch("builtins.input", side_effect=[valid_move, free_spot]):
        assert game.get_next_player_move() == free_spot - 1


def test_get_next_player_move_all_valid_moves(game: TicTacToe, valid_move: int) -> None:
    """Test that get_next_player_move returns the correct board idx = (move - 1)"""
    with unittest.mock.patch("builtins.input", return_value=str(valid_move)):
        assert game.get_next_player_move() == valid_move - 1


def test_get_next_player_move_wrong_inputs_first(game: TicTacToe) -> None:
    """Test that get_next_player_move constantly prompts the user for a valid input.
    When the input is valid the returned value should be a board idx = (input - 1)"""
    moves = [str(n) for n in range(0, 50, 10)]
    moves += ["1.1", "x", "", "$", "9"]
    with unittest.mock.patch("builtins.input", side_effect=moves):
        assert game.get_next_player_move() == int(moves[-1]) - 1


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


class TestBoardChecks:
    WINNING_BOARDS = [
        # fmt: off
        # Horizontal wins
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
        # fmt: on
    ]

    TIE_BOARDS = [
        # fmt: off
        ["X", "O", "X",
         "O", "X", "O",
         "O", "X", "O"],

        ["X", "O", "X",
         "O", "O", "X",
         "X", "X", "O"],
        # fmt: on
    ]

    IN_PLAY_BOARDS = [
        ["7", "8", "9", "4", "5", "6", "1", "2", "3"],
        ["7", "8", "O", "4", "5", "6", "X", "2", "3"],
        ["X", "8", "9", "4", "O", "6", "1", "X", "3"],
    ]

    @pytest.fixture
    def game_with_adapted_board(
        self, request: pytest.FixtureRequest, game: TicTacToe
    ) -> TicTacToe:
        game.board = request.param
        return game

    @pytest.mark.parametrize("game_with_adapted_board", WINNING_BOARDS, indirect=True)
    def test_check_win_with_winner(self, game_with_adapted_board: TicTacToe) -> None:
        """Test that check_win returns True when there is a winner"""
        assert game_with_adapted_board.check_win()

    @pytest.mark.parametrize(
        "game_with_adapted_board", TIE_BOARDS + IN_PLAY_BOARDS, indirect=True
    )
    def test_check_win_no_winner(self, game_with_adapted_board: TicTacToe) -> None:
        """Test that check_win returns False if there are no winners"""
        assert not game_with_adapted_board.check_win()

    @pytest.mark.parametrize("game_with_adapted_board", TIE_BOARDS, indirect=True)
    def test_check_tie_with_tie(self, game_with_adapted_board: TicTacToe) -> None:
        """Test that check_tie returns True with boards containing a tie"""
        assert game_with_adapted_board.check_tie()

    @pytest.mark.parametrize(
        "game_with_adapted_board", WINNING_BOARDS + IN_PLAY_BOARDS, indirect=True
    )
    def test_check_tie_no_tie(self, game_with_adapted_board: TicTacToe) -> None:
        """Test that check_tie returns False with boards that don't have a tie"""
        assert not game_with_adapted_board.check_tie()


# ------ Teting gull game-run ------

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

    # Check that the game ended with a win
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
