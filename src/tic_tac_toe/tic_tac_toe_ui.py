import pygame as pg

import tic_tac_toe


class TicTacToe(tic_tac_toe.TicTacToe):
    ROW_CNT, COL_CNT = 3, 3
    WIN_SIZE = WIDTH, HEIGHT = pg.Vector2(650)
    TILE_SIZE = WIN_SIZE // 3
    MARK_SIZE = WIN_SIZE // 4
    MARK_PADDING = (TILE_SIZE - MARK_SIZE) // 2

    def __init__(self) -> None:
        super().__init__()

        pg.init()
        pg.display.set_caption("Tic-Tac-Toe")
        self.screen = pg.display.set_mode(self.WIN_SIZE)
        self.FONT = pg.font.Font(None, 50)

        self.board_surface = pg.transform.scale(
            pg.image.load("assets/graphics/board.png"), self.WIN_SIZE
        )
        self.player_x = pg.transform.scale(
            pg.image.load("assets/graphics/board_x.png"),
            self.MARK_SIZE,
        )
        self.player_o = pg.transform.scale(
            pg.image.load("assets/graphics/board_o.png"),
            self.MARK_SIZE,
        )

        self.running = True

    def get_rendered_txt(self, text: str) -> pg.Surface:
        return self.FONT.render(text, True, "Black", "White")

    def get_mark_pos_from_row_col(self, row: int, col: int) -> tuple[float, float]:
        return (
            self.TILE_SIZE[0] * col + self.MARK_PADDING[0],
            self.TILE_SIZE[1] * row + self.MARK_PADDING[1],
        )

    def get_row_col_from_mouse(self, mouse_pos: tuple[int, int]) -> tuple[int, int]:
        posx, posy = mouse_pos
        return (
            int(posy // self.TILE_SIZE[0]),
            int(posx // self.TILE_SIZE[1]),
        )

    def print_board(self) -> None:
        self.screen.blit(self.board_surface, (0, 0))

        for row in range(self.ROW_CNT):
            for col in range(self.COL_CNT):
                mark_pos = self.get_mark_pos_from_row_col(row, col)

                if self.board[row][col] == "X":
                    self.screen.blit(self.player_x, mark_pos)
                elif self.board[row][col] == "O":
                    self.screen.blit(self.player_o, mark_pos)

    def get_next_player_move(self) -> tuple[int, int]:
        row, col = self.get_row_col_from_mouse(pg.mouse.get_pos())
        if self.is_valid_idx(row, col):
            return row, col
        return -1, -1

    def should_play_again(self) -> bool:
        msg = self.get_rendered_txt("Press space or click to play again!")
        self.screen.blit(
            msg, msg.get_rect(midtop=(self.WIN_SIZE + (0, msg.get_height())) // 2)
        )
        return pg.key.get_pressed()[pg.K_SPACE] or pg.mouse.get_pressed()

    def draw(self) -> None:
        self.print_board()
        pg.display.update()

    def run(self) -> None:
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT or (
                    (pg.key.get_mods() & pg.KMOD_CTRL) and event.key == pg.K_w
                ):
                    pg.quit()
                    exit()

                if self.running:
                    self.print_board()
                    if event.type == pg.MOUSEBUTTONDOWN:
                        player_move = self.get_next_player_move()
                        if player_move == (-1, -1):
                            continue

                        row, col = player_move
                        self.board[row][col] = self.player

                        if self.check_win() or (tie := self.check_tie()):
                            self.running = False
                            self.print_board()

                            msg = (
                                "It's a tie!"
                                if tie
                                else f"Player '{self.player}', you win!"
                            )
                            msg_surface = self.get_rendered_txt(f"***** {msg} *****")
                            self.screen.blit(
                                msg_surface,
                                msg_surface.get_rect(center=self.WIN_SIZE // 2),
                            )
                        self.change_player()

                elif self.should_play_again():
                    self.running = True
                    self.board = self.get_clean_board()

            pg.display.update()


if __name__ == "__main__":
    game = TicTacToe()
    game.run()
