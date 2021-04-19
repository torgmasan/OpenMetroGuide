"""Module representing the client user of OpenMetroGuide.

Client is capable of calculating the path that needs to be taken from one
station to another. Can use Distance/Cost as the calculation constraints.
"""

import sys
from typing import Optional

import pygame
from pygame.colordict import THECOLORS

from src.Display.Utils.general_utils import get_click_pos, WIDTH, in_circle, PALETTE_WIDTH, \
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
