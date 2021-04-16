"""This file contains helper functions which perform computations or
draw general assets on to the screen, which are present among multiple
screens and not unique to any one in particular. Also consists of static methods and
constants regarding pygame rendering."""

import math
import pygame

WIDTH = 800
HEIGHT = 800
GRID_SIZE = 20

PALETTE_WIDTH = 50

BOX_WIDTH = WIDTH // GRID_SIZE
BOX_HEIGHT = HEIGHT // GRID_SIZE

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


def get_click_pos(event: pygame.event.Event) -> tuple[int, int]:
    """Return the approximated coordinates of the mouse click for the station"""
    return (round(event.pos[0] / BOX_WIDTH) * BOX_WIDTH,
            round(event.pos[1] / BOX_HEIGHT) * BOX_HEIGHT)


def approximate_edge_click(event: pygame.event.Event) -> tuple[tuple[int, int], tuple[int, int]]:
    """Return the approximated coordinates of the mouse click for the track.

    https://en.wikipedia.org/wiki/Distance_from_a_point_to_a_line

    Preconditions:
        - 0<= event.pos[0] <= WIDTH
        - 0 <= event.pos[1] <= HEIGHT
    """
    x_0, y_0 = event.pos

    all_edges = _get_all_edges(event)

    min_distance_so_far = math.inf
    closest_edge_so_far = None

    for edge in all_edges:
        x_1, y_1 = edge[0]
        x_2, y_2 = edge[1]

        num = abs((x_2 - x_1) * (y_1 - y_0) - (x_1 - x_0) * (y_2 - y_1))
        den = math.sqrt((x_2 - x_1) ** 2 + (y_2 - y_1) ** 2)

        distance_from_edge = num / den

        if distance_from_edge < min_distance_so_far:
            min_distance_so_far = distance_from_edge
            closest_edge_so_far = edge

    return closest_edge_so_far


def _get_all_edges(event: pygame.event.Event) -> list[tuple[tuple[int, int], tuple[int, int]]]:
    """event is a pygame mouse click event object in one of the boxes of the grid.

    Return all edges in the box of the click (including the boundary edges).
    """
    top_left = ((event.pos[0] // BOX_WIDTH) * BOX_WIDTH,
                (event.pos[1] // BOX_HEIGHT) * BOX_HEIGHT)
    top_right = (top_left[0] + BOX_WIDTH, top_left[1])
    bottom_left = (top_left[0], top_left[1] + BOX_HEIGHT)
    bottom_right = (top_left[0] + BOX_WIDTH, top_left[1] + BOX_HEIGHT)

    return [(top_left, top_right), (top_left, bottom_left), (bottom_left, bottom_right),
            (top_right, bottom_right), (top_left, bottom_right), (top_right, bottom_left)]


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


if __name__ == '__main__':

    import doctest
    doctest.testmod()

    import python_ta
    python_ta.check_all(config={
        'max-line-length': 100,
        'extra-imports': ['pygame', 'math'],
        'max-nested-blocks': 4
    })
