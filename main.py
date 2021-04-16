"""Runs the home application window.
"""
import pygame
from pygame.colordict import THECOLORS

import user
from canvas_utils import draw_text, WHITE, BLACK, initialize_screen

from storage_manager import get_map, init_db, get_cities
import sys


def run_home() -> None:
    """Runs the home application which serves as a entrance
    to the OpenMetroGuide application.
    """
    screen = initialize_screen((400, 300))
    init_db()

    pygame.display.set_caption("OpenMetroGuide")
    current_user = 'admin'
    chk = True
    screen_type = 0  # screen type can be 0/1 if main screen or instruction set.

    queue_lst = get_cities()
    current_index = 0
    current_opt = 0
    enter_city_rect = pygame.Rect((110, 150, 200, 30))
    city_name = ''
    base_font = pygame.font.Font(None, 32)

    while chk:

        screen.fill(WHITE)

        if screen_type == 0:
            refresh_display(screen, screen_type)
        elif screen_type == 1:
            refresh_display(screen, screen_type, queue_lst, current_user, current_index, current_opt)
        else:
            refresh_display(screen, screen_type, active_color=THECOLORS['blue'],
                            name_rect=enter_city_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    if screen_type == 0:
                        current_user = 'client'
                    elif current_user == 'admin' and queue_lst:
                        # Key down only used by admin with multiple choices
                        current_opt = 1
                elif event.key == pygame.K_UP:
                    if screen_type == 0:
                        current_user = 'admin'
                    else:
                        current_opt = 0
                if event.key == pygame.K_RIGHT and screen_type == 1:
                    current_index = (current_index + 1) % len(queue_lst)
                elif event.key == pygame.K_UP and screen_type == 1:
                    current_index = (current_index - 1) % len(queue_lst)
                elif event.key == pygame.K_RETURN:
                    if screen_type == 1 and ((current_user == 'client') or
                                             (queue_lst and current_opt == 0)):
                        # Client stops at screen_type 1
                        # Admin who chose to use existing map stops
                        # at type 1
                        if city_name == '':
                            # TODO: convert to pygame drawing
                            print('Enter some name')
                        chk = False
                        break
                    elif screen_type == 2 and current_user == 'admin':
                        # Admin creating new map stops at screen_type 2
                        chk = False
                        break
                    else:
                        screen_type += 1
                else:
                    city_name = _handle_event_for_run_home(event, city_name)

        if chk and screen_type == 0:
            set_selection(screen, current_user)

        name_surface = base_font.render(city_name, True, (0, 0, 0))
        screen.blit(name_surface, (enter_city_rect.x + 5, enter_city_rect.y + 5))
        pygame.display.flip()

    if current_opt == 0 and queue_lst:
        city_name = queue_lst[current_index]

    if current_user == 'admin':
        admin = user.Admin(city_name)
        admin.display()
    else:
        metro_map = get_map(city_name)
        client = user.Client(metro_map, city_name)
        client.display()


def _handle_event_for_run_home(event: pygame.event.Event, name: str) -> str:
    """Update all the parameters (except rect) using mutation based on the event."""

    if event.key == pygame.K_BACKSPACE:

        name = name[:-1]

    else:

        name += event.unicode

    return name


def refresh_display(screen: pygame.Surface, screen_type: int, queue_lst: list = None,
                    current_user: str = None, current_index: int = None, current_opt: int = None,
                    active_color: tuple[int, int, int] = None,
                    name_rect: pygame.Rect = None) -> None:
    """Part of the GUI that remains constant throughout
    all interactions with the window. Therefore, during
    each refreshment of the screen, this code snippet is
    reused.
    """

    if screen_type == 0:  # Main Window
        draw_text(screen, 'Select an option (Use Up/Down keys):', 30, (20, 50))
        draw_text(screen, 'Run as Admin', 25, (150, 120))
        draw_text(screen, 'Run as Client', 25, (150, 220))
        pygame.draw.rect(screen, BLACK,
                         (5, 100, screen.get_width() - 10, 55), 10)
        pygame.draw.rect(screen, BLACK,
                         (5, 200, screen.get_width() - 10, 55), 10)
    elif screen_type == 1:  # Choosing Station or creating new map window
        if queue_lst and current_user == 'client':
            draw_text(screen, 'Select City (Right/Left)', 25,
                      (120, 50), BLACK)
            draw_text(screen, '->', 40, (350, 135), BLACK)
            draw_text(screen, '<-', 40, (50, 135), BLACK)
            font = pygame.font.Font(None, 25)
            text = font.render(queue_lst[current_index], True, THECOLORS['green'])
            text_rect = text.get_rect(center=(200, 150))
            screen.blit(text, text_rect)

        elif queue_lst and current_user == 'admin':
            draw_text(screen, 'Select City (Right/Left) or Create New Map (Up/Down)', 21,
                      (20, 50), BLACK)
            draw_text(screen, '->', 40, (350, 135), BLACK)
            draw_text(screen, '<-', 40, (50, 135), BLACK)
            if current_opt == 0:
                font = pygame.font.Font(None, 25)
                text = font.render(queue_lst[current_index], True, THECOLORS['green'])
                text_rect = text.get_rect(center=(200, 150))
                screen.blit(text, text_rect)
                draw_text(screen, '+ Create New Map', 35, (100, 250), BLACK)
            else:
                font = pygame.font.Font(None, 25)
                text = font.render(queue_lst[current_index], True, BLACK)
                text_rect = text.get_rect(center=(200, 150))
                screen.blit(text, text_rect)
                draw_text(screen, '+ Create New Map', 35, (100, 250), THECOLORS['green'])
        elif not queue_lst and current_user == 'client':
            draw_text(screen, 'No map in Database', 35, (90, 120), BLACK)
        else:
            draw_text(screen, '+ Create New Map', 35, (90, 120), THECOLORS['green'])
    else:  # Entering the city name
        draw_text(screen, 'Enter City Name', 30,
                  (120, 50), BLACK)
        pygame.draw.rect(screen, active_color, name_rect, 3)


def set_selection(screen: pygame.Surface, selected: str):
    """Darkens the borders of the button that represents
    the two options provided to the user, 'Run as Admin'
    or 'Run as 'Client'. Also whitens the borders of the
    unselected option. These options are represented by the
    selected attribute: 'admin' and 'client' respectively."""

    if selected == 'admin':
        pygame.draw.rect(screen, BLACK,
                         (5, 100, screen.get_width() - 10, 55), 3)
        pygame.draw.rect(screen, WHITE,
                         (5, 200, screen.get_width() - 10, 55), 3)
    else:
        pygame.draw.rect(screen, WHITE,
                         (5, 100, screen.get_width() - 10, 55), 3)
        pygame.draw.rect(screen, BLACK,
                         (5, 200, screen.get_width() - 10, 55), 3)


if __name__ == "__main__":
    run_home()
