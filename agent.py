from game import Game
from ChessBoard import GameBoard, ChessBoard
from Pieces import *
import time
import random


def score_board_state(board_state, white_to_move):
    new_board = ChessBoard(board_state, white_to_move)
    if new_board.check_checkmate(not white_to_move):
        return 9999
    if new_board.check_checkmate(white_to_move):
        return -9999
    else:
        return new_board.current_value()


def generate_move_tree(game_parameter, depth):
    # checkmate_moves = game_parameter.mate_in(game_parameter.board, depth, game_parameter.board.white_to_move)
    # if checkmate_moves is not False:
    #     return checkmate_moves
    print("NO CHECKMATE")
    return populate_dict(game_parameter.board.board_state(), game_parameter.board.white_to_move, depth, depth)


def populate_dict(initial_board_state, initial_white_to_move, depth, highest_depth, use_preferred_pieces=False):
    if depth == 0:
        return score_board_state(initial_board_state, initial_white_to_move)
    dict_to_populate = {}
    new_board = ChessBoard(initial_board_state, initial_white_to_move)
    if use_preferred_pieces:
        board_states = new_board.available_board_states(
            prefer_pieces=[new_board.find_pieces(initial_white_to_move, piece_type) for piece_type in
                           [Frog, Dog, Blob0, Blob1, Blob2, Blob3, King, Panda, Rook, Chicken]])
    else:
        board_states = new_board.available_board_states()
    for index, (board_state, move) in enumerate(board_states):
        if depth == highest_depth:
            print(f"{index + 1}/{len(board_states)}")
        dict_to_populate[move] = populate_dict(board_state, not initial_white_to_move, depth - 1, highest_depth, True)
    del new_board
    if len(dict_to_populate) == 0:
        return score_board_state(initial_board_state, initial_white_to_move)
    return dict_to_populate


# THIS CODE WAS WRITTEN BY CHATGPT
# I HAVE NO IDEA IF IT WILL WORK
def minimax(node, depth, maximizing_player):
    if depth == 0 or not isinstance(node, dict):
        return (node, [])

    if maximizing_player:
        best_value = -float("inf")
        best_moves = []
        for move, child_node in node.items():
            child_value, child_moves = minimax(child_node, depth - 1, False)
            if child_value > best_value:
                best_value = child_value
                best_moves = [move] + child_moves
            elif child_value == best_value:
                best_moves += [move] + child_moves
        random.shuffle(best_moves)
        return (best_value, best_moves)
    else:
        best_value = float("inf")
        best_moves = []
        for move, child_node in node.items():
            child_value, child_moves = minimax(child_node, depth - 1, True)
            if child_value < best_value:
                best_value = child_value
                best_moves = [move] + child_moves
            elif child_value == best_value:
                best_moves += [move] + child_moves
        random.shuffle(best_moves)
        return (best_value, best_moves)


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


frog_takes_knight = f"K{' ' * 30}f{' ' * 19}D{' ' * 47}k"

board = GameBoard(random_board_state(95))
game = Game(board)

starting_time = time.time()

print("Populating Dictionary")

move_dict = generate_move_tree(game, 4)

print(f"Process took {time.time() - starting_time} seconds")

value, moves = minimax(move_dict, 5, True)
move = random.choice(moves)

print("After:")

print(f"{move[0]}->{move[1]}")

print(f"The score is {value}")

while "Forever":
    game.play_turn()
