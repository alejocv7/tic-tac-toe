import argparse

parser = argparse.ArgumentParser()
parser.add_argument(
    "--cli", action="store_true", help="run the cli version of tictactoe"
)
args = parser.parse_args()

if args.cli:
    import tic_tac_toe_cli

    game = tic_tac_toe_cli
else:
    import tic_tac_toe_ui

    game = tic_tac_toe_ui

if __name__ == "__main__":
    game.TicTacToe().run()
