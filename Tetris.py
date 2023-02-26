import sys
import time
from random import randint
from typing import List, Optional

import pygame
from pygame import Surface, mixer, QUIT, KEYDOWN, K_ESCAPE, K_LEFT, K_s, K_RIGHT
from pygame.threads import Thread

from Tetromino import Tetromino
from globals import GAME_COLORS, SQUARE_SIZE, MUSIC_FILENAME, TETROMINO_COLORS, MAX_X_AXIS


class Tetris:
    """
    Singleton that represents the game itself.
    :arg window (Window/Surface object of the game)
    :arg spawn_piece (Should a piece be spawned?)
    :arg pieces (Pieces currently in the game)
    """
    window: Surface = None
    should_spawn_piece: bool = True
    pieces: List[Tetromino] = []
    current_piece: Optional[Tetromino] = None

    def __init__(self, window: Surface):
        self.window = window
        mixer.music.load(MUSIC_FILENAME)
        mixer.music.play()

    def start_game_loop(self):
        """
        Executes the main game loop.
        """
        self._clear_window()
        while True:
            self._handle_player_events()
            if self.should_spawn_piece:
                # Generate a new piece on top of the window in the center of the X axis.
                self._spawn_piece()
            # Draw all the game pieces
            self._draw_pieces()
            # if the current piece has hit the bottom => spawn new piece
            # OR the current piece has hit another piece => spawn new piece
            if self.current_piece.on_bottom or self.check_ingame_pieces_collision():
                self.should_spawn_piece = True
            else:
                # Drop the current piece
                self._drop_current_piece()
            # Wait
            time.sleep(1)
            # Disable last frame
            self._clear_window()

    def check_ingame_pieces_collision(self):
        """
        Checks if the current piece is colliding with any of the drawn pieces on the window.
        """
        # Obtain the current piece rects
        current_piece_rects = self.current_piece.as_sprite()
        # For each piece ingame
        for piece in self.pieces:
            # if it isnt the current playable piece...
            if piece != self.current_piece:
                # TODO Improvement -> Dont recalculate sprites; Save them inside the obj.
                # Get the current piece as rects
                piece_rects = piece.as_sprite()
                # For rect in the current piece
                for rect in piece_rects:
                    # for rect in current game piece rects
                    for current_rect in current_piece_rects:
                        if current_rect.bottom == rect.top: # TODO Theres a bug here.
                            return True
        return False

    def _clear_window(self):
        """
        Clears the game window (Surface).
        :return:
        """
        self.window.fill(GAME_COLORS["BLACK"])

    def _drop_current_piece(self):
        """
        Drops the current piece.
        """
        self._drop_piece(piece=self.current_piece)

    def _drop_piece(self, piece: Tetromino):
        """
        Drops piece by a SQUARE_SIZE value.
        """
        piece.set_position(left=piece.left, top=piece.top + SQUARE_SIZE)

    def _spawn_piece(self):
        """
        Generates a Tetromino object, adds it to the game and stops more pieces from spawning.
        """
        # Convert dict to list
        available_colors = list(TETROMINO_COLORS.values())
        # Generate random index to choose colors
        color_idx = randint(0, len(available_colors) - 1)
        self.current_piece = Tetromino(top=0, left=MAX_X_AXIS / 3, color=available_colors[color_idx])
        self.pieces.append(self.current_piece)
        self.should_spawn_piece = False

    def _draw_piece(self, piece: Tetromino):
        """
        Given a Tetromino object, draw it on the pygame window.
        :arg piece Tetromino Object
        """
        # Obtain list of rects
        sprite = piece.as_sprite()
        # For every rect, draw it on the window with the piece color.
        for rect in sprite:
            rect_kwargs = {
                'surface': self.window,
                'color': piece.color,
                'rect': rect
            }
            pygame.draw.rect(**rect_kwargs)  # Draw Rectangle

    def _draw_pieces(self):
        """
        Draws all the game window pieces.
        """
        for piece in self.pieces:
            self._draw_piece(piece=piece)
        pygame.display.flip()  # Update the game surface

    def _handle_player_events(self):
        """
        Handles user keyboard events.
        """

        for event in pygame.event.get():
            # if the event is to quit or press Esc
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                sys.exit(0)
            elif event.type == KEYDOWN:
                key = event.key
                if key == K_LEFT:
                    self.current_piece.move_left()
                elif key == K_RIGHT:
                    self.current_piece.move_right()
                elif key == K_s:
                    time.sleep(10)

