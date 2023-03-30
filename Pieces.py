class Piece:
    """
    Abstract Class: is never actually called, only inherited by other Piece objects.
    """

    def __init__(self, is_white, position):
        """
        Defines relevant attributes
        """
        self.is_white = is_white
        self.position = position
        self.has_moved = False
        self.invulnerable = False
        self.is_en_passantable = False
        self.value = 0

    def game_value(self):
        """
        Flips the value of the piece to positive and negative values depending on the colour of the piece
        """
        if self.is_white:
            return self.value
        else:
            return self.value * -1

    def colour_case(self):
        """
        Provides a colour string for each piece, giving context to the is_white statement
        """
        if self.is_white:
            colour = "White"
        else:
            colour = "Black"
        return colour

    @staticmethod
    def as_png():
        """
        Allows for pieces to specify their own PNG location
        """
        return 'pawns.png'

    def moves(self):
        """
        Unconditional moves
        """
        return []

    def takes(self):
        """
        Unconditional takes
        """
        return self.moves()

    def direction_moves(self):
        return []

    def direction_takes(self):
        return self.direction_moves()

    def dependant_moves(self):
        return []

    def dependant_takes(self):
        return self.dependant_moves()

    def move(self, start_position, end_position):
        """
        Some pieces do something special when they are moved, so it's nice to have a method in the superclass,
        even if it does nothing.
        It stops errors from occurring when an attempt is made to call the method on a piece which does not have the method.
        """
        self.has_moved = True

    def take(self, start_position, end_position):
        self.has_moved = True

    def tick(self):
        pass

    def as_char(self, char):
        """
        Sets the char to be the right case depending on piece.
        """
        if self.is_white:
            return char
        else:
            return char.upper()


class Pawn(Piece):
    def __init__(self, is_white, position):
        super().__init__(is_white, position)
        self.value = 1

    def moves(self):
        row, col = self.position
        if self.is_white:
            return [(row - 1, col)]
        else:
            return [(row + 1, col)]

    def takes(self):
        row, col = self.position
        if self.is_white:
            return [(row - 1, col + 1), (row - 1, col - 1)]
        else:
            return [(row + 1, col + 1), (row + 1, col - 1)]

    def direction_moves(self):
        if self.is_white and self.position[0] == 8:
            return [("N", 3)]
        elif not self.is_white and self.position[0] == 1:
            return [("S", 3)]
        else:
            return []

    def direction_takes(self):
        return []

    def move(self, start_position, end_position):
        super().move(start_position, end_position)
        if abs(start_position[0] - end_position[0]) > 1:
            self.is_en_passantable = True

    def tick(self):
        self.is_en_passantable = False

    def string(self):
        return self.colour_case() + "Pawn   "

    def as_char(self):
        if self.is_en_passantable:
            return super().as_char("e")
        return super().as_char("p")

    @staticmethod
    def as_png():
        return 'pawns.png'


class Rook(Piece):
    def __init__(self, is_white, position):
        super().__init__(is_white, position)
        self.value = 5

    def direction_moves(self):
        return [("N", 10), ("E", 10), ("S", 10), ("W", 10)]

    def string(self):
        return self.colour_case() + "Rook   "

    def as_char(self):
        return super().as_char("r" if not self.has_moved else "m")

    @staticmethod
    def as_png():
        return 'rooks.png'


class Bishop(Piece):
    def __init__(self, is_white, position):
        super().__init__(is_white, position)
        self.value = 3

    def direction_moves(self):
        return [("NE", 10), ("SE", 10), ("SW", 10), ("NW", 10)]

    def string(self):
        return self.colour_case() + "Bishop "

    def as_char(self):
        return super().as_char("b")

    @staticmethod
    def as_png():
        return 'bishops.png'


class King(Piece):
    def __init__(self, is_white, position):
        super().__init__(is_white, position)
        self.value = 10000

    def moves(self):
        row, col = self.position
        return [(row + 1, col - 1), (row + 1, col), (row + 1, col + 1),
                (row, col - 1), (row, col + 1),
                (row - 1, col - 1), (row - 1, col), (row - 1, col + 1)]

    def string(self):
        return self.colour_case() + "King   "

    def as_char(self):
        return super().as_char("k" if not self.has_moved else "(" if self.is_white else ")")

    @staticmethod
    def as_png():
        return 'kings.png'


