"""Runs the home application window.
"""
import sys
import pygame
from pygame.colordict import THECOLORS

import user
from canvas_utils import draw_text, WHITE, BLACK, initialize_screen
from map import Map

from storage_manager import get_map, init_db, get_cities

init_db()
screen_type = 0
screen = initialize_screen((400, 300))
queue_lst = get_cities()
is_admin = True
is_existing = True
current_index = 0
enter_city_rect = pygame.Rect((110, 150, 200, 30))


def run_home() -> None:
    """Runs the home application which serves as a entrance
    to the OpenMetroGuide application.
    """
    global is_admin, is_existing, current_index, screen_type

    pygame.display.set_caption("OpenMetroGuide")
    chk = True
    warning = city_name = ''
    base_font = pygame.font.Font(None, 32)

    while chk:

        screen.fill(WHITE)

        _display_correct_screen()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    if screen_type == 0:
                        is_admin = False

                    elif is_admin and queue_lst:
                        # Key down only used by admin with multiple choices
                        is_existing = False

                elif event.key == pygame.K_UP:

                    if screen_type == 0:
                        is_admin = True
                    else:
                        is_existing = True

                if event.key == pygame.K_RIGHT and screen_type == 1:
                    current_index = (current_index + 1) % len(queue_lst)

                elif event.key == pygame.K_LEFT and screen_type == 1:
                    current_index = (current_index - 1) % len(queue_lst)

                elif event.key == pygame.K_RETURN:

                    if screen_type == 1 and (not is_admin or (queue_lst and is_existing)):
                        # Client stops at screen_type 1
                        # Admin who chose to use existing map stops
                        # at type 1
                        chk = False
                        break

                    elif screen_type == 2 and is_admin:
                        # Admin creating new map stops at screen_type 2

                        if city_name == '':
                            warning = 'No input provided'

                        elif city_name in queue_lst:
                            warning = 'Name already present'

                        else:
                            chk = False
                            break

                    else:
                        screen_type += 1

                else:

                    if screen_type == 2:
                        city_name = _handle_event_for_run_home(event, city_name)

        if chk and screen_type == 0:
            set_selection()

        name_surface = base_font.render(city_name, True, (0, 0, 0))
        screen.blit(name_surface, (enter_city_rect.x + 5, enter_city_rect.y + 2.5))

        draw_text(screen, warning, 15, (160, 190), BLACK)
        pygame.display.flip()

    metro_map = Map()
    next_user(city_name, metro_map)


def _display_correct_screen() -> None:
    """Helper function to choose the correct screen to
    refresh.
    """
    if screen_type == 0:
        refresh_display()

    elif screen_type == 1:
        refresh_display()

    else:
        refresh_display(active_color=THECOLORS['blue'])


def next_user(city_name: str, metro_map: Map) -> None:
    """Uses the information received from the User to
    determine if User or Client, and use other details
    to create the setup for edit/view of metro map"""
    if is_existing and queue_lst:
        city_name = queue_lst[current_index]
        metro_map = get_map(city_name)

    if is_admin:
        admin = user.Admin(city_name, metro_map)
        admin.display()

    else:
        client = user.Client(metro_map, city_name)
        client.display()


def _handle_event_for_run_home(event: pygame.event.Event, name: str) -> str:
    """Update all the parameters (except rect) using mutation based on the event."""

    if event.key == pygame.K_BACKSPACE:
        name = name[:-1]
    else:
        name += event.unicode

    return name


def refresh_display(active_color: tuple[int, int, int] = None) -> None:
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

        if queue_lst and not is_admin:
            draw_text(screen, 'Select City (Right/Left)', 25,
                      (120, 50), BLACK)
            draw_text(screen, '->', 40, (350, 135), BLACK)
            draw_text(screen, '<-', 40, (50, 135), BLACK)
            font = pygame.font.Font(None, 25)
            text = font.render(queue_lst[current_index], True, THECOLORS['green'])
            text_rect = text.get_rect(center=(200, 150))
            screen.blit(text, text_rect)

        elif queue_lst and is_admin:
            draw_text(screen, 'Select City (Right/Left) or Create New Map (Up/Down)', 21,
                      (20, 50), BLACK)
            draw_text(screen, '->', 40, (350, 135), BLACK)
            draw_text(screen, '<-', 40, (50, 135), BLACK)

            if is_existing:
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

        elif not queue_lst and not is_admin:
            draw_text(screen, 'No map in Database', 35, (90, 120), BLACK)

        else:
            draw_text(screen, '+ Create New Map', 35, (90, 120), THECOLORS['green'])

    else:  # Entering the city name
        draw_text(screen, 'Enter City Name', 30,
                  (120, 50), BLACK)
        pygame.draw.rect(screen, active_color, enter_city_rect, 3)


def set_selection() -> None:
    """Darkens the borders of the button that represents
    the two options provided to the user, 'Run as Admin'
    or 'Run as 'Client'. Also whitens the borders of the
    unselected option. These options are represented by the
    selected attribute: 'admin' and 'client' respectively."""

    if is_admin:
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
    import doctest

    doctest.testmod()
    import python_ta

    python_ta.check_all(config={
        'max-line-length': 100,
        'disable': ['E1136', 'E1101', 'C0103', 'E9997', 'R0912'],
        'extra-imports': ['node', 'math', 'pygame', 'pygame.colordict', 'sys',
                          'user', 'canvas_utils', 'map', 'storage_manager'],
        'max-nested-blocks': 6
    })
