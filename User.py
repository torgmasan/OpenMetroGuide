"""
This file contains the hierarchy of class User and its children Admin and Client.
"""
from typing import Optional

from pygame.colordict import THECOLORS
import pygame
from canvas_utils import GRID_SIZE, get_click_pos, initialize_screen, approximate_edge_click, \
    WHITE, BLACK, in_circle, WIDTH, HEIGHT, PALETTE_WIDTH, draw_text
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
    active_nodes: set[_Node]

    def __init__(self, init_selected: str) -> None:
        self.metro_map = Map()
        self._screen = initialize_screen((WIDTH + PALETTE_WIDTH, HEIGHT))
        self.opt_to_center = {}
        self._curr_opt = init_selected
        self.active_nodes = set()

    def display(self) -> None:
        """Responsible for refreshing the screen and displaying required edges and nodes
        onto the map."""
        while True:
            self._screen.fill(WHITE)
            self.draw_grid()
            self.create_palette()
            self.set_selection(self._curr_opt)

            # for node in self.active_nodes:
            #     self.metro_map.add_node(node.name, node.coordinates, node.is_station, node.zone)

            for node in self.active_nodes:
                if node.is_station:
                    pygame.draw.circle(self._screen, BLACK, node.coordinates, 5)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_mouse_click(event, (WIDTH, HEIGHT), False)

            pygame.display.update()

    def node_exists(self, coordinates: tuple[float, float], kind: str = '') -> Optional[_Node]:
        """Return the node if it exists at given coordinates. Else, return None.

        Preconditions:
            - kind in {'', 'station', 'corner'}
        """
        for node in self.active_nodes:
            if node.coordinates == coordinates:
                return node
        return None

    def draw_grid(self) -> None:
        """Draws a square grid on the given surface.

        The drawn grid has GRID_SIZE columns and rows.
        You can use this to help you check whether you are drawing nodes and edges
        at the right spots.
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

    def hover_display(self, event) -> None:
        """Displays the information of the station such as name and zone
        when hovered over by the administrator or the client.

        Preconditions:
            - event.type == pygame.MOUSEMOTION
        """
        pygame.init()
        for node in self.active_nodes:

            if node.is_station:
                station_circle = pygame.draw.circle(self._screen, BLACK, node.coordinates, 5)
                # Will we have to delete twice(or as many times visited) for this?

                new_screen = pygame.display.set_mode((300, 150))
                new_screen.fill(WHITE)

                while station_circle.collidepoint(event.pos):
                    draw_text(screen=new_screen, text='Station - ', font=27, pos=(10, 65))
                    draw_text(screen=new_screen, text=node.name, font=27, pos=(25, 65))

                    draw_text(screen=new_screen, text='Zone - ', font=27, pos=(10, 135))
                    draw_text(screen=new_screen, text=node.zone, font=27, pos=(25, 135))

                    pygame.display.flip()


class Admin(User):
    """Admin is the aspect of the User which creates the metro map
    using pygame mouse click event objects. Once the map has been created
    on the screen, it is converted to a Map object. If the metro map is not connected,
    the Admin is given the option of editing the map again.
    """

    def __init__(self) -> None:
        """Initializes the Instance Attributes of the child class of User.
        """
        super(Admin, self).__init__('blue')

    def set_color(self, new_color: str):
        """Set color of track/node created.

        Preconditions:
            - new_color in LINE_COLORS
        """
        self._curr_opt = new_color

    def handle_mouse_click(self, event: pygame.event.Event,
                           screen_size: tuple[int, int], first: bool) -> None:
        """Handle a mouse click event.

        A pygame mouse click event object has two attributes that are important for this method:
            - event.pos: the (x, y) coordinates of the mouse click
            - event.button: an int representing which mouse button was clicked.
                            1: left-click, 3: right-click

        The screen_size is a tuple of (width, height), and should be used together with
        event.pos to determine which cell is being clicked.

        If the click is within the area of the palette, then check if it is within any color and
        handle accordingly.

        If the click is within the grid, check if the click is left or right.
        A right click is handled by creating a track. If left click is being pressed,
        a station created. Delete an existing track by right clicking on it, and delete
        a corner/station by left clicking on it.
        handle_mouse_click updates and maintains active_nodes.

        Preconditions:
            - event.type == pygame.MOUSEBUTTONDOWN
            - screen_size[0] >= ...
            - screen_size[1] >= ...
        """
        coordinates = get_click_pos(event)

        if event.pos[0] > WIDTH:  # The click is on the color palette
            radius = (PALETTE_WIDTH // 2)

            for option in self.opt_to_center:
                if in_circle(radius, self.opt_to_center[option], coordinates):
                    self.set_color(option)
                    return
        else:  # The click is on the map
            if event.button == 3:  # Right-click is for track
                line_coordinates = approximate_edge_click(event)
                n_1 = self.node_exists(line_coordinates[0])
                n_2 = self.node_exists(line_coordinates[1])

                # One of the nodes already exists, the other node has to be created and linked to
                # the pre-existing node
                if n_1 is None and n_2 is not None:
                    n_1 = _Node(name=str(line_coordinates[0]), is_station=False,
                                coordinates=line_coordinates[0], zone='')
                    self.active_nodes.add(n_1)
                    n_1.add_track(n_2, self._curr_opt)
                elif n_1 is not None and n_2 is None:
                    n_2 = _Node(name=str(line_coordinates[1]), is_station=False,
                                coordinates=line_coordinates[1], zone='')
                    self.active_nodes.add(n_2)
                    n_1.add_track(n_2, self._curr_opt)

                # Both nodes need to be created and linked to each other
                elif n_1 is None and n_2 is None:
                    n_1 = _Node(name=str(line_coordinates[0]), is_station=False,
                                coordinates=line_coordinates[0], zone='')
                    n_2 = _Node(name=str(line_coordinates[1]), is_station=False,
                                coordinates=line_coordinates[1], zone='')
                    self.active_nodes.add(n_1)
                    self.active_nodes.add(n_2)
                    n_1.add_track(n_2, self._curr_opt)

                # Both nodes already exist
                elif n_1 is not None and n_2 is not None:
                    if n_1.is_adjacent(n_2):
                        # if they already have a track between them, remove the track
                        n_1.remove_track(n_2)
                    else:
                        # else, add a track between them
                        n_1.add_track(n_2, self._curr_opt)

                    # if either or both of the nodes is a corner and is not connected
                    # to any other node, remove the node

                    if n_1.get_neighbours() == set() and not n_1.is_station:
                        self.active_nodes.remove(n_1)

                    if n_2.get_neighbours() == set() and not n_2.is_station:
                        self.active_nodes.remove(n_2)

                # pygame.draw.line(self._screen, self._curr_opt, line_coordinates[0],
                #                  line_coordinates[1], 3)

            elif event.button == 1:  # Left-click is for the nodes (station or corner)
                station = self.node_exists(coordinates)
                if station is None:
                    self.get_station_info(coordinates)
                else:
                    for neighbour in station.get_neighbours():
                        station.remove_track(neighbour)

                    self.active_nodes.remove(station)

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

    def get_station_info(self, coordinates: tuple[int, int]) -> None:
        """Gets the information from the admin
            about the station such as the
            name and zone.
        """
        pygame.init()
        screen = pygame.display.set_mode((700, 200))
        screen.fill(WHITE)

        base_font = pygame.font.Font(None, 32)
        pygame.display.set_caption('Station Information')
        name = ''
        zone = ''
        name_active = False
        zone_active = False
        chk = True
        while chk:

            screen.fill(WHITE)
            name_rect, zone_rect = _refresh_input_display(screen, name_active, zone_active)

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if name_rect.collidepoint(event.pos):
                        name_active = True
                        zone_active = False

                    if zone_rect.collidepoint(event.pos):
                        zone_active = True
                        name_active = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        chk = False
                        break

                    if event.key == pygame.K_BACKSPACE:

                        if zone_active:
                            zone = zone[:-1]

                        elif name_active:
                            name = name[:-1]

                    else:

                        if zone_active:
                            zone += event.unicode

                        if name_active:
                            name += event.unicode

            if not chk:
                initialize_screen((WIDTH + PALETTE_WIDTH, HEIGHT))
                station = _Node(name, coordinates, True, zone)
                self.active_nodes.add(station)
                self.display()
                break

            name_surface = base_font.render(name, True, (0, 0, 0))
            zone_surface = base_font.render(zone, True, (0, 0, 0))
            screen.blit(name_surface, (name_rect.x + 5, name_rect.y + 2.5))
            screen.blit(zone_surface, (zone_rect.x + 5, zone_rect.y + 2.5))
            pygame.display.flip()


def _refresh_input_display(screen: pygame.Surface,
                           active_name: bool, active_zone: bool) -> tuple[pygame.Rect, pygame.Rect]:
    """Displays all the textboxes asking the user for the
    name and zone of each station when added. This screen is always
    displayed.
    """
    active_color = pygame.Color((175, 238, 238))
    not_active_color = pygame.Color((119, 136, 153))

    if active_name:
        name_rect = pygame.Rect((295, 45, 400, 27))
        draw_text(screen, 'Enter the name of the Station ->', 27, (5, 50))
        pygame.draw.rect(screen, active_color, name_rect, 3)

    else:
        name_rect = pygame.Rect((295, 45, 400, 27))
        draw_text(screen, 'Enter the name of the Station ->', 27, (5, 50))
        pygame.draw.rect(screen, not_active_color, name_rect, 3)

    if active_zone:
        zone_rect = pygame.Rect((295, 115, 400, 27))
        draw_text(screen, 'Enter the zone of the Station ->', 27, (5, 120))
        pygame.draw.rect(screen, active_color, zone_rect, 3)

    else:
        zone_rect = pygame.Rect((295, 115, 400, 27))
        draw_text(screen, 'Enter the zone of the Station ->', 27, (5, 120))
        pygame.draw.rect(screen, not_active_color, zone_rect, 3)

    draw_text(screen, '(Click on name or zone to enter respective info and press enter when done)',
              20, (150, 170))

    return name_rect, zone_rect


class Client(User):
    """Client is the aspect of the User which displays a Map object on the screen,
    and then uses pygame mouse click event objects to determine the Client's
    starting point and final destination, and the variable of optimization the Client
    prefers. Then, the best possible route between the two stations is highlighted.
    """

    _curr_optimization: str

    def __init__(self) -> None:
        """ Initializes the Instance Attributes of
        the Client class which is a child of User.
        """
        super(Client, self).__init__()
        self._curr_optimization = 'distance'

    def handle_mouse_click(self, event: pygame.event.Event,
                           screen_size: tuple[int, int],
                           first: bool) -> None:
        """ Handles what happens once the client clicks the mouse.
        ...
        """
        pass

    def create_palette(self) -> None:
        """ ...
        """
        pass

    def set_selection(self, palette_choice: str) -> None:
        """Darkens the borders of the selected optimization from the palette provided.
        Also changes self._curr_optimization that represents the selected option to the
        selected one.
        """
        pass
