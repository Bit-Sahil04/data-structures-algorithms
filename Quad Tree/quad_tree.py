import pygame
from Quad import Quad
from math import sqrt
import random


RESOLUTION = (800, 600)
win = pygame.display.set_mode(RESOLUTION)

QUAD_COLOR = (128, 60, 128)
BG_COLOR = (80, 0, 80)
POINT_COLOR = (100, 255, 20)
POINT_COLOR2 = (80, 255, 255)
HIGHLIGHT_COLOR = (255, 255, 255)


def show_text(text, x, y, surf, size=10, color=(255, 255, 255)):
    text = str(text)
    font = pygame.font.SysFont('Arial', size, True)

    text_width, text_height = font.size(text)
    text = font.render(text, True, color)
    tRect = surf.blit(text, (x - (text_width / 2), y - (text_height / 2)))
    return tRect


def update_quads(screen, quad):
    line_width = 1
    if not quad.children:
        pygame.draw.lines(screen, QUAD_COLOR, True, quad.get_outline(), line_width)
    else:
        for k in quad.children:
            update_quads(screen, quad.children[k])


def main():
    pygame.init()
    pygame.display.set_caption("Quad Tree Visualisation - Bit-Sahil04")
    width, height = RESOLUTION
    clock = pygame.time.Clock()
    win.fill(BG_COLOR)
    quad_tree = Quad((1, 1, width - 1, height - 1), 1)
    points = []
    lmb = False
    while True:
        win.fill(BG_COLOR)
        update_quads(win, quad_tree)

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                exit()
            if pygame.mouse.get_pressed(3)[0] and not lmb:
                lmb = True
                rp = pygame.mouse.get_pos()
                p = Point(5, rp, (random.randint(-1, 3), random.randint(-1, 3)))
                p.quadrant = quad_tree.insert_point(rp)
                points.append(p)
            else:
                lmb = False

        for id, i in enumerate(points):
            i.update(quad_tree)
            pygame.draw.circle(win, POINT_COLOR, i.pos, i.radius)

        show_text(f"{1000 / clock.tick() :.0f}", 100, 20, win, size=15)
        show_text(f"{(len(points))}", 100, 40, win, size=15)
        pygame.display.flip()


class Point:
    def __init__(self, radius, pos, dv: (int, int)):
        self.pos = pos
        self.dv = dv
        self.quadrant = None
        self.radius = radius
        self.entry_position = pos

    def update(self, root_quad):
        # add acceleration dv to point position
        self.pos = (self.pos[0] + self.dv[0], self.pos[1] + self.dv[1])

        # Update quad tree if the point exits the bounds of current quad
        if not self.quadrant.has_point(self.pos):
            self.quadrant.pop(self.entry_position)
            self.entry_position = self.pos
            self.quadrant = root_quad.insert_point(self.entry_position)

        if self.collision_x():
            self.dv = (self.dv[0] * -1, self.dv[1])

        if self.collision_y():
            self.dv = (self.dv[0], self.dv[1] * -1)

        if self.collision_point():
            self.dv = (self.dv[0] * -1, self.dv[1] * -1)

    def collision_x(self):
        return (0 + self.radius * 2 > self.pos[0]) or (self.pos[0] > (RESOLUTION[0] - (self.radius * 2)))

    def collision_y(self):
        return (0 + self.radius * 2 > self.pos[1]) or (self.pos[1] > RESOLUTION[1] - (self.radius * 2))

    def collision_point(self):
        for p2 in self.quadrant.points:
            pygame.draw.line(win, QUAD_COLOR, self.pos, p2)
            if p2 != self.pos:
                px = p2[0] + self.radius
                py = p2[1] + self.radius
                dx = sqrt(((self.pos[0] + self.radius) - px) ** 2 + ((self.pos[1] + self.radius) - py) ** 2)
                if dx == 0:
                    return True

        return False


if __name__ == "__main__":
    main()
