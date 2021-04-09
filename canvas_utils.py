"""This file contains helper functions which perform computations or
draw general assets on to the screen, which are present among multiple
screens and not unique to any one in particular. Also consists of static methods and
constants regarding pygame rendering."""

import pygame
import math


INSTRUCT_ADMIN = ["Left click on a point in the grid to add a Metro Station or a",
                  "Node to the Map. Additional Left click deletes Node/Station.",
                  "Right Click on a side or diagonal to add a track line that",
                  " connects two Nodes/Stations. Additional Right click deletes ",
                  "track. Click on a Palette to select color.",
                  "",
                  "                      PRESS ENTER TO CONTINUE."]

INSTRUCT_CLIENT = ""

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRID_SIZE = 20


def draw_text(screen: pygame.Surface, text: str, font: int, pos: tuple[int, int]) -> None:
    """Draw the given text to the pygame screen at the given position.

    pos represents the *upper-left corner* of the text.
    """
    font = pygame.font.SysFont('inconsolata', font)
    text_surface = font.render(text, True, BLACK)
    width, height = text_surface.get_size()
    screen.blit(text_surface,
                pygame.Rect(pos, (pos[0] + width, pos[1] + height)))


def get_click_pos(event: pygame.event.Event) -> tuple[int, int]:
    """Returns the coordinates of the mouse click"""
    return (round(event.pos[0] / GRID_SIZE) * GRID_SIZE,
            round(event.pos[1] / GRID_SIZE) * GRID_SIZE)


def initialize_screen(screen_size: tuple[int, int], allowed: list) -> pygame.Surface:
    """Initialize pygame and the display window.

    allowed is a list of pygame event types that should be listened for while pygame is running.
    """
    pygame.display.init()
    pygame.font.init()
    screen = pygame.display.set_mode(screen_size)
    screen.fill(WHITE)
    pygame.display.flip()

    pygame.event.clear()
    pygame.event.set_blocked(None)
    pygame.event.set_allowed([pygame.QUIT] + allowed)

    return screen


def in_circle(radius: int, centre_coordinates: tuple[int, int],
              entered_coordinates: tuple[int, int]) -> bool:
    """Check if the entered_coordinates is present inside the
    circle of given radius and centre_coordinates"""
    x_1, y_1 = centre_coordinates
    x_2, y_2 = entered_coordinates
    dist = math.sqrt((x_2 - x_1) ** 2 + (y_2 - y_1) ** 2)

    return dist <= radius
