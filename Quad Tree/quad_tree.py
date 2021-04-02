import pygame
from Quad import Quad
from math import sqrt
import random

# Todo:
# - Design a collision system with efficient use of quad tree (WIP)
# - implement async highlight function
# - Fix collision bug between points of diff radius in point.update() function
# - fix pop operation
# - test insert operation functionality
# - Fix point collision bug
# - Improve truncate_tree implementation
# - find a way to efficiently store points without modifying the quad tree DS too much
# - Restructure Quad.py to put core functions first followed by utility functions


# FIXME: (optimization candidates)
# Profiler report. Execution time: 52.3 seconds
# - ncalls          tottime  percall  cumtime  percall  filename:lineno(function)
# - 102870/78361    0.096    0.000   40.000    0.001    Quad.py:118(pop)
# - 91807206/102870 36.328   0.000   39.788    0.000    Quad.py:148(dfs)
# - 69038342        3.469    0.000    3.469    0.000    {built-in method builtins.len}
# - 2201962/3646    1.392    0.000    4.278    0.001    quad_tree.py:38(update_quads)
# - 493331          0.681    0.000   43.055    0.000    quad_tree.py:89(update)
# - 1652383         0.670    0.000    0.670    0.000    Quad.py:106(get_outline)
# - 102870          0.082    0.000   39.869    0.000    Quad.py:137(truncate_tree)

RESOLUTION = (800, 600)
win = pygame.display.set_mode(RESOLUTION)

QUAD_COLOR = (128, 60, 128)
BG_COLOR = (90, 30, 110)
POINT_COLOR = (255, 255, 255)  # (100, 255, 20)
POINT_COLOR2 = (80, 255, 255)
HIGHLIGHT_COLOR = (255, 255, 255)


def show_text(text, x, y, surf, size=10, color=(255, 255, 255)):
    text = str(text)
    font = pygame.font.SysFont('Arial', size, True)

    text_width, text_height = font.size(text)
    text = font.render(text, True, color)
    tRect = surf.blit(text, (x - (text_width / 2), y - (text_height / 2)))
    return tRect


def redraw_quads(screen, quad):
    line_width = 1
    if not quad.children:
        pygame.draw.lines(screen, BG_COLOR, True, quad.get_outline(), line_width)
    else:
        for k in quad.children:
            redraw_quads(screen, quad.children[k])


def main():
    pygame.init()
    pygame.display.set_caption("Quad Tree Visualisation - Bit-Sahil04")
    width, height = RESOLUTION
    clock = pygame.time.Clock()
    win.fill(BG_COLOR)
    quad_tree = Quad((1, 1, width - 1, height - 1), 1)
    points = []
    lmb = False
    rmb = False
    while True:
        win.fill(BG_COLOR)
        redraw_quads(win, quad_tree)

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                exit()
            if pygame.mouse.get_pressed(3)[0] and not lmb:
                lmb = True
                rp = pygame.mouse.get_pos()
                # generate random velocity of point except 0
                p = Point(1, rp, (random.randint(-1, 2) or 1, random.randint(-1, 2) or 1))
                p.quadrant = quad_tree.insert_point(rp)
                points.append(p)
            else:
                lmb = False
            if pygame.mouse.get_pressed(3)[2]:
                rmb = True
                for i in points:
                    mx, my = pygame.mouse.get_pos()
                    dx = (mx - i.pos[0]) or 1
                    dy = (my - i.pos[1]) or 1
                    i.dv = (dx / abs(dx), dy / abs(dy))
            else:
                rmb = False

        for id, i in enumerate(points):
            i.update(quad_tree)
            pygame.draw.circle(win, POINT_COLOR, i.pos, i.radius)

        # show_text(f"{1000 / clock.tick(60) :.0f}", 100, 20, win, size=15)
        show_text(f"{(len(points))}", 100, 40, win, size=15)
        pygame.display.flip()


class Point:
    def __init__(self, radius, pos, dv):
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
