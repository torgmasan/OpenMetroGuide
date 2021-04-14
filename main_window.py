import pygame
import User
from canvas_utils import draw_text, WHITE, BLACK, \
    INSTRUCT_CLIENT, INSTRUCT_ADMIN
import sys


def run_home() -> None:
    """Runs the home application which serves as a entrance
    to the OpenMetroGuide application.
    """
    pygame.init()
    screen = pygame.display.set_mode((400, 300))
    screen.fill(WHITE)

    pygame.display.set_caption("OpenMetroGuide")
    current = 'admin'
    chk = True
    screen_type = 0  # screen type can be 0/1 if main screen or instruction set.

    while chk:

        screen.fill(WHITE)

        if screen_type == 0:
            refresh_display(screen, screen_type)
        else:
            refresh_display(screen, screen_type, current)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN and screen_type == 0:
                    current = 'client'
                elif event.key == pygame.K_UP and screen_type == 0:
                    current = 'admin'
                elif event.key == pygame.K_RETURN:
                    if screen_type == 1:
                        chk = False
                        break
                    else:
                        screen_type = 1

        if chk and screen_type == 0:
            set_selection(screen, current)
        pygame.display.flip()

    if current == 'admin':
        admin = User.Admin()
        admin.display()
    else:
        client = User.Client()
        client.display()


def refresh_display(screen: pygame.Surface, screen_type: int, current: str = None) -> None:
    """Part of the GUI that remains constant throughout
    all interactions with the window. Therefore, during
    each refreshment of the screen, this code snippet is
    reused.
    """

    if screen_type == 0:
        draw_text(screen, 'Select an option (Use Up/Down keys):', 30, (20, 50))
        draw_text(screen, 'Run as Admin', 25, (150, 120))
        draw_text(screen, 'Run as Client', 25, (150, 220))
        pygame.draw.rect(screen, BLACK,
                         (5, 100, screen.get_width() - 10, 55), 10)
        pygame.draw.rect(screen, BLACK,
                         (5, 200, screen.get_width() - 10, 55), 10)
    else:
        if current == 'client':
            instructions = INSTRUCT_CLIENT
        else:
            instructions = INSTRUCT_ADMIN

        cnt = 10
        for instruction in instructions:
            draw_text(screen, instruction, 20, (10, cnt))
            cnt += 35


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


run_home()
