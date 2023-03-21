import enum
from typing import Literal

import pygame as pg

import tic_tac_toe

WIN_SIZE = WIDTH, HEIGHT = pg.Vector2(650)
TILE_SIZE = WIN_SIZE // 3
MARK_SIZE = WIN_SIZE // 4
MARK_PADDING = (TILE_SIZE - MARK_SIZE) // 2

BOARD_IMG = pg.transform.scale(pg.image.load("assets/graphics/board.png"), WIN_SIZE)
X_SYMBOL = pg.transform.scale(pg.image.load("assets/graphics/board_x.png"), MARK_SIZE)
O_SYMBOL = pg.transform.scale(pg.image.load("assets/graphics/board_o.png"), MARK_SIZE)


class State(enum.Enum):
    """Enum for the Game's State Machine"""

    initialized = "initialized"  # Pygame is configured, images are loaded, etc
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


class TicTacToe:
    def __init__(self) -> None:
        pg.init()
        pg.display.set_caption("Tic-Tac-Toe")

        self.screen = pg.display.set_mode(WIN_SIZE)
        self.player: Literal["X", "O"] = "X"
        self.board = Board(self.screen)
        self.FONT = pg.font.Font(None, 50)
        self.state = State.initialized

    def run(self) -> None:
        self.board.show()
        self.state = State.game_play

        while True:
            for event in pg.event.get():
                if (
                    event.type == pg.QUIT
                    or (pg.key.get_mods() & pg.KMOD_CTRL)
                    and event.key == pg.K_w
                ):
                    pg.quit()
                    exit()

                if self.state == State.game_play:
                    self.handle_player_move_event(event)
                elif self.state == State.check_game_over:
                    self.handle_game_over_check()
                    self.change_player()
                elif self.state == State.game_ended:
                    self.handle_game_over(event)

            pg.display.update()

    def handle_player_move_event(self, event: pg.event.Event) -> None:
        if event.type == pg.MOUSEBUTTONDOWN:
            row, col = self.board.get_row_col_from_mouse(pg.mouse.get_pos())
            try:
                self.board.insert_mark(self.player, row, col)
            except ValueError:
                # This happens if the spot is occupied or row/col are out of bounds.
                # For the most part, row/col should be inside the game screen, since
                # that is how clicks are registered. But, for whatever reason, sometimes
                # pygame adds a clickable frame causing the input to be out of bounds
                return
            self.state = State.check_game_over
            self.board.show()

    def handle_game_over_check(self) -> None:
        if (win := self.board.check_win()) or self.board.check_tie():
            self.state = State.game_ended
            self.board.show()

            msg = f"Player '{self.player}', you win!" if win else "It's a tie"
            msg_surface = self.render_txt(f"***** {msg} *****")
            self.screen.blit(msg_surface, msg_surface.get_rect(center=WIN_SIZE // 2))
        else:
            self.state = State.game_play

    def handle_game_over(self, event: pg.event.Event) -> None:
        msg = self.render_txt("Press space or click to play again!")
        self.screen.blit(
            msg, msg.get_rect(midtop=(WIN_SIZE + (0, msg.get_height())) // 2)
        )

        if event.type == pg.MOUSEBUTTONDOWN:
            self.state = State.game_play
            self.board.clean()
            self.board.show()

    def render_txt(self, text: str) -> pg.Surface:
        return self.FONT.render(text, True, "Black", "White")

    def change_player(self) -> None:
        self.player = "O" if self.player == "X" else "X"


if __name__ == "__main__":
    game = TicTacToe()
    game.run()
