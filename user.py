"""
This file contains the hierarchy of class User and its children Admin and Client.
"""
from typing import Optional
import sys

from pygame.colordict import THECOLORS
import pygame
from canvas_utils import GRID_SIZE, get_click_pos, initialize_screen, approximate_edge_click, \
    WHITE, BLACK, in_circle, WIDTH, HEIGHT, PALETTE_WIDTH, draw_text


from map import Map
from node import Node
from storage_manager import store_map, init_db

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

    _screen: pygame.Surface
    _curr_opt: str
    opt_to_center: dict[str: tuple[int, int]]
    city_name: str

    def __init__(self, init_selected: str, city_name: str) -> None:
        self._screen = initialize_screen((WIDTH + PALETTE_WIDTH, HEIGHT))
        self.opt_to_center = {}
        self._curr_opt = init_selected
        self.city_name = city_name

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


class Admin(User):
    """Admin is the aspect of the User which creates the metro map
    using pygame mouse click event objects. Once the map has been created
    on the screen, it is converted to a Map object. If the metro map is not connected,
    the Admin is given the option of editing the map again.
    """
    active_nodes: set[Node]

    def __init__(self, city_name: str, input_map: Map) -> None:
        """Initializes the Instance Attributes of the child class of User.
        """
        super(Admin, self).__init__('blue', city_name)
        self.active_nodes = input_map.get_all_nodes()

    def display(self) -> None:
        """Performs the display of the screen for an Admin"""
        while True:
            self._screen.fill(WHITE)
            self.draw_grid()
            self.create_palette()
            self.set_selection(self._curr_opt)

            visited = set()
            for node in self.active_nodes:
                visited.add(node)
                if node.is_station:
                    pygame.draw.circle(self._screen, BLACK, node.coordinates, 5)
                for u in node.get_neighbours():
                    if u not in visited:
                        pygame.draw.line(self._screen, node.get_color(u), node.coordinates,
                                         u.coordinates, 3)

            draw_text(self._screen, self.is_proper_map(), 17, (10, 10))

            for event in pygame.event.get():
                if event.type == pygame.QUIT and self.is_proper_map() == '':
                    init_db()
                    store_map(self.city_name, self.active_nodes)
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_mouse_click(event, (WIDTH, HEIGHT))

            self.hover_display()

            pygame.display.update()

    def node_exists(self, coordinates: tuple[float, float]) -> Optional[Node]:
        """Return the node if it exists at given coordinates. Else, return None.
        """
        for node in self.active_nodes:
            if node.coordinates == coordinates:
                return node
        return None

    def is_proper_map(self) -> str:
        """Return whether the nodes in self.active_nodes form a connected map
        and there are stations at both ends of the metro line(s).
        """
        no_of_stations = 0
        for node_1 in self.active_nodes:
            if node_1.is_station:
                no_of_stations += 1
            for node_2 in self.active_nodes:
                if not node_1.check_connected(node_2, set()):
                    return 'MAP IS NOT CONNECTED'

        if no_of_stations == 0:
            return 'MAP IS INCOMPLETE'

        for node_1 in self.active_nodes:
            if not node_1.is_station:
                neighbours = node_1.get_neighbours()
                if len(neighbours) > 2:
                    return 'TRACK INTERSECTION CAN ONLY HAPPEN AT STATIONS AND ' \
                           'TRACK OVERLAP CAN ONLY HAPPEN AT CROSSES OF THE GRID'
                elif len(neighbours) < 2:
                    return 'MAP IS INCOMPLETE'

        return ''

    def set_color(self, new_color: str) -> None:
        """Set color of track/node created.

        Preconditions:
            - new_color in LINE_COLORS
        """
        self._curr_opt = new_color

    def hover_display(self) -> None:
        """Gains the current nodes which can be displayed through
        the self.active_nodes attribute. Provides information on both name and zone."""
        for node in self.active_nodes:
            if in_circle(5, node.coordinates, pygame.mouse.get_pos()) and node.is_station:
                show = node.name + ' ' + str(node.coordinates)
                draw_text(self._screen, show, 17,
                          (node.coordinates[0] + 4, node.coordinates[1] - 15))

    def handle_mouse_click(self, event: pygame.event.Event,
                           screen_size: tuple[int, int]) -> None:
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
        if event.pos[0] > WIDTH:  # The click is on the color palette
            radius = (PALETTE_WIDTH // 2)
            coordinates = get_click_pos(event)
            for option in self.opt_to_center:
                if in_circle(radius, self.opt_to_center[option], coordinates):
                    self.set_color(option)
                    return

        else:  # The click is on the map
            if event.button == 3:  # Right-click is for track
                self._handle_right_click(event)
            elif event.button == 1:  # Left-click is for the nodes (station or corner)
                self._handle_left_click(event)
            else:
                return

    def _handle_right_click(self, event: pygame.event.Event) -> None:
        """Helper method for handle_mouse_click"""
        line_coordinates = approximate_edge_click(event)
        n_1 = self.node_exists(line_coordinates[0])
        n_2 = self.node_exists(line_coordinates[1])

        # One of the nodes already exists, the other node has to be created and linked to
        # the pre-existing node
        if n_1 is None and n_2 is not None:
            n_1 = Node(name=str(line_coordinates[0]), is_station=False,
                       coordinates=line_coordinates[0], zone='')
            self.active_nodes.add(n_1)
            n_1.add_track(n_2, self._curr_opt)
        elif n_1 is not None and n_2 is None:
            n_2 = Node(name=str(line_coordinates[1]), is_station=False,
                       coordinates=line_coordinates[1], zone='')
            self.active_nodes.add(n_2)
            n_1.add_track(n_2, self._curr_opt)

        # Both nodes need to be created and linked to each other
        elif n_1 is None and n_2 is None:
            n_1 = Node(name=str(line_coordinates[0]), is_station=False,
                       coordinates=line_coordinates[0], zone='')
            n_2 = Node(name=str(line_coordinates[1]), is_station=False,
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

    def _handle_left_click(self, event: pygame.event.Event) -> None:
        """Helper method for handle_mouse_click"""
        coordinates = get_click_pos(event)
        station = self.node_exists(coordinates)

        if station is None:
            # create new station
            self.get_station_info(coordinates)
        elif station.is_station:
            # remove the station and the tracks it is part of
            for neighbour in station.get_neighbours():
                station.remove_track(neighbour)
                if not neighbour.is_station and neighbour.get_neighbours() == set():
                    self.active_nodes.remove(neighbour)
            self.active_nodes.remove(station)
        else:
            # replace the corner with a station
            self.active_nodes.remove(station)
            self.get_station_info(coordinates, station)

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

    def get_station_info(self, coordinates: tuple[int, int],
                         replace: Optional[Node] = None) -> None:
        """Gets the information from the admin about the station such as the name and zone
         and creates a new station.

         If replace is not None, then tracks are added between the new station and the
         neighbours of replace.
        """
        screen = initialize_screen((700, 200))

        base_font = pygame.font.Font(None, 32)
        pygame.display.set_caption('Station Information')
        info = ['', '']
        info_active = [True, False]
        chk = [True, False]
        while chk[0]:

            screen.fill(WHITE)
            rect = _refresh_input_display(screen, info_active[0], info_active[1], chk[1])

            for event in pygame.event.get():

                chk[1] = False
                for node in self.active_nodes:
                    if node.name == info[0]:
                        chk[1] = True

                _handle_event_for_station_info(event, info, info_active, chk, rect)
                if not chk[0]:
                    break

            if not chk[0]:
                initialize_screen((WIDTH + PALETTE_WIDTH, HEIGHT))
                station = Node(name=info[0], coordinates=coordinates,
                               is_station=True, zone=info[1])

                if replace is not None:
                    for neighbour in replace.get_neighbours():
                        station.add_track(neighbour, replace.get_color(neighbour))
                        replace.remove_track(neighbour)

                self.active_nodes.add(station)
                self.display()
                break

            name_surface = base_font.render(info[0], True, (0, 0, 0))
            zone_surface = base_font.render(info[1], True, (0, 0, 0))
            screen.blit(name_surface, (rect[0].x + 5, rect[0].y + 2.5))
            screen.blit(zone_surface, (rect[1].x + 5, rect[1].y + 2.5))
            pygame.display.flip()


def _handle_event_for_station_info(event: pygame.event.Event, info: list[str],
                                   info_active: list[bool], chk: list[bool],
                                   rect: tuple[pygame.Rect, pygame.Rect]) -> None:
    """Update all the parameters (except rect) using mutation based on the event."""
    if event.type == pygame.QUIT:
        sys.exit()

    elif event.type == pygame.MOUSEBUTTONDOWN:
        if rect[0].collidepoint(event.pos):
            info_active[0], info_active[1] = True, False

        if rect[1].collidepoint(event.pos):
            info_active[0], info_active[1] = False, True

    elif event.type == pygame.KEYDOWN:
        if event.key == pygame.K_RETURN:
            chk[0] = chk[1] or info[0] == '' or info[1] == ''

        elif event.key == pygame.K_BACKSPACE:

            if info_active[1]:
                info[1] = info[1][:-1]

            elif info_active[0]:
                info[0] = info[0][:-1]

        else:

            if info_active[1]:
                info[1] += event.unicode

            if info_active[0]:
                info[0] += event.unicode


def _refresh_input_display(screen: pygame.Surface,
                           active_name: bool, active_zone: bool,
                           check: bool) -> tuple[pygame.Rect, pygame.Rect]:
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

    if check:
        draw_text(screen, 'Station with this name already exists', 20, (5, 70))

    return name_rect, zone_rect


class Client(User):
    """Client is the aspect of the User which displays a Map object on the screen,
    and then uses pygame mouse click event objects to determine the Client's
    starting point and final destination, and the variable of optimization the Client
    prefers. Then, the best possible route between the two stations is highlighted.

    Instance Attributes:
        - metro_map: Refers to the current metro transit map being used by the client to
        locate the stations and find the optimized path as per requirement.
    """

    metro_map: Map
    _start: Optional[Node]
    _end: Optional[Node]

    def __init__(self, input_map: Map, city_name: str) -> None:
        """ Initializes the Instance Attributes of
        the Client class which is a child of User.
        """
        super(Client, self).__init__('distance', city_name)
        self.metro_map = input_map
        self._start = None
        self._end = None

    def handle_mouse_click(self, event: pygame.event.Event,
                           screen_size: tuple[int, int]) -> None:
        """ Handle a mouse click event.

        A pygame mouse click event object has two attributes that are important for this method:
            - event.pos: the (x, y) coordinates of the mouse click
            - event.button: an int representing which mouse button was clicked.
                            1: left-click, 3: right-click

        The screen_size is a tuple of (width, height), and should be used together with
        event.pos to determine which cell is being clicked.

        If the click is within the area of the palette, then check if it is within the option of
        distance or cost and handle accordingly.

        If the click is within the grid, check if the click is left or right.
        If it is the left click, this marks the starting station. If the click is a right click
        this marks the destination station. The right click is only possible if a starting station
        has already been selected.

        Preconditions:
            - event.type == pygame.MOUSEBUTTONDOWN
            - screen_size[0] >= ...
            - screen_size[1] >= ...
        """
        pygame.init()
        click_coordinates = get_click_pos(event)

        if click_coordinates[0] > WIDTH:  # The click is on the palette

            for option in self.opt_to_center:
                target = self.opt_to_center[option]
                input_rect = pygame.Rect(target[0], target[1], 35, 35)

                if input_rect.collidepoint(click_coordinates):
                    self._curr_opt = option

        else:  # The click is on the map.

            for station in self.metro_map.get_all_nodes('station'):

                # Checks whether the click was in the vicinity of a station node
                if in_circle(5, station.coordinates, click_coordinates):

                    # Selects the 'From' station creating a small box around it indicating 'From'.
                    if event.button == 1:
                        self._start = station

                    # Selects the 'To' station creating a small box around it indicating 'To'.
                    if event.button == 3:
                        self._end = station

                continue

        return

    def _connect_final_route(self, path: list[str]) -> None:
        """Displays the final path highlighting the tracks being used,
        making the others gray.
        """
        lst = [n for n in self.metro_map.get_all_nodes('') if n.name not in path]

        for i in range(0, len(path) - 1):
            node = self.metro_map.get_node(path[i])

            for neighbours in node.get_neighbours():

                if neighbours.name == path[i + 1]:
                    color = node.get_color(neighbours)
                    pygame.draw.line(surface=self._screen,
                                     color=color,
                                     start_pos=node.coordinates,
                                     end_pos=neighbours.coordinates,
                                     width=5)

        for node in lst:

            for neighbours in node.get_neighbours():
                pygame.draw.line(surface=self._screen,
                                 color=THECOLORS['gray50'],
                                 start_pos=node.coordinates,
                                 end_pos=neighbours.coordinates,
                                 width=3)

        return

    def create_palette(self) -> None:
        """ Draw the palette which contains the images
        representing distance and cost for the client
        to choose as per their requirement.
        """
        rect_width = (PALETTE_WIDTH // 4)
        ht = PALETTE_WIDTH * 6

        image1 = pygame.image.load('distance.png')
        image_distance = pygame.transform.scale(image1, (30, 30))

        image2 = pygame.image.load('cost.png')
        image_cost = pygame.transform.scale(image2, (30, 30))

        self._screen.blit(image_distance, (WIDTH + rect_width, ht))
        self.opt_to_center['distance'] = (WIDTH + rect_width, ht)

        self._screen.blit(image_cost, (WIDTH + rect_width, 2 * ht - 50))
        self.opt_to_center['cost'] = (WIDTH + rect_width, 2 * ht - 50)

    def set_selection(self, palette_choice: str) -> None:
        """Darkens the borders of the selected
        optimization from the palette provided.
        """

        target = self.opt_to_center[palette_choice]

        input_rect = pygame.Rect(target[0] - 2, target[1], 35, 35)
        pygame.draw.rect(self._screen, BLACK, input_rect, 3)

    def display(self) -> None:
        """Performs the display of the screen for a Client."""
        while True:
            self._screen.fill(WHITE)
            self.draw_grid()
            self.create_palette()
            self.set_selection(self._curr_opt)

            visited = set()

            for node in self.metro_map.get_all_nodes('station'):
                pygame.draw.circle(self._screen, BLACK, node.coordinates, 5)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_mouse_click(event, (WIDTH, HEIGHT))

            if self._start is not None and self._end is not None:
                path = self.metro_map.optimized_route(start=self._start.name,
                                                      destination=self._end.name,
                                                      optimization=self._curr_opt)
                self._connect_final_route(path)

            else:
                for node in self.metro_map.get_all_nodes(''):
                    visited.add(node)
                    for u in node.get_neighbours():
                        if u not in visited:
                            pygame.draw.line(self._screen, node.get_color(u), node.coordinates,
                                             u.coordinates, 3)

            self.hover_display()

            pygame.display.update()

    def hover_display(self) -> None:
        """Gains the current nodes which can be displayed through
        the self.active_nodes attribute. Provides information on both name and zone."""
        for node in self.metro_map.get_all_nodes('station'):
            if node == self._start and self._start is not None:
                show = node.name + ' ' + '(' + node.zone + ')' + ' START'
                draw_text(self._screen, show, 17,
                          (node.coordinates[0] + 4, node.coordinates[1] - 15), THECOLORS['green'])

            elif node == self._end and self._start is not None:
                show = node.name + ' ' + '(' + node.zone + ')' + ' END'
                draw_text(self._screen, show, 17,
                          (node.coordinates[0] + 4, node.coordinates[1] - 15), THECOLORS['red'])

            elif in_circle(5, node.coordinates, pygame.mouse.get_pos()):
                show = node.name + ' ' + '(' + node.zone + ')'
                draw_text(self._screen, show, 17,
                          (node.coordinates[0] + 4, node.coordinates[1] - 15))

        return


if __name__ == '__main__':
    import doctest
    doctest.testmod()

    import python_ta
    python_ta.check_all(config={
        'max-line-length': 100,
        'disable': ['E1101', 'E1136', ],
        'extra-imports': ['map', 'node', 'canvas_utils', 'storage_manager', 'pygame', 'sys',
                          'pygame.colordict'],
        'max-nested-blocks': 5
    })
