import pygame
import sys

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


def run_home():
    pygame.init()
    screen = pygame.display.set_mode((400, 300))
    screen.fill(WHITE)

    pygame.display.set_caption("OpenMetroGuide")

    make_text(screen, 'Select an option (Use Up/Down keys):', 30, (20, 50))
    make_text(screen, 'Run as Admin', 25, (150, 120))
    make_text(screen, 'Run as Client', 25, (150, 220))
    current = ''

    while True:

        screen.fill(WHITE)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYUP:
                current = 'admin'
            elif event.type == pygame.KEYDOWN:
                current = 'client'

        print(current)
        set_selection(screen, current)

        pygame.display.flip()


def make_text(screen: pygame.Surface, text: str, size: int, location: tuple[int, int]):
    font = pygame.font.SysFont(name=None, size=size)
    render = font.render(text, True, BLACK)
    screen.blit(render, location)


def set_selection(screen: pygame.Surface, selected: str):
    make_text(screen, 'Select an option (Use Up/Down keys):', 30, (20, 50))
    make_text(screen, 'Run as Admin', 25, (150, 120))
    make_text(screen, 'Run as Client', 25, (150, 220))

    if selected == 'admin':
        pygame.draw.rect(screen, BLACK, (5, 100, screen.get_width() - 10, 55), 3)

        pygame.draw.rect(screen, WHITE, (5, 200, screen.get_width() - 10, 55), 3)
    else:
        pygame.draw.rect(screen, WHITE, (5, 100, screen.get_width() - 10, 55), 3)

        pygame.draw.rect(screen, BLACK, (5, 200, screen.get_width() - 10, 55), 3)


run_home()
