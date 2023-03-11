import sys

import pygame

# Constants
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
CELL_SIZE = 200
BOARD_WIDTH = SCREEN_WIDTH // CELL_SIZE
BOARD_HEIGHT = SCREEN_HEIGHT // CELL_SIZE
LINE_WIDTH = 10
FONT_SIZE = 100
TEXT_MARGIN = 10
X_COLOR = (255, 0, 0)
O_COLOR = (0, 0, 255)
TEXT_COLOR = (255, 255, 255)
WAIT_TIME = 1000


class Board:
    def __init__(self):
        self.board = [["" for _ in range(BOARD_WIDTH)] for _ in range(BOARD_HEIGHT)]
        self.current_player = "X"

    def make_move(self, row, col):
        if self.board[row][col] == "":
            self.board[row][col] = self.current_player
            self.current_player = "O" if self.current_player == "X" else "X"
            return True
        else:
            return False

    def check_win(self):
        for row in range(BOARD_HEIGHT):
            if self.board[row][0] == self.board[row][1] == self.board[row][2] != "":
                return self.board[row][0]
        for col in range(BOARD_WIDTH):
            if self.board[0][col] == self.board[1][col] == self.board[2][col] != "":
                return self.board[0][col]
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != "":
            return self.board[0][0]
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != "":
            return self.board[0][2]
        if all(
            self.board[row][col] != ""
            for row in range(BOARD_HEIGHT)
            for col in range(BOARD_WIDTH)
        ):
            return "Tie"
        return None

    def reset(self):
        self.board = [["" for _ in range(BOARD_WIDTH)] for _ in range(BOARD_HEIGHT)]
        self.current_player = "X"


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Tic Tac Toe")
        self.font = pygame.font.SysFont("Arial", FONT_SIZE)
        self.board = Board()

    def draw_board(self):
        self.screen.fill((0, 0, 0))
        for i in range(1, 3):
            pygame.draw.line(
                self.screen,
                (255, 255, 255),
                (0, CELL_SIZE * i),
                (SCREEN_WIDTH, CELL_SIZE * i),
                LINE_WIDTH,
            )
            pygame.draw.line(
                self.screen,
                (255, 255, 255),
                (CELL_SIZE * i, 0),
                (CELL_SIZE * i, SCREEN_HEIGHT),
                LINE_WIDTH,
            )

    def draw_x(self, row, col):
        pygame.draw.line(
            self.screen,
            X_COLOR,
            (col * CELL_SIZE + TEXT_MARGIN, row * CELL_SIZE + TEXT_MARGIN),
            ((col + 1) * CELL_SIZE - TEXT_MARGIN, (row + 1) * CELL_SIZE - TEXT_MARGIN),
            LINE_WIDTH,
        )
        pygame.draw.line(
            self.screen,
            X_COLOR,
            ((col + 1) * CELL_SIZE - TEXT_MARGIN, row * CELL_SIZE + TEXT_MARGIN),
            (col * CELL_SIZE + TEXT_MARGIN, (row + 1) * CELL_SIZE - TEXT_MARGIN),
            LINE_WIDTH,
        )

    def draw_o(self, row, col):
        pygame.draw.circle(
            self.screen,
            O_COLOR,
            (col * CELL_SIZE + CELL_SIZE // 2, row * CELL_SIZE + CELL_SIZE // 2),
            CELL_SIZE // 2 - TEXT_MARGIN,
            LINE_WIDTH,
        )

    def draw_text(self, text):
        text_surface = self.font.render(text, True, TEXT_COLOR)
        text_rect = text_surface.get_rect(
            center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        )
        self.screen.blit(text_surface, text_rect)

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    row, col = event.pos[1] // CELL_SIZE, event.pos[0] // CELL_SIZE
                    if self.board.make_move(row, col):
                        winner = self.board.check_win()
                        self.draw_board()
                        for row in range(BOARD_HEIGHT):
                            for col in range(BOARD_WIDTH):
                                if self.board.board[row][col] == "X":
                                    self.draw_x(row, col)
                                elif self.board.board[row][col] == "O":
                                    self.draw_o(row, col)
                        if winner is not None:
                            if winner == "Tie":
                                self.draw_text("Tie!")
                            else:
                                self.draw_text(f"{winner} wins!")
                            pygame.display.update()
                            pygame.time.wait(WAIT_TIME)
                            self.board.reset()
                            self.draw_board()
                        else:
                            pygame.display.update()

            pygame.display.update()


if __name__ == "__main__":
    game = Game()
    game.draw_board()
    game.run()
    pygame.quit()
    sys.exit()
