"""i have no thoughts"""

from pygame.colordict import THECOLORS
import pygame
from canvas_utils import GRID_SIZE, get_click_pos, initialize_screen, \
    BLACK, in_circle, WIDTH, HEIGHT, PALETTE_WIDTH
import sys

from Map import Map
from Node import _Node

LINE_COLORS = ['blue', 'red', 'yellow', 'green', 'brown', 'purple', 'orange',
               'pink']


class User:
    """ummm i"m just here for the lols"""
    metro_map: Map
    _screen: pygame.Surface
    _curr_opt: str
    opt_to_center: dict[str: tuple[int, int]]

    def __init__(self, init_selected: str):
        self.metro_map = Map()
        self._screen = initialize_screen((WIDTH + PALETTE_WIDTH, HEIGHT)
                                         , [pygame.MOUSEBUTTONDOWN])
        self.opt_to_center = {}
        self._curr_opt = init_selected

        while True:
            self.draw_grid()
            self.create_palette()
            self.set_selection(self._curr_opt)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_mouse_click(event, (WIDTH, HEIGHT), False)

            pygame.display.update()

    def draw_grid(self) -> None:
        """Draws a square grid on the given surface.

        The drawn grid has GRID_SIZE columns and rows.
        You can use this to help you check whether you are drawing nodes and edges in the right spots.
        """
        color = THECOLORS['grey']
        width, height = WIDTH, HEIGHT

        pygame.draw.line(self._screen, color, (0, 0), (width, height))
        pygame.draw.line(self._screen, color, (0, height), (width, 0))

        for dim in range(1, GRID_SIZE):
            x = dim * (width // GRID_SIZE)  # for column (vertical lines)
            y = dim * (height // GRID_SIZE)  # for row (horizontal lines)

            pygame.draw.line(self._screen, color, (x, 0), (x, height))
            pygame.draw.line(self._screen, color, (0, y), (width, y))

            pygame.draw.line(self._screen, color, (x, 0), (0, y))
            pygame.draw.line(self._screen, color, (width - x, height), (width, height - y))
            pygame.draw.line(self._screen, color, (x, 0), (width, height - y))
            pygame.draw.line(self._screen, color, (0, y), (width - x, height))

    def handle_mouse_click(self, event: pygame.event.Event,
                           screen_size: tuple[int, int],
                           first: bool) -> None:
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


class Admin(User):
    """Hello, I am the Creator"""

    def __init__(self):
        super(Admin, self).__init__('blue')

    def set_color(self, new_color: str):
        """Set color of track/node created.

        Preconditions:
            - new_color in LINE_COLORS
        """
        self._curr_opt = new_color

    def handle_mouse_click(self, event: pygame.event.Event,
                           screen_size: tuple[int, int],
                           first: bool) -> None:
        """Handle a mouse click event.

        A pygame mouse click event object has two attributes that are important for this method:
            - event.pos: the (x, y) coordinates of the mouse click
            - event.button: an int representing which mouse button was clicked.
                            1: left-click, 3: right-click

        The screen_size is a tuple of (width, height), and should be used together with
        event.pos to determine which cell is being clicked.

        If the click is within the area

        Preconditions:
            - event.type == pygame.MOUSEBUTTONDOWN
            - screen_size[0] >= 200
            - screen_size[1] >= 200
        """
        coordinates = get_click_pos(event)

        name = ...
        colors = ...
        is_station = ...

        if event.button == 3 and first and self.metro_map.node_exists(coordinates, kind='station'):
            event_2 = pygame.event.wait()
            self.handle_mouse_click(event_2, screen_size, not first)

        elif event.button == 3 and not first and self.metro_map.node_exists(coordinates, kind='station'):
            self.metro_map.add_track()

        elif event.button == 1 and not self.metro_map.node_exists(coordinates, kind='station'):
            radius = (PALETTE_WIDTH // 2)

            for option in self.opt_to_center:
                if in_circle(radius, self.opt_to_center[option], coordinates):
                    self.set_color(option)
                    return
            # self.metro_map.add_node(name, colors, coordinates, is_station)

        else:
            return

    def create_palette(self) -> None:
        """Draw the palette of colors available to the user to choose
            from. This color will be used to draw on the screen"""

        radius = (PALETTE_WIDTH // 2)
        ht = radius

        for color in LINE_COLORS:
            pygame.draw.circle(self._screen, THECOLORS[color], (WIDTH + radius, ht),
                               radius - 5)
            self.opt_to_center[color] = (WIDTH + radius, ht)
            ht += 4 * radius

    def set_selection(self, palette_choice: str) -> None:
        """Darkens the borders of the selected color from the palette provided.

        Preconditions:
            - palette_choice in self.opt_to_center
        """
        radius = (PALETTE_WIDTH // 2)

        target = self.opt_to_center[palette_choice]

        pygame.draw.circle(self._screen, BLACK, target,
                           radius - 5, 5)


class Client(User):
    """Hello, I am the follower"""

    _curr_optimization: str

    def __init__(self):
        super(Client, self).__init__()
        self._curr_optimization = 'distance'

    def handle_mouse_click(self, event: pygame.event.Event,
                           screen_size: tuple[int, int],
                           first: bool) -> None:
        pass

    def create_palette(self) -> None:
        pass

    def set_selection(self, palette_choice: str) -> None:
        """Darkens the borders of the selected optimization from the palette provided.
        Also changes self._curr_optimization that represents the selected option to the
        selected one.
        """
        pass
