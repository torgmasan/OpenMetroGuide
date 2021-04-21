"""Module representing the client user of OpenMetroGuide.

Client is capable of calculating the path that needs to be taken from one
station to another. Can use Distance/Cost as the calculation constraints.
"""

import sys
from typing import Optional

import pygame
from pygame.colordict import THECOLORS

from src.Display.Utils.general_utils import WIDTH, in_circle, PALETTE_WIDTH, \
    BLACK, WHITE, draw_text, HEIGHT
from src.Base.map import Map
from src.Base.node import Node
from src.Display.Canvas.user import User


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
        for node in self.metro_map.get_all_nodes():
            for neighbor in node.get_neighbours():
                node.update_weights(neighbor)

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
        click_coordinates = self.get_click_pos(event)

        if event.pos[0] > WIDTH:  # The click is on the palette

            for option in self.opt_to_center:
                target = self.opt_to_center[option]
                input_rect = pygame.Rect(target[0], target[1], 35, 35)

                if input_rect.collidepoint(event.pos):
                    self._curr_opt = option

        else:  # The click is on the map.

            station = self.node_exists(click_coordinates)

            if event.button == 1:
                self._start = station

            elif event.button == 3:
                self._end = station

        return

    def _connect_final_route(self, path: list[str]) -> None:
        """Displays the final path highlighting the tracks being used,
        making the others gray.
        """
        lst = [n for n in self.metro_map.get_all_nodes('') if n.name not in path]

        for i in range(0, len(path) - 1):
            node = self.metro_map.get_node(path[i])
            transform_node = self.scale_factor_transformations(node.coordinates)

            for neighbours in node.get_neighbours():

                if neighbours.name == path[i + 1]:
                    color = node.get_color(neighbours)

                    transform_neighbor = self.scale_factor_transformations(neighbours.coordinates)

                    if transform_neighbor[0] <= WIDTH and transform_node[0] <= WIDTH:
                        pygame.draw.line(surface=self._screen,
                                         color=color,
                                         start_pos=transform_node,
                                         end_pos=transform_neighbor,
                                         width=5)

        for node in lst:

            transform_node = self.scale_factor_transformations(node.coordinates)

            for neighbours in node.get_neighbours():

                transform_neighbor = self.scale_factor_transformations(neighbours.coordinates)

                if transform_neighbor[0] <= WIDTH and transform_node[0] <= WIDTH:
                    pygame.draw.line(surface=self._screen,
                                     color=THECOLORS['gray50'],
                                     start_pos=transform_node,
                                     end_pos=transform_neighbor,
                                     width=3)

        return

    def create_palette(self) -> None:
        """ Draw the palette which contains the images
        representing distance and cost for the client
        to choose as per their requirement.
        """
        rect_width = (PALETTE_WIDTH // 4)
        ht = PALETTE_WIDTH * 6

        image1 = pygame.image.load('../Assets/distance.png')
        image_distance = pygame.transform.scale(image1, (30, 30))

        image2 = pygame.image.load('../Assets/cost.png')
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
                transform_node = self.scale_factor_transformations(node.coordinates)

                if 0 < transform_node[0] <= 800 and 0 < transform_node[1] < 800:
                    pygame.draw.circle(self._screen, BLACK,
                                       transform_node, 5)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_mouse_click(event, (WIDTH, HEIGHT))
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_DOWN:
                        self.handle_d_shift()
                    elif event.key == pygame.K_UP:
                        self.handle_u_shift()
                    elif event.key == pygame.K_LEFT:
                        self.handle_l_shift()
                    elif event.key == pygame.K_RIGHT:
                        self.handle_r_shift()
                    elif event.key == pygame.K_p and pygame.key.get_mods() & pygame.KMOD_CTRL:
                        self.handle_zoom_in()
                    elif event.key == pygame.K_m and pygame.key.get_mods() & pygame.KMOD_CTRL:
                        self.handle_zoom_out()

            if self._start is not None and self._end is not None:
                path = self.metro_map.optimized_route(start=self._start.name,
                                                      destination=self._end.name,
                                                      optimization=self._curr_opt)
                self._connect_final_route(path)

            else:
                for node in self.metro_map.get_all_nodes(''):
                    visited.add(node)
                    transform_node = self.scale_factor_transformations(node.coordinates)

                    for u in node.get_neighbours():
                        if u not in visited:
                            transform_u = self.scale_factor_transformations(u.coordinates)

                            if transform_u[0] <= WIDTH and transform_node[0] <= WIDTH:
                                pygame.draw.line(self._screen, node.get_color(u),
                                                 transform_node,
                                                 transform_u, 3)

            self.hover_display()

            pygame.display.update()

    def node_exists(self, coordinates: tuple[float, float]) -> Optional[Node]:
        """Return the node if it exists at given coordinates. Else, return None.
        """
        for node in self.metro_map.get_all_nodes():
            if self.scale_factor_transformations(node.coordinates) == coordinates:
                return node
        return None

    def hover_display(self) -> None:
        """Gains the current nodes which can be displayed through
        the self.active_nodes attribute. Provides information on both name and zone."""
        for node in self.metro_map.get_all_nodes('station'):
            transformed = self.scale_factor_transformations(node.coordinates)

            if node == self._start and self._start is not None:
                show = node.name + ' ' + '(' + node.zone + ')' + ' START'
                draw_text(self._screen, show, 17,
                          (transformed[0] + 4, transformed[1] - 15), THECOLORS['green'])

            elif node == self._end and self._start is not None:
                show = node.name + ' ' + '(' + node.zone + ')' + ' END'
                draw_text(self._screen, show, 17,
                          (transformed[0] + 4, transformed[1] - 15), THECOLORS['red'])

            elif in_circle(5, transformed, pygame.mouse.get_pos()):
                show = node.name + ' ' + '(' + node.zone + ')'
                draw_text(self._screen, show, 17,
                          (transformed[0] + 4, transformed[1] - 15))

        return
