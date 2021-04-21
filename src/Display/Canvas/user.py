"""
This file contains the details of abstract class User, of which
admin and client inherit.
"""
from typing import Optional

from pygame.colordict import THECOLORS
import pygame

from src.Base.node import Node
from src.Display.Utils.general_utils import GRID_SIZE, initialize_screen, WIDTH, HEIGHT, PALETTE_WIDTH

LINE_COLORS = ['blue', 'red', 'yellow', 'green', 'brown', 'purple', 'orange',
               'pink']


class User:
    """The user class is the class that represents the 2 types of users that can access this
    application such as the admin who creates a metro transit map and the client who can
    select the starting station and destination station to create a final shortest or cheapest
    route displaying it on the map.

    Instance Attributes:
        - opt_to_center: Dictionary which maps the option as a string to the center
        (top-left in the case of rectangle) coordinates of that option as a tuple.

    """

    # Private Instance Attributes:
    #   - screen: The screen being used by pygame.
    #   - _curr_opt: The current optimization option which can be colors in the case of admin or
    #               'distance' or 'cost' in the case of client.
    #   - _curr_zoom: The current zoom level of the canvas
    #   - _curr_shift: The current amount by which the map is displaced

    _screen: pygame.Surface
    _curr_zoom: int
    _curr_shift: list[int, int]
    _curr_opt: str
    opt_to_center: dict[str: tuple[int, int]]
    city_name: str

    def __init__(self, init_selected: str, city_name: str) -> None:
        self._screen = initialize_screen((WIDTH + PALETTE_WIDTH, HEIGHT))
        self.opt_to_center = {}
        self._curr_opt = init_selected
        self.city_name = city_name
        self._curr_zoom = 1
        self._curr_shift = [0, 0]

    def draw_grid(self) -> None:
        """Draws a square grid on the given surface.

        The drawn grid has GRID_SIZE columns and rows.
        You can use this to help you check whether you are drawing nodes and edges
        at the right spots.
        """
        color = THECOLORS['grey']
        width, height = WIDTH, HEIGHT
        curr_grid_size = self._curr_zoom * GRID_SIZE

        pygame.draw.line(self._screen, color, (0, 0), (width, height))
        pygame.draw.line(self._screen, color, (0, height), (width, 0))

        for dim in range(1, curr_grid_size):
            x = dim * (width // curr_grid_size)  # for column (vertical lines)
            y = dim * (height // curr_grid_size)  # for row (horizontal lines)

            pygame.draw.line(self._screen, color, (x, 0), (x, height))
            pygame.draw.line(self._screen, color, (0, y), (width, y))

            pygame.draw.line(self._screen, color, (x, 0), (0, y))
            pygame.draw.line(self._screen, color, (width - x, height), (width, height - y))
            pygame.draw.line(self._screen, color, (x, 0), (width, height - y))
            pygame.draw.line(self._screen, color, (0, y), (width - x, height))

    def scale_factor_transformations(self, actual: tuple[int, int], reverse: bool = False) -> tuple[int, int]:
        """Transforms the actual location (scale factor of 1) to where it should be displayed on
        the map"""
        h_shift = self._curr_shift[0] * (WIDTH // (self._curr_zoom * GRID_SIZE))
        v_shift = self._curr_shift[1] * (HEIGHT // (self._curr_zoom * GRID_SIZE))

        if reverse:
            return (actual[0] * self._curr_zoom + h_shift,
                    actual[1] * self._curr_zoom + v_shift)

        return (actual[0] // self._curr_zoom - h_shift,
                actual[1] // self._curr_zoom - v_shift)

    def handle_zoom_in(self) -> None:
        """Handles key down even for zooming out
        """
        if self._curr_zoom != 1:
            self._curr_zoom //= 2

    def handle_zoom_out(self) -> None:
        """Handles key down even for zooming in
        """
        if self._curr_zoom != 4:
            self._curr_zoom *= 2

    def handle_d_shift(self) -> None:
        """Handles key down even for up shift
        """
        self._curr_shift[1] += 1

    def handle_u_shift(self) -> None:
        """Handles key down even for down shift
        """
        self._curr_shift[1] -= 1

    def handle_r_shift(self) -> None:
        """Handles key down even for left shift
        """
        self._curr_shift[0] += 1

    def handle_l_shift(self) -> None:
        """Handles key down even for right shift
        """
        self._curr_shift[0] -= 1

    def handle_mouse_click(self, event: pygame.event.Event,
                           screen_size: tuple[int, int], ) -> None:
        """Handle a mouse click event.

        This is an abstract method.
        """
        raise NotImplementedError

    def create_palette(self) -> None:
        """Draw the palette of options available to the user to choose
        from. These options will be used to draw on the screen"""
        raise NotImplementedError

    def set_selection(self, palette_choice: str) -> None:
        """Darkens the borders of the selected option from the palette provided.
        Also changes the parameter that represents the selected option to the
        selected one.
        """
        raise NotImplementedError

    def display(self) -> None:
        """Responsible for refreshing the screen and displaying required edges and nodes
        onto the map."""
        raise NotImplementedError

    def hover_display(self) -> None:
        """Displays the information of the station
        when hovered over by the administrator or the client.

        The amount of information provided and the means of gaining this
        information is different in both scenarios.

        """
        raise NotImplementedError

    def node_exists(self, coordinates: tuple[float, float]) -> Optional[Node]:
        """Return the node if it exists at given coordinates. Else, return None.
        """
        raise NotImplementedError
