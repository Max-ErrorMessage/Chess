import random
import pygame
from Pieces import *


class ChessBoard:
    """
    The ChessBoard class manages the actual Chess+ game, and much of the logic associated with it that is not directly tied
    to the Pieces objects.

    For example, the ChessBoard class:
    - Stores all the pieces
    - Checks for checks
    - Moves pieces
    - Gathers legal moves for pieces
    - Creates a board_state for the board

    The ChessBoard class does not have any GUI methods, so it is best used for calculating chess moves not directly relevant
    to the user.
    """

    def __init__(self,
                 board_state="RDOZAKCFDRPPPPPPPPPP                                                            pppppppppprdozakcfdr",
                 white_to_move=True):
        """
        The constructor takes 2 arguments:
        - white_to_move is a boolean variable which tracks whose turn it is
        - board_state is a String which represents the state of the board,
          such that it is possible to create a board with a different starting position to the standard layout.
        """
        self.white_to_move = white_to_move
        self.selected_piece = None
        self.current_legal_moves = []
        self.victor = None
        self.moves = []
        self.forced_move = None
        self.checked_positions = []
        self.previous_board_states = []
        self.squares = []

        self.set_board_state(board_state)

    def board_state(self):
        """
        The board_state is a 100 character string representing the current board.
        Each piece type has a unique letter.
        Black Pieces are uppercase and White Pieces are lowercase.
        There is a unique letter for pieces like an immortal panda or chicken,
         or a pawn who is enpassantable on the next move.
        """
        board_state = ""
        for row in self.squares:
            for square in row:
                if issubclass(type(square), Piece):
                    board_state += square.as_char()
                else:
                    board_state += " "
        return board_state

    def set_board_state(self, board_state):
        """
        Takes in a board_state as a parameter, and edits the squares such that they match the board_state that is passed in.
        Primarily called during self.__init__()
        """
        self.squares = [[None for j in range(10)] for i in range(10)]
        position = [0, 0]
        for char in board_state:
            if char.lower() == char:
                is_white = True
            else:
                is_white = False

            piece = None
            if char is None:
                pass
            elif char.lower() == "p":
                piece = Pawn(is_white, (position[0], position[1]))
                if (position[0] == 1 and not is_white) or (position[0] == 8 and is_white):
                    piece.has_moved = True
            elif char.lower() == "e":
                piece = Pawn(is_white, (position[0], position[1]))
                piece.is_en_passantable = True
            elif char.lower() == "r":
                piece = Rook(is_white, (position[0], position[1]))
            elif char.lower() == "m":
                piece = Rook(is_white, (position[0], position[1]))
                piece.has_moved = True
            elif char.lower() == "n":
                piece = Knight(is_white, (position[0], position[1]))
            elif char.lower() == "d":
                piece = Dog(is_white, (position[0], position[1]))
            elif char.lower() == "f":
                piece = Frog(is_white, (position[0], position[1]))
            elif char.lower() == "z":
                piece = Blob0(is_white, (position[0], position[1]))
            elif char.lower() == "x":
                piece = Blob1(is_white, (position[0], position[1]))
            elif char.lower() == "v":
                piece = Blob2(is_white, (position[0], position[1]))
            elif char.lower() == "j":
                piece = Blob3(is_white, (position[0], position[1]))
            elif char.lower() == "q":
                piece = Queen(is_white, (position[0], position[1]))
            elif char.lower() == "a":
                piece = Panda(is_white, (position[0], position[1]))
            elif char.lower() == "i":
                piece = Panda(is_white, (position[0], position[1]))
                piece.invulnerable = True
            elif char.lower() == "h":
                piece = Chicken(is_white, (position[0], position[1]))
                piece.has_moved = True
            elif char.lower() == "y":
                piece = Chicken(is_white, (position[0], position[1]))
                piece.invulnerable = True
                piece.has_moved = True
            elif char.lower() == "o":
                piece = Chicken(is_white, (position[0], position[1]))
                piece.has_moved = False
            elif char.lower() == "g":
                piece = Egg(is_white, (position[0], position[1]))
            elif char.lower() == "b":
                piece = Bishop(is_white, (position[0], position[1]))
            elif char.lower() == "c":
                piece = Cleric(is_white, (position[0], position[1]))
            elif char.lower() == "k":
                piece = King(is_white, (position[0], position[1]))
            elif char == "(":
                piece = King(True, (position[0], position[1]))
                piece.has_moved = True
            elif char == ")":
                piece = King(False, (position[0], position[1]))
                piece.has_moved = True
            elif char.lower() == "q":
                piece = Dog(is_white, (position[0], position[1]))
                self.forced_move = piece
            elif char.lower() == "w":
                piece = Chicken(is_white, (position[0], position[1]))
                self.forced_move = piece
            elif char.lower() == "#":
                piece = Wall(is_white, (position[0], position[1]))
            elif char in ["5", "4", "3", "2", "1"]:
                piece = Egg(True, (position[0], position[1]))
                piece.char_to_hatch_time(char)
            elif char in ["%", "$", "£", '"', "!"]:
                piece = Egg(False, (position[0], position[1]))
                piece.char_to_hatch_time(char)
            elif char == "8":
                piece = Death(True, (position[0], position[1]))
            elif char == "*":
                piece = Death(False, (position[0], position[1]))
            else:
                piece = None

            self.squares[position[0]][position[1]] = piece

            if position[1] == 9:
                position = [position[0] + 1, 0]
            else:
                position[1] += 1

    def square_in_position(self, position):
        """
        Takes a parameter 'position'
        The position is a tuple storing the row and column of the targeted square: (3, 6)
        This format for 'position' is used throughout the project.

        Returns the object located in the square. If the square is out of bounds for the board, e.g. (11, -3),
        returns None
        """

        row, col = position
        if not 0 <= row <= 9 or not 0 <= col <= 9:
            return None
        return self.squares[position[0]][position[1]]

    def set_square_in_position(self, position, new_square_value):
        """
        Sets the square in the specified position to the new for the square to be changed to.
        """
        row, col = position
        if 0 <= row <= 9 and 0 <= col <= 9:
            self.squares[row][col] = new_square_value

    def find_pieces(self, is_white, piece_type):
        """
        Returns a list of positions for any piece that fits the parameters
        """
        pieces = []
        for row in self.squares:
            for square in row:
                if square is not None:
                    if square.is_white == is_white and issubclass(type(square), piece_type):
                        pieces.append(square.position)
        return pieces

    def legal_moves_for_every_piece(self, care_about_colour=True, prefer_pieces=None):
        """
        Returns a list of moves that can be made from the current position
        Moves are stored in the form (start_position, end_position)
        The method does not account for all places that double-moving pieces can go after their first move:
        Only the available first moves.

        care_about_colour is a boolean value which toggles whether the method checks for moves for only the relevant player
        Example: If it is Black's turn to move and care_about_colour is True, only the legal moves for black pieces will
        be included. If care_about_colour is False, white's pieces will also be included.

        invertColour means that if it is Black's turn, only white pieces' moves will be considered.
        """
        all_pieces = []
        for row in self.squares:
            for square in row:
                if issubclass(type(square), Piece):
                    all_pieces.append(square)
        if care_about_colour:
            all_pieces = [piece for piece in all_pieces if piece.is_white == self.white_to_move]
        if prefer_pieces is not None:
            all_pieces = [piece for piece in all_pieces if piece in prefer_pieces]
        all_moves = []
        for piece in all_pieces:
            for move in self.all_legal_moves(piece.position):
                all_moves.append((piece.position, move))
        return all_moves

    def all_legal_moves(self, position, prevent_checks=True):
        """
        Gets the legal moves and takes for a piece in a given position, regardless of whose turn it is.
        If prevent_checks is true, it will only allow moves that mean that they will not be in check afterward.
        """
        if type(self.square_in_position(position)) == King:
            castle_moves = self.castle_moves(self.square_in_position(position))
        else:
            castle_moves = []

        return self.legal_moves(position, prevent_checks) + self.legal_takes(position, prevent_checks) + castle_moves

    def legal_moves(self, position, prevent_checks=True):
        """
        Gets the legal moves for a piece in a given position. Does not include available takes.
        """
        if self.forced_move is not None:
            if not self.forced_move.position == position:
                return []
        target_square = self.square_in_position(position)
        if target_square is None:
            return []

        legal_moves = []
        legal_moves.extend(self.legal_moves_from_directions(target_square))
        legal_moves.extend([position for position in target_square.moves() if self.is_legal_move(position)])
        legal_moves.extend(self.legal_moves_from_dependancies(target_square))

        if type(target_square) == Chicken:
            adjacent_pieces = self.adjacent_piece_types(target_square.position)
            if Pawn in adjacent_pieces:
                legal_moves.extend([position for position in target_square.pawn_moves()
                                    if self.is_legal_move(position)])
            if Dog in adjacent_pieces or Knight in adjacent_pieces:
                legal_moves.extend([position for position in target_square.knight_moves()
                                    if self.is_legal_move(position)])
            if Frog in adjacent_pieces:
                legal_moves.extend([position for position in target_square.frog_moves()
                                    if self.is_legal_move(position)])
            if Panda in adjacent_pieces or King in adjacent_pieces:
                legal_moves.extend([position for position in target_square.king_moves()
                                    if self.is_legal_move(position)])
            if Cleric in adjacent_pieces:
                legal_moves.extend([position for position in target_square.cleric_moves()
                                    if self.is_legal_move(position)])
        try:
            legal_moves = list(
                {(row, col) for (row, col) in legal_moves if 0 <= row <= 9 and 0 <= col <= 9 and (row, col) !=
                 self.find_pieces(is_white=not target_square.is_white, piece_type=King)[0]})
        except IndexError:
            pass
        if prevent_checks:
            legal_moves = [move for move in legal_moves if
                           not self.would_be_check(self.white_to_move, (position, move))]
        return legal_moves

    def legal_takes(self, position, prevent_checks=True):
        """
        Gets the legal takes for a piece in a given position. Does not include available moves.
        """
        if self.forced_move is not None:
            if not self.forced_move.position == position:
                return []
        target_square = self.square_in_position(position)
        if target_square is None:
            return []

        legal_moves = []
        legal_moves.extend(self.legal_takes_from_directions(target_square))
        legal_moves.extend([position for position in target_square.takes()
                            if self.is_legal_take(position, is_white=target_square.is_white)])
        legal_moves.extend(self.legal_takes_from_dependancies(target_square))
        if type(target_square) == Chicken:
            adjacent_pieces = self.adjacent_piece_types(target_square.position)
        else:
            adjacent_pieces = []
        if type(target_square) == Pawn or (
                type(target_square) == Chicken and Pawn in adjacent_pieces):
            if target_square.is_white:
                if target_square.position[0] == 3:
                    row, col = target_square.position
                    if type(self.square_in_position((row, col - 1))) == Pawn:
                        if self.square_in_position((row, col - 1)).is_en_passantable:
                            legal_moves.append((row - 1, col - 1))
                    if type(self.square_in_position((row, col + 1))) == Pawn:
                        if self.square_in_position((row, col + 1)).is_en_passantable:
                            legal_moves.append((row - 1, col + 1))
                    if type(self.square_in_position((row + 1, col - 1))) == Pawn:
                        if self.square_in_position((row + 1, col - 1)).is_en_passantable:
                            legal_moves.append((row - 1, col - 1))
                    if type(self.square_in_position((row + 1, col + 1))) == Pawn:
                        if self.square_in_position((row + 1, col + 1)).is_en_passantable:
                            legal_moves.append((row - 1, col + 1))
                elif target_square.position[0] == 4:
                    row, col = target_square.position
                    if type(self.square_in_position((row, col - 1))) == Pawn:
                        if self.square_in_position((row, col - 1)).is_en_passantable:
                            legal_moves.append((row - 1, col - 1))
                    if type(self.square_in_position((row, col + 1))) == Pawn:
                        if self.square_in_position((row, col + 1)).is_en_passantable:
                            legal_moves.append((row - 1, col + 1))
            else:
                if target_square.position[0] == 6:
                    row, col = target_square.position
                    if type(self.square_in_position((row, col - 1))) == Pawn:
                        if self.square_in_position((row, col - 1)).is_en_passantable:
                            legal_moves.append((row + 1, col - 1))
                    if type(self.square_in_position((row, col + 1))) == Pawn:
                        if self.square_in_position((row, col + 1)).is_en_passantable:
                            legal_moves.append((row + 1, col + 1))
                    if type(self.square_in_position((row - 1, col - 1))) == Pawn:
                        if self.square_in_position((row - 1, col - 1)).is_en_passantable:
                            legal_moves.append((row + 1, col - 1))
                    if type(self.square_in_position((row - 1, col + 1))) == Pawn:
                        if self.square_in_position((row - 1, col + 1)).is_en_passantable:
                            legal_moves.append((row + 1, col + 1))
                elif target_square.position[0] == 5:
                    row, col = target_square.position
                    if type(self.square_in_position((row, col - 1))) == Pawn:
                        if self.square_in_position((row, col - 1)).is_en_passantable:
                            legal_moves.append((row + 1, col - 1))
                    if type(self.square_in_position((row, col + 1))) == Pawn:
                        if self.square_in_position((row, col + 1)).is_en_passantable:
                            legal_moves.append((row + 1, col + 1))
        if type(target_square) == Chicken:
            if Pawn in adjacent_pieces:
                legal_moves.extend([position for position in target_square.pawn_takes()
                                    if self.is_legal_take(position, target_square.is_white)])
            if Dog in adjacent_pieces or Knight in adjacent_pieces:
                legal_moves.extend([position for position in target_square.knight_moves()
                                    if self.is_legal_take(position, target_square.is_white)])
            if Frog in adjacent_pieces:
                legal_moves.extend([position for position in target_square.frog_moves()
                                    if self.is_legal_take(position, target_square.is_white)])
            if King in adjacent_pieces or Panda:
                legal_moves.extend([position for position in target_square.king_moves()
                                    if self.is_legal_take(position, target_square.is_white)])
        legal_moves = list({(row, col) for (row, col) in legal_moves if 0 <= row <= 9 and 0 <= col <= 9})
        if prevent_checks:
            if position in self.double_hop_start_positions():
                valid_moves = []
                for move in legal_moves:
                    new_board = ChessBoard(self.board_state(), self.white_to_move)
                    new_board.double_move_piece(position, move)
                    for doubleMove in new_board.all_legal_moves(move, False):
                        newer_board = ChessBoard(new_board.board_state(), new_board.white_to_move)
                        newer_board.double_move_piece(move, doubleMove)
                        is_check_after_two_moves = newer_board.check_check(target_square.is_white)
                        del newer_board
                        if not is_check_after_two_moves:
                            valid_moves.append(move)
                    del new_board
                    legal_moves = valid_moves
            else:
                legal_moves = [move for move in legal_moves if
                               not self.would_be_check(self.white_to_move, (position, move))]
        return legal_moves

    def is_legal_move(self, end_position):
        """
        Checks if the end position for any given move is legal.
        For a move to be legal, it has to be unoccupied previously to the move.
        """
        if not (0 <= end_position[0] <= 9 and 0 <= end_position[1] <= 9):
            return False
        if self.square_in_position(end_position) is None:
            return True
        else:
            return False

    def is_legal_take(self, end_position, is_white):
        """
        Checks if the end position for any given move is legal.
        For a move to be legal, it has to be occupied by an enemy piece previously to the move.
        """
        if not (0 <= end_position[0] <= 9 and 0 <= end_position[1] <= 9):
            return False
        target_square = self.square_in_position(end_position)
        if issubclass(type(target_square), Piece) and target_square.is_white \
                is not is_white and not target_square.invulnerable:
            return True
        else:
            return False

    def legal_moves_from_directions(self, piece):
        """
        Calculates the legal moves for sliding pieces such as bishops and rooks.
        Returns this as a list of available positions
        """
        legal_moves = []
        if type(piece) == Chicken:
            directions = []
            adjacent_pieces = self.adjacent_piece_types(piece.position)
            if Pawn in adjacent_pieces:
                directions.extend(piece.pawn_direction_moves())
            if Rook in adjacent_pieces:
                directions.extend(piece.rook_direction_moves())
            if Bishop in adjacent_pieces:
                directions.extend(piece.bishop_direction_moves())
            if Queen in adjacent_pieces:
                directions.extend(piece.rook_direction_moves())
                directions.extend(piece.bishop_direction_moves())
            if Blob0 in adjacent_pieces:
                directions.extend(piece.blob0_direction_moves())
            if Blob1 in adjacent_pieces or Panda in adjacent_pieces:
                directions.extend(piece.blob1_direction_moves())
            if Blob2 in adjacent_pieces:
                directions.extend(piece.blob2_direction_moves())
            if Blob3 in adjacent_pieces:
                directions.extend(piece.blob3_direction_moves())
        else:
            directions = piece.direction_moves()
        position = piece.position
        for orientation, limit in directions:
            found_piece = False
            squares_travelled = 0
            movement = [0, 0]
            current_position = position

            if "N" in orientation:
                movement[0] = -1
            elif "S" in orientation:
                movement[0] = +1

            if "E" in orientation:
                movement[1] = 1
            elif "W" in orientation:
                movement[1] = -1

            while not found_piece and squares_travelled < limit:
                squares_travelled += 1
                current_position = current_position[0] + movement[0], current_position[1] + movement[1]
                try:
                    currentSquare = self.square_in_position(current_position)
                except IndexError:
                    break
                if currentSquare is not None:
                    found_piece = True
                else:
                    legal_moves.append(current_position)
        return legal_moves

    def legal_takes_from_directions(self, piece):
        """
        Calculates the legal takes for sliding pieces such as bishops and rooks.
        Returns this as a list of available positions
        """
        legal_moves = []
        if type(piece) == Chicken:
            directions = []
            adjacent_pieces = self.adjacent_piece_types(piece.position)
            if Rook in adjacent_pieces:
                directions.extend(piece.rook_direction_moves())
            if Bishop in adjacent_pieces or Cleric in adjacent_pieces:
                directions.extend(piece.bishop_direction_moves())
            if Queen in adjacent_pieces:
                directions.extend(piece.rook_direction_moves())
                directions.extend(piece.bishop_direction_moves())
            if Blob0 in adjacent_pieces:
                directions.extend(piece.blob0_direction_moves())
            if Blob1 in adjacent_pieces:
                directions.extend(piece.blob1_direction_moves())
            if Blob2 in adjacent_pieces or King in adjacent_pieces or Panda in adjacent_pieces:
                directions.extend(piece.blob2_direction_moves())
            if Blob3 in adjacent_pieces:
                directions.extend(piece.blob3_direction_moves())
        else:
            directions = piece.direction_takes()
        for orientation, limit in directions:
            found_piece = False
            squares_travelled = 0
            movement = [0, 0]
            current_position = piece.position

            if "N" in orientation:
                movement[0] = 1
            elif "S" in orientation:
                movement[0] = -1

            if "E" in orientation:
                movement[1] = 1
            elif "W" in orientation:
                movement[1] = -1

            while not found_piece and squares_travelled < limit:
                squares_travelled += 1
                current_position = current_position[0] + movement[0], current_position[1] + movement[1]
                if not (0 <= current_position[0] <= 9 and 0 <= current_position[1] <= 9):
                    break
                currentSquare = self.square_in_position(current_position)
                if currentSquare is not None:
                    found_piece = True
                    if currentSquare.is_white != piece.is_white and not currentSquare.invulnerable:
                        legal_moves.append(current_position)
        return legal_moves

    def legal_moves_from_dependancies(self, piece):
        """
        Some moves don't fit into unconditional moves (like Dog or Frog hops), but also aren't directional.
        (Such as the Blob0 moving like a knight being dependent on the pawn to its diagonal.

        This method looks through the available squares for those pieces and their dependancies
        And returns a list of available moves
        """
        legal_moves = [move for move, dependancy in piece.dependant_moves() if
                       self.square_in_position(dependancy) is None and self.square_in_position(move) is None]
        if type(piece) == Chicken:
            row, col = piece.position
            adjacent_pieces = [self.square_in_position((row - 1, col - 1)), self.square_in_position((row - 1, col)),
                               self.square_in_position((row - 1, col + 1)),
                               self.square_in_position((row, col - 1)), self.square_in_position((row, col + 1)),
                               self.square_in_position((row + 1, col - 1)), self.square_in_position((row + 1, col)),
                               self.square_in_position((row + 1, col + 1))]
            if Blob0 in [type(adjacentPiece) for adjacentPiece in adjacent_pieces]:
                legal_moves.extend([move for move, dependancy in piece.blob0_dependant_moves() if
                                    self.square_in_position(dependancy) is None and self.square_in_position(
                                        move) is None])
        return legal_moves

    def legal_takes_from_dependancies(self, piece):
        """
        Looks through legal takes from dependancies and returns them as a list of available moves.
        """
        dependant_takes = []
        legal_moves = [move for move, dependancy in piece.dependant_takes() if
                       self.square_in_position(dependancy) is None and issubclass(type(self.square_in_position(move)),
                                                                                  Piece) and self.square_in_position(
                           move).is_white != piece.is_white]
        if type(piece) == Chicken:
            adjacent_pieces = self.adjacent_piece_types(piece.position)
            if Blob0 in adjacent_pieces:
                legal_moves.extend([move for move, dependancy in piece.blob0_dependant_moves() if
                                    self.square_in_position(dependancy) is None and
                                    issubclass(type(self.square_in_position(move)), Piece) and
                                    self.square_in_position(move).is_white != piece.is_white])
        return legal_moves

    def castle_moves(self, piece):
        if type(piece) != King and not piece.has_moved:
            return []
        if self.check_check(piece.is_white):
            return []
        castle_moves = []
        back_rank_row = 9 if piece.is_white else 1
        back_rank = self.squares[back_rank_row]
        if type(back_rank[0]) is Rook and not back_rank[0].has_moved and \
                {back_rank[1], back_rank[2], back_rank[3], back_rank[4]} == {None} and not \
                (self.would_be_check(piece.is_white, ((piece.position), (back_rank_row, 3))) or
                 self.would_be_check(piece.is_white, ((piece.position), (back_rank_row, 4)))):
            castle_moves.append((back_rank_row, 3))
        if type(back_rank[9]) is Rook and not back_rank[9].has_moved and \
                {back_rank[6], back_rank[7], back_rank[8]} == {None} and not \
                (self.would_be_check(piece.is_white, ((piece.position), (back_rank_row, 7))) or
                 self.would_be_check(piece.is_white, ((piece.position), (back_rank_row, 6)))):
            castle_moves.append((back_rank_row, 7))
        return castle_moves

    def tick_all_pieces(self):
        """
        Some pieces have properties that they lose after a certain time (Panda invulnerability, Pawn enPassantable)
        This method simply iterates through every pieces in self.squares and runs the tick() method on them.
        """
        for row in self.squares:
            for square in row:
                if issubclass(type(square), Piece):
                    output = square.tick()
                    if output is not None:
                        self.set_square_in_position(square.position, output)

    def selectPiece(self, position):
        """
        Selects a piece and updates relevant board attributes, including currentlegal_moves.
        """
        if self.forced_move is not None and self.forced_move.position != position:
            return False
        square_in_position = self.square_in_position(position)
        if square_in_position.is_white == self.white_to_move:
            self.selected_piece = square_in_position
            self.current_legal_moves = self.all_legal_moves(position)
            return True
        else:
            return False

    def unselectPiece(self):
        """
        Unselects pieces and updates relevant board attributes
        """
        if self.forced_move is None:
            self.selected_piece = None
            self.current_legal_moves = []
            self.fakelegal_moves = []
            return True
        return False

    def move_piece(self, start_position, end_position):
        """
        Moves a piece from a given start position to an end position
        Also, performs many complex checks for additional actions that must be performed when a piece moves.
        (Dog doubleHopping, Blob duplication)
        """
        self.previous_board_states.append(self.board_state())
        self.checked_positions = None
        take = False
        piece_to_be_moved = self.square_in_position(start_position)

        if type(piece_to_be_moved) == Chicken:
            adjacent_pieces = self.adjacent_piece_types(start_position)
            if Pawn in adjacent_pieces:
                forwards = -1 if piece_to_be_moved.is_white else 1
                if end_position in [(start_position[0] + forwards, start_position[1] + 1),
                                    (start_position[0] + forwards, start_position[1] - 1)]:
                    squares_behind = [self.square_in_position((end_position[0] - forwards, end_position[1])),
                                      self.square_in_position((end_position[0] - (2 * forwards), end_position[1])),
                                      self.square_in_position((end_position[0] - (3 * forwards), end_position[1]))]
                    if squares_behind[0] is None and squares_behind[1] is None \
                            and issubclass(type(squares_behind[2]), Piece) and \
                            squares_behind[2].is_en_passantable:
                        self.set_square_in_position(squares_behind[2].position, None)
                        enPassant = True
                    elif squares_behind[0] is None \
                            and issubclass(type(squares_behind[1]), Piece) and \
                            squares_behind[1].is_en_passantable:
                        self.set_square_in_position(squares_behind[1].position, None)
                        enPassant = True
                    elif issubclass(type(squares_behind[0]), Piece) and squares_behind[0].is_en_passantable:
                        self.set_square_in_position(squares_behind[0].position, None)
                        enPassant = True
                    else:
                        enPassant = False

                    if enPassant and Dog in adjacent_pieces:
                        take = True

        self.tick_all_pieces()
        if self.square_in_position(end_position) is not None:
            take = True
        piece_to_be_moved.position = end_position
        self.set_square_in_position(end_position, piece_to_be_moved)
        self.set_square_in_position(start_position, None)
        self.selected_piece = None

        if take:
            if type(piece_to_be_moved) == Dog \
                    or (type(piece_to_be_moved) == Chicken and Dog in adjacent_pieces) \
                    or type(piece_to_be_moved) == Death:
                self.forced_move = piece_to_be_moved
            if type(piece_to_be_moved) == Chicken and Panda in adjacent_pieces:
                piece_to_be_moved.pandaTake()
            if type(piece_to_be_moved) == Chicken and (
                    Blob0 in adjacent_pieces or Blob1 in adjacent_pieces or Blob2 in adjacent_pieces):
                self.set_square_in_position(start_position,
                                            Egg(is_white=piece_to_be_moved.is_white, position=start_position))
            elif type(piece_to_be_moved) == Blob0:
                self.set_square_in_position(start_position,
                                            Blob1(is_white=piece_to_be_moved.is_white, position=start_position))
                self.set_square_in_position(end_position,
                                            Blob1(is_white=piece_to_be_moved.is_white, position=end_position))
            elif type(piece_to_be_moved) == Blob1:
                self.set_square_in_position(start_position,
                                            Blob2(is_white=piece_to_be_moved.is_white, position=start_position))
                self.set_square_in_position(end_position,
                                            Blob2(is_white=piece_to_be_moved.is_white, position=end_position))
            elif type(piece_to_be_moved) == Blob2:
                self.set_square_in_position(start_position,
                                            Blob3(is_white=piece_to_be_moved.is_white, position=start_position))
                self.set_square_in_position(end_position,
                                            Blob3(is_white=piece_to_be_moved.is_white, position=end_position))
            piece_to_be_moved.take(start_position, end_position)
        else:
            if type(piece_to_be_moved) == Pawn and start_position[1] != end_position[1]:
                if piece_to_be_moved.is_white:
                    forwards = 1
                else:
                    forwards = -1
                pieceRemoved = False
                while not pieceRemoved:
                    row, col = end_position
                    if self.square_in_position((row + forwards, col)) is not None and self.square_in_position(
                            (row + forwards, col)).is_white != piece_to_be_moved.is_white:
                        self.set_square_in_position((row + forwards, col), None)
                        pieceRemoved = True
                    else:
                        if forwards > 0:
                            forwards += 1
                        else:
                            forwards -= 1
            if type(piece_to_be_moved) == King and abs(start_position[1] - end_position[1]) == 2:
                if end_position == (9, 3):
                    rook_to_move = self.square_in_position((9, 0))
                    self.set_square_in_position((9, 4), rook_to_move)
                    self.set_square_in_position((9, 0), None)
                    rook_to_move.position = (9, 4)
                    rook_to_move.has_moved = True
                elif end_position == (9, 7):
                    rook_to_move = self.square_in_position((9, 9))
                    self.set_square_in_position((9, 6), rook_to_move)
                    self.set_square_in_position((9, 9), None)
                    rook_to_move.position = (9, 6)
                    rook_to_move.has_moved = True
                elif end_position == (0, 3):
                    rook_to_move = self.square_in_position((0, 0))
                    self.set_square_in_position((0, 4), rook_to_move)
                    self.set_square_in_position((0, 0), None)
                    rook_to_move.position = (9, 4)
                    rook_to_move.has_moved = True
                elif end_position == (0, 7):
                    rook_to_move = self.square_in_position((0, 9))
                    self.set_square_in_position((0, 6), rook_to_move)
                    self.set_square_in_position((0, 9), None)
                    rook_to_move.position = (0, 6)
                    rook_to_move.has_moved = True
            piece_to_be_moved.move(start_position, end_position)
        if type(piece_to_be_moved) == Pawn and end_position[0] in (0, 9):
            column = piece_to_be_moved.position[1]
            availablePromotionPieces = [Rook(is_white=piece_to_be_moved.is_white, position=end_position),
                                        Dog(is_white=piece_to_be_moved.is_white, position=end_position),
                                        Chicken(is_white=piece_to_be_moved.is_white, position=end_position),
                                        Blob1(is_white=piece_to_be_moved.is_white, position=end_position),
                                        Panda(is_white=piece_to_be_moved.is_white, position=end_position),
                                        Panda(is_white=piece_to_be_moved.is_white, position=end_position),
                                        Cleric(is_white=piece_to_be_moved.is_white, position=end_position),
                                        Frog(is_white=piece_to_be_moved.is_white, position=end_position),
                                        Dog(is_white=piece_to_be_moved.is_white, position=end_position),
                                        Rook(is_white=piece_to_be_moved.is_white, position=end_position)]
            self.set_square_in_position(end_position, availablePromotionPieces[column])

        if self.forced_move is not None:
            if not len(self.all_legal_moves(self.forced_move.position)) > 0:
                self.white_to_move = not self.white_to_move
        else:
            self.white_to_move = not self.white_to_move

        self.moves.append([start_position, end_position])

    def double_move_piece(self, start_position, end_position):
        """
        A simpler version of the move_piece method that is run in its place for the second move in doubleHop moves.
        This method does not tick pieces or check for duplication, simply updates relevant square positions.
        """
        piece = self.square_in_position(start_position)
        self.set_square_in_position(start_position, None)
        piece.position = end_position
        self.set_square_in_position(end_position, piece)
        self.selected_piece = None
        self.forced_move = None
        if len(self.moves) > 0:
            lastMove = self.moves[len(self.moves) - 1]
            lastMove.append(end_position)
            self.moves[len(self.moves) - 1] = lastMove
        else:
            self.moves.append([start_position, end_position])
        self.check_check(not piece.is_white)

    def check_check(self, whiteInCheck, checkDoubleHops=True):
        """
        Checks if a given player is in check in the current position.
        """
        king_positions = self.find_pieces(whiteInCheck, King)
        self.checked_positions = []
        if len(king_positions) == 0:
            return True
        for kingPos in king_positions:
            for row in self.squares:
                for square in row:
                    if square is not None:
                        if kingPos in self.legal_takes(square.position, False):
                            self.checked_positions.append(kingPos)
                            return True

        # Adds the ability to not check for double hops so that it is possible to check only one hop into the future
        if not checkDoubleHops:
            return False

        # Do a simple check for available captures first, and then check the more complicated double-moves.
        for row in self.squares:
            for square in row:
                if type(square) == Chicken:
                    adjacent_pieces = self.adjacent_piece_types(square.position)
                if type(square) == Dog or type(square) == Death or (type(square) == Chicken and Dog in adjacent_pieces):
                    for move in self.legal_takes(square.position, False):
                        if type(square) == Dog:
                            newPiece = Dog(is_white=square.is_white, position=move)
                        else:
                            newPiece = Chicken(is_white=square.is_white, position=move)
                        board = ChessBoard(board_state=self.board_state(), white_to_move=square.is_white)
                        board.set_square_in_position(square.position, None)
                        board.set_square_in_position(move, newPiece)
                        isCheck = board.check_check(whiteInCheck, checkDoubleHops=False)
                        del newPiece
                        del board
                        if isCheck:
                            self.checked_positions.append(kingPos)
                            return True
        return False

    def check_checkmate(self, whiteInCheck):
        """
        Checks if a given player is in checkmate
        First checks that the player is in check, then if they are,
        check for how many moves the player has available to them. If they don't have any moves: return True
        """
        if self.check_check(whiteInCheck):
            if len(self.legal_moves_for_every_piece()) == 0:
                return True
        return False

    def scheck_stalemate(self):
        """
        Checks for stalemate by counting the number of legal pieces. If the amount is 0, returns True
        """
        if len(self.legal_moves_for_every_piece()) == 0 and self.forced_move is None:
            return True
        elif len(self.moves) >= 1000:
            self.victor = False
            return True
        elif len(self.moves) >= 12:
            lastMoves = self.moves[len(self.moves) - 12:len(self.moves)]
            if lastMoves[0] == lastMoves[4] == lastMoves[8] and lastMoves[1] == lastMoves[5] == lastMoves[9] \
                    and lastMoves[2] == lastMoves[6] == lastMoves[10] and lastMoves[3] == lastMoves[7] == lastMoves[11]:
                return True
        return False

    def would_be_check(self, whiteInCheck, move):
        """
        Creates a new chessBoard object with the same board_state, makes the given move, and checks for check in the
        new ChessBoard object. Deleted the new object before returning.
        """
        board = ChessBoard(self.board_state(), whiteInCheck)
        board.move_piece(move[0], move[1])
        would_be_check = board.check_check(whiteInCheck)
        del board
        return would_be_check

    def simulate_game(self, moves):
        """
        Given a list of moves, simulates the game
        Highly prone to errors, as there is no checks as to if the next move is legal.
        """
        self.__init__()
        for move in moves:
            if len(move) == 2:
                self.move_piece(move[0], move[1])
            else:
                self.move_piece(move[0], move[1])
                self.move_piece(move[1], move[2])

    def is_legal(self, start_position, end_position):
        """
        Checks that a move is fundamentally allowed:
        Is the starting square occupied by a piece and that the ending square is occupied by:
        either nothing or an enemy piece
        """
        start_pos = (start_position[0], start_position[1])
        end_pos = (end_position[0], end_position[1])
        if start_pos is None:
            return False
        if end_pos in self.all_legal_moves(start_pos) and self.square_in_position(
                start_pos).is_white == self.white_to_move and self.victor is None:
            return True
        return False

    def as_txt(self):
        """
        Returns a string value that represents the board with |ExamplePieces | in squares. Primarily for debugging
        """
        return_output = ""
        for row in self.squares:
            for column in row:
                if column is None:
                    return_output += "|              |"
                else:
                    return_output += "| " + column.toString() + " |"
            return_output = return_output + "\n"
        return return_output

    def current_value(self):
        """
        Adds up the values of all the current pieces.
        """
        total = 0
        for row in self.squares:
            for square in row:
                if issubclass(type(square), Piece):
                    total += square.game_value()
        return total

    def adjacent_spaces(self, position, discovered=None):
        if discovered is None:
            discovered = []
        disc = discovered[:]
        disc.append(position)
        row, col = position
        adjacent_spaces = [(row, col) for (row, col) in [(row + 1, col + 1), (row + 1, col),
                                                         (row + 1, col - 1), (row, col + 1),
                                                         (row, col - 1), (row - 1, col + 1),
                                                         (row - 1, col), (row - 1, col - 1)] if
                           0 <= row <= 9 and 0 <= col <= 9]
        for space in adjacent_spaces:
            if space in disc:
                continue
            elif type(self.square_in_position(space)) == Chicken:
                disc.extend(self.adjacent_spaces(space, disc))
            else:
                disc.append(space)
        return disc

    def adjacent_piece_types(self, position):
        return {type(self.square_in_position(space)) for space in self.adjacent_spaces(position)}

    def double_hop_start_positions(self):
        """
        Returns the start positions for anything that can move twice
        """
        available_positions = []
        for position in self.find_pieces(is_white=self.white_to_move, piece_type=Dog):
            available_positions.append(position)
        for position in self.find_pieces(is_white=self.white_to_move, piece_type=Death):
            available_positions.append(position)
        for position in self.find_pieces(is_white=self.white_to_move, piece_type=Chicken):
            adjacent_pieces = self.adjacent_piece_types(position)
            if Dog in adjacent_pieces:
                available_positions.append(position)
        return available_positions

    def available_board_states(self, prefer_pieces=None):
        """
        Returns a list of all the available board states that can be reached in one move from the current position
        """
        board_states = []
        doubleHops = self.double_hop_start_positions()
        new_board = ChessBoard(board_state=self.board_state(), white_to_move=self.white_to_move)
        for move in [move for move in self.legal_moves_for_every_piece(prefer_pieces=prefer_pieces) if
                     move[0] not in doubleHops]:
            new_board.move_piece(move[0], move[1])
            board_states.append((new_board.board_state(), move))
            new_board.undo_move()
        for start_pos in doubleHops:
            for move in self.all_legal_moves(start_pos):
                new_board.move_piece(start_pos, move)
                if new_board.white_to_move == self.white_to_move:
                    for doubleMove in new_board.all_legal_moves(move):
                        new_board.move_piece(move, doubleMove)
                        board_states.append((new_board.board_state(), (start_pos, move, doubleMove)))
                        new_board.undo_move()
                    new_board.undo_move()
                else:
                    board_states.append((new_board.board_state(), (start_pos, move)))
                    new_board.undo_move()
        del new_board
        return board_states

    def make_random_move(self):
        """
        Literally just selects a random move and makes it
        """
        random_board_state = random.choice(self.available_board_states())
        self.set_board_state(random_board_state[1])
        self.moves.append(random_board_state[0])
        self.white_to_move = not self.white_to_move
        if self.check_check(self.white_to_move):
            self.check_checkmate(self.white_to_move)
        else:
            self.scheck_stalemate()

    def undo_move(self):
        """
        Sends the board back to its previous position.
        """
        self.moves.pop(len(self.moves) - 1)
        self.set_board_state(self.previous_board_states[len(self.previous_board_states) - 1])
        self.previous_board_states = self.previous_board_states[:len(self.previous_board_states) - 1]
        self.white_to_move = not self.white_to_move
        self.checked_positions = None
        self.victor = None