class Knight(Piece):
    def __init__(self, is_white, position):
        super().__init__(is_white, position)
        self.value = 3

    def string(self):
        return self.colour_case() + "Knight "

    def as_char(self):
        return super().as_char("n")

    def moves(self):
        row, col = self.position
        return [(row + 2, col - 1), (row + 2, col + 1),
                (row + 1, col - 2), (row + 1, col + 2),
                (row - 1, col - 2), (row - 1, col + 2),
                (row - 2, col - 1), (row - 2, col + 1)]

    @staticmethod
    def as_png():
        return 'knights.png'


class Panda(Piece):
    def __init__(self, is_white, position):
        super().__init__(is_white, position)
        self.value = 3

    def string(self):
        return self.colour_case() + "Panda  "

    def as_char(self):
        if self.invulnerable:
            return super().as_char("i")
        return super().as_char("a")

    def moves(self):
        row, col = self.position
        return [(row + 1, col - 1), (row + 1, col), (row + 1, col + 1),
                (row, col - 1), (row, col + 1),
                (row - 1, col - 1), (row - 1, col), (row - 1, col + 1)]

    def direction_moves(self):
        return [("N", 2), ("NE", 1), ("S", 2), ("SE", 1), ("E", 2), ("NW", 1), ("W", 2), ("SW", 1)]

    def direction_takes(self):
        return []

    def take(self, start_position, end_position):
        super().take(start_position, end_position)
        self.invulnerable = True

    def tick(self):
        self.invulnerable = False

    @staticmethod
    def as_png():
        return 'pandas.png'


class Queen(Piece):
    def __init__(self, is_white, position):
        super().__init__(is_white, position)
        self.value = 7

    def string(self):
        return self.colour_case() + "Queen  "

    def as_char(self):
        return super().as_char("q")

    def direction_moves(self):
        return [("N", 10), ("NE", 10), ("E", 10), ("SE", 10), ("S", 10), ("SW", 10), ("W", 10), ("NW", 10)]

    @staticmethod
    def as_png():
        return 'queens.png'


class Frog(Piece):
    def __init__(self, is_white, position):
        super().__init__(is_white, position)
        self.value = 6

    def string(self):
        return self.colour_case() + "Frog   "

    def as_char(self):
        return super().as_char("f")

    def moves(self):
        row, col = self.position
        return [(row + 3, col),
                (row + 2, col - 2), (row + 2, col), (row + 2, col + 2),
                (row + 1, col - 1), (row + 1, col), (row + 1, col + 1),
                (row, col - 3), (row, col - 2), (row, col - 1), (row, col + 1), (row, col + 2), (row, col + 3),
                (row - 1, col - 1), (row - 1, col), (row - 1, col + 1),
                (row - 2, col - 2), (row - 2, col), (row - 2, col + 2),
                (row - 3, col)]

    @staticmethod
    def as_png():
        return 'frogs.png'


class Dog(Piece):
    def __init__(self, is_white, position):
        super().__init__(is_white, position)
        self.value = 10

    def string(self):
        return self.colour_case() + "Dog    "

    def as_char(self):
        return super().as_char("d")

    def moves(self):
        row, col = self.position
        return [(row + 2, col - 1), (row + 2, col + 1),
                (row + 1, col - 2), (row + 1, col + 2),
                (row - 1, col - 2), (row - 1, col + 2),
                (row - 2, col - 1), (row - 2, col + 1)]

    @staticmethod
    def as_png():
        return 'knights.png'


class Blob0(Piece):
    def __init__(self, is_white, position):
        super().__init__(is_white, position)
        self.value = 8

    def string(self):
        return self.colour_case() + "Blob0  "

    def as_char(self):
        return super().as_char("z")

    def direction_moves(self):
        return [("N", 2), ("NE", 1), ("E", 2), ("SE", 1), ("S", 2), ("SW", 1), ("W", 2), ("NW", 1)]

    def dependant_moves(self):
        row, col = self.position
        return [[(row - 2, col - 1), (row - 1, col - 1)],
                [(row - 2, col + 1), (row - 1, col + 1)],
                [(row - 1, col - 2), (row - 1, col - 1)],
                [(row - 1, col + 2), (row - 1, col + 1)],
                [(row + 1, col - 2), (row + 1, col - 1)],
                [(row + 1, col + 2), (row + 1, col + 1)],
                [(row + 2, col - 1), (row + 1, col - 1)],
                [(row + 2, col + 1), (row + 1, col + 1)],
                ]

    @staticmethod
    def as_png():
        return 'zeros.png'


