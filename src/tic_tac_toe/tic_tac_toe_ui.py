import abc
import dataclasses
import enum

import pygame as pg

import tic_tac_toe

WIN_SIZE = WIDTH, HEIGHT = pg.Vector2(650)
TILE_SIZE = WIN_SIZE // 3
MARK_SIZE = WIN_SIZE // 4
MARK_PADDING = (TILE_SIZE - MARK_SIZE) // 2

BOARD_IMG = pg.transform.scale(pg.image.load("assets/graphics/board.png"), WIN_SIZE)
X_SYMBOL = pg.transform.scale(pg.image.load("assets/graphics/board_x.png"), MARK_SIZE)
O_SYMBOL = pg.transform.scale(pg.image.load("assets/graphics/board_o.png"), MARK_SIZE)


def render_txt(text: str) -> pg.Surface:
    return pg.font.Font(None, 50).render(text, True, "Black", "White")


class State(enum.Enum):
    """Enum for the Game's State Machine"""

    game_play = "game_play"  # Players are still making moves
    check_game_over = "check_game_over"
    game_ended = "game_ended"  # Rendering the game ended screen


class Board(tic_tac_toe.Board):
    def __init__(self, screen: pg.Surface) -> None:
        super().__init__()
        self.screen = screen

    def show(self) -> None:
        self.screen.blit(BOARD_IMG, (0, 0))

        for row in range(self.ROWS):
            for col in range(self.COLS):
                mark_pos = self.get_mark_pos_from_row_col(row, col)

                if self.board[row][col] == "X":
                    self.screen.blit(X_SYMBOL, mark_pos)
                elif self.board[row][col] == "O":
                    self.screen.blit(O_SYMBOL, mark_pos)

    def get_mark_pos_from_row_col(self, row: int, col: int) -> tuple[float, float]:
        return (
            TILE_SIZE[0] * col + MARK_PADDING[0],
            TILE_SIZE[1] * row + MARK_PADDING[1],
        )

    def get_row_col_from_mouse(self, mouse_pos: tuple[int, int]) -> tuple[int, int]:
        posy, posx = mouse_pos
        return int(posx // TILE_SIZE[0]), int(posy // TILE_SIZE[1])


@dataclasses.dataclass
class GameState(abc.ABC):
    screen: pg.Surface
    board: Board
    next_state: State

    def handle_events(self) -> None:
        for event in pg.event.get():
            if (
                event.type == pg.QUIT
                or (pg.key.get_mods() & pg.KMOD_CTRL)
                and event.key == pg.K_w
            ):
                pg.quit
                exit()
            self.handle_event(event)

    @abc.abstractmethod
    def handle_event(self, event: pg.event.Event) -> None:
        """Handle an individual event"""

    @abc.abstractmethod
    def update(self) -> None:
        """Update the state"""

    @abc.abstractmethod
    def draw(self) -> None:
        """Draw requirements"""


@dataclasses.dataclass
class Move(GameState):
    next_state: State = State.game_play
    row, col = -1, -1

    def handle_event(self, event: pg.event.Event) -> None:
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            self.row, self.col = self.board.get_row_col_from_mouse(pg.mouse.get_pos())

    def update(self) -> None:
        try:
            self.board.insert_mark(self.row, self.col)
        except ValueError:
            self.next_state = State.game_play
        else:
            self.row, self.col = -1, -1
            self.next_state = State.check_game_over

    def draw(self) -> None:
        self.board.show()


@dataclasses.dataclass
class CheckGameOver(GameState):
    next_state: State = State.check_game_over
    msg: str = ""

    def handle_event(self, event: pg.event.Event) -> None:
        return

    def update(self) -> None:
        if (win := self.board.check_win()) or self.board.check_tie():
            self.next_state = State.game_ended
            self.msg = f"Player '{self.board.mark}', you win!" if win else "It's a tie"
        else:
            self.next_state = State.game_play
        self.board.change_player()

    def draw(self) -> None:
        if self.msg:
            self.board.show()
            rendered_msg = render_txt(f"***** {self.msg} *****")
            self.screen.blit(rendered_msg, rendered_msg.get_rect(center=WIN_SIZE // 2))
            self.msg = ""


@dataclasses.dataclass
class CheckGameEnded(GameState):
    next_state: State = State.game_ended
    play_again: bool = False

    def handle_event(self, event: pg.event.Event) -> None:
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            self.play_again = True

    def update(self) -> None:
        if self.play_again:
            self.play_again = False
            self.board.clean()
            self.next_state = State.game_play
        else:
            self.next_state = State.game_ended

    def draw(self) -> None:
        msg = render_txt("Click to play again!")
        self.screen.blit(
            msg, msg.get_rect(midtop=(WIN_SIZE + (0, msg.get_height())) // 2)
        )


class TicTacToe:
    def __init__(self) -> None:
        pg.init()
        pg.display.set_caption("Tic-Tac-Toe")

        self.screen = pg.display.set_mode(WIN_SIZE)
        self.board = Board(self.screen)

        self.states = {
            State.game_play: Move(self.screen, self.board),
            State.check_game_over: CheckGameOver(self.screen, self.board),
            State.game_ended: CheckGameEnded(self.screen, self.board),
        }
        self.game_state = self.states[State.game_play]

    def run(self) -> None:
        self.board.show()
        while True:
            self.game_state = self.states[self.game_state.next_state]
            self.game_state.handle_events()
            self.game_state.update()
            self.game_state.draw()
            pg.display.update()


if __name__ == "__main__":
    game = TicTacToe()
    game.run()
