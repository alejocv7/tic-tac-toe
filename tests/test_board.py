import typing

import pytest

from tic_tac_toe import Board

ROWS = Board.ROWS
COLS = Board.COLS


@pytest.fixture
def board() -> Board:
    return Board()


@pytest.fixture(params=((row, col) for col in range(COLS) for row in range(ROWS)))
def valid_row_col(request: pytest.FixtureRequest) -> typing.Any:
    return request.param


def test_is_valid_row_col(board: Board, valid_row_col: tuple[int, int]) -> None:
    """Test that is_valid_row_col returns True for an empty and in-range spot"""
    assert board.is_valid_row_col(*valid_row_col)


def test_is_valid_row_col_ocupied(board: Board, valid_row_col: tuple[int, int]) -> None:
    """Test that is_valid_row_col returns False for an occupied spot"""
    row, col = valid_row_col
    board.board[row][col] = "X"
    assert not board.is_valid_row_col(row, col)


@pytest.fixture(
    params=[(-1, -1), (ROWS * 10, COLS), (ROWS, COLS * 10), (ROWS * 10, COLS * 10)]
)
def invalid_row_col(request: pytest.FixtureRequest) -> typing.Any:
    return request.param


def test_is_valid_row_col_out_of_range(
    board: Board, invalid_row_col: tuple[int, int]
) -> None:
    """Test that is_valid_row_col returns False for an out of range row, col"""
    assert not board.is_valid_row_col(*invalid_row_col)


def test_insert_mark_valid(board: Board, valid_row_col: tuple[int, int]) -> None:
    """Test that a mark can be inserted (no expection raised) when the input
    is in range and not on an occupied spot
    """
    board.insert_mark("X", *valid_row_col)


def test_insert_mark_invalid(board: Board, invalid_row_col: tuple[int, int]) -> None:
    """Test that insert_mark raises an exepction when the input is outside the range"""
    with pytest.raises(ValueError):
        board.insert_mark("X", *invalid_row_col)


class TestBoardChecks:
    WINNING_BOARDS = [
        # fmt: off
        # Horizontal wins
        [["X", "X", "X"],
         ["O", "O", "6"],
         ["1", "2", "3"]],

        [["O", "8", "9"],
         ["X", "X", "X"],
         ["O", "2", "3"]],

        [["7", "8", "9"],
         ["O", "O", "O"],
         ["X", "X", "X"]],

        # Vertical wins
        [["O", "X", "9"],
         ["O", "X", "6"],
         ["O", "2", "3"]],

        [["7", "O", "X"],
         ["4", "O", "X"],
         ["1", "O", "3"]],

        [["X", "8", "O"],
         ["X", "5", "O"],
         ["1", "2", "O"]],

        # Diagonal wins
        [["X", "8", "9"],
         ["4", "X", "6"],
         ["1", "2", "X"]],

        [["O", "8", "X"],
         ["4", "O", "6"],
         ["X", "2", "O"]],
        # fmt: on
    ]

    TIE_BOARDS = [
        # fmt: off
        [["X", "O", "X"],
         ["O", "X", "O"],
         ["O", "X", "O"]],

        [["X", "O", "X"],
         ["O", "O", "X"],
         ["X", "X", "O"]],
        # fmt: on
    ]

    IN_PLAY_BOARDS = [
        [["7", "8", "9"], ["4", "5", "6"], ["1", "2", "3"]],
        [["7", "8", "O"], ["4", "5", "6"], ["X", "2", "3"]],
        [["X", "8", "9"], ["4", "O", "6"], ["1", "X", "3"]],
    ]

    @pytest.fixture
    def adapted_board(self, request: pytest.FixtureRequest, board: Board) -> Board:
        board.board = request.param
        return board

    @pytest.mark.parametrize("adapted_board", WINNING_BOARDS, indirect=True)
    def test_check_win_with_winner(self, adapted_board: Board) -> None:
        """Test that check_win returns True when there is a winner"""
        assert adapted_board.check_win()

    @pytest.mark.parametrize(
        "adapted_board", TIE_BOARDS + IN_PLAY_BOARDS, indirect=True
    )
    def test_check_win_no_winner(self, adapted_board: Board) -> None:
        """Test that check_win returns False if there are no winners"""
        assert not adapted_board.check_win()

    @pytest.mark.parametrize("adapted_board", TIE_BOARDS, indirect=True)
    def test_check_tie_with_tie(self, adapted_board: Board) -> None:
        """Test that check_tie returns True with boards containing a tie"""
        assert adapted_board.check_tie()

    @pytest.mark.parametrize(
        "adapted_board", WINNING_BOARDS + IN_PLAY_BOARDS, indirect=True
    )
    def test_check_tie_no_tie(self, adapted_board: Board) -> None:
        """Test that check_tie returns False with boards that don't have a tie"""
        assert not adapted_board.check_tie()
