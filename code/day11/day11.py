"""
--- Day 11: Hex Ed ---

Crossing the bridge, you've barely reached the other side of the stream when a program comes up to you, clearly in distress. "It's my child process," she says, "he's gotten lost in an infinite grid!"

Fortunately for her, you have plenty of experience with infinite grids.

Unfortunately for you, it's a hex grid.

The hexagons ("hexes") in this grid are aligned such that adjacent hexes can be found to the north, northeast, southeast, south, southwest, and northwest:

  \ n  /
nw +--+ ne
  /    \
-+      +-
  \    /
sw +--+ se
  / s  \
You have the path the child process took. Starting where he started, you need to determine the fewest number of steps required to reach him. (A "step" means to move from the hex you are in to any adjacent hex.)

For example:

ne,ne,ne is 3 steps away.
ne,ne,sw,sw is 0 steps away (back where you started).
ne,ne,s,s is 2 steps away (se,se).
se,sw,se,sw,sw is 3 steps away (s,s,sw).

--- Part Two ---

How many steps away is the furthest he ever got from his starting position?

"""


def input_loader(file):
    with open(file, 'r') as f:
        for line in f.readlines():
            for instruction in line.strip().split(","):
                yield(instruction.lower())


def traverse_grid(instructions, initial_position=[0, 0], return_max_dist=False):
    # Implements an axial coordinate system
    instructions_map = {'n': [1, -1], 'ne': [1, 0], 'se': [0, 1], 's': [-1, 1], 'sw': [-1, 0], 'nw': [0, -1]}

    current_location = initial_position
    max_dist = 0
    for instruction in instructions:
        current_location = [i + j for i, j in zip(current_location, instructions_map[instruction])]
        current_distance = hex_distance(initial_position, current_location)
        max_dist = current_distance if current_distance > max_dist else max_dist

    if return_max_dist:
        return((current_location, max_dist))
    else:
        return(current_location)


def hex_distance(a, b):
    # Hex distance equation for distance in an axial coordinate system
    return (abs(a[0] - b[0]) + abs(sum(a) - sum(b)) + abs(a[1] - b[1])) / 2


def distance_traversed(instructions):
    initial_position = [0, 0]
    final_position = traverse_grid(instructions, initial_position)
    return(hex_distance(initial_position, final_position))


if __name__ == "__main__":
    assert distance_traversed(['ne', 'ne', 'ne']) == 3
    assert distance_traversed(['se', 'sw', 'se', 'sw', 'sw']) == 3

    print(distance_traversed(input_loader('input.txt')))
    print(traverse_grid(input_loader('input.txt'), return_max_dist=True)[1])
