import math
import pygame

from ChessBoard import *


class Game:
    """
    The Game class is the class which interacts with the GameBoard object.
    It implements the pygame library to allow the user to play the game with an interactive GUI
    """

    def __init__(self, board):
        pygame.init()

        WIDTH = 600
        HEIGHT = 600

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))

        pygame.display.flip()
        pygame.display.set_caption("Chess+")

        self.board = board
        self.board.update_board()
        pygame.display.update()

        self.start_square = None
        self.mate_depth = 1
        self.undo_enabled = True

        self.arrows = []
        self.highlighted_squares = []

    def playTurn(self, flipped=False):
        """
        The playTurn method uses the pygame library to listen for events.
        When an event matches the MOUSEBUTTONDOWN id, the game registers the location of the mouse click.
        This can then be translated to a position on the board, at which point calculations are made to determine:
        - If the position clicked is a piece
        - If the piece is the same colour as the player who's turn it is to move
        - If not a piece, is the square one of the legal moves of the selected piece

        Once this has been determined, the function calls the appropriate method within the GameBoard object.

        I also use an event with id 771 for debugging purposes: Pressing almost any key on the keyboard calls this event,
        so I use to for printing values or variables that I'd like to know as the game is running.

        The playTurn method runs once for each turn, and returns None unless there is a victor,
        in which case it return the victor.
        """
        flipped = self.board.flipped
        while "I have literally no intention of ever exiting this loop without a return statement.":
            event = pygame.event.wait()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                column, row = math.trunc(x / 60), math.trunc(y / 60)
                if flipped:
                    column, row = 9 - column, 9 - row
                clickedSquare = self.board.square_in_position((row, column))
                if event.button == 1:
                    self.highlighted_squares = []
                    self.arrows = []
                    self.board.update_board()
                    if self.board.selected_piece is not None and (row, column) not in self.board.current_legal_moves:
                        self.board.unselectPiece()
                    elif self.board.selected_piece is not None and (
                            row, column) in self.board.current_legal_moves and self.board.forced_move is None:
                        square = self.board.square_in_position((row, column))
                        self.board.move_piece(self.board.selected_piece.position, (row, column))
                        self.board.pieceSelected = None
                        return
                    elif self.board.selected_piece is not None and (
                            row, column) in self.board.current_legal_moves and self.board.forced_move is not None:
                        self.board.double_move_piece(self.board.selected_piece.position, (row, column))
                        self.board.white_to_move = not self.board.white_to_move
                        self.board.update_board()
                        return
                    elif self.board.selected_piece is None and clickedSquare is not None:
                        self.board.selectPiece((row, column))
                elif event.button == 3:
                    self.start_square = (column, row)
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 3:
                x, y = pygame.mouse.get_pos()
                column, row = math.trunc(x / 60), math.trunc(y / 60)
                if flipped:
                    column, row = 9 - column, 9 - row
                clickedSquare = self.board.square_in_position((row, column))
                if self.start_square is not None and self.start_square != (column, row):
                    if (self.start_square, (column, row)) not in self.arrows:
                        self.arrows.append((self.start_square, (column, row)))
                        self.draw_arrow(Game.position_to_pixels(self.start_square),
                                        Game.position_to_pixels((column, row)),
                                        flipped=flipped)
                    else:
                        self.arrows.remove((self.start_square, (column, row)))
                        self.board.update_board(False)
                        self.board.place_png("highlighted.png", self.highlighted_squares)
                        for arrow in self.arrows:
                            self.draw_arrow(Game.position_to_pixels(arrow[0]), Game.position_to_pixels(arrow[1]),
                                            flipped=flipped, update_display=False)
                        pygame.display.update()
                elif self.start_square is not None:
                    if (column, row) not in self.highlighted_squares:
                        self.start_square = None
                        self.board.place_png('highlighted.png', [(row, column)])
                        self.highlighted_squares.append((column, row))
                        pygame.display.update()
                    else:
                        self.highlighted_squares.remove((column, row))
                        self.board.update_board(False)
                        self.board.place_png("highlighted.png", self.highlighted_squares)
                        for arrow in self.arrows:
                            self.draw_arrow(Game.position_to_pixels(arrow[0]), Game.position_to_pixels(arrow[1]),
                                            flipped=flipped, update_display=False)
                        pygame.display.update()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if not self.undo_enabled:
                        print("Undo Disabled")
                    else:
                        try:
                            self.board.undo_move()
                        except IndexError:
                            self.board.moves = []
                            self.board.lastMovesSquares = []
                            self.board.update_board()
                elif event.key == pygame.K_SPACE:
                    print(f"Finding Mate in {self.mate_depth}...")
                    try:
                        mate_tuple = self.mate_in(self.board, self.mate_depth, self.board.white_to_move,
                                                  prefer_pieces=[self.board.selected_piece])
                        if mate_tuple is False:
                            print(
                                f"No Mate in {self.mate_depth} for {'white' if self.board.white_to_move else 'black'}")
                        else:
                            moves_for_mate, mate_in_number = mate_tuple
                            print(f"Mate in {mate_in_number} for {'white' if self.board.white_to_move else 'black'}, "
                                  f"starting with {moves_for_mate[0]}")
                            self.mate_depth = mate_in_number
                            starting_position, ending_position = \
                                Game.position_to_pixels(moves_for_mate[0][0], invert=True), \
                                Game.position_to_pixels(moves_for_mate[0][1], invert=True)
                            self.draw_arrow(starting_position, ending_position, (52, 110, 235))
                    except KeyboardInterrupt:
                        print("Finding Mate Interrupted. Press CTRL + C again to exit the program.")
            elif event.type == pygame.QUIT:
                pygame.quit()
                quit()

    def draw_arrow(self, start_pos, end_pos, colour=(252, 186, 3), thickness=10, arrow_size=-30, flipped=False,
                   update_display=True):
        """
        Draws an arrow between two pixel positions on the given Pygame screen.
        """
        if flipped:
            start_pos, end_pos = (600 - start_pos[0], 600 - start_pos[1]), (600 - end_pos[0], 600 - end_pos[1])
        dx = end_pos[0] - start_pos[0]
        dy = end_pos[1] - start_pos[1]
        angle = math.atan2(dy, dx)

        # draw the arrow line
        line_length = math.hypot(dx, dy)
        end_offset = thickness / 2  # offset to adjust for line thickness
        start_offset = (thickness) / 2  # offset to adjust for line thickness
        pygame.draw.line(self.screen, colour, (start_pos[0] + start_offset * math.cos(angle),
                                               start_pos[1] + start_offset * math.sin(angle)),
                         (end_pos[0] - end_offset * math.cos(angle),
                          end_pos[1] - end_offset * math.sin(angle)),
                         thickness)

        # draw the arrowhead
        arrowhead_end = (end_pos[0] - (end_offset - 10) * math.cos(angle),
                         end_pos[1] - (end_offset - 10) * math.sin(angle))
        arrowhead_left = (arrowhead_end[0] + arrow_size * math.cos(angle + math.pi / 3),
                          arrowhead_end[1] + arrow_size * math.sin(angle + math.pi / 3))
        arrowhead_right = (arrowhead_end[0] + arrow_size * math.cos(angle - math.pi / 3),
                           arrowhead_end[1] + arrow_size * math.sin(angle - math.pi / 3))
        pygame.draw.polygon(self.screen, colour, [arrowhead_end, arrowhead_left, arrowhead_right])
        self.start_square = None
        if update_display:
            pygame.display.update()

    def mate_in(self, board, depth, whiteToWin, prefer_pieces=None):
        if depth == 0:
            return False
        if board.white_to_move == whiteToWin:
            board_states = board.available_board_states(prefer_pieces=prefer_pieces)
            for index, boardState in enumerate(board_states):
                if self.mate_depth == depth:
                    print(f"{index}/{len(board_states)}")
                newBoard = ChessBoard(boardState=boardState[0], whiteToMove=not board.white_to_move)
                if newBoard.checkCheckmate(not whiteToWin):
                    del newBoard
                    return [boardState[1]], 1
                elif newBoard.checkCheck(not whiteToWin):
                    recursion_result = self.mate_in(newBoard, depth - 1, whiteToWin=whiteToWin)
                    if recursion_result is not False:
                        moves, inverse_depth = recursion_result
                        del newBoard
                        return [boardState[1]] + moves, inverse_depth + 1
                del newBoard
        else:
            available_moves_for_checkmate = []
            for boardState in board.available_board_states():
                newBoard = ChessBoard(boardState=boardState[0], whiteToMove=whiteToWin)
                recursion_result = self.mate_in(newBoard, depth, whiteToWin)
                del newBoard
                if recursion_result is False:
                    return False
                else:
                    moves, inverse_depth = recursion_result
                    available_moves_for_checkmate.append(moves)
            return random.choice(available_moves_for_checkmate), inverse_depth
        return False

    @staticmethod
    def position_to_pixels(position, invert=False):
        if invert:
            col, row = position
        else:
            row, col = position
        row = row * 60 + 30
        col = col * 60 + 30
        return row, col


class CompetitiveGame(Game):
    def __init__(self, board):
        super().__init__(board)
        self.undo_enabled = False

    def playTurn(self, flipped=False):
        starting_move = self.board.white_to_move
        super().playTurn(flipped=self.board.flipped)
        if starting_move is not self.board.white_to_move and self.board.victor is None:
            self.board.flip()
            self.board.update_board()
            pygame.display.update()
        elif self.board.victor is not None:
            self.board.displayVictory(
                True if self.board.victor == "White" else False if self.board.victor == "Black" else None)

    def mate_in(self, board, depth, whiteToWin):
        print(f"Calculating Mates is disabled in competitive mode.")
        return False
