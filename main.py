from typing import Optional

import pygame

from Tetris import Tetris
from globals import GAME_CONFIG

GAME: Optional[Tetris] = None

if __name__ == '__main__':
    # Initialize display
    window = pygame.display.set_mode(GAME_CONFIG['screensize'])
    # Initialize engine
    pygame.init()
    # Block mouse interaction
    pygame.event.set_blocked(pygame.MOUSEMOTION)
    # Create timer to control the frames
    pygame.time.set_timer(pygame.USEREVENT + 1, GAME_CONFIG["timer_constant"])
    # Start clock
    clock = pygame.time.Clock()
    # Fill window with black
    GAME = Tetris(window=window)
    GAME.start_game_loop()
