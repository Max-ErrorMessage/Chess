import sys
import pygame.display
from game import Game, CompetitiveGame
from ChessBoard import ChessBoard, GameBoard, DumbBoard
import random
import time as alice

mode = 0
mate_depth = 0

if len(sys.argv) > 1:
    if sys.argv[1][0] == "-":
        # -mode
        mode_string = sys.argv[1][1:]
        if mode_string in ["casual", "cas", "default"]:
            mode = 0
        elif mode_string in ["comp", "competitive"]:
            mode = 1
        elif mode_string in ["silly", "dumb", "stupid"]:
            mode = 2
        else:
            print("Mode not in list, using default")
            mode = 0

    if len(sys.argv) > 2:
        if sys.argv[2][:2] == "--":
            mate_depth = sys.argv[2][2:]


def random_board_state(average_empty_squares=0):
    possible_pieces = "perdbcqkfpihzxvoy"
    possible_pieces += possible_pieces.upper()
    while True:
        board_state = [random.choice(possible_pieces + (" " * average_empty_squares)) for _ in range(100)]
        if (len([char for char in board_state if char == "k"]), len([char for char in board_state if char == "K"])) != (
        1, 1):
            continue
        new_board = ChessBoard(board_state)
        is_check = new_board.check_check(white_in_check=True) or new_board.check_check(white_in_check=False)
        del new_board
        if not is_check:
            return board_state


common_boards = {"Panda End Game":
                    "    KA       PPPP   "
                    "                                                            "
                    "   pppp       ka    ",
                "Chicken Hell":
                    "HHHCKADHHHHHHHHHHHHH"
                    "                    HHHHHHHHHHhhhhhhhhhh                    "
                    "hhhhhhhhhhhhhckadhhh",
                "Chicken Line":
                    "K        h         hhhhhhhhhhhh         hhhhhhhhhh         "
                    "hhhhhhhhhhhh         hhhhhhhh k         r",
                "Back to Basics": "####################RNBQKBNR##PPPPPPPP##        ##        "
                                  "##        ##        ##pppppppp##rnbqkbnr##",
                "I sure do wonder": "k  K      q  Q      k  K",
                "We ball": random_board_state(random.randint(30, 70)),
                "No mate in 1": "R HZAKC DR PP   PPPP      F   P  xP      D  hfc     pdx    "
                                "          h         ppp pppppp r   ak  dr"}

starting_board_state, white_to_move = "RDOZAKCFDRPPPPPPPPPP                                                            pppppppppprdozakcfdr", True

if mode == 0:
    board = GameBoard(starting_board_state, white_to_move)
    game = Game(board)
elif mode == 1:
    board = GameBoard(starting_board_state, white_to_move)
    game = CompetitiveGame(board)
elif mode == 2:
    board = DumbBoard(starting_board_state, white_to_move)
    game = Game(board)
else:
    board = GameBoard()
    game = Game(board)



game.mate_depth = int(mate_depth)

while game.board.victor is None or type(game) == Game:
    game.playTurn()
    if game.board.victor is not None:
        game.board.displayVictory(True if game.board.victor == "White"
                                  else False if game.board.victor == "Black" else None)

game.board.displayVictory(True if game.board.victor == "White" else False if game.board.victor == "Black" else None)
print("Game Over")

while "Never exiting this loop LLLLLL":
    event = pygame.event.wait()
    if event.type == pygame.QUIT:
        pygame.quit()
        quit()
    alice.sleep(3)  # The only purpose of this is to prevent "Python is not responding" pop-up.
    # time.sleep(3) is so the CPU isn't overwhelmed

