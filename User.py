"""i have no thoughts"""

from pygame.colordict import THECOLORS
import pygame

from Map import Map
from Node import _Node

SCREEN_SIZE = (600, 600)  # (width, height)
GRID_SIZE = 20


def initialize_screen(screen_size: tuple[int, int], allowed: list) -> pygame.Surface:
    """Initialize pygame and the display window.

    allowed is a list of pygame event types that should be listened for while pygame is running.
    """
    pygame.display.init()
    pygame.font.init()
    screen = pygame.display.set_mode(screen_size)
    screen.fill(THECOLORS['white'])
    pygame.display.flip()

    pygame.event.clear()
    pygame.event.set_blocked(None)
    pygame.event.set_allowed([pygame.QUIT] + allowed)

    return screen


def draw_text(screen: pygame.Surface, text: str, pos: tuple[int, int]) -> None:
    """Draw the given text to the pygame screen at the given position.

    pos represents the *upper-left corner* of the text.
    """
    font = pygame.font.SysFont('inconsolata', 22)
    text_surface = font.render(text, True, THECOLORS['black'])
    width, height = text_surface.get_size()
    screen.blit(text_surface,
                pygame.Rect(pos, (pos[0] + width, pos[1] + height)))


def draw_grid(screen: pygame.Surface) -> None:
    """Draws a square grid on the given surface.

    The drawn grid has GRID_SIZE columns and rows.
    You can use this to help you check whether you are drawing nodes and edges in the right spots.
    """
    color = THECOLORS['grey']
    width, height = screen.get_size()

    pygame.draw.line(screen, color, (0, 0), (width, height))
    pygame.draw.line(screen, color, (0, height), (width, 0))

    for dim in range(1, GRID_SIZE):
        x = dim * (width // GRID_SIZE)  # for column (vertical lines)
        y = dim * (height // GRID_SIZE)  # for row (horizontal lines)

        pygame.draw.line(screen, color, (x, 0), (x, height))
        pygame.draw.line(screen, color, (0, y), (width, y))

        pygame.draw.line(screen, color, (x, 0), (0, y))
        pygame.draw.line(screen, color, (width - x, height), (width, height - y))
        pygame.draw.line(screen, color, (x, 0), (width, height - y))
        pygame.draw.line(screen, color, (0, y), (width - x, height))


class User:
    """ummm i"m just here for the lols"""
    metro_map: Map

    def node_exists(self, coordinates: tuple[float, float], kind: str = '') -> bool:
        """Return whether a node already exists at the given coordinates.

        Preconditions:
            - kind in {'', 'station', 'corner'}
        """
        for node in self.metro_map.get_all_nodes(kind):
            if node.coordinates == coordinates:
                return True
        return False

    def handle_mouse_click(self, event: pygame.event.Event,
                           screen_size: tuple[int, int],
                           first: bool) -> None:
        """Handle a mouse click event.

        This is an abstract method.
        """
        raise NotImplementedError


class Admin(User):
    """Hello, I am the Creator"""

    def handle_mouse_click(self, event: pygame.event.Event,
                           screen_size: tuple[int, int],
                           first: bool) -> None:
        """Handle a mouse click event.

        A pygame mouse click event object has two attributes that are important for this method:
            - event.pos: the (x, y) coordinates of the mouse click
            - event.button: an int representing which mouse button was clicked.
                            1: left-click, 3: right-click

        The screen_size is a tuple of (width, height), and should be used together with
        event.pos to determine which cell is being clicked. If a click happens exactly on
        the boundary between two cells, you may decide which cell is selected.

        Preconditions:
            - event.type == pygame.MOUSEBUTTONDOWN
            - screen_size[0] >= 200
            - screen_size[1] >= 200
        """
        coordinates = (round(event.pos[0] / GRID_SIZE) * GRID_SIZE,
                       round(event.pos[1] / GRID_SIZE) * GRID_SIZE)

        name = ...
        colors = ...
        is_station = ...

        if coordinates[0] % GRID_SIZE != 0 or coordinates[1] % GRID_SIZE != 0:
            return

        elif event.button == 3 and first and self.node_exists(coordinates, kind='station'):
            event_2 = pygame.event.wait()
            self.handle_mouse_click(event_2, screen_size, not first)

        elif event.button == 3 and not first and self.node_exists(coordinates, kind='station'):
            self.metro_map.add_track()

        elif event.button == 1 and not self.node_exists(coordinates, kind='station'):
            self.metro_map.add_node(name, colors, coordinates, is_station)

        else:
            return
