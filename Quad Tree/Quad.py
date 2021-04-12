class Item:
    """
    Serves as an End Point for the quad tree to store coordinates
    make sure to call super().__init__((x,y)) when inherited
    """

    def __init__(self, pos):
        self.pos = pos


class Quad:
    max_points = 5
    max_depth = 6

    def __init__(self, bounds: (int, int, int, int), depth: int, parent=None):
        self.depth = depth
        self.bounds = bounds  # abXY
        self._parent = parent

        self.points = set()
        self.children = dict()

    def __get_quadrant(self, point: Item, flipY=True):
        """
        return normalized values xy <= {-1, 1} to find appropriate quad
        Takes optional argument flipY if dealing with canvas with inverted Y axis
        """
        # Translating absolute coordinates to quadrant's relative coordinates
        cx = self.bounds[0] + (self.bounds[2] - self.bounds[0]) // 2
        cy = self.bounds[1] + (self.bounds[3] - self.bounds[1]) // 2
        px = (point.pos[0] - cx)
        if flipY:
            py = (cy - point.pos[1])  # Y axis in pygame is flipped, so modified the eqn
        else:
            py = (point.pos[1] - cy)

        return px / abs(px) if px != 0 else 1, py / abs(py) if py != 0 else 1

    def has_point(self, point: Item):
        """
        Returns True if a point exists within the region of the quadrant
        """
        within_region = self.bounds[0] < point.pos[0] < self.bounds[2] and self.bounds[1] < point.pos[1] < self.bounds[
            3]
        return (not self.children) and within_region

    def insert_point(self, point: Item):
        """
        Append a point to a quadrant or generate a new sub-quad and append to that quad
        Return deepest quad containing point
        """
        q = self.__get_quadrant(point)

        # Base Case:: either append points at max depth or append if quad has no children && does not exceed max pts
        if self.depth >= self.max_depth or (not self.children and len(self.points) < self.max_points):
            self.points.add(point)
            # self.points.append(point)
            return self

        # Case 2:: if quad has existing sub-quads, go to the appropriate sub-quad
        elif self.children:
            return self.children[q].insert_point(point)

        # Case 3:: If quad has no  children, and exceeds max pts, create sub-quad and insert pt in appropriate sub-quad
        else:
            self.children = self.__create_subquad()
            return self.children[q].insert_point(point)

    def __create_subquad(self):
        """
        Create a new sub-quadrant for the parent quad
        """
        # Center points of the quad
        cx = self.bounds[0] + (self.bounds[2] - self.bounds[0]) // 2
        cy = self.bounds[1] + (self.bounds[3] - self.bounds[1]) // 2

        # create bounds for quadrants abXY(x1, y1,  x2, y2)
        b_NW = (self.bounds[0], self.bounds[1], cx, cy)
        b_NE = (cx, self.bounds[1], self.bounds[2], cy)
        b_SW = (self.bounds[0], cy, cx, self.bounds[3])
        b_SE = (cx, cy, self.bounds[2], self.bounds[3])

        # Create child quadrants
        subtrees = {
            (-1, 1): Quad(b_NW, self.depth + 1, parent=self),
            (1, 1): Quad(b_NE, self.depth + 1, parent=self),
            (-1, -1): Quad(b_SW, self.depth + 1, parent=self),
            (1, -1): Quad(b_SE, self.depth + 1, parent=self),
        }

        # Placing current node's points in appropriate sub-quadrants
        for p in self.points:
            q = self.__get_quadrant(p)
            p.quadrant = subtrees[q].insert_point(p)

        # remove points stored in current node
        self.points.clear()

        return subtrees

    def find_quad(self, point):
        """
        Get the deepest quadrant containing a point
        """
        # Base case: if sub-quad has no children, then check in set of points
        if not self.children:
            if point in self.points:
                return self
            else:
                return None

        # Case 2: If the sub-quad has children, check for points in them
        elif self.children:
            q = self.__get_quadrant(point)
            self.children[q].find_quad(point)

    def get_parent(self):
        """
        Get parent of the current quad if it exists, otherwise return itself
        """
        return self._parent if self._parent else self

    def get_outline(self):
        """
        Get the four corners of the current quad
        """
        return [
            #        x     ,    y
            (self.bounds[0], self.bounds[1]),
            (self.bounds[2], self.bounds[1]),
            (self.bounds[2], self.bounds[3]),
            (self.bounds[0], self.bounds[3]),
        ]

    def pop(self, point: Item):
        """
        Removes the point from the appropriate quadrant
        Deletes the quadrant if all children are empty
        """

        # Base Case: No children exist then check if point is stored in current quad
        if not self.children:
            if point in self.points:
                self.points.remove(point)
                # Clean-up: check the parent of quadrant and clear if necessary
                return self.clear_parent()
            return self

        # Case 2: If children exist, remove point inside them
        if self.children:
            q = self.__get_quadrant(point)
            return self.children[q].pop(point)

    def truncate_tree(self):
        """
        Traverse the entire tree and clean all quadrants
        (very slow)
        """
        # traversing back to the root quad
        t = self
        while t._parent:
            t = t._parent

        # perform DFS to check if a sub-quad is empty and prune it
        def dfs(instance):
            total = 0
            if instance.children:
                for k in instance.children:
                    total += dfs(instance.children[k])
            else:
                return len(instance.points)

            if total == 0:
                instance.children = {}
                return 0 + len(instance.points)
            else:
                return 1

        dfs(t)

    def clear_tree(self):
        """
        Clear the entire tree
        """
        if self.children:
            self.children = {}

        if self.points:
            self.points.clear()

    def clear_parent(self):
        """
        recursively check if the parent quadrant is empty, and clean it
        :return: instance of parent quad or self if root
        """
        parent = self.get_parent()
        if parent is not self:
            empty = True
            for child in parent.children:
                if parent.children[child].points or parent.children[child].children:
                    empty = False
                    break
            if empty:
                parent.children = {}
                return parent.clear_parent()

        return parent
