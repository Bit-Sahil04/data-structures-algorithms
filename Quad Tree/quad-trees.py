import pygame
import random
from Quad import Quad


QUAD_COLOR = (128, 255, 128)
BG_COLOR = (80, 0, 80)
POINT_COLOR = (100, 255, 20)
POINT_COLOR2 = (80, 255, 255)


def update_quads(screen, quad):
    line_width = 1
    if not quad.children:
        pygame.draw.lines(screen, QUAD_COLOR, True, quad.get_outline(), line_width)
    else:
        for k in quad.children:
            update_quads(screen, quad.children[k])


def main():
    pygame.init()
    pygame.display.set_caption("Quad Tree Visuallisation - Bit-Sahil04")
    width, height = (800, 600)
    win = pygame.display.set_mode((width, height))
    clock = pygame.time.Clock()
    win.fill(BG_COLOR)
    q = Quad((1, 1, width - 1, height - 1), 1)
    p = set()
    lp = None
    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                exit()
            if e.type == pygame.MOUSEBUTTONUP:
                rp = pygame.mouse.get_pos()
                q.insert_point(rp)
                p.add(rp)
                lp = rp
                update_quads(win, q)

        for i in p:
            pygame.draw.circle(win, POINT_COLOR, i, 5)
        if lp:
            pygame.draw.circle(win, POINT_COLOR2, lp, 5)

        clock.tick(60)
        pygame.display.flip()


if __name__ == "__main__":
    main()