class Blob1(Piece):
    def __init__(self, is_white, position):
        super().__init__(is_white, position)
        self.value = 4

    def string(self):
        return self.colour_case() + "Blob1  "

    def as_char(self):
        return super().as_char("x")

    def direction_moves(self):
        return [("N", 2), ("NE", 1), ("E", 2), ("SE", 1), ("S", 2), ("SW", 1), ("W", 2), ("NW", 1)]

    @staticmethod
    def as_png():
        return 'ones.png'


class Blob2(Piece):
    def __init__(self, is_white, position):
        super().__init__(is_white, position)
        self.value = 2

    def string(self):
        return self.colour_case() + "Blob2  "

    def as_char(self):
        return super().as_char("v")

    def direction_moves(self):
        return [("N", 1), ("NE", 1), ("E", 1), ("SE", 1), ("S", 1), ("SW", 1), ("W", 1), ("NW", 1)]

    @staticmethod
    def as_png():
        return 'twos.png'


class Blob3(Piece):
    def __init__(self, is_white, position):
        super().__init__(is_white, position)
        self.value = 1

    def string(self):
        return self.colour_case() + "Blob3  "

    def as_char(self):
        return super().as_char("j")

    def direction_moves(self):
        return [("N", 1), ("E", 1), ("S", 1), ("W", 1)]

    @staticmethod
    def as_png():
        return 'threes.png'


class Cleric(Piece):
    def __init__(self, is_white, position):
        super().__init__(is_white, position)
        self.value = 5

    def direction_moves(self):
        return [("NE", 10), ("SE", 10), ("SW", 10), ("NW", 10)]

    def moves(self):
        moves = []
        for i in range(10):
            for j in range(10):
                moves.append((i, j))
        return moves

    def takes(self):
        return []

    def string(self):
        return self.colour_case() + "Cleric "

    def as_char(self):
        return super().as_char("c")

    @staticmethod
    def as_png():
        return 'bishops.png'


