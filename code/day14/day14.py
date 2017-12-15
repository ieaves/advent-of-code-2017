"""
--- Day 14: Disk Defragmentation ---

Suddenly, a scheduled job activates the system's disk defragmenter. Were the situation different, you might sit and watch it for a while, but today, you just don't have that kind of time. It's soaking up valuable system resources that are needed elsewhere, and so the only option is to help it finish its task as soon as possible.

The disk in question consists of a 128x128 grid; each square of the grid is either free or used. On this disk, the state of the grid is tracked by the bits in a sequence of knot hashes.

A total of 128 knot hashes are calculated, each corresponding to a single row in the grid; each hash contains 128 bits which correspond to individual grid squares. Each bit of a hash indicates whether that square is free (0) or used (1).

The hash inputs are a key string (your puzzle input), a dash, and a number from 0 to 127 corresponding to the row. For example, if your key string were flqrgnkx, then the first row would be given by the bits of the knot hash of flqrgnkx-0, the second row from the bits of the knot hash of flqrgnkx-1, and so on until the last row, flqrgnkx-127.

The output of a knot hash is traditionally represented by 32 hexadecimal digits; each of these digits correspond to 4 bits, for a total of 4 * 32 = 128 bits. To convert to bits, turn each hexadecimal digit to its equivalent binary value, high-bit first: 0 becomes 0000, 1 becomes 0001, e becomes 1110, f becomes 1111, and so on; a hash that begins with a0c2017... in hexadecimal would begin with 10100000110000100000000101110000... in binary.

Continuing this process, the first 8 rows and columns for key flqrgnkx appear as follows, using # to denote used squares, and . to denote free ones:

##.#.#..-->
.#.#.#.#
....#.#.
#.#.##.#
.##.#...
##..#..#
.#...#..
##.#.##.-->
|      |
V      V

In this example, 8108 squares are used across the entire 128x128 grid.

Given your actual key string, how many squares are used?

--- Part Two ---

Now, all the defragmenter needs to know is the number of regions. A region is a group of used squares that are all adjacent, not including diagonals. Every used square is in exactly one region: lone used squares form their own isolated regions, while several adjacent squares all count as a single region.

In the example above, the following nine regions are visible, each marked with a distinct digit:

11.2.3..-->
.1.2.3.4
....5.6.
7.8.55.9
.88.5...
88..5..8
.8...8..
88.8.88.-->
|      |
V      V

Of particular interest is the region marked 8; while it does not appear contiguous in this small view, all of the squares marked 8 are connected when considering the whole 128x128 grid. In total, in this example, 1242 regions are present.

How many regions are present given your key string?

"""
import numpy as np

def circle_hash(instructions, circle_length=256):
    circle = [i for i in range(0, circle_length)]
    pos = 0
    skip_size = 0
    for length in instructions:
        if length > circle_length:
            continue

        max_val = (pos + length) % circle_length

        if pos <= max_val:
            circle[pos:max_val] = circle[pos:max_val][::-1]
        else:
            temp_circle = (circle[pos - circle_length:] + circle[:max_val])[::-1]
            circle[pos - circle_length:] = temp_circle[:circle_length - pos]
            circle[:max_val] = temp_circle[circle_length - pos:]

        pos = (pos + length + skip_size) % circle_length
        skip_size += 1
    return(circle)


def iterable_xor(iterable):
    xored = iterable[0] ^ iterable[1]
    for i in range(2, len(iterable)):
        xored = xored ^ iterable[i]
    return(xored)


def convert_to_hex(num):
    assert num >= 0
    num_hex = hex(num)
    num_hex = '0' + num_hex[2:] if len(num_hex[2:]) < 2 else num_hex[2:]
    assert len(num_hex) == 2
    return(num_hex)


def densify(sparse_hash, length=16):
    n_elems = len(sparse_hash)
    assert n_elems % length == 0

    segment_size = 2 * int(n_elems/length)
    n_segments = int(length / 2)
    segments = (sparse_hash[i*segment_size:(i+1)*segment_size] for i in range(0, n_segments))
    xors = (iterable_xor(segment) for segment in segments)
    xors = list(xors)
    hex_val = ''.join([convert_to_hex(xor) for xor in xors])
    return(hex_val)


def ascii_instructions(ascii_seed, repetitions=64):
    spec_instructions = [17, 31, 73, 47, 23]
    instructions = [ord(char) for char in ascii_seed]
    instructions.extend(spec_instructions)
    repeat = 0
    while repeat < repetitions:
        for instruction in instructions:
            yield(instruction)
        repeat += 1


def dense_hash(input_str, dense_length=16, circle_length=256):
    instructions = ascii_instructions(input_str)
    sparse_hash = circle_hash(instructions, circle_length)
    dense_hash = densify(sparse_hash, dense_length)
    return(dense_hash)


def convert_to_binary(char, scale, num_bits=0):
    return bin(int(char, scale))[2:].zfill(num_bits)


def binary_hash(input_str, num_bits, *args, **kwargs):
    _hash = dense_hash(input_str, *args, **kwargs)  # in hexadecimal
    return ''.join([convert_to_binary(char, 16, num_bits) for char in _hash])


def build_grid(seed, num_bits, size):
    density_length = int(size / num_bits)
    for i in range(0, size):
        eval_str = '-'.join([seed, str(i)])
        row = binary_hash(eval_str, num_bits, density_length)
        yield(row)


def grid_counter(seed, num_bits, size):
    count = 0
    grid_generator = build_grid(seed, num_bits, size)
    i = 0
    for row in grid_generator:
        i += 1
        count += sum(int(j) for j in row if j == '1')
    return(count)


def propagate_adjacency(grid, regions, ix, iy, region_num):

    if grid[iy][ix] == "0" or regions[iy][ix] != 0:
        return region_num

    regions[iy][ix] = region_num

    tests = []
    if ix != 0:
        tests.append([0, -1])
    if ix != len(grid[0]) - 1:
        tests.append([0, 1])
    if iy != 0:
        tests.append([-1, 0])
    if iy != len(grid) - 1:
        tests.append([1, 0])

    for test in tests:
        nix = ix + test[1]
        niy = iy + test[0]
        propagate_adjacency(grid, regions, nix, niy, region_num)

    return region_num + 1


def region_counter(grid):
    grid = list(grid)
    n_y = len(grid)
    n_x = len(grid[0])

    regions = [[0 for i in range(0, n_x)] for j in range(0, n_y)]
    region_num = 1
    for i in range(0, n_y):
        for j in range(0, n_x):
            region_num = propagate_adjacency(grid, regions, j, i, region_num)

    return region_num - 1


if __name__ == "__main__":
    assert convert_to_binary('0', 16, 4) == '0000'
    assert convert_to_binary('1', 16, 4) == '0001'
    assert convert_to_binary('e', 16, 4) == '1110'
    assert convert_to_binary('f', 16, 4) == '1111'

    test_input = "flqrgnkx"
    assert region_counter(build_grid(test_input, 4, 128)) == 1242

    puzzle_input = "jxqlasbh"
    count = grid_counter(puzzle_input, 4, 128)
    print(count)
    print(region_counter(build_grid(puzzle_input, 4, 128)))
