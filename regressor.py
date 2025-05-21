import ChessBoard as cb


def minmax(boardstate, white_to_play, depth):
    board = cb.ChessBoard(boardstate, white_to_play)
    available_states = board.available_board_states()
    state_values = {}

    if depth <= 1:
        for state in available_states:
            board.set_board_state(state[0])
            material_value = board.material_values
            state_values[state[0]] = material_value
        state_values = sorted(state_values.items(), key=lambda x: x[1], reverse=not white_to_play)
        return state_values[0]

    for state in available_states:
        lower = minmax(state[0], not white_to_play, depth - 1)
        state_values[state[0]] = lower[1]
    state_values = sorted(state_values.items(), key=lambda x: x[1], reverse=not white_to_play)
    if depth % 2 == 0: state_values = state_values[0:int(len(state_values)/4)] # TODO: check that not all values are the same before split
    return state_values[0]


board = cb.ChessBoard()
out = minmax(board.board_state(), board.white_to_move, 4)

print(out)

