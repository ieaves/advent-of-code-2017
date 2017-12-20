"""
--- Day 16: Permutation Promenade ---

You come upon a very unusual sight; a group of programs here appear to be dancing.

There are sixteen programs in total, named a through p. They start by standing in a line: a stands in position 0, b stands in position 1, and so on until p, which stands in position 15.

The programs' dance consists of a sequence of dance moves:

    Spin, written sX, makes X programs move from the end to the front, but maintain their order otherwise. (For example, s3 on abcde produces cdeab).
    Exchange, written xA/B, makes the programs at positions A and B swap places.
    Partner, written pA/B, makes the programs named A and B swap places.

For example, with only five programs standing in a line (abcde), they could do the following dance:

    s1, a spin of size 1: eabcd.
    x3/4, swapping the last two programs: eabdc.
    pe/b, swapping programs e and b: baedc.

After finishing their dance, the programs end up in order baedc.

You watch the dance for a while and record their dance moves (your puzzle input). In what order are the programs standing after their dance?

--- Part Two ---

Now that you're starting to get a feel for the dance moves, you turn your attention to the dance as a whole.

Keeping the positions they ended up in from their previous dance, the programs perform it again and again: including the first dance, a total of one billion (1000000000) times.

In the example above, their second dance would begin with the order baedc, and use the same dance moves:

    s1, a spin of size 1: cbaed.
    x3/4, swapping the last two programs: cbade.
    pe/b, swapping programs e and b: ceadb.

In what order are the programs standing after their billion dances?
"""
from collections import deque
from fractions import gcd
from functools import reduce
import string
import copy


def input_loader(file):
    with open(file, 'r') as f:
        for line in f.readlines():
            dance_steps = line.strip().split(',')
            for dance_step in dance_steps:
                yield dance_step


def spin(order_deque, size):
    order_deque.rotate(size)


def exchange(order_iter, a, b):
    order_iter[a], order_iter[b] = order_iter[b], order_iter[a]


def swap(order_iter, a, b):
    exchange(order_iter, order_iter.index(a), order_iter.index(b))


def lets_dance(init_state, dance_moves):
    dancers = deque(init_state)
    for dance_move in dance_moves:
        if dance_move[0] == 's':
            spin(dancers, int(dance_move[1:]))
        elif dance_move[0] == 'x':
            ind1, ind2 = [int(ind) for ind in dance_move[1:].split('/')]
            exchange(dancers, ind1, ind2)
        else:
            name1, name2 = [ind for ind in dance_move[1:].split('/')]
            swap(dancers, name1, name2)
    return ''.join(dancers)


def lcm(a, b):
    return a * b // gcd(a, b)


def lcmm(*args):
    return reduce(lcm, args)


def repeated_dance(init_state, dance_moves, repetitions):
    current_state = list(init_state)
    dance_moves = list(dance_moves)
    discovered_states = [''.join(current_state)]
    
    for i in range(1, repetitions):
        current_state = lets_dance(current_state, dance_moves)
        if current_state in discovered_states:
            cycle_length = len(discovered_states)
            return discovered_states[repetitions % cycle_length]

        discovered_states.append(current_state)

    return current_state


if __name__ == "__main__":
    programs = list(string.ascii_lowercase)[0:16]

    result = lets_dance(programs, input_loader('input.txt'))
    print(result)
    print(repeated_dance(programs, input_loader('input.txt'), 1000000000))