class GameBoard(ChessBoard):
    """
    The GameBoard class extends the ChessBoard class, but allows for interaction with the pygame screen.
    """

    def __init__(self,
                 board_state="RDOZAKCFDRPPPPPPPPPP                                                            pppppppppprdozakcfdr",
                 white_to_move=True):
        """
        Extends the ChessBoard constructor, and creates a screen to display.
        """
        super().__init__(board_state, white_to_move)
        pygame.init()
        self.screen = pygame.display.set_mode((600, 600))

        pygame.display.set_caption("Chess+")
        self.checked_positions = None
        self.last_move_squares = []
        self.highlighted_squares = []
        self.flipped = False
        self.update_board()

    def flip(self):
        self.flipped = not self.flipped

    def update_board(self, update_display=True):
        """
        Updates the board to add pieces on all the spaces for which there is a piece in the GameBoard object.
        Also adds a check mark if there is a check
        """
        visual_board = []
        for row in range(10):
            row_list = []
            for col in range(10):
                x = col * 60
                y = row * 60
                rect = pygame.Rect(x, y, 60, 60)
                row_list.append(rect)
            visual_board.append(row_list)

        LIGHT = (255, 255, 255)
        DARK = (50, 168, 82)
        LAST_MOVE = (168, 50, 160)
        colors = [LIGHT, DARK]
        color_index = 0

        for row in range(10):
            for col in range(10):
                if self.flipped:
                    rect = visual_board[9 - row][9 - col]
                else:
                    rect = visual_board[row][col]
                if (row, col) in self.last_move_squares:
                    pygame.draw.rect(self.screen, LAST_MOVE, rect)
                else:
                    pygame.draw.rect(self.screen, colors[color_index], rect)
                color_index = (color_index + 1) % 2

            color_index = (color_index + 1) % 2

        for row in self.squares:
            for square in row:
                if square is not None and issubclass(type(square), Piece):
                    if True:
                        self.place_piece(visual_board, square, square.position, square.is_white)
                    else:
                        self.place_piece(visual_board, square, (9 - square.position[0], 9 - square.position[1]),
                                         square.is_white)

        if self.checked_positions is not None:
            self.place_png('check.png', self.checked_positions)

        if update_display:
            pygame.display.update()

    def selectPiece(self, position):
        """
        Selects a piece and places a 'selected-square.png' on the relevant position.
        Also places 'legal-move.png' on all the legal moves from that position
        """
        if super().selectPiece(position):
            self.update_board()
            if self.checked_positions is not None:
                self.place_png('check.png', self.checked_positions)
            self.place_png("selected-square.png", [position])
            self.place_png("legal-move.png", self.current_legal_moves)
            pygame.display.update()

    def unselectPiece(self):
        """
        Removes any pngs related to the selected piece
        """
        if super().unselectPiece():
            self.update_board()
        if self.checked_positions is not None:
            self.place_png('check.png', self.checked_positions)
        pygame.display.update()

    def move_piece(self, start_position, end_position):
        """
        Moves the piece and checks for checks. Places a check cross if either king is in check.
        Displays a victory statement if either player is in checkmate
        """
        super().move_piece(start_position, end_position)
        self.last_move_squares = self.moves[len(self.moves) - 1]
        self.update_board()
        self.checked_positions = None
        if self.check_check(self.white_to_move):
            if self.check_checkmate(self.white_to_move):
                self.displayVictory(not self.white_to_move)
                for row in self.squares:
                    for square in row:
                        if type(square) == King and square.is_white == self.white_to_move:
                            kingPos = square.position
                self.checked_positions = kingPos
                self.place_png('check.png', [kingPos])
                pygame.display.update()
        else:
            if self.scheck_stalemate():
                self.displayVictory(None)
        self.update_board()
        if self.forced_move is not None:
            self.selectPiece(self.forced_move.position)

    def double_move_piece(self, start_position, end_position):
        """
        Only adds another update_board() to the super method
        """
        self.update_board()
        super().double_move_piece(start_position, end_position)
        self.update_board()

    def displayVictory(self, whiteVictory):
        """
        Displays the victory text
        """
        if whiteVictory == True:
            victoryText = "White Wins!"
            self.victor = "White"
        elif whiteVictory == False:
            victoryText = "Black Wins!"
            self.victor = "Black"
        else:
            victoryText = "Stalemate"
            self.victor = False

        pygame.display.set_caption('Victory Screen')

        font = pygame.font.Font(None, 50)
        text = font.render(victoryText, True, (184, 61, 42))
        text_rect = text.get_rect(center=(self.screen.get_width() / 2, self.screen.get_height() / 2))

        self.screen.blit(text, text_rect)
        pygame.display.update()

    def check_check(self, whiteInCheck, checkDoubleHops=True):
        if super().check_check(whiteInCheck, checkDoubleHops):
            self.place_png('check.png', self.checked_positions)
            pygame.display.update()
            return True
        return False

    def check_checkmate(self, whiteInCheck):
        """
        Extends the check_checkmate method of the superclass to display victory if True
        """
        if super().check_checkmate(whiteInCheck):
            self.displayVictory(not whiteInCheck)

    def scheck_stalemate(self):
        if super().scheck_stalemate():
            self.displayVictory(None)

    def undo_move(self):
        pygame.display.set_caption('Chess+')
        self.last_move_squares = self.moves[len(self.moves) - 2]
        super().undo_move()
        self.update_board()

    def make_random_move(self):
        super().make_random_move()
        self.last_move_squares = self.moves[len(self.moves) - 1]
        self.update_board()

    def place_piece(self, visual_board, piece, position, is_white):
        """
        Places a piece PNG on a given position
        """
        piece_img = pygame.image.load(f"Images/{piece.as_png()}").convert_alpha()
        piece_rect = piece_img.get_rect()
        if is_white:
            piece_half_rect = pygame.Rect(piece_rect.left, piece_rect.top, 60, 60)
        else:
            piece_half_rect = pygame.Rect(piece_rect.left + 60, piece_rect.top, 60, 60)
        piece_img = piece_img.subsurface(piece_half_rect)

        piece_rect = piece_img.get_rect()
        if self.flipped:
            piece_rect.top = visual_board[9 - position[0]][9 - position[1]].top
            piece_rect.right = visual_board[9 - position[0]][9 - position[1]].right
        else:
            piece_rect.top = visual_board[position[0]][position[1]].top
            piece_rect.right = visual_board[position[0]][position[1]].right

        self.screen.blit(piece_img, piece_rect)

    def place_png(self, PNGLocation, positions):
        """
        Places a series of PNGs on the given locations
        """
        img = pygame.image.load(f"Images/{PNGLocation}").convert_alpha()
        img_rect = img.get_rect()
        img = img.subsurface(img_rect)

        for position in positions:
            if self.flipped:
                img_rect.y = (9 - position[0]) * 60
                img_rect.x = (9 - position[1]) * 60
            else:
                img_rect.y = position[0] * 60
                img_rect.x = position[1] * 60

            self.screen.blit(img, img_rect)


