import pygame
import Quad
from math import sqrt
import random

# Todo:
# - Restructure Quad.py to put core functions first followed by utility functions
# - Implement neighbour finding algorithm for more efficient insertion
# - https://geidav.wordpress.com/2017/12/02/advanced-octrees-4-finding-neighbor-nodes/
# - implement async highlight function

RESOLUTION = (800, 600)
win = pygame.display.set_mode(RESOLUTION)

QUAD_COLOR = (128, 200, 128)
BG_COLOR = (0, 0, 0)
POINT_COLOR = (255, 255, 255)  # (100, 255, 20)
POINT_COLOR2 = (255, 80, 255)
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
        pygame.draw.lines(screen, QUAD_COLOR, True, quad.get_outline(), line_width)
        for p in quad.points:
            pygame.draw.circle(win, POINT_COLOR2, p.pos, 1)
    else:
        for k in quad.children:
            redraw_quads(screen, quad.children[k])


def main():
    pygame.init()
    pygame.display.set_caption("Quad Tree Visualisation - Bit-Sahil04")
    width, height = RESOLUTION
    clock = pygame.time.Clock()
    win.fill(BG_COLOR)
    quad_tree = Quad.Quad((0, 0, width, height), 1)
    points = set()
    lmb = False
    rmb = False

    while True:
        win.fill(BG_COLOR)

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                exit()
            if pygame.mouse.get_pressed(3)[0] and not lmb:
                lmb = True
                rp = pygame.mouse.get_pos()
                # generate random velocity of point except 0
                for i in range(1):
                    p = Point(2, rp, (random.randint(-1, 2) or 1, random.randint(-1, 2) or 1))
                    p.quadrant = quad_tree.insert_point(p)
                    points.add(p)
            else:
                lmb = False
            if pygame.mouse.get_pressed(3)[2]:
                rmb = True
                for i in points:
                    mx, my = pygame.mouse.get_pos()
                    dx = 0 + ((mx - i.pos[0]) / abs(mx - i.pos[0] or 1))
                    dy = 0 + ((my - i.pos[1]) / abs(mx - i.pos[0] or 1))
                    i.dv = (dx, dy)
            else:
                rmb = False

        for id, i in enumerate(points):
            i.update(quad_tree)
            pygame.draw.circle(win, POINT_COLOR, i.pos, i.radius)

        show_text(f"{1000 / clock.tick(60) :.0f}", 100, 20, win, size=15)
        show_text(f"{(len(points))}", 100, 40, win, size=15)
        redraw_quads(win, quad_tree)
        pygame.display.flip()


class Point(Quad.Item):
    def __init__(self, radius, pos, dv):
        super().__init__(pos)
        self.dv = dv
        self.quadrant = None
        self.radius = radius

    def update(self, root_quad):
        # add acceleration dv to point position
        self.pos = (self.pos[0] + self.dv[0], self.pos[1] + self.dv[1])

        # Update quad tree if the point exits the bounds of current quad
        if not self.quadrant.has_point(self):
            self.quadrant.pop(self)
            self.quadrant = root_quad.insert_point(self)

        if self.collision_x():
            self.dv = (self.dv[0] * -1, self.dv[1])

        if self.collision_y():
            self.dv = (self.dv[0], self.dv[1] * -1)

        if self.collision_point():
            pygame.draw.polygon(win, QUAD_COLOR, self.quadrant.get_outline())

    def collision_x(self):
        return (0 + self.radius * 2 > self.pos[0]) or (self.pos[0] > (RESOLUTION[0] - (self.radius * 2)))

    def collision_y(self):
        return (0 + self.radius * 2 > self.pos[1]) or (self.pos[1] > RESOLUTION[1] - (self.radius * 2))

    def collision_point(self):
        for p2 in self.quadrant.points:
            pygame.draw.line(win, QUAD_COLOR, self.pos, p2.pos)
            if p2 != self:
                px = p2.pos[0] + p2.radius
                py = p2.pos[1] + p2.radius

                dx = sqrt(((self.pos[0] + self.radius) - px) ** 2 + ((self.pos[1] + self.radius) - py) ** 2)

                if dx <= self.radius:
                    self.dv = (self.dv[0] * -1, self.dv[1] * -1)
                    p2.dv = (p2.dv[0] * -1, p2.dv[1] * -1)
                    return True

        return False


if __name__ == "__main__":
    main()
