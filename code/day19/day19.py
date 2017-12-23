"""
--- Day 19: A Series of Tubes ---

Somehow, a network packet got lost and ended up here. It's trying to follow a routing diagram (your puzzle input), but it's confused about where to go.

Its starting point is just off the top of the diagram. Lines (drawn with |, -, and +) show the path it needs to take, starting by going down onto the only line connected to the top of the diagram. It needs to follow this path until it reaches the end (located somewhere within the diagram) and stop there.

Sometimes, the lines cross over each other; in these cases, it needs to continue going the same direction, and only turn left or right when there's no other option. In addition, someone has left letters on the line; these also don't change its direction, but it can use them to keep track of where it's been. For example:

     |
     |  +--+
     A  |  C
 F---|----E|--+
     |  |  |  D
     +B-+  +--+

Given this diagram, the packet needs to take the following path:

    Starting at the only line touching the top of the diagram, it must go down, pass through A, and continue onward to the first +.
    Travel right, up, and right, passing through B in the process.
    Continue down (collecting C), right, and up (collecting D).
    Finally, go all the way left through E and stopping at F.

Following the path to the end, the letters it sees on its path are ABCDEF.

The little packet looks up at you, hoping you can help it find the way. What letters will it see (in the order it would see them) if it follows the path? (The routing diagram is very wide; make sure you view it without line wrapping.)

--- Part Two ---

The packet is curious how many steps it needs to go.

For example, using the same routing diagram from the example above...

     |
     |  +--+
     A  |  C
 F---|--|-E---+
     |  |  |  D
     +B-+  +--+

...the packet would go:

    6 steps down (including the first line at the top of the diagram).
    3 steps right.
    4 steps up.
    3 steps right.
    4 steps down.
    3 steps right.
    2 steps up.
    13 steps left (including the F it stops on).

This would result in a total of 38 steps.

How many steps does the packet need to go?
"""
import string


def load_path_matrix(file):
    output = []
    with open(file, 'r') as f:
        for i, line in enumerate(f.readlines()):
            output.append([char.strip() for char in line.rstrip()])

    max_length = max([len(x) for x in output])
    for line in output:
        line.extend(['' for i in range(max_length - len(line))])
    entrance = (0, output[0].index('|'))
    return (output, entrance)


def traverse_direction(location, direction):
    new_location = [location[i] + direction[i] for i in range(len(location))]
    return new_location


def get_char(path_matrix, location):
    lx = len(path_matrix[0])
    ly = len(path_matrix)
    if location[0] < 0 or location[0] >= ly or location[1] < 0 or location[1] >= lx:
        return 'oob'

    return path_matrix[location[0]][location[1]]


def traverse_matrix(path_matrix, entrance):
    landmark_names = set(list(string.ascii_uppercase))

    current_location = entrance
    prev_direction = [1, 0]
    prev_direction_char = "|"

    landmarks = []
    step_count = 1
    while True:
        current_location = traverse_direction(current_location, prev_direction)
        current_character = get_char(path_matrix, current_location)
        if current_character == "U":
            debug = True
            count = 0

        if current_character == 'oob' or current_character == "":
            break

        if current_character in landmark_names:
            landmarks.append(current_character)
        elif current_character == "+":
            if prev_direction_char == "|":
                prev_direction_char = "-"
                test_directions = [[i, j] for i, j in zip([0, 0], [1, -1])]
            else:
                prev_direction_char = "|"
                test_directions = [[i, j] for i, j in zip([1, -1], [0, 0])]

            test_chars = []
            for test_direction in test_directions:
                test_location = traverse_direction(current_location, test_direction)
                test_character = get_char(path_matrix, test_location)
                test_chars.append(test_character)

            if prev_direction_char in test_chars:
                prev_direction = test_directions[test_chars.index(prev_direction_char)]
            else:
                for i, char in enumerate(test_chars):
                    if char in landmark_names:
                        prev_direction = test_directions[i]

        step_count += 1

    return(''.join(landmarks), step_count)


if __name__ == "__main__":
    landmarks, step_count = traverse_matrix(*load_path_matrix('test_input.txt'))
    assert landmarks == "ABCDEF"
    assert step_count == 38

    path_matrix, entrance = load_path_matrix('input.txt')
    landmarks, step_count = traverse_matrix(path_matrix, entrance)
    print(landmarks, step_count)
