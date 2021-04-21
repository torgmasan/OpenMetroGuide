"""This file contains helper functions which perform computations or
draw general assets on to the screen, which are present among multiple
screens and not unique to any one in particular. Also consists of static methods and
constants regarding pygame rendering."""

import math
import pygame

WIDTH = 800
HEIGHT = 800
PALETTE_WIDTH = 50

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


def draw_text(screen: pygame.Surface, text: str, font: int, pos: tuple[int, int],
              color: tuple[int, int, int] = BLACK) -> None:
    """Draw the given text to the pygame screen at the given position.

    pos represents the *upper-left corner* of the text.
    """
    font = pygame.font.SysFont('inconsolata', font)
    text_surface = font.render(text, True, color)
    width, height = text_surface.get_size()
    screen.blit(text_surface,
                pygame.Rect(pos, (pos[0] + width, pos[1] + height)))


def initialize_screen(screen_size: tuple[int, int]) -> pygame.Surface:
    """Initialize pygame and the display window.

    allowed is a list of pygame event types that should be listened for while pygame is running.
    """
    pygame.display.init()
    pygame.font.init()
    screen = pygame.display.set_mode(screen_size)
    screen.fill(WHITE)
    pygame.display.flip()

    return screen


def in_circle(radius: int, centre_coordinates: tuple[int, int],
              entered_coordinates: tuple[int, int]) -> bool:
    """Check if the entered_coordinates is present inside the
    circle of given radius and centre_coordinates"""
    x_1, y_1 = centre_coordinates
    x_2, y_2 = entered_coordinates
    dist = math.sqrt((x_2 - x_1) ** 2 + (y_2 - y_1) ** 2)

    return dist <= radius
