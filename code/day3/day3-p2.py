"""
--- Part Two ---

As a stress test on the system, the programs here clear the grid and then store the value 1 in square 1. Then, in the same allocation order as shown above, they store the sum of the values in all adjacent squares, including diagonals.

So, the first few squares' values are chosen as follows:

Square 1 starts with the value 1.
Square 2 has only one adjacent filled square (with value 1), so it also stores 1.
Square 3 has both of the above squares as neighbors and stores the sum of their values, 2.
Square 4 has all three of the aforementioned squares as neighbors and stores the sum of their values, 4.
Square 5 only has the first and fourth squares as neighbors, so it gets the value 5.
Once a square is written, its value does not change. Therefore, the first few squares would receive the following values:

147  142  133  122   59
304    5    4    2   57
330   10    1    1   54
351   11   23   25   26
362  747  806--->   ...
What is the first value written that is larger than your puzzle input?

Your puzzle input is still 325489.
"""


def generate_coordinates():
    ring = 1
    prev_coord = [0, 0]
    yield prev_coord

    while True:
        while prev_coord[0] < ring:
            prev_coord[0] += 1
            yield prev_coord
        while prev_coord[1] < ring:
            prev_coord[1] += 1
            yield prev_coord
        while prev_coord[0] > -1.0 * ring:
            prev_coord[0] -= 1
            yield prev_coord
        while prev_coord[1] > -1.0 * ring:
            prev_coord[1] -= 1
            yield prev_coord
        ring += 1


class spiralizer():
    def __init__(self):
        import itertools
        self.coords = {}
        self.tests = list(itertools.product([-1, 0, 1], [-1, 0, 1]))
        self.coordinate_generator = generate_coordinates()
        self.init_value = 1

    def coord_string(self, coord):
        return(",".join([str(i) for i in coord]))

    def update_coords(self, coord, value):
        self.coords[self.coord_string(coord)] = value

    def get_coord_value(self, coord):
        return self.coords.get(self.coord_string(coord), 0)

    def get_local_value(self, coord):
        test_coords = [[i + j for i, j in zip(coord, test_delta)] for test_delta in self.tests]
        ret = sum(self.get_coord_value(test_coord) for test_coord in test_coords)
        return(ret)

    def generate_coordinate_values(self):
        coord = next(self.coordinate_generator)
        self.update_coords(coord, self.init_value)
        yield([coord, self.init_value])
        while True:
            coord = next(self.coordinate_generator)
            val = self.get_local_value(coord)
            self.update_coords(coord, val)
            yield([coord, val])


def find_bigger(x):
    spiral_values = spiralizer().generate_coordinate_values()
    val = next(spiral_values)
    while val[1] < x:
        val = next(spiral_values)
    return(val)


if __name__ == "__main__":
    import timeit
    big_val = find_bigger(325489)
    num = 100
    print(timeit.timeit(lambda: find_bigger(325489), number=num)/num)
    print(big_val)
