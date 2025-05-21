import ChessBoard as cb

def minmax(boardstate, white_to_play):
    board = cb.ChessBoard(boardstate, white_to_play)
    available_states_1 = board.available_board_states()
    best_opposing_moves = {}
    for index, state_1 in enumerate(available_states_1):
        board.set_board_state(state_1[0])
        board.white_to_move = not white_to_play
        available_states_2 = board.available_board_states()
        states_results = {}
        for state_2 in available_states_2:
            board.set_board_state(state_2[0])
            board.white_to_move = white_to_play
            states_results[state_2[0]] = board.material_values
        best_moves = sorted(states_results.items(), key=lambda x: x[1], reverse=True)
        best_opposing_moves[state_1] = best_moves[0]
        print(f'{index}/{len(available_states_1)}')
    best_opposing_moves = sorted(best_opposing_moves.items(), key=lambda x: x[1])
    print(best_opposing_moves)

board = cb.ChessBoard()
minmax(board.board_state(), board.white_to_move)



