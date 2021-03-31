import pygame
from Quad import Quad
import random
from math import sqrt

# Todo:
# - Create point class
# - Design a collision system with efficient use of quad tree
# - implement async highlight function
# - Fix collision bug between points of diff radius in point.update() function

RESOLUTION = (800, 600)
win = pygame.display.set_mode(RESOLUTION)

QUAD_COLOR = (128, 60, 128)
BG_COLOR = (80, 0, 80)
POINT_COLOR = (100, 255, 20)
POINT_COLOR2 = (80, 255, 255)
HIGHLIGHT_COLOR = (255, 255, 255)


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
            if pygame.mouse.get_pressed()[0] and not lmb:
                lmb = True
                rp = pygame.mouse.get_pos()
                p = Point(5, rp, (random.randint(-2, 3), random.randint(-2, 3)))
                p.quadrant = quad_tree.insert_point(rp)
                print('hi')
                print(p.quadrant.bounds) # crash

                points.append(p)
            else:
                lmb = False

        for id, i in enumerate(points):
            i.update(quad_tree, id )
            pygame.draw.circle(win, POINT_COLOR, i.pos, i.radius)

        clock.tick(60)
        pygame.display.flip()


class Point:
    def __init__(self, radius, pos, dv: (int, int)):
        self.pos = pos
        self.dv = dv
        self.quadrant = None
        self.radius = radius

    def update(self, root_quad, i):
        # add acceleration dv to point position
        self.pos = (self.pos[0] + self.dv[0], self.pos[1] + self.dv[1])

        # Update quad tree if the point exits the bounds of current quad
        if not self.quadrant.has_point(self.pos):
            self.quadrant.pop(self.pos)
            self.quadrant = root_quad.insert_point(self.pos)
            # temp_quad = root_quad.find_quad(self.pos)
            # self.quadrant = temp_quad.insert_point(self.pos)
            # self.quadrant = temp_quad.find_quad(self.pos)

        if self.collision_x():
            self.dv = (self.dv[0] * -1, self.dv[1])

        if self.collision_y():
            self.dv = (self.dv[0], self.dv[1] * -1)

        if self.collision_point():
           self.dv = (self.dv[0] * -1, self.dv[1] * -1)
           #print(f"{i} :collision: point")

       # print(f"id:{i} pos: {self.pos} quad: {self.quadrant.bounds}")

    def collision_x(self):
        return (0 + self.radius * 2 > self.pos[0]) or (self.pos[0] >(RESOLUTION[0] - (self.radius * 2)))

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
