"""This file contains helper functions which perform computations or
draw general assets on to the screen, which are present among multiple
screens and not unique to any one in particular. Also consists of static methods and
constants regarding pygame rendering."""

import pygame

INSTRUCT_ADMIN = ["Left click on a point in the grid to add a Metro Station or a",
                  "Node to the Map. Additional Left click deletes Node/Station.",
                  "Right Click on a side or diagonal to add a track line that",
                  " connects two Nodes/Stations. Additional Right click deletes ",
                  "track. Click on a Palette to select color.",
                  "",
                  "                      PRESS ENTER TO CONTINUE."]

INSTRUCT_CLIENT = ""

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


def draw_text(screen: pygame.Surface, text: str, font: int, pos: tuple[int, int]) -> None:
    """Draw the given text to the pygame screen at the given position.

    pos represents the *upper-left corner* of the text.
    """
    font = pygame.font.SysFont('inconsolata', font)
    text_surface = font.render(text, True, BLACK)
    width, height = text_surface.get_size()
    screen.blit(text_surface,
                pygame.Rect(pos, (pos[0] + width, pos[1] + height)))
