import argparse

from tic_tac_toe import tic_tac_toe_cli, tic_tac_toe_ui


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--cli", action="store_true", help="run the cli version of tictactoe"
    )
    args = parser.parse_args()
    game = tic_tac_toe_cli if args.cli else tic_tac_toe_ui
    game.TicTacToe().run()


if __name__ == "__main__":
    main()