class DumbBoard(GameBoard):
    def __init__(self,
                 board_state="RDOZAKCFDRPPPPPPPPPP                                                            pppppppppprdozakcfdr",
                 white_to_move=True):
        super().__init__(board_state, white_to_move)

    def move_piece(self, start_position, end_position):
        random_value = random.random()
        print(random_value)

        if random_value >= 0.3:
            super().move_piece(start_position, end_position)

        elif 0.2 <= random_value < 0.3:
            self.flip()
            self.update_board()

            super().move_piece(start_position, end_position)

            font = pygame.font.Font(None, 50)
            text = font.render("Get Flipped Lol", True, (184, 61, 42))
            text_rect = text.get_rect(center=(self.screen.get_width() / 2, self.screen.get_height() / 2))

            self.screen.blit(text, text_rect)
            pygame.display.update()

        elif 0.1 <= random_value < 0.2:
            super().move_piece(start_position, end_position)

            random_pos_found = False
            while not random_pos_found:
                random_position = random.randint(0, 9), random.randint(0, 9)
                random_square = self.square_in_position(random_position)
                if issubclass(type(random_square), Piece) and type(random_square) != King:
                    random_pos_found = True
            self.set_square_in_position(random_position, None)
            self.update_board()

            font = pygame.font.Font(None, 25)
            text = font.render(f"I decided to remove the piece on {random_position}", True, (184, 61, 42))
            text_rect = text.get_rect(center=(self.screen.get_width() / 2, self.screen.get_height() / 2))

            self.screen.blit(text, text_rect)
            pygame.display.update()

        elif random_value < 0.1:
            font = pygame.font.Font(None, 50)
            text = font.render("No.", True, (184, 61, 42))
            text_rect = text.get_rect(center=(self.screen.get_width() / 2, self.screen.get_height() / 2))

            self.screen.blit(text, text_rect)
            pygame.display.update()

            self.white_to_move = not self.white_to_move
