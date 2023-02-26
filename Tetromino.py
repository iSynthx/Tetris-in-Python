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
    :arg left Pivot position of the piece
    :arg top Pivot position of the piece
    """
    fill_position: List[List[bool]] = [[False for _ in range(4)] for _ in range(4)]  # grid 4X4
    color: Tuple[int] = GAME_COLORS["WHITE"]  # white
    left: int = 0
    top: int = 0
    sprite: List[Rect] = []

    def __init__(self, **kwargs):
        if 'top' in kwargs:
            self.top = kwargs["top"]
        if 'left' in kwargs:
            self.left = kwargs["left"]
        if 'color' in kwargs:
            self.color = kwargs["color"]
        # Choose random piece
        random_idx_piece = randint(0, len(AVAILABLE_TETROMINOS) - 1)
        # Save the piece fill matrix
        self.fill_position = AVAILABLE_TETROMINOS[random_idx_piece]
        # Generate the list of Rects (Sprite)
        self.build_sprite()
        # TODO apply random transformation/reflection/rotation
        # TODO control appearence rates

    def build_sprite(self):
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
                    rects.append(
                        Rect((self.left + (j * SQUARE_SIZE), self.top + (i * SQUARE_SIZE)), (SQUARE_SIZE, SQUARE_SIZE))
                    )
        self.sprite = rects

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
        # Rebuild sprite
        self.build_sprite()

    def move_right(self):
        """
        Move the piece to the right.
        (Shifts one Square Size to the right.)
        """
        right_collide = False
        for rect in self.sprite:
            if (rect.right + SQUARE_SIZE) > MAX_X_AXIS:
                right_collide = True
        if not right_collide:
            self.left += SQUARE_SIZE
            # Rebuild sprite
            self.build_sprite()

    def check_bottom_collision(self):
        """
        Returns true if the piece is on the bottom.

        """
        for i, rect in enumerate(self.sprite):
            if rect.bottom == MAX_Y_AXIS:
                return True
        return False

    def _debug_piece(self):
        """
        Displays debug information about the Tetromino on the terminal.
        """
        print(f"""[!] Current Piece: Top: {self.top}; Left: {self.left}""")
