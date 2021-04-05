import pygame
import User
import sys

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


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
    while chk:

        screen.fill(WHITE)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    current = 'client'
                elif event.key == pygame.K_UP:
                    current = 'admin'
                elif event.key == pygame.K_RETURN:
                    chk = False
                    break

        if chk:
            set_selection(screen, current)
        pygame.display.flip()

    if current == 'admin':
        User.Admin()
    else:
        User.Client()


def refresh_display(screen: pygame.Surface) -> None:
    """Part of the GUI that remains constant throughout
    all interactions with the window. Therefore, during
    each refreshment of the screen, this code snippet is
    reused."""
    User.draw_text(screen, 'Select an option (Use Up/Down keys):', 30, (20, 50))
    User.draw_text(screen, 'Run as Admin', 25, (150, 120))
    User.draw_text(screen, 'Run as Client', 25, (150, 220))
    pygame.draw.rect(screen, BLACK,
                     (5, 100, screen.get_width() - 10, 55), 10)
    pygame.draw.rect(screen, BLACK,
                     (5, 200, screen.get_width() - 10, 55), 10)


def set_selection(screen: pygame.Surface, selected: str):
    """Darkens the borders of the button that represents
    the two options provided to the user, 'Run as Admin'
    or 'Run as 'Client'. Also whitens the borders of the
    unselected option. These options are represented by the
    selected attribute: 'admin' and 'client' respectively."""
    refresh_display(screen)

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
