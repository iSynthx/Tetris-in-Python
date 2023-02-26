from random import randint
from typing import List, Tuple

from pygame import Rect

from globals import GAME_COLORS, SQUARE_SIZE, MAX_Y_AXIS, MAX_X_AXIS

# ====
I_TETROMINO = [
    [True, True, True, True],
    [False, False, False, False],
    [False, False, False, False],
    [False, False, False, False],
]

# ==
# ==
O_TETROMINO = [
    [True, True, False, False],
    [True, True, False, False],
    [False, False, False, False],
    [False, False, False, False],
]

# ===
#  =
T_TETROMINO = [
    [True, True, True, False],
    [False, True, False, False],
    [False, False, False, False],
    [False, False, False, False],
]

#  =
#  =
# ==
J_TETROMINO = [
    [False, True, False, False],
    [False, True, False, False],
    [True, True, False, False],
    [False, False, False, False],
]

#  =
#  =
#  ==
L_TETROMINO = [
    [False, True, False, False],
    [False, True, False, False],
    [False, True, True, False],
    [False, False, False, False],
]

#  ==
# ==
S_TETROMINO = [
    [False, True, True, False],
    [True, True, False, False],
    [False, False, False, False],
    [False, False, False, False],
]

# ==
#  ==
Z_TETROMINO = [
    [True, True, False, False],
    [False, True, True, False],
    [False, False, False, False],
    [False, False, False, False],
]

AVAILABLE_TETROMINOS = [
    I_TETROMINO, O_TETROMINO, T_TETROMINO, J_TETROMINO, L_TETROMINO, S_TETROMINO, Z_TETROMINO
]


class Tetromino:
    """
    Represents a Tetris piece (Tetromino).
    Initializes a random piece everytime.
    :arg fill_position Matrix with each square positions
    :arg color of the piece
    :arg on_bottom if the piece has reached the bottom
    :arg left Pivot position of the piece
    :arg top Pivot position of the piece
    """
    fill_position: List[List[bool]] = [[False for _ in range(4)] for _ in range(4)]  # grid 4X4
    color: Tuple[int] = GAME_COLORS["WHITE"]  # white
    on_bottom: bool = False
    left: int = 0
    top: int = 0

    def __init__(self, **kwargs):
        random_idx_piece = randint(0, len(AVAILABLE_TETROMINOS) - 1)
        self.fill_position = AVAILABLE_TETROMINOS[random_idx_piece]
        if 'top' in kwargs:
            self.top = kwargs["top"]
        if 'left' in kwargs:
            self.left = kwargs["left"]
        if 'color' in kwargs:
            self.color = kwargs["color"]
        # TODO apply random transformation/reflection/rotation
        # TODO control appearence rates

    def as_sprite(self) -> List[Rect]:
        """
        Returns a list of rect objects drawn on the correct positions,
        depending on the type of piece.
        Positions: (top+(n_row*square_size)) ; (left+(n_col*square_size))
        """
        rects = []
        for i, row in enumerate(self.fill_position):
            for j, square in enumerate(row):
                if square:
                    # Top Position + Height of the Square + (Height of the Square * Vertical Matrix Position )
                    self._check_bottom_collision(self.top + SQUARE_SIZE + (SQUARE_SIZE * i))
                    rects.append(
                        Rect((self.left + (j * SQUARE_SIZE), self.top + (i * SQUARE_SIZE)), (SQUARE_SIZE, SQUARE_SIZE))
                    )
        return rects

    def set_position(self, top: int, left: int):
        """
        Sets the pivot positions of the piece.
        :param left:
        :param top:
        """
        self.left = left
        self.top = top

    def move_left(self):
        """
        Move the piece to the left.
        (Shifts one Square Size to the left.)
        """
        if (self.left - SQUARE_SIZE) >= 0:
            self.left -= SQUARE_SIZE

    def move_right(self):
        """
        Move the piece to the right.
        (Shifts one Square Size to the right.)
        """
        rects = self.as_sprite()
        right_collide = False
        for rect in rects:
            if (rect.right + SQUARE_SIZE) > MAX_X_AXIS:
                right_collide = True
        if not right_collide:
            self.left += SQUARE_SIZE

    def _check_bottom_collision(self, y_position: int):
        """
        Returns true if the provided position from the piece rect is on the bottom.
        :param y_position: Calculated position of the rect.
        """
        if not self.on_bottom and y_position == MAX_Y_AXIS:
            self.on_bottom = True

    def _debug_piece(self):
        """
        Displays debug information about the Tetromino on the terminal.
        """
        print(f"""[!] Current Piece: Top: {self.top}; Left: {self.left}""")
