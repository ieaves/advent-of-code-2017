"""
--- Day 3: Spiral Memory ---

You come across an experimental new kind of memory stored on an infinite two-dimensional grid.

Each square on the grid is allocated in a spiral pattern starting at a location marked 1 and then counting up while spiraling outward. For example, the first few squares are allocated like this:

17  16  15  14  13
18   5   4   3  12
19   6   1   2  11
20   7   8   9  10
21  22  23---> ...
While this is very space-efficient (no squares are skipped), requested data must be carried back to square 1 (the location of the only access port for this memory system) by programs that can only move up, down, left, or right. They always take the shortest path: the Manhattan Distance between the location of the data and square 1.

For example:

Data from square 1 is carried 0 steps, since it's at the access port.
Data from square 12 is carried 3 steps, such as: down, left, left.
Data from square 23 is carried only 2 steps: up twice.
Data from square 1024 must be carried 31 steps.
How many steps are required to carry the data from the square identified in your puzzle input all the way to the access port?

Your puzzle input is 325489.
"""
import math


def manhattan_distance(x1, x2):
    dist = abs(x1[0] - x2[0]) + abs(x1[1] - x2[1])
    return(dist)


def center_distance(x):
    """
    Bottom Right corner of the square tells you the volume of the square up to
    that point and acts as a reference coordinate
    """
    if x == 1:
        return(0)

    sqrtx = x**.5
    width = math.floor(sqrtx)

    if width % 2 == 0 or sqrtx != width:
        width = width + 2 if (width - 1) % 2 == 0 else width + 1

    width_dist = width - 1
    ring = (width_dist) / 2
    center = [ring, ring]

    volume = width ** 2

    side = (volume - x) / (width_dist)

    if side <= 1:
        # bottom
        coords = [volume - x, 0]
    elif side <= 2:
        # left
        coords = [width_dist, volume - x - width_dist]
    elif side <= 3:
        # top
        coords = [volume - x - width_dist * 2, width_dist]
    else:
        # right
        coords = [0, width_dist - (volume - width_dist * 3 - x)]

    dist = manhattan_distance(coords, center)
    return(dist)


if __name__ == "__main__":
    assert center_distance(1) == 0
    assert center_distance(12) == 3
    assert center_distance(23) == 2
    assert center_distance(1024) == 31

    print(center_distance(325489))