class Chicken(Piece):
    """
    The chicken simply has many available methods for each piece it could inherit.
    """

    def __init__(self, is_white, position):
        super().__init__(is_white, position)
        self.value = 3

    def pawn_moves(self):
        row, col = self.position
        if self.is_white:
            return [(row - 1, col)]
        else:
            return [(row + 1, col)]

    def pawn_takes(self):
        row, col = self.position
        if self.is_white:
            return [(row - 1, col + 1), (row - 1, col - 1)]
        else:
            return [(row + 1, col + 1), (row + 1, col - 1)]

    def pawn_direction_moves(self):
        if not self.has_moved:
            if self.is_white:
                return [("N", 3)]
            else:
                return [("S", 3)]
        else:
            return []

    def rook_direction_moves(self):
        return [("N", 10), ("E", 10), ("S", 10), ("W", 10)]

    def bishop_direction_moves(self):
        return [("NE", 10), ("SE", 10), ("SW", 10), ("NW", 10)]

    def king_moves(self):
        row, col = self.position
        return [(row + 1, col - 1), (row + 1, col), (row + 1, col + 1),
                (row, col - 1), (row, col + 1),
                (row - 1, col - 1), (row - 1, col), (row - 1, col + 1)]

    def knight_moves(self):
        row, col = self.position
        return [(row + 2, col - 1), (row + 2, col + 1),
                (row + 1, col - 2), (row + 1, col + 2),
                (row - 1, col - 2), (row - 1, col + 2),
                (row - 2, col - 1), (row - 2, col + 1)]

    def frog_moves(self):
        row, col = self.position
        return [(row + 3, col),
                (row + 2, col - 2), (row + 2, col), (row + 2, col + 2),
                (row + 1, col - 1), (row + 1, col), (row + 1, col + 1),
                (row, col - 3), (row, col - 2), (row, col - 1), (row, col + 1), (row, col + 2), (row, col + 3),
                (row - 1, col - 1), (row - 1, col), (row - 1, col + 1),
                (row - 2, col - 2), (row - 2, col), (row - 2, col + 2),
                (row - 3, col)]

    def cleric_moves(self):
        moves = []
        for i in range(10):
            for j in range(10):
                moves.append((i, j))
        return moves

    def blob0_direction_moves(self):
        return [("N", 2), ("NE", 1), ("E", 2), ("SE", 1), ("S", 2), ("SW", 1), ("W", 2), ("NW", 1)]

    def blob0_dependant_moves(self):
        row, col = self.position
        return [[(row - 2, col - 1), (row - 1, col - 1)],
                [(row - 2, col + 1), (row - 1, col + 1)],
                [(row - 1, col - 2), (row - 1, col - 1)],
                [(row - 1, col + 2), (row - 1, col + 1)],
                [(row + 1, col - 2), (row + 1, col - 1)],
                [(row + 1, col + 2), (row + 1, col + 1)],
                [(row + 2, col - 1), (row + 1, col - 1)],
                [(row + 2, col + 1), (row + 1, col + 1)],
                ]

    def blob1_direction_moves(self):
        return [("N", 2), ("NE", 1), ("E", 2), ("SE", 1), ("S", 2), ("SW", 1), ("W", 2), ("NW", 1)]

    def blob2_direction_moves(self):
        return [("N", 1), ("NE", 1), ("E", 1), ("SE", 1), ("S", 1), ("SW", 1), ("W", 1), ("NW", 1)]

    def blob3_direction_moves(self):
        return [("N", 1), ("E", 1), ("S", 1), ("W", 1)]

    def panda_take(self):
        self.invulnerable = True

    def tick(self):
        self.invulnerable = False

    def string(self):
        return self.colour_case() + "Chicken"

    def as_char(self):
        if self.invulnerable:
            return super().as_char("y")
        elif not self.has_moved:
            return super().as_char("o")
        return super().as_char("h")

    @staticmethod
    def as_png():
        return 'chickens.png'


class Egg(Piece):
    def __init__(self, is_white, position):
        super().__init__(is_white, position)
        self.value = 1
        self.timeUntilHatch = 6

    def string(self):
        return self.colour_case() + "Egg    "

    def as_char(self):
        if self.is_white:
            return ['0', '1', '2', '3', '4', '5', '6'][self.timeUntilHatch]
        else:
            return [')', '!', '"', '£', '$', '%', "^"][self.timeUntilHatch]

    def tick(self):
        self.timeUntilHatch = self.timeUntilHatch - 1
        if self.timeUntilHatch == 0:
            return Chicken(is_white=self.is_white, position=self.position)

    def char_to_hatch_time(self, char):
        char_dict = {"6": 6, "5": 5, "4": 4, "3": 3, "2": 2, "1": 1, "0": 0, "^": 6, "%": 5, "$": 4, "£": 3, '"': 1,
                     "!": 1, ")": 0}
        self.timeUntilHatch = char_dict[char]

    @staticmethod
    def as_png():
        return 'eggs.png'


class Wall(Piece):
    def __init__(self, is_white, position):
        super().__init__(is_white, position)
        self.invulnerable = True

    def as_char(self):
        return '#'

    @staticmethod
    def as_png():
        return 'rooks.png'


class Death(Piece):
    def __init__(self, is_white, position):
        super().__init__(is_white, position)
        self.value = 100

    def string(self):
        return self.colour_case() + "Death  "

    def as_char(self):
        return "8" if self.is_white else "*"

    def direction_moves(self):
        return [("N", 10), ("NE", 10), ("E", 10), ("SE", 10), ("S", 10), ("SW", 10), ("W", 10), ("NW", 10)]

    def moves(self):
        row, col = self.position
        return [(row + 2, col - 1), (row + 2, col + 1),
                (row + 1, col - 2), (row + 1, col + 2),
                (row - 1, col - 2), (row - 1, col + 2),
                (row - 2, col - 1), (row - 2, col + 1)]

    def take(self, start_position, end_position):
        self.invulnerable = True

    def tick(self):
        self.invulnerable = False

    @staticmethod
    def as_png():
        return 'skulls.png'
